#!/usr/bin/env python3

""" The purpose of this script is to provide python tools to access Lobo data via web services """

__author__ = 'Nick Dickens'
__copyright__ = 'Copyright 2016, Nick Dickens FAU Harbor Branch Oceanographic Institute'
__credits__ = ['Nick Dickens']

import sys
import urllib.request
import urllib.parse
from urllib.error import URLError
import json
import traceback
from pprint import pprint

from Node import Node

class Lobo(object):
    '''
    Class for Lobo data, built around FAU HBOI data but should work with all Loboviz if the
    interface is the same and you can make an appropriate json (see fau_hboi.json)
    built from http://fau.loboviz.com/cgidoc/

        Parameter	Description
        min_date	first day of data query in format [YYYYMMDD]
        max_date	last day of data query in format [YYYYMMDD]
        y	comma-separated list of measurement names for dependent variable(s)
        data_format	required to be 'text' for text output

    '''
    def __init__(self,json="fau_hboi.json"):
        self.json_file =  json
        self.load_json()
        self.set_base_url()

    def check_json_file(self):
        '''
        check the json file exists, isn't empty and has all the required field (do this now and it won't
         need to be done in individual methods
        :return:
        '''

        pass

    def load_json(self):
        '''
        :return:
        '''
        self.check_json_file()
        with open(self.json_file, "r") as json_file:
            json_data = json.load(json_file)
            self.host = json_data['host']
            self.cgi =  json_data['cgi']
            #sys.exit(0)

    def set_base_url(self):
        #set the url once the json is loaded as something like:
        self.base_url = "http://" + self.host + "/" + self.cgi

    def web_request(self, query_data, measurements):
        '''
        :param query_data: this is not self.query_data because one lobo can have multiple queries
        :return:
        '''
        request = urllib.request.Request(self.base_url, query_data)
        try:
            response = urllib.request.urlopen(request)
        except URLError as e:
            sys.stderr.write('ERROR: web_request urrlib error! [' + str(e.reason) + ']\n')
            sys.exit(1)
        except Exception as e:
            sys.stderr.write('ERROR: web_request exception! [' + traceback.format_exc() + ']\n')
            sys.exit(1)
        # this_content = response.readall().decode('utf-8')
        # print (self.base_url, query_data)
        self.parse_response(response, measurements)


    def parse_response(self,response,measurements):


        response_data = response.read().decode('utf-8').split("\n")
        for line_num, response_line in enumerate(response_data):
            data = response_line.split("\t")
            if line_num<3:
                continue
            if len(data) == len(measurements)+1:
                x, *y = data
                print(x, y[0],y[1])
            else:
                pass
        # example response
        # Sensor 0035 - IRL-LP
        # Indian River Lagoon - Link Port
        # date [EST]	CDOM [QSDE]
        # 2013-05-01 00:00:00	15.47
        # 2013-05-01 01:00:00	14.33
        # 2013-05-01 02:00:00	14.83
        # 2013-05-01 03:00:00	14.73
        #print(this_content)


    def load_nodes(self):
        self.nodes = [] # list of nodes - using a list as there are few nodes, change this to a dict of id : node object
        for id in self.json_data.nodes:
            node = Node(id, self.json_data.nodes[id])
            self.nodes.append(node)

    def load_measurements(self):
        self.measurements = {}
        pass

    def load_queries(self):
        pass

    def load_measurements(self):
        pass

    def set_data_range(self):
        '''
        start_year - year in the format yyyy
        start_month - month in the format mm
        start_day - day in the formay dd
        end_year - yyyy year
        end_month - mm number
        end_day - dd number
        :return:
        '''

    def fetch_data(self,node=36,dates=["20160901","20160929"],measurements=["temperature", "cdom"],format="text"):
        #node = 35 # replace this with node object so this will be node.serial_number
        #dates = ["20160901","20160929"]
        #measurements = ["cdom"]
        query_values = {'y': ",".join(measurements)}
        query_values['data_format'] = "xml"
        query_values['node'] = node
        #add with query_values[key] = value

        query_data = urllib.parse.urlencode(query_values)  # I added this
        query_data = query_data.encode('utf-8')  # I added this
        #return query_data
        self.web_request(query_data,measurements)



if  __name__ == '__main__':
    lobo = Lobo()
    lobo.fetch_data()
