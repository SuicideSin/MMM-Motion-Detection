# MMM-Motion-Detection
This an extension for the [MagicMirror](https://github.com/MichMich/MagicMirror). It provides motion detection to only turn the mirror's display on when there is people in the room.

This was ported from [Paviro's MMM-Facial-Recognition module](https://github.com/paviro/MMM-Facial-Recognition) mostly to get the python code for camera usage and OpenCV support.

By default it uses the Rasberry Pi's PiCam, but can also be configured to work with a USB Webcam. It emits `motion-detected` and `motion-stopped` notifications for other modules to use.

## Usage

Configuration variables shown here are the defaults and don't have to be specified unless you want to change them:

```
{
	module: 'MMM-Motion-Detection',
	config: {
        // force the use of a usb webcam on raspberry pi
        useUSBCam: false,
        // recognition interval in seconds (smaller number = faster but more CPU intensive!)
        interval: 1,
        // Notificaiton Delay after movement stops being sensed (in seconds).
        motionStopDelay: 120,
        // Threshold for motion detection, smaller numbers means more sensitive
        detectionThreshold: 1000,
        // Turn off display when no motion is detected.
        turnOffDisplay: true
	}
}
```

## Dependencies
- [python-shell](https://www.npmjs.com/package/python-shell) (installed via `npm install`)
- [OpenCV](http://opencv.org) (`sudo apt-get install libopencv-dev python-opencv`)
