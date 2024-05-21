# Motion detector system to send MMS messages when motion is detected. Created with M5GO IoT starter kit. 

Developed with MicroPython
![Micropython Logo](https://dashboard.snapcraft.io/site_media/appmedia/2018/12/mp_logo.png) 


Developer with M5GO kit\
![M5GO Kit](https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSS2YtHgVWWzzhsuiFNPCIjIHTisbo3g6TOfmewtrU9gA&s) 

## How to use? 
1. Follow manual instructions to plug the Motion sensor with appropriate wires into the ESP32 device.

2. Create a Gmail account (or use an existing one).
   - Turn on two-factor authentication and obtain an app password. It should be in this format `xxxx-xxxx-xxxx`

4. Connect your M5GO device or ESP32 board. Click the `connected` button in the bottom-left corner and ensure the connection is successful. 

5. Visit [m5stack website](https://flow.m5stack.com/) and insert [main.py](https://github.com/AdityaRao127/motion-detector-system/blob/main/main.py) into the file.

6. Add the environment variables into the appropriate fields. Choose the appropriate domain name for the `sender_email`:
   [Taken from source](https://www.wikihow.com/Send-a-Text-from-Email)
  - AT&T: **number@txt.att.net** for a normal text message (SMS), or **number@mms.att.net** for a multimedia message (MMS)
  - Verizon: **number@vtext.com** for both SMS and MMS messages
  - Sprint PCS: **number@messaging.sprintpcs.com** for both SMS and MMS messages
  - T-Mobile: **number@tmomail.net** for both SMS and MMS messages

6. Name the Python file `main` if it's not already. Then run the [main.py](https://github.com/AdityaRao127/motion-detector-system/blob/main/main.py) and test if it works.
   - `1` means motion detected
   - `0` means no motion detected

8. Change M5GO device into APP Mode -> Reset Device -> Go to Programs -> Scroll down and select the `main.py` file.
   - Since you are in APP mode, the device will run `main.py`  whenever the M5GO device is online.
  

## How does the motion detector work? 
The PIR sensor detects the heat emitted by a person or object, and this detection signal is sent to the microcontroller, which then sends an email to the specified recipient.

PIR sensor image
[PIR sensor](https://ars.els-cdn.com/content/image/3-s2.0-B9780128236949000190-f08-05-9780128236949.jpg)


### GitHub Stats

[![GitHub Stars](https://img.shields.io/github/stars/AdityaRao127/motion-detector-system.svg)](https://github.com/AdityaRao127/motion-detector-system/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/AdityaRao127/motion-detector-system.svg)](https://github.com/AdityaRao127/motion-detector-system/network)
[![GitHub Watchers](https://img.shields.io/github/watchers/AdityaRao127/motion-detector-system.svg)](https://github.com/AdityaRao127/motion-detector-system/watchers)




















Developed with MicroPython
