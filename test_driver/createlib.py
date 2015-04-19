#!/usr/bin/env python
import urllib
import urllib2
import optparse
import json
import sys

__author__ = 'Andrew Tanner <andrew@refleqtive.com>'

####
# Define .pjson (or is there a better extension?)
# Define request in seperate .json file, with templating i.e. something like
# <% values.integer() %> embedded in the .json
#
# create.py -j <jsonfile> -n <number> -f|--front <front:port>

# TODO:
# 1. Add templating functionality to embed data generation functions
# 2. Add argparse functionality

# Inserter
#    - Manages the interface to the front for insertion
#    - Calls ___ to retrieve JSON strings to insert
#    - Perhaps threaded? for maximum insertion effeciancy
# Reader
#    - Does 1 evaluator == 1 json file?
#    - Loads JSON, parses it, comes up with final json data strings
#    - Returns a generator which can be called

# eval = Evaluator("foo.json")
# for i in xrange(0,100):
#    j = eval.get_json()
#    inserter.insert(j)


class Inserter(object):
    def __init__(self):
        self.front_host_url = None
        self.instane = None
        self.instance_url = None
        self.table_name = None

    def connect(self, front_host_url, instance, table_name):
        self.front_host_url = front_host_url
        self.instance = instance
        self.instance_url = "http://" + self.front_host_url + "/%s/schema" % self.instance
        self.table_name = table_name

    def insert_string(self, insert_data):
        try:
            full_url = "%s/%s" % (self.instance_url, self.table_name)
            print "Full URL: ", full_url

            req = urllib2.Request(full_url)
            insert_data.replace("\n", "\r\n")
            req.add_data(insert_data)
            response = urllib2.urlopen(req)
            response.close()

            print "Return Code: ", response.code

            # check status of response code
            if response.code != 200:
                print "Error, unexpected response code: ", rep.code

            response.close()

        except urllib2.HTTPError as e:
            print e

        #    # TODO: implement some kind of instance verification / error maybe?

        #    #curl http://10.0.1.110:8080/scdb_config/scdb/scdb_instances

# TODO: "Reader" really isn't descriptive enough, it also returns results
# Maybe "Extractor"?
class Reader(object):
    def __init__(self, json_file):
        self.json_file = json_file
        self.json_fh = None
        self.json_raw = None
        self.json = None

        # load the file I was handed
        self.eat_json_file()

    def eat_json_file(self):
        # TODO: try .. except?
        self.json_fh = open(self.json_file, 'r')

        # read into string first
        self.json_raw = self.json_fh.readlines()

        # evaluate templating

    def read_result(self):
        # read json
        #import pdb; pdb.set_trace()
        self.json = json.loads("".join(self.json_raw))
        return self.json

    # create read alias to read_result
    read = read_result

if __name__ == "__main__":
    r = Reader('tweet_v1.json')
    print "Returning JSON\n", r
    res = r.read_result()

    i = Inserter()
    i.connect("10.0.1.110:8080", "tdb", "tweet")
    i.insert_string(json.dumps(res)+"\r\n")

    # TODO: set up test environment
