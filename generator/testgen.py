#!/usr/bin/env python
import os
import time
import uuid
from subprocess import Popen, PIPE, STDOUT


def test_gen(gen_rec, tempdir="/tmp"):
    tmpfile = str(uuid.uuid4())
    gen_rec['file'] = os.path.join(tempdir, tmpfile)
    cmd = 'julia generate.jl %s %s %s %s %s > %s' % (gen_rec['rows'], gen_rec['max_x'], gen_rec['min_x'],
                                                     gen_rec['max_y'], gen_rec['min_y'], gen_rec['file'])

    print "executing cmd: ", cmd

    # record start time
    formatted_start_ingest_set = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    start_time = time.time()

    # run command
    p = Popen(cmd, shell=True, stdout=PIPE, stderr=STDOUT)

    # read lines from output
    res = p.stdout.readlines()
    p.wait()

    # record end time of data load
    end_time = time.time()
    formatted_end_ingest_set = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

    gen_time = end_time-start_time

    gen_rec['res'] = res
    gen_rec['total_time'] = gen_time
    gen_rec['rc'] = p.returncode

    return gen_rec



if __name__ == "__main__":
    gen_rec = {}
    gen_rec['rows'] = 1000
    gen_rec['max_x'] = 20
    gen_rec['min_x'] = -20
    gen_rec['max_y'] = 20
    gen_rec['min_y'] = -20

    out = test_gen(gen_rec)

    print out
