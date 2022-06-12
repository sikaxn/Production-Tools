# What does this script do

It convert the current OpenLP Slides text to what VMix Data Source. If it's a video or image source, it will show the filename. 

# How to launch this script

First you need to turn on Remote of your OpenLP. Than you'll need to know the port and IP address of your OpenLP machine. open app.py and edit the IP address of your OpenLP. If you use authentication, please do ```username:password@OpenLP.Machine.IP.Addr```.

Please install python and add it to your PATH. After that, open powershell and run ```pip install flash```. After this, click on start.bat can launch the service. 

# text ignore feature

In some case you want some text to show on projector but not the overlay text. by not commenting ```strip_ignore()``` function, you can enable ignore feature. Everything you put in ( ) or [ ] will be stripped this scrip and not being sent to the overlay.

# OBS Compatibility

http://127.0.0.1:5000/view is the OBS View. You can add it as a browser source and do a green chroma key. 

To edit the format of text, please edit h1 for view.html. To change background of the webpage, please change body setting.

# What to add to VMix Data Source? 

Please add a text data source. http://127.0.0.1:5000/sel should be the URI.

# Troubleshooting

If you can't launch http://127.0.0.1:5000/ the service isn't running. If see nothing on http://127.0.0.1:5000/raw OpenLP isn't connected.

DONOT close command prompt window when you're using this script. This will kill the service. 