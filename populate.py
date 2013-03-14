# -*- coding: utf-8 -*-
# Pathos Charity Stream
# Non-Profit Organization Database Population Scripts - 2013
# Written by Glen Baker - iepathos@gmail.com

"""
    NPOPopulateAll()
    NPOPopulateByState(US_state_abbreviation)
    CategoryPopulate()

"""
from npo.models import Npo
from categories.models import Category
import sys

# Dictionary of valid US states by abbreviation
states = {
    'AL': 'Alabama',
    'AK': 'Alaska',
    'AZ': 'Arizona',
    'AR': 'Arkansas',
    'CA': 'California',
    'CO': 'Colorado',
    'CT': 'Connecticut',
    'DC': 'District of Columbia',
    'DE': 'Delaware',
    'FL': 'Florida',
    'GA': 'Georgia',
    'HI': 'Hawaii',
    'ID': 'Idaho',
    'IL': 'Illinois',
    'IN': 'Indiana',
    'IA': 'Iowa',
    'KS': 'Kansas',
    'KY': 'Kentucky',
    'LA': 'Louisiana',
    'ME': 'Maine',
    'MD': 'Maryland',
    'MA': 'Massachusetts',
    'MI': 'Michigan',
    'MN': 'Minnesota',
    'MS': 'Mississippi',
    'MO': 'Missouri',
    'MT': 'Montana',
    'NE': 'Nebraska',
    'NV': 'Nevada',
    'NH': 'New Hampshire',
    'NJ': 'New Jersey',
    'NM': 'New Mexico',
    'NY': 'New York',
    'NC': 'North Carolina',
    'ND': 'North Dakota',
    'OH': 'Ohio',
    'OK': 'Oklahoma',
    'OR': 'Oregon',
    'PA': 'Pennsylvania',
    'RI': 'Rhode Island',
    'SC': 'South Carolina',
    'SD': 'South Dakota',
    'TN': 'Tennessee',
    'TX': 'Texas',
    'UT': 'Utah',
    'VT': 'Vermont',
    'VA': 'Virginia',
    'WA': 'Washington',
    'WV': 'West Virginia',
    'WI': 'Wisconsin',
    'WY': 'Wyoming',
}

def NPOPopulateAll():
    """ 
        Internal Function to populate the database with the initial 
        NPO information from the IRS pub78 download
    """
    # IRS Tax-Exempt NPO's list http://apps.irs.gov/app/eos/forwardToPub78Download.do

    # wget http://apps.irs.gov/pub/epostcard/data-download-pub78.zip

    lines = open('irs-pub78.txt', 'r').readlines()
    # Information in format: ein | name | city | state | - | United States |

    for line in lines:
        npodata = line.split('|')
        try:
            npo = Npo.objects.get(ein=npodata[0])
            print 'Found NPO :', npo.name, 'skipping.'
        except Npo.DoesNotExist:
            npo = Npo(ein=npodata[0], name=npodata[1], city=npodata[2], state=npodata[3], country=npodata[5])
            print 'Writing NPO :', npo.name, 'to database.'
            npo.save()

def NPOPopulateByState(state):
    """
        Internal function to populate the database with NPO's by state.

        Takes an abbreviated state string, ex. 'CA', 'NY', 'WA'

    """
    state = str(state) # safety dance
    if state in states.keys():
        print 'Populating database with Non-Profit Organizations in the state of', states[state]

        lines = open('irs-pub78.txt', 'r').readlines()
        # Information in format: ein | name | city | state | - | United States |

        for line in lines:
            npodata = line.split('|')
            if npodata[3] == state:
                try:
                    npo = Npo.objects.get(ein=npodata[0])
                    print 'Found NPO :', npo.name, 'skipping.'
                except Npo.DoesNotExist:
                    npo = Npo(ein=npodata[0], name=npodata[1], city=npodata[2], state=npodata[3], country=npodata[5])
                    print 'Writing NPO :', npo.name, 'to database.'
                    npo.save()
    else:
        print 'Error, not a valid state abbreviation.'

def CategoryPopulate():
    """ 
        Internal Function to populate the database with the initial 
        Category information from the National Taxonomy of Tax Exempt
        Organizations (NTEE)
    """
    lines = open('ntee-categories.txt', 'r').readlines()
    for line in lines:
        if line != '':
            try:
                # Clean lines and write them to database
                category = Category.objects.get(name=line.strip())
                print 'Category', category, 'already exists.'
            except Category.DoesNotExist:
                category = Category(name=line.strip(), meta_keywords=line.split()[0])
                print 'Writing Category %s to database...' % line.strip()
            # NTEE Code set as first meta keyword for each category
            category.meta_keywords = str(category.name).split()[0]
            category.save()

            ### Assign Parent Categories
            if line.startswith('A') and line[1] != ' ':
                # A is the parent Category
                category.parent = Category.objects.get(name='A Arts, Culture, and Humanities')
            if line.startswith('B') and line[1] != ' ':
                # B is the parent Category
                category.parent = Category.objects.get(name='B Educational Institutions')
            if line.startswith('C') and line[1] != ' ':
                # C is the parent Category
                category.parent = Category.objects.get(name='C Environmental Quality Protection, Beautification')
            if line.startswith('D') and line[1] != ' ':
                # D is the parent Category
                category.parent = Category.objects.get(name='D Animal related')
            if line.startswith('E') and line[1] != ' ':
                # E is the parent Category
                category.parent = Category.objects.get(name='E Health—General & Rehabilitative')
            if line.startswith('F') and line[1] != ' ':
                # F is the parent Category
                category.parent = Category.objects.get(name='F Mental Health, Crisis Intervention')
            if line.startswith('G') and line[1] != ' ':
                # G is the parent Category
                category.parent = Category.objects.get(name='G Disease, Disorders, Medical Disciplines')
            if line.startswith('H') and line[1] != ' ':
                # H is the parent Category
                category.parent = Category.objects.get(name='H Medical Research')
            if line.startswith('I') and line[1] != ' ':
                # I is the parent Category
                category.parent = Category.objects.get(name='I Crime, Legal Related')
            if line.startswith('J') and line[1] != ' ':
                # J is the parent Category
                category.parent = Category.objects.get(name='J Employment, Job Related')
            if line.startswith('K') and line[1] != ' ':
                # K is the parent Category
                category.parent = Category.objects.get(name='K Agriculture, Food, Nutrition')
            if line.startswith('L') and line[1] != ' ':
                # L is the parent Category
                category.parent = Category.objects.get(name='L Housing, Shelter')
            if line.startswith('M') and line[1] != ' ':
                # M is the parent Category
                category.parent = Category.objects.get(name='M Public Safety, Disaster Preparedness and Relief')
            if line.startswith('N') and line[1] != ' ':
                # N is the parent Category
                category.parent = Category.objects.get(name='N Recreation, Sports, Leisure, Athletics')
            if line.startswith('O') and line[1] != ' ':
                # O is the parent Category
                category.parent = Category.objects.get(name='O Youth Development')
            if line.startswith('P') and line[1] != ' ':
                # P is the parent Category
                category.parent = Category.objects.get(name='P Human Services')
            if line.startswith('Q') and line[1] != ' ':
                # Q is the parent Category
                category.parent = Category.objects.get(name='Q International, Foreign Affairs, and National Security')
            if line.startswith('R') and line[1] != ' ':
                # R is the parent Category
                category.parent = Category.objects.get(name='R Civil Rights, Social Action, Advocacy')
            if line.startswith('S') and line[1] != ' ':
                # S is the parent Category
                category.parent = Category.objects.get(name='S Community Improvement, Capacity Building')
            if line.startswith('T') and line[1] != ' ':
                # T is the parent Category
                category.parent = Category.objects.get(name='T Philanthropy, Voluntarism, and Grantmaking')
            if line.startswith('U') and line[1] != ' ':
                # U is the parent Category
                category.parent = Category.objects.get(name='U Science and Technology Research Institutes')
            if line.startswith('V') and line[1] != ' ':
                # V is the parent Category
                category.parent = Category.objects.get(name='V Social Science Research Institutes')
            if line.startswith('W') and line[1] != ' ':
                # W is the parent Category
                category.parent = Category.objects.get(name='W Public, Society Benefit')
            if line.startswith('X') and line[1] != ' ':
                # X is the parent Category
                category.parent = Category.objects.get(name='X Religion, Spiritual Development')
            if line.startswith('Y') and line[1] != ' ':
                # Y is the parent Category
                category.parent = Category.objects.get(name='Y Mutual/Membership Benefit Organizations, Other')
            if line.startswith('Z') and line[1] != ' ':
                # Z is the parent Category
                category.parent = Category.objects.get(name='Z Unknown')

            category.save()
