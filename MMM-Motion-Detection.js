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
    // recognition interval in seconds (smaller number = faster but more CPU intensive!)
    interval: 1,
    // Turn off delay after movement stops being sensed (in seconds).
    turnOffDelay: 120,
    // Threshold for motion detection, smaller numbers means more sensitive
    detectionThreshold: 1000
  },

  start: function () {
    this.sendSocketNotification('CONFIG', this.config);
    Log.info('Starting module: ' + this.name);
  },

  socketNotificationReceived: function (notification, payload) {
    Log.info(this.name + " received a socket notification: " + notification + " - Payload: " + payload);
    switch (notification) {
      case "motion-detected":
        this.sendNotification("motion-detected");
        break;
      case "motion-stopped":
        this.sendNotification("motion-stopped");
        break;
      default:
        Log.info("[" + this.name + "] unknown socket notification: " + notification + " - Payload: " + payload);
    }
  }

});
