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

emptyFrame = None
detectedMotion = False
last_motion = time.time()

# Main Loop
while True:
    # Sleep for x seconds specified in module config
    time.sleep(config.get("interval"))

    # Get image
    image = camera.read()
    # Convert image to grayscale.
    image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    # Blur it
    image = cv2.GaussianBlur(image, (21, 21), 0)

    # if the empty frame is None, initialize it
    if emptyFrame is None:
        emptyFrame = image
        continue

    frameDelta = cv2.absdiff(emptyFrame, image)
    thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

    # dilate the thresholded image to fill in holes, then find contours
    # on thresholded image
    thresh = cv2.dilate(thresh, None, iterations=2)
    (cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                    cv2.CHAIN_APPROX_SIMPLE)

    detectedMotion = False

    # loop over the contours
    for c in cnts:
        # if the contour is too small, ignore it
        if cv2.contourArea(c) > config.get("detectionThreshold"):
            detectedMotion = True
            break

    if last_motion is None and detectedMotion is True:
        last_motion = time.time()
        to_node("motion-detected", {})
    elif last_motion != None and time.time() - last_motion > config.get("turnOffDelay"):
        last_motion = None
        to_node("motion-stopped", {})
