import os
import sys
from datetime import datetime


sys.path.insert(1, os.path.join(sys.path[0], '../../../'))

from app.database.usda_interaction.usda_conf import USDAParams, USDA_COUNT_URL, USDA_PROD_TYPE, USDA_UNITS, USDA_URL
from app.api.constants import STATES
from app.database.models.models import allProduction, wnrProduction, spProduction, srwProduction

import requests
import json

class USDAInteraction():

    def __init__(self):
        pass

    def check_prod_last_year(self, type, unit):
        curr_year = datetime.today().year
        params = USDAParams(year=curr_year,type=type, unit=unit).__dict__
        if json.loads(requests.get(USDA_COUNT_URL, params=params).content)['count']:
            return curr_year
        else:
            return curr_year - 1

    def check_state(self, type, unit, year):
        params = USDAParams(year=year, type=type, unit=unit).__dict__
        if json.loads(requests.get(USDA_COUNT_URL, params=params).content)['count']:
            return True
        else: 
            return False

    def get_prod_all(self):
        prod_all = []
        for year in range(1999, self.check_prod_last_year(USDA_PROD_TYPE['all'], USDA_UNITS['bu']) + 1):
            params = USDAParams(year=year, type=USDA_PROD_TYPE['all'], unit=USDA_UNITS['bu']).__dict__
            for line in json.loads(requests.get(USDA_URL, params=params).content)['data']:
                prod_all.append(allProduction(
                    stateAbbr=line['state_alpha'],
                    year=year,
                    value=int(line['Value'].replace(',',''))
                ))
        return prod_all
    
    def get_prod_wnr(self):
        prod_wnr = []
        for year in range(1999, self.check_prod_last_year(USDA_PROD_TYPE['wnr'], USDA_UNITS['bu']) + 1):
            params = USDAParams(year=year, type=USDA_PROD_TYPE['wnr'], unit=USDA_UNITS['bu']).__dict__
            for line in json.loads(requests.get(USDA_URL, params=params).content)['data']:
                prod_wnr.append(wnrProduction(
                    stateAbbr=line['state_alpha'],
                    year=year,
                    value=int(line['Value'].replace(',',''))
                ))
        return prod_wnr

    def get_prod_sp(self):
        prod_sp = []
        for year in range(1999, self.check_prod_last_year(USDA_PROD_TYPE['sp'], USDA_UNITS['bu']) + 1):
            params = USDAParams(year=year, type=USDA_PROD_TYPE['sp'], unit=USDA_UNITS['bu']).__dict__
            for line in json.loads(requests.get(USDA_URL, params=params).content)['data']:
                prod_sp.append(spProduction(
                    stateAbbr=line['state_alpha'],
                    year=year,
                    value=int(line['Value'].replace(',',''))
                ))
        return prod_sp

    def get_prod_srw(self):
        prod_srw = []
        for year in range(1999, self.check_prod_last_year(USDA_PROD_TYPE['srw'], USDA_UNITS['pct']) + 1):
            params = USDAParams(year=year, type=USDA_PROD_TYPE['srw'], unit=USDA_UNITS['pct']).__dict__
            for line in json.loads(requests.get(USDA_URL, params=params).content)['data']:
                prod_srw.append(srwProduction(
                    stateAbbr=line['state_alpha'],
                    year=year,
                    value=int(line['Value'].replace(',',''))
                ))
        return prod_srw

