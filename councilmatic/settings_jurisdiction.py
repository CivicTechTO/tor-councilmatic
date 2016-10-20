# These are all the settings that are specific to a jurisdiction

import os
from configurations.values import Value, ListValue, DictValue, URLValue

class JurisdictionConfig(object):
    ###############################
    # These settings are required #
    ###############################

    OCD_CITY_COUNCIL_NAME = Value('Toronto City Council')
    CITY_COUNCIL_NAME = Value('Toronto City Council')
    OCD_JURISDICTION_ID = Value('ocd-jurisdiction/country:ca/csd:3520005/legislature')
    LEGISLATIVE_SESSIONS = ListValue(None) # the last one in this list should be the current legislative session
    CITY_NAME = Value('Toronto')
    CITY_NAME_SHORT = Value(None)

    # TODO: Yuck.
    # See: https://github.com/jazzband/django-configurations/issues/149
    @classmethod
    def setup(cls):
        default_city_short = cls.CITY_NAME_SHORT.value
        super().setup()
        if default_city_short == cls.CITY_NAME_SHORT:
            cls.CITY_NAME_SHORT = cls.CITY_NAME


    city_vocab = {
        'MUNICIPAL_DISTRICT': 'Ward',
        'SOURCE': 'City of Toronto',
        'COUNCIL_MEMBER': 'Councillor',
        'COUNCIL_MEMBERS': 'Councillors',
        'EVENTS': 'Meetings',
    }

    BOUNDARY_API_BASE_URL = Value('http://represent.opennorth.ca')

    # TODO: Keep track of this issue
    # Ref: https://github.com/jazzband/django-configurations/issues/151
    CITY_VOCAB = DictValue(city_vocab)

    APP_NAME = 'toronto'


    #########################
    # The rest are optional #
    #########################


    # this is for populating meta tags
    if os.environ.get('HEROKU_APP_NAME') :
        # Available when labs feature has been turned on: `heroku labs:enable runtime-dyno-metadata`
        # See: https://devcenter.heroku.com/articles/dyno-metadata
        HEROKU_URL = 'https://{}.herokuapp.com'.format(os.environ['HEROKU_APP_NAME'])
    else :
        HEROKU_URL = None

    SITE_URL = URLValue(HEROKU_URL or 'https://chicago.councilmatic.org')

    SITE_META = {
        'site_name' : 'Toronto Councilmatic',
        'site_desc' : 'City Council, demystified. Keep tabs on Toronto legislation, councillors, & meetings.',
        'site_author' : 'Civic Tech Toronto',
        'twitter_site': '@councilmatic',
        'twitter_creator': '@CivicTechTO',
    }

    LEGISTAR_URL = 'https://chicago.legistar.com/Legislation.aspx'


    # this is for the boundaries of municipal districts, to add
    # shapes to posts & ultimately display a map with the council
    # member listing. the boundary set should be the relevant
    # slug from the ocd api's boundary service
    # available boundary sets here: http://ocd.datamade.us/boundary-sets/
    BOUNDARY_SET = Value('toronto-wards')

    # this is for configuring a map of council districts using data from the posts
    # set MAP_CONFIG = None to hide map
    map_config = {
        'center': [43.7245,-79.3882],
        'zoom': 10,
        'color': "#54afe8",
        'highlight_color': "#C00000",
    }

    MAP_CONFIG = DictValue(map_config)


    FOOTER_CREDITS = [
        {
            'name':     'Civic Tech Toronto',
            'url':      'http://civictech.ca/',
            'image':    'civictechto-logo.png',
        },
        {
            'name':     'DataMade',
            'url':      'http://datamade.us/',
            'image':    'datamade-logo.png',
        },
        {
            'name':     'Sunlight Foundation',
            'url':      'http://sunlightfoundation.org/',
            'image':    'sunlight-logo.png',
        },
    ]

    # this is the default text in search bars
    SEARCH_PLACEHOLDER_TEXT = "police, zoning, O2015-7825, etc."



    # these should live in APP_NAME/static/
    IMAGES = {
        'logo': 'images/metro-toronto-logo.png',
    }
    # you can generate icons from the logo at http://www.favicomatic.com/
    # & put them in APP_NAME/static/images/icons/




    # THE FOLLOWING ARE VOCAB SETTINGS RELEVANT TO DATA MODELS, LOGIC
    # (this is diff from VOCAB above, which is all for the front end)

    # this is the name of the meetings where the entire city council meets
    # as stored in legistar
    CITY_COUNCIL_MEETING_NAME = 'City Council'

    COMMITTEE_CHAIR_TITLES = ListValue(['Chair', 'Vice Chair'])

    # this is for convenience, & used to populate a table
    # describing legislation types on the about page template
    LEGISLATION_TYPE_DESCRIPTIONS = [
        {
            'name': 'Action Items',
            'search_term': 'Action',
            'fa_icon': 'check-square-o',
            'html_desc': True,
            'desc': "Generally, these items are seeking some kind of direction or resolution from Council or Committee. Usually there are proposed recommendations which Council or Committee can adopt or amend by vote.",

        },
        {
            'name': 'Information Reports',
            'search_term': 'Information',
            'fa_icon': 'pie-chart',
            'html_desc': True,
            'desc': "A City official's report that advises and informs without recommending. <br />A vote is required to dispose of the item (normally, a <em>motion to receive</em>).",

        },
        {
            'name': 'Presentations',
            'search_term': 'Presentation',
            'fa_icon': 'bullhorn',
            'html_desc': True,
            'desc': "Normally a verbal update, a ceremonial presentation or presentations to the committee without a covering report, such as slide presentations or playing of videos. <br />A vote is required to dispose of the item (normally, a <em>motion to receive</em>).",

        },
    ]

    # these keys should match committee slugs
    # Source: http://www1.toronto.ca/wps/portal/contentonly?vgnextoid=762b6804e1f22410VgnVCM10000071d60f89RCRD&vgnextchannel=9632acb640c21410VgnVCM10000071d60f89RCRD
    COMMITTEE_DESCRIPTIONS = {
            "community-development-and-recreation-committee": "Social inclusion and undertaking work to strengthen services to communities and neighbourhoods.",
            "economic-development-committee": "Monitors and makes recommendations to strengthen Toronto’s economy and investment climate.",
            "government-management-committee": "Government assets and resources; monitors and makes recommendations on the administrative operations of the City.",
            "licensing-and-standards-committee": "Consumer safety and protection; monitors and makes recommendations on the licensing of business and the enforcement of property standards.",
            "parks-and-environment-committee": "Monitors, makes recommendations and undertakes work to ensure the sustainability of Toronto’s natural environment.",
            "planning-and-growth-management-committee": "Urban form and work related to good city planning; monitors and makes recommendations on the planning, growth and development of the City.",
            "public-works-and-infrastructure-committee": "Delivers and maintains Toronto’s infrastructure; monitors and makes recommendations on Toronto’s infrastructure needs and services.Urban form and work related to good city planning; monitors and makes recommendations on the planning, growth and development of the City.",
            "executive-committee": "Monitors and makes recommendations on Council’s strategic policy and priorities, governance policy and structure, financial planning and budgeting, fiscal policy including revenue and tax policies, intergovernmental and international relations, Council and its operations, and human resources and labour relations.",
            "affordable-housing-committee": "Affordable housing policies, acquiring land for affordable housing, providing funding and financing, development fee and charge waivers and property tax reductions or waivers for affordable housing projects. Proposes legislation and advocates to the provincial and federal governments. In charge of strategic planning for Toronto Community Housing, and measuring the effectiveness of Affordable Housing Office projects.",
            "budget-committee": "Includes, but is not limited to, coordinating the preparation of the capital and operating estimates, and making recommendations on the capital and operating budgets.",
            "employee-and-labour-relations-committee": "Reviews corporate human resource policy issues related to achieving and maintaining excellence in the public service and issues that affect the workforce. Responsibilities include compensation, performance management, training and development, recruitment, retention, retirement, labour relations, human rights, equity goals, wellness, and health and safety strategic policy direction on collective bargaining.",
            "audit-committee": "Considers and recommends to Council the appointment of external auditors for the City and the Auditor General’s office; the annual external audits of the financial statements of the City, its agencies and the Auditor General’s office; the Auditor General’s reports, audit plan and accomplishments.",
            "board-of-health": "Ensures that Toronto Public Health delivers programs and services in response to local needs; determines and sets public health policy and advises City Council on a broad range of health issues; recommendations with city-wide or financial implications are forwarded to City Council for final approval.",
            "civic-appointments-committee": "Considers and recommends to Council the citizens to appoint to agencies.",
            "striking-committee": "Recommends councillor appointments to fill the positions of the boards outlined above, as well many other boards, agencies and advisory committees; makes recommendations to Council on the meeting schedule for Council and Council Committees.",
    }

    ABOUT_BLURBS = {
        "COMMITTEES" : "<p>Most meaningful legislative activity happens in committee meetings, where committee members debate proposed legislation. These meetings are open to the public.</p>\
                        <p>Each committee has a Chair, who controls the committee meeting agenda (and thus, the legislation to be considered).</p>\
                        <p>Committee jurisdiction, memberships, and appointments all require City Council approval.</p>",
        "EVENTS":       "<p>There are two types of meetings: committee meetings and full city council meetings.</p>\
                        <p>Most of the time, meaningful legislative debate happens in committee meetings, which occur several times a month.</p>\
                        <p>Meetings of the entire City Council generally occur once a month at City Hall.</p>\
                        <p>All City Council meetings are open to public participation.</p>",
        "COUNCIL_MEMBERS": ""

    }

    # notable positions that aren't district representatives, e.g. mayor & city clerk
    # keys should match person slugs
    EXTRA_TITLES = {
        'mendoza-susana-a': 'City Clerk',
        'emanuel-rahm': 'Mayor',
    }


    TOPIC_HIERARCHY = [
        {
            'name': 'Citywide matters',
            'children': [
                {
                    'name': 'Municipal Code',
                    'children': [],
                },
                {
                    'name': 'City Business',
                    'children': [   {'name': 'Getting and Giving Land'},
                                    {'name': 'Intergovernmental Agreement'},
                                    {'name': 'Lease Agreement'},
                                    {'name': 'Vacation of Public Street'},],
                },
                {
                    'name': 'Finances',
                    'children': [ {'name': 'Bonds'} ],
                },
                {
                    'name': 'Appointment',
                    'children': [],
                },
                {
                    'name': 'Oath of Office',
                    'children': [],
                },
                {
                    'name': 'Airports',
                    'children': [],
                },
                {
                    'name': 'Special Funds',
                    'children': [   {'name': 'Open Space Impact Funds'} ],
                },
                {
                    'name': 'Inspector General',
                    'children': [],
                },
                {
                    'name': 'Council Matters',
                    'children': [   {'name': 'Call for Action'},
                                    {'name': 'Transfer of Committee Funds'},
                                    {'name': 'Correction of City Council Journal'},
                                    {'name': 'Next Meeting'},],
                },
            ]

        },
        {
            'name': 'Ward matters',
            'children': [
                {
                    'name': 'Business Permits and Privileges',
                    'children': [   {'name': 'Grant of privilege in public way'},
                                    {'name': 'Awnings'},
                                    {'name': 'Sign permits'},
                                    {'name': 'Physical barrier exemption'},
                                    {'name': 'Canopy'}],
                },
                {
                    'name': 'Residents',
                    'children': [   {'name': 'Handicapped Parking Permit'},
                                    {'name': 'Residential permit parking'},
                                    {'name': 'Condo Refuse Claim'},
                                    {'name': 'Senior citizen sewer refund'},],
                },
                {
                    'name': 'Land Use',
                    'children': [   {'name': 'Zoning Reclassification'},
                                    {'name': 'Liquor and Package Store Restrictions'},],
                },
                {
                    'name': 'Parking',
                    'children': [   {'name': 'Loading/Standing/Tow Zone'},
                                    {'name': 'Parking Restriction'},],
                },
                {
                    'name': 'Economic Development',
                    'children': [   {'name': 'Special Service Area'},
                                    {'name': 'Tax Incentives'},
                                    {'name': 'Tax Increment Financing'},],
                },
                {
                    'name': 'Traffic',
                    'children': [   {'name': 'Traffic signs and signals'},
                                    {'name': 'Vehicle Weight Limitation'},],
                },
                {
                    'name': 'Churches and Non-Profits',
                    'children': [   {'name': 'Tag Day Permits'} ],
                },
                {
                    'name': 'Redevelopment Agreement',
                    'children': [],
                },
            ],
        },
        {
            'name': 'Individual matters',
            'children': [
                {
                    'name': 'Small Claims',
                    'children': [   {'name': 'Damage to vehicle claim'},
                                    {'name': 'Damage to property claim'},
                                    {'name': 'Settlement of Claims'},
                                    {'name': 'Excessive water rate claim'},],
                },
                {
                    'name': 'Honorifics',
                    'children': [   {'name': 'Honorific Resolution'},
                                    {'name': 'Honorary street'},],
                },
            ],
        }
    ]

