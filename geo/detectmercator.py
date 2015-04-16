import os
import re
from itertools import islice



#myreg = re.compile('.+coordinates\": \[(.+)\].+')
myreg = re.compile('.+coordinates\": \[([\-\,\d\.\s]+)\].+')

data_path = ""

file_list = os.listdir(data_path)

for file_name in file_list:
    file_path = os.path.join(data_path, file_name)
    #print "filename: ", file_name
    print "Parsing file: ", file_path

    try:
        curr_file = open(file_path)
    except IOError, i:
        continue

    try:
        #head = [next(curr_file) for x in xrange(500)]
        #head = list(islice(curr_file, 1000))
        head = curr_file.readlines()
    except StopIteration, s:
        pass

    bad_coords = 0

    for line in head:

        m = myreg.match(line)
        if m:
            coordstr = m.groups()[0]

            coords = coordstr.split(", ")
            #print "coords[0]", float(coords[0])
            #print "coords[1]", float(coords[1])

            if bad_coords > 5:
                break

            if (float(coords[0]) > 180.0) or (float(coords[0]) < -180.0):
                print "Bad coords in %s: %s" % (file_name, coords)
                bad_coords += 1
                continue

            if (float(coords[1]) > 90.0) or (float(coords[1]) < -90.0):
                print "Bad coords in %s: %s" % (file_name, coords)
                bad_coords += 1
                continue


    if bad_coords > 0:
        print "File: coordinate out of range in file_name: %s, full_path: %s" % (file_name, file_path)
        continue




    curr_file.close()

