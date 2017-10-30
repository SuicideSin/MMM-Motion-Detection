# MMM-Motion-Detection
This an extension for the [MagicMirror](https://github.com/MichMich/MagicMirror). With this module your mirror will only turn on when it detects motion through the Rasberry Pi's PiCam or a USB webcam. It also emits `motion-detected` and `motion-stopped` notifications for other modules to use.

This was ported from [Paviro's MMM-Facial-Recognition module](https://github.com/paviro/MMM-Facial-Recognition) mostly to get the python code for camera usage and OpenCV support.

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
