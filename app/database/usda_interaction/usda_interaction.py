from app.database.models.models import allProduction, wnrProduction, spProduction, srwProduction
import os
import sys
from datetime import datetime


sys.path.insert(1, os.path.join(sys.path[0], '../../../'))

from app.database.usda_interaction.usda_conf import USDAParams, USDA_COUNT_URL, USDA_PROD_TYPE, USDA_UNITS, USDA_URL
from app.api.constants import STATES
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
        for year in range(1999, self.check_prod_last_year(USDA_PROD_TYPE['all'], USDA_UNITS['bu'])):
            for state in STATES.keys():
                if self.check_state(state):
                    params = USDAParams(str(state), year, USDA_PROD_TYPE['all'], USDA_UNITS['bu']).__dict__
                    line = json.loads(requests.get(USDA_URL, params=params).content)['data'][0]
                    prod_all.append(allProduction(
                        stateAbbr=state,
                        year=year,
                        value=line['Value']
                    ))
        return prod_all
    
    def get_prod_wnr(self):
        prod_wnr = []
        for year in range(1999, self.check_prod_last_year(USDA_PROD_TYPE['wnr'], USDA_UNITS['bu'])):
            for state in STATES.keys():
                if self.check_state(state):
                    params = USDAParams(str(state), year, USDA_PROD_TYPE['wnr'], USDA_UNITS['bu']).__dict__
                    line = json.loads(requests.get(USDA_URL, params=params).content)['data'][0]
                    prod_wnr.append(wnrProduction(
                        stateAbbr=state,
                        year=year,
                        value=line['Value']
                    ))
        return prod_wnr

    def get_prod_sp(self):
        prod_sp = []
        for year in range(1999, self.check_prod_last_year(USDA_PROD_TYPE['sp'], USDA_UNITS['bu'])):
            for state in STATES.keys():
                if self.check_state(state):
                    params = USDAParams(str(state), year, USDA_PROD_TYPE['sp'], USDA_UNITS['bu']).__dict__
                    line = json.loads(requests.get(USDA_URL, params=params).content)['data'][0]
                    prod_sp.append(spProduction(
                        stateAbbr=state,
                        year=year,
                        value=line['Value']
                    ))
        return prod_sp

    def get_prod_srw(self):
        prod_srw = []
        for year in range(1999, self.check_prod_last_year(USDA_PROD_TYPE['srw'], USDA_UNITS['pct'])):
            for state in STATES.keys():
                if self.check_state(state):
                    params = USDAParams(str(state), year, USDA_PROD_TYPE['srw'], USDA_UNITS['pct']).__dict__
                    line = json.loads(requests.get(USDA_URL, params=params).content)['data'][0]
                    prod_srw.append(srwProduction(
                        stateAbbr=state,
                        year=year,
                        value=line['Value']
                    ))
        return prod_srw

if __name__ == '__main__':
    usda = USDAInteraction()
    print(usda.check_prod_last_year(USDA_PROD_TYPE['srw'], USDA_UNITS['pct']))