#!/usr/bin/python
# coding: utf8
"""MMM-Motion-Detection - MagicMirror Module
Motion Detection Script
The MIT License (MIT)

Copyright (c) 2017 Doug McInnes (MIT License)
Based on work by Paul-Vincent Roll (Copyright 2016) (MIT License)
Based on work by Tony DiCola (Copyright 2013) (MIT License)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import time
import cv2
import config
import signal
import sys
import json

def to_node(type, message):
    # convert to json and print (node helper will read from stdout)
    try:
        print(json.dumps({type: message}))
    except Exception:
        pass
    # stdout has to be flushed manually to prevent delays in the node helper communication
    sys.stdout.flush()

to_node("status", "Motion Detection started...")

# get camera
camera = config.get_camera()

def shutdown(self, signum):
    to_node("status", 'Shutdown: Cleaning up camera...')
    camera.stop()
    quit()

signal.signal(signal.SIGINT, shutdown)

# sleep for a second to let the camera warm up
time.sleep(1)

frame = camera.read()
if frame == None:
  to_node("status", 'Camera Failed to Initialize! Shutting Down.')
  camera.stop()
  sys.exit(1)

def diffImg(t0, t1, t2):
  d1 = cv2.absdiff(t2, t1)
  d2 = cv2.absdiff(t1, t0)
  return cv2.bitwise_and(d1, d2)

t_minus = None
t       = cv2.cvtColor(camera.read(), cv2.COLOR_RGB2GRAY)
t_plus  = cv2.cvtColor(camera.read(), cv2.COLOR_RGB2GRAY)

last_motion = None

# Main Loop
while True:
    # Sleep for x seconds specified in module config
    time.sleep(config.get("interval"))

    t_minus = t
    t       = t_plus
    t_plus  = cv2.cvtColor(camera.read(), cv2.COLOR_RGB2GRAY)

    diff = diffImg(t_minus, t, t_plus)
    thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)[1]

    # dilate the thresholded image to fill in holes, then find contours
    # on thresholded image
    thresh = cv2.dilate(thresh, None, iterations=2)
    (cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                    cv2.CHAIN_APPROX_SIMPLE)

    max = 0
    # loop over the contours
    for c in cnts:
        area = cv2.contourArea(c)
        if area > max:
            max = area

    if max > config.get("detectionThreshold"):
        if last_motion is None:
            to_node("motion-detected", {})
        last_motion = time.time()
    elif last_motion != None and time.time() - last_motion > config.get("motionStopDelay"):
        last_motion = None
        to_node("motion-stopped", {})
