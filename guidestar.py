# -*- coding: utf-8 -*-
# Pathos Charity Stream
# Guidestar Database Sync Script - 2013
# Written by Glen Baker - iepathos@gmail.com
"""
    Guidestar(npo)
    SoftSyncToGuidestar()
    HardSyncToGuidestar()

"""
from BeautifulSoup import BeautifulSoup
import sys
import requests
import time
from django.template.defaultfilters import slugify

from npo.models import Npo
from categories.models import Category

from decimal import Decimal
#getcontext().prec = 2 # Keep only 2 digits past decimal ex. $1.00

def CategorizeUnknown(category_str):
    """
        Internal function for adding categories that aren't already
        listed in the initial NTEE category population.  This function
        is called when a category is found on the Guidestar database
        that doesn't already exist.
    """
    category_str = str(category_str) # safety dance
    try:
        cat = Category.objects.get(name=category_str)
        print 'Found NTEE category already in database.'
    except Category.DoesNotExist:
        try:
            cat = Category.objects.get(meta_keywords=category_str.split()[0])
            print 'Found NTEE Code already in database.'
        except Category.DoesNotExist:
            try:
                cat = Category(name=category_str, meta_keywords=category_str.split()[0])
                cat.alternate_title = cat.name.split()[0]
                cat.parent = Category.objects.get(meta_keywords=category_str.split()[0][0])
                cat.save()
            except:
                print 'Error trying to categorize unknown.'

def Guidestar(npo):
    """ 
        Updates an NPO with information from 
        the Guidestar Database.
        
                web_url
                mission_statement
                total_revenue
                total_expenses
                zipcode

            Categories:
                npoinfo['primary_org_type']
                npoinfo['primary_org_subtype']
                npoinfo['secondary_org_type']
                npoinfo['secondary_org_subtype']
                npoinfo['tertiary_org_type']
                npoinfo['tertiary_org_subtype']
    """
    def CleanCategory(category_str):
        """
            Internal function for cleaning up parantheses 
            from strings.
        """
        split_str = [item.strip('()') for item in str(category_str).strip().split()]
        category_cleaned = ''
        for item in split_str:
            category_cleaned += item + ' '
        return category_cleaned.strip()

    guidestar_ein = npo.ein[:2] + '-' + npo.ein[2:] # insert '-' after first 2 numbers in Electronic Identification Number
    slug = slugify(npo.name)

    # Guidestar removes inc from slugs
    if slug.endswith('-inc'):
        guidestar_slug = slug[:-4]
    else:
        guidestar_slug = slug
    
    targeturl = 'http://www.guidestar.org/organizations/%s/%s.aspx' % (guidestar_ein, guidestar_slug)
    print 'Target URL: ', targeturl
    npo.guidestar_url = targeturl
    npo.save()
    
    try:
        r = requests.get(targeturl)
        soup = BeautifulSoup(r.text)            
    except:
        print 'Error souping.'

    ### Website URL
    if soup.findAll(lambda tag: tag.name=='a' and tag.has_key('id') and str(tag['id'])=='ctl00_phMainBody_aQuickUrl') != []:
        web_url = soup.findAll(lambda tag: tag.name=='a' and tag.has_key('id') and str(tag['id'])=='ctl00_phMainBody_aQuickUrl')
        cleaned_web_url = str(web_url[0])[41:-31].split()[0].strip().rstrip('&\"') # cut out everything but the url
        if npo.web_url and npo.web_url != cleaned_web_url:
            print 'Found previous website URL:', npo.web_url
            print 'Updating website URL to:', cleaned_web_url
            npo.web_url = cleaned_web_url
            npo.save()
        elif npo.web_url and npo.web_url == cleaned_web_url:
            print 'Found previous website URL:', npo.web_url, 'unchanged.'
        else:
            npo.web_url = cleaned_web_url
            npo.save()
            print 'Found website URL:', npo.web_url
    else:
        print 'No website URL found.'

    ### Mission Statement
    if soup.findAll(lambda tag: tag.name=='div' and tag.has_key('id') and str(tag['id'])=='mission') != []:
        mission_statement = soup.findAll(lambda tag: tag.name=='div' and tag.has_key('id') and str(tag['id'])=='mission')
        cleaned_mission_statement = str(mission_statement[0])[118:-13].strip()
        if npo.mission_statement and cleaned_mission_statement != 'This organization has not provided a mission statement.':
            if npo.mission_statement != cleaned_mission_statement:
                print 'Found previous mission statement:', npo.mission_statement
                print 'Updating mission statement to:', cleaned_mission_statement
                npo.mission_statement = cleaned_mission_statement
                npo.save()
            elif npo.mission_statement == cleaned_mission_statement:
                print 'Found previous mission statement:', npo.mission_statement, 'unchanged.'
        elif cleaned_mission_statement == 'This organization has not provided a mission statement.':
            if npo.mission_statement:
                # The Guidestar mission statement has been checked and still doesn't exist
                print 'This organization has not provided a mission statement.'
            elif not npo.mission_statement:
                npo.mission_statement = cleaned_mission_statement
                npo.save()
                print 'This organization has not provided a mission statement.'
        else:
            npo.mission_statement = cleaned_mission_statement
            npo.save()
            print 'Found mission statement:', npo.mission_statement
    else:
        print 'No mission statement found.'

    ### Total Annual Revenue
    if soup.findAll(lambda tag: tag.name=='tr' and tag.has_key('id') and str(tag['id'])=='ctl00_phMainBody_trChartTotalRev') != []:
        total_revenue = soup.findAll(lambda tag: tag.name=='tr' and tag.has_key('id') and str(tag['id'])=='ctl00_phMainBody_trChartTotalRev')
        cleaned_revenue = str(total_revenue[0])[98:-11].strip('$-<>() \\').replace(',', '')
        if cleaned_revenue != '':
            cleaned_revenue = Decimal(cleaned_revenue)
            if npo.total_revenue and npo.total_revenue != cleaned_revenue:
                print 'Found previous annual revenue: $' + str(npo.total_revenue)
                print 'Updating annual revenue to: $' + str(cleaned_revenue)
                npo.total_revenue = cleaned_revenue
                npo.save()
            elif npo.total_revenue and npo.total_revenue == cleaned_revenue:
                print 'Found previous annual revenue: $' + str(npo.total_revenue), 'unchanged.'
            else:
                npo.total_revenue = cleaned_revenue
                npo.save()
                print 'Found total annual revenue: $' + str(npo.total_revenue)
    else:
        print 'No annual revenue found.'

    ### Total Annual Expenses
    if soup.findAll(lambda tag: tag.name=='tr' and tag.has_key('id') and str(tag['id'])=='ctl00_phMainBody_trChartTotalExpenses') != []:
        total_expenses = soup.findAll(lambda tag: tag.name=='tr' and tag.has_key('id') and str(tag['id'])=='ctl00_phMainBody_trChartTotalExpenses')
        cleaned_expenses = str(total_expenses[0])[103:-11].strip('$-<>() \\').replace(',', '')
        if cleaned_expenses != '':
            cleaned_expenses = Decimal(cleaned_expenses)
            if npo.total_expenses and npo.total_expenses != cleaned_expenses:
                print 'Found previous annual expenses: $' + str(npo.total_expenses)
                print 'Updating annual expenses to: $' + str(cleaned_expenses)
                npo.total_expenses = cleaned_expenses
                npo.save()
            elif npo.total_expenses and npo.total_expenses == cleaned_expenses:
                print 'Found previous annual expenses: $' + str(npo.total_expenses), 'unchanged.'
            else:
                npo.total_expenses = cleaned_expenses
                npo.save()
                print 'Found total annual expenses: $' + str(npo.total_expenses)
    else:
        print 'No annual expenses found.'

    ### Zipcode
    if soup.findAll(lambda tag: tag.name=='dd' and tag.has_key('id') and str(tag['id'])=='ctl00_phMainBody_divMailingAddress') != []:
        zipcode = soup.findAll(lambda tag: tag.name=='dd' and tag.has_key('id') and str(tag['id'])=='ctl00_phMainBody_divMailingAddress')
        cleaned_zipcode = str(zipcode[0])[118:-31].strip('&nbsp ')
        if len(cleaned_zipcode) != 5:
            print 'Error cleaning zipcode.'
        else:
            if npo.zipcode and npo.zipcode != cleaned_zipcode:
                print 'Found previous zipcode:', npo.zipcode
                print 'Updating zipcode to:', cleaned_zipcode
                npo.zipcode = cleaned_zipcode
                npo.save()
            elif npo.zipcode and npo.zipcode == cleaned_zipcode:
                print 'Found zipcode unchanged.'
            else:
                npo.zipcode = cleaned_zipcode
                npo.save()
                print 'Found zipcode:', npo.zipcode
    else:
        print 'No zipcode found.'

    ### NPO Categorization
    npoinfo = {}
    ## Primary Organization Type
    if soup.findAll(lambda tag: tag.name=='dd' and tag.has_key('id') and str(tag['id'])=='ctl00_phMainBody_divPrimaryOrganizationType') != []:
        primary_org_type = soup.findAll(lambda tag: tag.name=='dd' and tag.has_key('id') and str(tag['id'])=='ctl00_phMainBody_divPrimaryOrganizationType')
        npoinfo['primary_org_type'] = CleanCategory(str(primary_org_type[0])[75:-31])
        print 'Found primary category', npoinfo['primary_org_type']
    else:
        print 'Organization is uncategorized on Guidestar.'

    ## Primary Organization SubType
    if soup.findAll(lambda tag: tag.name=='dd' and tag.has_key('id') and str(tag['id'])=='ctl00_phMainBody_divPrimaryOrganizationSubType') != []:
        primary_org_subtype = soup.findAll(lambda tag: tag.name=='dd' and tag.has_key('id') and str(tag['id'])=='ctl00_phMainBody_divPrimaryOrganizationSubType')
        npoinfo['primary_org_subtype'] = CleanCategory(str(primary_org_subtype[0])[78:-31])
        print 'Found primary sub-category', npoinfo['primary_org_subtype']

    ## Secondary Organization Type
    if soup.findAll(lambda tag: tag.name=='dd' and tag.has_key('id') and str(tag['id'])=='ctl00_phMainBody_divSecondaryOrganizationType') != []:
        secondary_org_type = soup.findAll(lambda tag: tag.name=='dd' and tag.has_key('id') and str(tag['id'])=='ctl00_phMainBody_divSecondaryOrganizationType')
        npoinfo['secondary_org_type'] = CleanCategory(str(secondary_org_type[0])[77:-31])
        print 'Found secondary category', npoinfo['secondary_org_type']

    ## Secondary Organization SubType
    if soup.findAll(lambda tag: tag.name=='dd' and tag.has_key('id') and str(tag['id'])=='ctl00_phMainBody_divSecondaryOrganizationSubType') != []:
        secondary_org_subtype = soup.findAll(lambda tag: tag.name=='dd' and tag.has_key('id') and str(tag['id'])=='ctl00_phMainBody_divSecondaryOrganizationSubType')
        npoinfo['secondary_org_subtype'] = CleanCategory(str(secondary_org_subtype[0])[80:-31])
        print 'Found secondary sub-category', npoinfo['secondary_org_subtype']

    ## Tertiary Organization Type
    if soup.findAll(lambda tag: tag.name=='dd' and tag.has_key('id') and str(tag['id'])=='ctl00_phMainBody_divTertiaryOrganizationType') != []:
        tertiary_org_type = soup.findAll(lambda tag: tag.name=='dd' and tag.has_key('id') and str(tag['id'])=='ctl00_phMainBody_divTertiaryOrganizationType')
        npoinfo['tertiary_org_type'] = CleanCategory(str(tertiary_org_type[0])[76:-31])
        print 'Found tertiary category', npoinfo['tertiary_org_type']

    ## Tertiary Organization SubType
    if soup.findAll(lambda tag: tag.name=='dd' and tag.has_key('id') and str(tag['id'])=='ctl00_phMainBody_divTertiaryOrganizationSubType') != []:
        tertiary_org_subtype = soup.findAll(lambda tag: tag.name=='dd' and tag.has_key('id') and str(tag['id'])=='ctl00_phMainBody_divTertiaryOrganizationSubType')
        npoinfo['tertiary_org_subtype'] = CleanCategory(str(tertiary_org_subtype[0])[78:-31])
        print 'Found tertiary sub-category', npoinfo['tertiary_org_subtype']

    # Add NPO to categories based on Guidestar Organization Types
    if 'primary_org_type' in npoinfo:
        try:
            primary_category = Category.objects.get(meta_keywords=npoinfo['primary_org_type'].split()[0])
            npo.categories.add(primary_category)
            npo.save()
        except Category.DoesNotExist:
            print 'Error, category %s does not exist.' % npoinfo['primary_org_type']
    if 'primary_org_subtype' in npoinfo:
        try:
            primary_category_subtype = Category.objects.get(meta_keywords=npoinfo['primary_org_subtype'].split()[0])
            npo.categories.add(primary_category_subtype)
            npo.save()
        except Category.DoesNotExist:
            print 'Error, category %s does not exist.' % npoinfo['primary_org_subtype']
            CategorizeUnknown(npoinfo['primary_org_subtype'])
            print 'Created new category:', Category.objects.get(name=npoinfo['primary_org_subtype'])
    if 'secondary_org_type' in npoinfo:
        try:
            secondary_category = Category.objects.get(meta_keywords=npoinfo['secondary_org_type'].split()[0])
            npo.categories.add(secondary_category)
            npo.save()
        except Category.DoesNotExist:
            print 'Error, category %s does not exist.' % npoinfo['secondary_org_type']
    if 'secondary_org_subtype' in npoinfo:
        try:
            secondary_category_subtype = Category.objects.get(meta_keywords=npoinfo['secondary_org_subtype'].split()[0])
            npo.categories.add(secondary_category_subtype)
            npo.save()
        except Category.DoesNotExist:
            print 'Error, category %s does not exist.' % npoinfo['secondary_org_subtype']
            CategorizeUnknown(npoinfo['secondary_org_subtype'])
            print 'Created new category:', Category.objects.get(name=npoinfo['secondary_org_subtype'])
    if 'tertiary_org_type' in npoinfo:
        try:
            tertiary_category = Category.objects.get(meta_keywords=npoinfo['tertiary_org_type'].split()[0])
            npo.categories.add(tertiary_category)
            npo.save()
        except Category.DoesNotExist:
            print 'Error, category %s does not exist.' % npoinfo['tertiary_org_type']
    if 'tertiary_org_subtype' in npoinfo:
        try:
            tertiary_category_subtype = Category.objects.get(meta_keywords=npoinfo['tertiary_org_subtype'].split()[0])
            npo.categories.add(tertiary_category_subtype)
            npo.save()
        except Category.DoesNotExist:
            print 'Error, category %s does not exist.' % npoinfo['tertiary_org_subtype']
            CategorizeUnknown(npoinfo['tertiary_org_subtype'])
            print 'Created new category:', Category.objects.get(name=npoinfo['tertiary_org_subtype'])

def SoftSyncToGuidestar():
    """
        If Mission Statement doesn't exist, then the
        Guidestar info has never been synced.
    """
    i = 0
    for npo in Npo.objects.all():
        if not npo.mission_statement:
            Guidestar(npo)
            print npo.name, 'is now synced with the Guidestar database.'
            i += 1
            if i % 10 == 0:
                # Wait a minute every 10 NPO syncs 
                # to keep from overloading Guidestar
                print 'Waiting...'
                time.sleep(60)
        else:
            print npo.name, 'has already been synced with the Guidestar database.'

def HardSyncToGuidestar():
    i = 0
    for npo in Npo.objects.all():
        Guidestar(npo)
        print npo.name, 'is now synced with the Guidestar database.'
        i += 1
        if i % 10 == 0:
            print 'Waiting...'
            time.sleep(60)