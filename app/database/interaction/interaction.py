from flask.wrappers import Response
from app.database.exceptions import DSCIWeekDataNotFoundException
import os
import sys 
import json

from flask.json import jsonify
from sqlalchemy import inspect
from werkzeug.wrappers import response
import io
import csv

from app.database.models.models import Base, DSCIWeekData, allProduction, srwProduction, srwProductionPct
from app.database.client.client import MySQLConnection

from app.database.exceptions import DSCIWeekDataNotFoundException



class DbInteraction:

    def __init__(self, host, port, user, password, db_name, rebuild_db=False):

        self.mysql_connection = MySQLConnection(
            host=host,
            port=port,
            user=user,
            password=password,
            db_name=db_name,
            rebuild_db=rebuild_db
        )

        self.engine = self.mysql_connection.connection.engine
        self.inspector = inspect(self.engine)

        if rebuild_db:
            self.create_dsci_clean_table()
            self.create_all_prod_table()
            self.create_wnr_prod_table()
            self.create_sp_prod_table()
            self.create_srw_prod_table()
            self.create_srw_prod_pct_table()
            self.create_dsci_wnr_table()
            self.create_dsci_all_table()
            self.create_dsci_srw_table()
            self.create_dsci_sp_table()
    
    def create_dsci_clean_table(self):
        if not self.inspector.has_table('dsci_clean'):
            Base.metadata.tables['dsci_clean'].create(self.engine)
        else:
            self.mysql_connection.execute_query('DROP TABLE IF EXISTS dsci_clean')
            Base.metadate.tables['dsci_clean'].create(self.engine)

    def create_dsci_all_table(self):
        if not self.inspector.has_table('dsci_all'):
            Base.metadata.tables['dsci_all'].create(self.engine)
        else:
            self.mysql_connection.execute_query('DROP TABLE IF EXISTS dsci_all')
            Base.metadate.tables['dsci_all'].create(self.engine)

    def create_dsci_wnr_table(self):
        if not self.inspector.has_table('dsci_wnr'):
            Base.metadata.tables['dsci_wnr'].create(self.engine)
        else:
            self.mysql_connection.execute_query('DROP TABLE IF EXISTS dsci_wnr')
            Base.metadate.tables['dsci_wnr'].create(self.engine)

    def create_dsci_sp_table(self):
        if not self.inspector.has_table('dsci_sp'):
            Base.metadata.tables['dsci_sp'].create(self.engine)
        else:
            self.mysql_connection.execute_query('DROP TABLE IF EXISTS dsci_sp')
            Base.metadate.tables['dsci_sp'].create(self.engine)

    def create_dsci_srw_table(self):
        if not self.inspector.has_table('dsci_srw'):
            Base.metadata.tables['dsci_srw'].create(self.engine)
        else:
            self.mysql_connection.execute_query('DROP TABLE IF EXISTS dsci_srw')
            Base.metadate.tables['dsci_srw'].create(self.engine)
    
    def create_all_prod_table(self):
        if not self.inspector.has_table('all_prod'):
            Base.metadata.tables['all_prod'].create(self.engine)
        else:
            self.mysql_connection.execute_query('DROP TABLE IF EXISTS all_prod')
            Base.metadate.tables['all_prod'].create(self.engine)

    def create_wnr_prod_table(self):
        if not self.inspector.has_table('wnr_prod'):
            Base.metadata.tables['wnr_prod'].create(self.engine)
        else:
            self.mysql_connection.execute_query('DROP TABLE IF EXISTS wnr_prod')
            Base.metadate.tables['wnr_prod'].create(self.engine)
    
    def create_sp_prod_table(self):
        if not self.inspector.has_table('sp_prod'):
            Base.metadata.tables['sp_prod'].create(self.engine)
        else:
            self.mysql_connection.execute_query('DROP TABLE IF EXISTS sp_prod')
            Base.metadate.tables['sp_prod'].create(self.engine)

    def create_srw_prod_table(self):
        if not self.inspector.has_table('srw_prod'):
            Base.metadata.tables['srw_prod'].create(self.engine)
        else:
            self.mysql_connection.execute_query('DROP TABLE IF EXISTS srw_prod')
            Base.metadate.tables['srw_prod'].create(self.engine)

    def create_srw_prod_pct_table(self):
        if not self.inspector.has_table('srw_prod_pct'):
            Base.metadata.tables['srw_prod_pct'].create(self.engine)
        else:
            self.mysql_connection.execute_query('DROP TABLE IF EXISTS srw_prod_pct')
            Base.metadate.tables['srw_prod_pct'].create(self.engine)

    def add_dsci_clean_week_data(self, releaseID, mapDate, stateAbbr, none, d0, d1, d2, d3, d4):
        dsci_clean_week_data = DSCIWeekData(
            releaseID=releaseID,
            mapDate=mapDate,
            stateAbbr=stateAbbr,
            none=none,
            d0=d0,
            d1=d1,
            d2=d2,
            d3=d3,
            d4=d4
        )
        self.mysql_connection.session.add(dsci_clean_week_data)
        self.mysql_connection.session.flush()
        self.mysql_connection.session.refresh(dsci_clean_week_data)
        return self.get_dsci_clean_week_data(dsci_clean_week_data.id)

    def bulk_add_dsci_clean_week_data(self, bulk_data):
        self.mysql_connection.session.bulk_save_objects(bulk_data)
        self.mysql_connection.session.expire_all()
        return 'Created'

    def bulk_add_prod_data(self, bulk_data):
        self.mysql_connection.session.bulk_save_objects(bulk_data)
        self.mysql_connection.session.expire_all()
        return 'Created'

    def is_week_exists(self, mapDate):
        exists = self.mysql_connection.session.query(DSCIWeekData.mapDate).filter_by(mapDate=mapDate).first() is not None
        return exists

    def download_dsci_clean(self):
        data = self.mysql_connection.connection.execute('SELECT * FROM dsci_clean')
        result = data.fetchall()
        output = io.StringIO()
        writer = csv.writer(output)

        line = ['id, releasID, mapDate, stateAbbr, none, d0, d1, d2, d3, d4']

        writer.writerow(line)

        for row in result:
            line = [str(row[0]) + ',' + str(row[1]) + ',' + str(row[2]) + ',' + str(row[3]) + ',' + str(row[4]) + ',' + str(row[5]) + ',' + str(row[6]) + ',' + str(row[7]) + ',' + str(row[8]) + ',' + str(row[9])]
            writer.writerow(line)
        
        output.seek(0)
        return Response(
            output,
            mimetype='text/csv',
            headers={"Content-Disposition":"attachment;filename=actual_dsci_clean.csv"}
        )

    def get_dsci_clean_week_data(self, id):
        dsci_clean_week_data = self.mysql_connection.session.query(DSCIWeekData).filter_by(id=id).first()
        if dsci_clean_week_data:
            self.mysql_connection.session.expire_all()
            return {
                    'id': dsci_clean_week_data.id,
                    'mapDate': dsci_clean_week_data.mapDate,
                    'stateAbbr': dsci_clean_week_data.stateAbbr,
                    'none': dsci_clean_week_data.none,
                    'd0': dsci_clean_week_data.d0,
                    'd1': dsci_clean_week_data.d1,
                    'd2': dsci_clean_week_data.d2,
                    'd3': dsci_clean_week_data.d3,
                    'd4': dsci_clean_week_data.d4,
                }
        else:
            raise DSCIWeekDataNotFoundException(f'DSCI week data {id} is not found')

    def srw_prod_calc(self):
        objs = []
        srw_pct_prod = self.mysql_connection.session.query(srwProductionPct).all()
        for item in srw_pct_prod:
            all_val = self.mysql_connection.session.query(allProduction).filter_by(year=item.year).filter_by(stateAbbr=item.stateAbbr).first()
            srw_prod_item = srwProduction(
                stateAbbr=item.stateAbbr,
                year=item.year,
                value=int(all_val.value*(1/item.value)) if item.value > 0 else 0
            )
            objs.append(srw_prod_item)
        self.mysql_connection.session.bulk_save_objects(objs)
        self.mysql_connection.session.expire_all()
        return 'ok'



    


