# Breaks GeoJSON multipolygon features into polygon features.
# Expects the GeoJSON to be preprocessed with getfeatures.py.

import json
import sys
import math
import fileinput
from optparse import OptionParser

DEBUG=True




# Bretts code


def ecef(point):
    a = 6378137.0       # major axis wgs84
    b = 6356752.314245  # minor axis wgs84
    e = math.sqrt(1 - ((b*b)/(a*a)))
    esqr = e*e
    h = 0 # ignore altitude
    phi = point[1] * math.pi / 180.0
    L   = point[0] * math.pi / 180.0
    sinphi = math.sin(phi)
    chi = math.sqrt(1 - (esqr * sinphi * sinphi))
    term = ((a/chi) + h) * math.cos(phi)
    return [term * math.cos(L), term * math.sin(L), (((1-esqr) * a/chi) + h) * sinphi]

def orient(p, q, r):
    pryz = (p[2] * r[1]) - (p[1] * r[2])
    prxz = (p[0] * r[2]) - (p[2] * r[0])
    prxy = (p[1] * r[0]) - (p[0] * r[1])
    d = (q[0] * pryz) + (q[1] * prxz) + (q[2] * prxy)
    return (d > 0) - (0 > d)




# old stuffs

def xy(points):
    x = list()
    y = list()
    temp = 0

    for point in points:
        x.extend([point[0]])
        y.extend([point[1]])

    return x, y


def signed_area(points):
    """Return the signed area enclosed by a ring in linear time using the
    algorithm at: http://www.cgafaq.info/wiki/Polygon_Area.
    """
    #xs, ys = ring.coords.xy
    # this just returns
    xs, ys = xy(points)
    xs.append(xs[1])
    ys.append(ys[1])


    if DEBUG: print "xs: ", xs
    if DEBUG: print "ys: ", ys

    return sum(xs[i]*(ys[i+1]-ys[i-1]) for i in range(1, len(points)))/2.0

def is_ccw_impl(name):
    """Predicate implementation"""
    def is_ccw_op(ring):
        return signed_area(ring) >= 0.0
    return is_ccw_op


def rewind(line, fout):
    try:
        feature = json.loads(line)
    except:
        sys.stderr.write("error: failed to process JSON: %s\n" % line)
    else:
        assert feature["type"] == "Feature"
        if feature["geometry"]["type"] == "Polygon":
            for index in xrange(len(feature["geometry"]["coordinates"])):
                feature["geometry"]["coordinates"][index].reverse()
            fout.write(json.dumps(feature) + '\n')
        else:
            fout.write(line)

def test_reverse(line, fout):
    try:
        feature = json.loads(line)
    except:
        sys.stderr.write("error: failed to process JSON: %s\n" % line)
    else:
        assert feature["type"] == "Feature"
        if feature["geometry"]["type"] == "Polygon":
            points = feature["geometry"]["coordinates"]

            #print points[0]
            val =  signed_area(points[0])
            print "val: %f, points: %s" % (val, points[0])
            #print "points: ", points

            #for index in xrange(len(feature["geometry"]["coordinates"])):
            #    feature["geometry"]["coordinates"][index].reverse()
            #fout.write(json.dumps(feature) + '\n')
        else:
            #fout.write(line)
            pass

# http://stackoverflow.com/questions/1165647/how-to-determine-if-a-list-of-polygon-points-are-in-clockwise-order
# http://mathworld.wolfram.com/PolygonArea.html

def reverse_if_needed(line, fout):
    try:
        feature = json.loads(line)
    except:
        sys.stderr.write("error: failed to process JSON: %s\n" % line)
    else:
        assert feature["type"] == "Feature"
        if feature["geometry"]["type"] == "Polygon":
            points = feature["geometry"]["coordinates"]

            sarea = signed_area(points[0])
            if DEBUG: print "sarea: %0.10f" % sarea
            if sarea < 0.0:
                if DEBUG: print "reversed"

                for index in xrange(len(feature["geometry"]["coordinates"])):
                    feature["geometry"]["coordinates"][index].reverse()

                #import pdb; pdb.set_trace()

                if DEBUG: print "feature: ", feature
                fout.write(json.dumps(feature) + '\n')
            else:
                if DEBUG: print "not reversed"
                if DEBUG: print "feature: ", feature
                fout.write(line)
        else:
            fout.write(line)
            pass



def parseargs():
    """ Parse command line arguments """

    parser = OptionParser()

    parser.add_option('-i', '--in', dest="in_file", type="string", default=None,
                      help="name of input file to process")

    parser.add_option('-o', '--out', dest="out_file", type="string", default=None,
                      help="name of output file to write")

    parser.add_option('-d', '--debug', dest="debug", action="store_true", default=False,
                      help="enable debug logging")

    opt, arg = parser.parse_args()

    if not (opt.in_file or opt.out_file):
        print "Error: must specify an --in and an --out file"
        sys.exit(1)

    if opt.debug:
        DEBUG=True

    return opt, arg



if __name__ == "__main__":

    options, args = parseargs()

    infh = open(options.in_file, 'r')
    outfh = open(options.out_file, 'w')

    #map(lambda x: rewind(x, sys.stdout), fileinput.input())
    #map(lambda x: test_reverse(x, sys.stdout), fileinput.input())
    #map(lambda x: reverse_if_needed(x, sys.stdout), fileinput.input())
    #map(lambda x: reverse_if_needed(x, sys.stdout), fileinput.input())

    #for inline in infh.readlines():
    #    reverse_if_needed(inline, outfh)

    for line in infh.readlines():
        data = json.loads(line)
        angle = map(ecef, data["geometry"]["coordinates"][0][0:3])

        if orient(*angle) < 0:
            data["geometry"]["coordinates"][0].reverse()

        outfh.write(json.dumps(data) + '\n')

