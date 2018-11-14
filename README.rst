Microhomie firmware with setup wizard
#####################################

This firmware and the setup wizard are in alpha stage.

Supported device: `ESP8266`

Setup
=====

This makes most fun on your mobile.

1. Erase and flash your device with the `microhomie-wizard` firmware
2. Reset device (button or power)
3. Wait until you see the `Microhomie-xxxxxx` Wifi network, connect to this network with password `microhomiE`
4. Open the URL http://192.168.4.1 in your favorite browser and follow the instructions
5. Subsrcibe to the MQTT base topic (homie/#) to watch the incomming messages
6. Reset your device
7. Play


Setup Build environment
=======================

To bootstrap the development environment you need packages, headers, binaries, dependencies, etc for to build `esp-open-sdk <https://github.com/pfalcon/esp-open-sdk>`_ and `micropython <https://github.com/micropython/micropython>`_. Go-lang (binary) is also a dependencie.

If you have installed the requirements and dependencies the Makefile will do the rest for you. Just type::

    make bootstrap



Build an deploy
===============

`ttyUSB0` is set as the default port for the device. You can change this in the Makefile on line 5.

::

    make
    make deploy

