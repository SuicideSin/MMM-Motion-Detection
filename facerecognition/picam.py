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
        self.currentBuffer = 0
        self.buffers = [io.BytesIO(), io.BytesIO()]
        self.lock = threading.Lock()
        self.running = True

    def getBuffer(self):
        while self.running:
            self.lock.acquire()
            self.currentBuffer = (self.currentBuffer + 1) % 2
            self.lock.release()
            buffer = self.buffers[self.currentBuffer]
            buffer.truncate()
            buffer.seek(0)
            yield buffer
	    time.sleep(config.get("interval"))

    def run(self):
        with picamera.PiCamera() as camera:
            camera.resolution = (620, 540)
            camera.framerate = 10
            camera.capture_sequence(self.getBuffer(), format='jpeg', use_video_port=True)

    def read(self):
        """Read a single frame from the camera and return the data as an OpenCV
        image (which is a numpy array).
        """
        self.lock.acquire()
        try:
            free_buffer = (self.currentBuffer + 1) % 2
            buffer = self.buffers[free_buffer]
            # Construct a numpy array from the stream
            data = np.fromstring(buffer.getvalue(), dtype=np.uint8)
        finally:
            self.lock.release()
        image = cv2.imdecode(data, 1)
        return image

    def stop(self):
        self.running = False
        self.join()
