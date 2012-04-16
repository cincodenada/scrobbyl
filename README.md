Scrobbyl
==========================

This is a fork of the original Scrobbyl, because I tried to get it to work and couldn't.

It's certainly incomplete, and I've had trouble getting it to recognize songs recorded
from a microphone due to the fingerprinting not recgonizing it, which isn't something
that can really be adjusted for on the client side, so no guarantees there.  Do let me
know if you have success with that though.

You'll need at least the following Python packages to run this.  Use whatever package manager you
prefer, I uses `pip`, so I run `pip install <packagename>`:

 * pyechonest
 * pyaudio

If you run `python scrobbyl.py` (after running the lastfm auth detailed below), the script
will run a loop of recording a sample, trying to identify it.  If it recognizes a song
that it hasn't scrobbled, it will scrobble said song.  The length recorded defaults to
20 seconds, you can change that in `scrobbyl.py` in the call to recorder.recordAudio.

This hasn't been extensively tested, I just threw my latest stuff up here because someone
e-mailed me asking about it.  But in any case, it should work better than the original
stuff, which was quite broken by now.  It at least runs in a loop, takes in audio,
and tries to recognize it and scrobble it.

I have ambitions to make a GUI out of it and such, but honestly there are more 
important/interesting things on my plate at the moment, so I make no promises.

If you have questions/comments, just leave comments here or otherwise contact me via GitHub.

Original Readme
==========================

Don't you wish you could **scrobb**le your vin**yl**?  Well, now you can.

What it does
------------

 1. Listens to line-in for 20 seconds
 2. Uses the echonest fingerprinter to work out what the song is
 3. If this segment is different to the previous 20 seconds, scrobble it
 4. rinse and repeat

To run
----------
 
 * make sure ffmpeg is in your path
 * run 'python lastfm.py auth' to link scrobbyl to your account
 * plug in your turntable through your line in
 * run

To do
----------
Stay tuned for fingerprinting with a microphone instead of line-in

FAQ
----------
**Wait, I can't work out how to run it**

  Scrobbyl is only in proof of concept stage now.  We'll have an OS X and Linux frontend available soon.

**How can I scrobble from a cafe/stereo/concert/store?**

  Sorry, you can only scrobble from a direct line-in at the moment.

