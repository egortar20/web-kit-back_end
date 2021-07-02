USDA_URL = 'http://quickstats.nass.usda.gov/api/api_GET/'
USDA_COUNT_URL = 'http://quickstats.nass.usda.gov/api/get_counts/'
USDA_API_KEY = 'A92F852D-5F52-318B-82B6-03D090E8663B'
USDA_PROD_TYPE = {
    'srw': 'WINTER, RED, SOFT',
    'all': 'ALL CLASSES',
    'wnr': 'WINTER',
    'sp': 'SPRING, (EXCL DURUM)'
}
USDA_UNITS = {
    'bu': 'BU',
    'pct': 'PCT BY TYPE'
}

class USDAParams():
    def __init__(self, stateAbbr=None, year=None, type=None, unit=None):    
        self.key = USDA_API_KEY
        self.source_desc =  'SURVEY'
        self.sector_desc =  'CROPS'
        self.group_desc =  'FIELD CROPS'
        self.commodity_desc =  'WHEAT'
        self.class_desc =  type
        self.prodn_practice_desc =  'ALL PRODUCTION PRACTICES'
        self.util_practice_desc =  'ALL UTILIZATION PRACTICES'
        self.statisticcat_desc =  'PRODUCTION'
        self.unit_desc =  unit
        self.domain_desc =  'TOTAL'
        self.agg_level_desc =  'STATE'
        if stateAbbr:
            self.state_alpha = stateAbbr
        self.freq_desc = 'ANNUAL'
        self.reference_period_desc = 'YEAR'
        if year:
            self.year = year
    
