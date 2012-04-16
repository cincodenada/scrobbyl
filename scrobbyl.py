#!/usr/bin/env python

import ConfigParser
import pprint
import sys
import os
import subprocess
import json
import time
import pyechonest.config as config
import pyechonest.song as song
from fp import fingerprint
import lastfm
import recorder

config.ECHO_NEST_API_KEY="F4LP3UJVBPYSPVKRZ"

def main():
    platform = os.uname()[0]
    if platform == "Darwin":
        codegen = "./ext/codegen.Darwin"
        path = ".:"+os.getenv("PATH")
    elif platform == "Linux":
        codegen = "./ext/codegen.Linux-i686"
        path = os.getenv("PATH")
    config.CODEGEN_BINARY_OVERRIDE = os.path.abspath(codegen)

    while(True):
        recorder.recordAudio("recorded.wav",20)
        try:
            scrobbled = tagSong("recorded.wav")
        except Exception:
            pass

def tagSong(filename):
    #Get status info
    statusfile = os.path.expanduser("~/.scrobbyl")
    lines = []

    if os.path.exists(statusfile):
        fp = open(statusfile, "r")
        lines = fp.readlines()
        fp.close()
    lasttime = 0
    lastartist = ""
    lasttrack = ""
    lastscrobble = 0
    if len(lines) == 4:
        lasttime = int(lines[0])
        lastartist = lines[1].strip()
        lasttrack = lines[2].strip()
        lastscrobble = int(lines[3])
    


    fp = song.util.codegen(filename)
    pprint.pprint(fp)

    #Make sure we have a valid fp
    if fp == None or len(fp) == 0 or "code" not in fp[0]:
        raise Exception("Could not calculate fingerprint!")

    result = song.identify(query_obj=fp, version="4.11",buckets="audio_summary")
    pprint.pprint(result)

    if len(result) == 0:
        raise Exception("Song not found in database.")

    track = result[0].title
    artist = result[0].artist_name
    songlength = result[0].audio_summary.duration

    #Check to make sure it's not a duplicate
    now = time.time()
    doscrobble = True
    if lasttime:
        if (now - lasttime) < 100:
            #Check for duplicate song
            if lasttrack == track and lastartist == artist:
                #if config.getboolean('scrobble_rules','allow_repeat') and prevlength < (now - config.get('runtime_info','last_scrobble')):
                if False:
                    print "Same song, but looks like it repeated..."
                else:
                    print "Same song as last time, skipping..."
                    doscrobble = False
            else:
                print "New song!"
        else:
            print "It's been longer than the songlength since we last checked."
    else:
        lasttrack = lastartist = "none"
        print "No previous song found."

    if(doscrobble):
        print "Last track was %s by %s, now %s by %s.  Scrobbling..." % (lasttrack, lastartist, track, artist)
        #lastfm.scrobble(artist, track)
        lastscrobble = now
            
    fp = open(statusfile, "w")
    fp.write("%d\n%s\n%s\n%d" % (now, artist, track, lastscrobble))
    fp.close()

    return (track, artist, doscrobble)

if __name__=="__main__":
    main()
