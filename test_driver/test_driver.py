#!/usr/bin/env python
import json
import random
import sys
import os
import shutil
import re
from valuelib import ValueLib

# Base Design:
#  * Consists of intelligence for driving values for particular types
#    of tests.
#  * Users of the class subscribe to different data values (including
#    ones passed in)
#  * Class returns a generator based on the type specified (random, or
#    iterative)

class TestDriver(object):
    def __init__(self, config_filename="test_values.json"):
        self.load_config(config_filename)
        self.valuelib = ValueLib()

    def get_contexts(self):
        ''' get_contexts(): returns a list of test value contexts '''
        return self.config.keys()

    def get_values(self, context):
        ''' get_values(context): returns a list of test values for the specified context '''
        try:
            return self.config[context]
        except KeyError:
            sys.stderr.write("Error: No entry in config for specified context \'%s\'\n" % context)
            raise

        return False

    def add_context(self, context):
        ''' add_context(context): creates a new context entry in the test config '''
        if self.config.has_key(context):
            sys.stderr.write("Error: Context \'%s\' already exists.\n" % context)
            return False
        else:
            self.config[context] = list()

        return True

    def add_value(self, context, value):
        ''' add_value(context, value): adds a new test value to the specified context '''
        if not self.config.has_key(context):
            sys.stderr.write("Error: Non existant context \'%s\'\n" % context)
            return False

        if value in self.config[context]:
            sys.stderr.write("Error: Value \'%s\' already exists in context \'%s\'\n" % (value, context))
            return False

        self.config[context].append(value)
        return True

    def write_config(self, config_filename=None):
        ''' write_config([filename]): write the existing test values config to disk, if
            no filename is specified use the classes config_filename. '''
        if (config_filename==None):
            config_filename=self.config_filename

        # if the file to write data to exists, attempt to make a backup
        if os.path.exists(config_filename):
            # backup existing config if possible
            backup_file = "."+os.path.basename(config_filename)+".bak"
            backup_path = os.path.dirname(config_filename)

            # if no path, leave path alone otherwise recombine the file
            if backup_path != "":
                backup_path += "/"+backup_file
            else:
                backup_path = backup_file

            # make a backup of the existing config in case of error
            shutil.move(config_filename, backup_path)

        # write new config
        config_fh = open(config_filename, 'w')
        json.dump(self.config, config_fh, indent=4)
        config_fh.close()

    def evaluate(self, valstr):
        value = valstr

        # test if value contains a function call like "func(args)"
        match = re.match("([\w_]+)\((|[\W\d\w\,]+)\)", valstr)
        if match:
            print "matched a function!"
        else:
            print "didn't match a function!"

        # return the evaluated value
        return value

    def load_config(self, config_filename=None):
        if (config_filename==None):
            config_filename=self.config_filename

        self.config_filename = config_filename
        self.config_fh = open(config_filename, 'r')
        self.config = json.load(self.config_fh)

    def iterative_test(self, selector):
        ''' iterative_test(context): creates and returns a generator that supplies
            test values iteratively from specified context. '''
        tests = list()
        for context in selector.split(","):
            tests.extend(self.get_values(context))

        for test in tests:
            yield self.evaluate(test)

    def random_test(self, selector, count=50):
        tests = list()
        for context in selector.split(","):
            tests.extend(self.get_values(context))

        for num in xrange(count):
            yield self.evaluate(random.choice(tests))

if __name__=="__main__":
    pass
