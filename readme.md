# Caption Viewer for OpenLP
This Script turn a standard ECS/POS compliance Customer Pole Display to a caption viewer (similar to Captiview in movie theater) for OpenLP. 

# System requirement

 1. ECS/POS compliance Customer Pole Display. This code is tested on CD-5220, however any other display compatible with ECS/POS standard should work.
 2. Raspberry Pi with Raspberry Pi OS.
 3. USB-RS232 converter.

# Prepare Raspberry Pi

Install dependency: pyserial, subprocess, pinyin, urllib.

# Setup config file

```ECSDisplay.cfg``` contains setup information. It should be placed at the same directory with ```ECSDisplayOpenLPLyric.py```.

There are 4 line of configure file. They are:

 1. IP address of the computer running OpenLP
 2. Port of OpenLP Remote
 3. Serial port resource address
 4. Enable PinYin converter (0 as disabled, 1 as enabled, this function is in beta. If you're not dealing with Chinese please leave it as 0)
 5. What to display if no lyric currently present. (if you want nothing, leave a space `` `` but don't remove that line.)

Sample  ```ECSDisplay.cfg```

```
10.0.0.159
4316
/dev/ttyUSB0
0
(Currently none)
```
 # Setup OpenLP
 
 OpenLP can be obtained [Here](https://openlp.org/). 
 
You need to enable remote function of OpenLP. Currently password function doesn't work so don't turn on password for OpenLP remote.

Please note that CD-5220 support total of 40 characters, 20 per line. If one single lyric exceed this length scrolling will automatically start. This is a not optimized situation. To have best user experience, please edit the lyric so there's only less than 40 characters per screen of your lyric. This might affect the projection screen but not likely to affect stage view. This is somewhat the limitation of OpenLP.

# Setup to have this script run at Raspberry Pi startup

**IT IS RECOMMENDED THAT YOU USE A DEDICATED RASPBERRY PI FOR THIS.**
1. Copy both ```ECSDisplayOpenLPLyric.py``` and ```ECSDisplay.cfg``` to the home folder of your Raspberry Pi.
2. SSH into your Pi, run ``sudo raspi-config``.
3. In raspi-config, go to System Options, Boot / Auto Login, have the Pi, Console Autologin.
4. Save and quit raspi-config.
5. Run ``sudo nano /etc/profile``,
6. At the last line, add ``python3 ECSDisplayOpenLPLyric.py``
7. Use ctrl+x to save the file, than reboot your Pi.

# Issues and todo

1. Better Pinyin translation.
2. Web interface for editing ``ECSDisplay.cfg``, reboot Pi, scrolling control, etc.
3. When there's mixed chinese and english in the same line of lyric, weared output will be shown.
 
