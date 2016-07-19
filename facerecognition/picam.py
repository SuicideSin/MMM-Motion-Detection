"""Raspberry Pi Face Recognition Treasure Box
Pi Camera OpenCV Capture Device
Copyright 2013 Tony DiCola

Pi camera device capture class for OpenCV.  This class allows you to capture a
single image from the pi camera as an OpenCV image.
"""
import io
import cv2
import numpy as np
import picamera
import threading
import time
import config


from threading import Thread

class OpenCVCapture(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        self.camera = picamera.PiCamera()
        self.camera.resolution = (620, 540)
        self.camera.exposure_mode = "night"
        self.camera.brightness = 60

    def read(self):
        """Read a single frame from the camera and return the data as an OpenCV
        image (which is a numpy array).
        """
        data = io.BytesIO()
        self.camera.capture(data, format='jpeg')
        # Construct a numpy array from the stream
        data = np.fromstring(data.getvalue(), dtype=np.uint8)
        image = cv2.imdecode(data, 1)
        cv2.imwrite("debug.jpg", image)
        return image

    def stop(self):
        self.camera.close()
        self.join()
