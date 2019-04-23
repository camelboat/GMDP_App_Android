# GMDP_App_Android

This is a room devices control application on Android, written by Python, and packaged by python-for-android with buildozer. It is Modified from kivymd example kitchen_sink. The application will communicate with Matlab ThingSpeak IoT platform. To make it work, corresponding programs(one data collection program, and one program for acting the instructions) should be run on the Raspberry Pi with the access to the Internet and GPIO properly connected with the devices.

## Build, Debug and Run
Build and debug by:
```bash
$ buildozer android debug
```
Deploy on the phone and run by:

```bash
$ buildozer deploy run logcat
```

## Files
`main.kv`: Layout file, where you can modify according to the example from kivymd.

`main.py`: Application main file

`buildozer.spec`: Building configuration file


## Function Introduction

Currently the application has four function pages, which are "Lighting System", "Temperature", "Room Occupancy", and "Energy Saving".

### Lighitng System
In this page, you would be able to switch on/off two lights. Detailed information about how to set your light can be found in GMDP_Local_Monitor_Panel_Pi.

### Temperature
In this page, you would be able to get the latest temperature value of your room, and use it as an air-conditioner controller to control your room's air-conditioner. Detailed information about how to set the temperature sensor can be found in GMDP_Data_Collection_Pi. Detailed information about how to set the controller(IR instruction decoding and emission) can be found in GMDP_Control_Arduino.

### Room Occupancy
In this page, you would be able to get the room occupancy information in your target room. The room occupancy index is calculated based on the data collected by both PIR sensors and camera in the last two minutes.

This function may not be quite easy for implementing, because the calculation function would change with by different rooms.

### Energy Saving
In this page, you would be able to get the room energy consumption and saved value from the devices running time uploaded by the program running for operating the devices control instructions. Detailed information about that program can be found in GMDP_Local_Monitor_Panel_Pi.

## Future Work

### 2019/4/22
1. Links of repositories and detailed README for corresponding program's.
3. Application optimiazation for multiple room users.
4. Fix of application crush by the invalid data fetch from ThingSpeak.

