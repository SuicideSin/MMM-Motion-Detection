#!/usr/bin/python
# coding: utf8
"""MMM-Facial-Recognition - MagicMirror Module
Face Recognition script config
The MIT License (MIT)

Copyright (c) 2016 Paul-Vincent Roll (MIT License)
Based on work by Tony DiCola (Copyright 2013) (MIT License)
"""
import inspect
import os
import json
import sys
import platform

CONFIG = json.loads(sys.argv[1]);

def to_node(type, message):
    print(json.dumps({type: message}))
    sys.stdout.flush()

def get(key):
    return CONFIG[key]

def get_camera():
    to_node("status", "-" * 20)
    try:
        if get("useUSBCam") == False:
            import picam
            to_node("status", "PiCam starting...")
            cam = picam.OpenCVCapture()
            cam.start()
            return cam
        else:
            raise Exception
    except Exception:
        import webcam
        to_node("status", "Webcam starting...")
        return webcam.OpenCVCapture(device_id=0)
    to_node("status", "-" * 20)
