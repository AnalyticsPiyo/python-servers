"""Hello Analytics Reporting API V4."""
# 公式：https://developers.google.com/analytics/devguides/reporting/core/v4/basics?hl=ja
# 参考：https://note.nkmk.me/python-google-analytics-reporting-api-download/

import argparse

from apiclient.discovery import build
import httplib2
from oauth2client import client
from oauth2client import file
from oauth2client import tools

import json
import pprint
import pandas as pd

SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
DISCOVERY_URI = ('https://analyticsreporting.googleapis.com/$discovery/rest')
CLIENT_SECRETS_PATH = './modules/client_secrets.json' # Path to client_secrets.json file.

class Analytics():
    def __init__(self, viewid):
        self.viewid = viewid
        self.initialize_analyticsreporting()

        self.start_date = ""
        self.end_date = ""
        self.metrics = list()
        self.dimensions = list()
        self.orders = list()
        self.df = pd.DataFrame()

    def initialize_analyticsreporting(self):
        """Initializes the analyticsreporting service object.
        Returns:
          analytics an authorized analyticsreporting service object.
        """
        # Parse command-line arguments.
        parser = argparse.ArgumentParser(
            formatter_class=argparse.RawDescriptionHelpFormatter,
            parents=[tools.argparser])
        flags = parser.parse_args([])

        # Set up a Flow object to be used if we need to authenticate.
        flow = client.flow_from_clientsecrets(
            CLIENT_SECRETS_PATH, scope=SCOPES,
            message=tools.message_if_missing(CLIENT_SECRETS_PATH))

        # Prepare credentials, and authorize HTTP object with them.
        # If the credentials don't exist or are invalid run through the native client
        # flow. The Storage object will ensure that if successful the good
        # credentials will get written back to a file.
        storage = file.Storage('analyticsreporting.dat')
        credentials = storage.get()
        if credentials is None or credentials.invalid:
          credentials = tools.run_flow(flow, storage, flags)
        http = credentials.authorize(http=httplib2.Http())

        # Build the service object.
        self.analytics = build('analytics', 'v4', http=http, discoveryServiceUrl=DISCOVERY_URI)

        return self.analytics

    def get_report(self, s_date, e_date, m_list, d_list = list(), o_dict = dict()):
        self.start_date = s_date
        self.end_date = e_date
        self.metrics = [{'expression': 'ga:' + m} for m in m_list]
        
        if not d_list:
            self.columns = m_list
        else:
            self.dimensions = [{'name': 'ga:' + d} for d in d_list]
            self.columns = d_list + m_list 
        
        # orderのデータ作成
        if not o_dict:
            for k, v in o_dict.items():
                tmp_dict = dict()
                tmp_dict["fieldName"] = k
                tmp_dict["sortOrder"] = v
                self.order.append(tmp_dict)
        
        self.excute_query()
        self.print_response()
        
        return self.df

    def excute_query(self):
        # Use the Analytics Service Object to query the Analytics Reporting API V4.
        self.response =  self.analytics.reports().batchGet(
            body={
              'reportRequests': [
              {
                'viewId': self.viewid,
                'dateRanges': [{'startDate': self.start_date, 'endDate': self.end_date}],
                'metrics': self.metrics,
                'dimensions': self.dimensions,
                'orderBys': self.orders,
              }]
            }
        ).execute()
        
    def print_response(self):
        """Parses and prints the Analytics Reporting API V4 response"""
        date_list = list()

        # 第2引数はnullだった時のデフォルト値
        for i in self.response.get('reports')[0].get('data').get('rows'):
            if not i.get('dimensions'):
                adr_dict = dict(zip(self.columns, i.get('metrics')[0].get('values')))
            else:
                adr_dict = dict(zip(self.columns, i.get('dimensions') + i.get('metrics')[0].get('values')))
            date_list.append(adr_dict)
        self.df = pd.io.json.json_normalize(date_list)
