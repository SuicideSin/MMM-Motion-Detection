/* global Module */

/* Magic Mirror
 * Module: MMM-Motion-Detection
 *
 * By Doug McInnes http://dougmcinnes.com
 *
 * Modified from https://github.com/paviro/MMM-Facial-Recognition
 * By Paul-Vincent Roll http://paulvincentroll.com
 *
 * MIT Licensed.
 */

Module.register('MMM-Motion-Detection', {

  defaults: {
    // force the use of a usb webcam on raspberry pi (on other platforms this is always true automatically)
    useUSBCam: false,
    // recognition interval in seconds (smaller number = faster but CPU intens!)
    interval: 2,
    // Turn off delay after movement stops being sensed.
    turnOffDelay: 60
  }
});
