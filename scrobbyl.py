#!/usr/bin/env python

import pprint
import sys
import os
import subprocess
import json
import time
import pyechonest.config as config
import pyechonest.song as song
from fp import fingerprint

config.ECHO_NEST_API_KEY="F4LP3UJVBPYSPVKRZ"

def main(file):
    statusfile = os.path.expanduser("~/.scrobbyl")
    lines = []

    platform = os.uname()[0]
    if platform == "Darwin":
        codegen = "./ext/codegen.Darwin"
        path = ".:"+os.getenv("PATH")
    elif platform == "Linux":
        codegen = "./ext/codegen.Linux-i686"
        path = os.getenv("PATH")
    
    config.CODEGEN_BINARY_OVERRIDE = os.path.abspath(codegen)

    if os.path.exists(statusfile):
        fp = open(statusfile, "r")
        lines = fp.readlines()
        fp.close()
    lasttime = 0
    lastartist = ""
    lasttrack = ""
    if len(lines) == 3:
        lasttime = int(lines[0])
        lastartist = lines[1]
        lasttrack = lines[2]
    
    fp = song.util.codegen(file)
    pprint.pprint(fp)
    if len(fp) and "code" in fp[0]:

        result = song.identify(query_obj=fp, version="4.11")
        pprint.pprint(result)

        if len(result):
            track = result[0].title
            artist = result[0].artist_name
            now = time.time()

            print (now-lasttime)
            if now - lasttime < 100:
                # Only scrobble if we've just been playing
                if lasttrack != "" and lasttrack != track:
                    print "Last track was",lasttrack,"now",track,", scrobbling"
                    lastfm.scrobble(artist, track)
                else:
                    print "same song"
            else:
                print "too long since we last did it,", now-lasttime

            fp = open(statusfile, "w")
            fp.write("%d\n%s\n%s" % (now, artist, track))
            fp.close()

if __name__=="__main__":
    if len(sys.argv) < 2:
        print >>sys.stderr, "usage: %s <file>" % sys.argv[0]
        sys.exit(0)
    main(sys.argv[1])
