import os
import sys

from flask.wrappers import Response
sys.path.insert(1, os.path.join(sys.path[0], '../../'))

from app.database.interaction.interaction import DbInteraction
from app.database.models.models import DSCIWeekData


from app.api.utils import config_parser
from flask import Flask, request
from flask_cors import CORS, cross_origin
from flask.json import jsonify
import threading
import argparse
import requests
import json

from app.api.constants import DSCI_URL, STATES, STATS_TYPE


class Server:
    def __init__(self, host, port, db_host, db_port, db_user, db_pass, db_name, rebuild_db=False):
        #Server
        self.host = host
        self.port = port

        self.app = Flask(__name__)
        CORS(self.app)

        self.app.add_url_rule('/', view_func=self.get_home)
        self.app.add_url_rule('/initiate', view_func=self.initiate)
        self.app.add_url_rule('/download', view_func=self.download_dsci_clean)

        self.app.register_error_handler(404, self.page_not_found)

        self.db_interaction = DbInteraction(
            user=db_user,
            password=db_pass,
            host=db_host,
            port=db_port,
            db_name=db_name,
            rebuild_db=False
        )

    def run_server(self):
        self.server = threading.Thread(target=self.app.run, kwargs={'host' : self.host, 'port': self.port})
        self.server.start()
        return self.server

    def get_home(self):
        return 'Hello, it`s a working APIv1.0 for TEOSS web-kit'

    def page_not_found(self, err):
        return jsonify(error=str(err)), 404

    def initiate(self):
        self.get_dsci_clean()

    def load_full_dsci_table(self):
        self.get_dsci_clean()

    def load_last_week_dsci(self):
        objs = []
        for i in range(1, len(STATES)):
            state_no = "'" + (('0' + str(i)) if i < 10 else str(i)) + "'"
            params = {
                'area': state_no,
                'statstype': STATS_TYPE
            }
            last_week = json.loads(requests.get(DSCI_URL, headers={'Content-Type': 'application/json'}, params=params).content)['d'][0]
            last_week_res = DSCIWeekData(
                releaseID=last_week['ReleaseID'],
                mapDate=last_week['mapDate'],
                stateAbbr=last_week['stateAbbr'],
                none=last_week['NONE'],
                d0=last_week['D0'],
                d1=last_week['D1'],
                d2=last_week['D2'],
                d3=last_week['D3'],
                d4=last_week['D4']
            )
            objs.append(last_week_res)
        if self.db_interaction.is_week_exists(objs[0].mapDate):
            resp = self.db_interaction.bulk_add_dsci_clean_week_data(objs)
            response = jsonify(resp)
            response.status_code = 200
            return response
        else:
            response = jsonify('Already exists')
            response.status_code = 200
            return response

    def download_dsci_clean(self):
        return self.db_interaction.download_dsci_clean()

    def get_dsci_clean(self):
        objs = []
        for i in range(1, len(STATES)):
            state_no = "'" + (('0' + str(i)) if i < 10 else str(i)) + "'"
            params = {
                'area': state_no,
                'statstype': STATS_TYPE
            }
            res = json.loads(requests.get(DSCI_URL, headers={'Content-Type': 'application/json'}, params=params).content)['d']
            if len(res):
                for item in res:
                    item_res = DSCIWeekData(
                        releaseID=item['ReleaseID'],
                        mapDate=item['mapDate'],
                        stateAbbr=item['stateAbbr'],
                        none=item['NONE'],
                        d0=item['D0'],
                        d1=item['D1'],
                        d2=item['D2'],
                        d3=item['D3'],
                        d4=item['D4']
                    )
                    objs.append(item_res)
        resp = self.db_interaction.bulk_add_dsci_clean_week_data(objs)
        response = jsonify(resp)
        response.status_code = 200
        return response

            

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', type=str, dest='config')

    args = parser.parse_args()

    config = config_parser(args.config)

    #Server config
    server_host = config["SERVER_HOST"]
    server_port = config["SERVER_PORT"]

    #DB config
    db_host = config["DB_HOST"]
    db_port = config["DB_PORT"]
    db_user = config["DB_USER"]
    db_pass = config["DB_PASS"]
    db_name = config["DB_NAME"]


    server = Server(
        host=server_host,
        port=server_port,
        db_host=db_host,
        db_port=db_port,
        db_user=db_user,
        db_pass=db_pass,
        db_name=db_name
    )

    server.run_server()


        


        