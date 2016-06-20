mcsystray
=========

System tray icon that shows the status of a minecraft server.

Setup
-----
Open config.ini and set the server's address and port. Then optionally change
the check frequency. Save and then run mcsystray.pyw (Python version) or
mcsystray.exe (Windows stand-alone version.)

Requirements
------------

Nothing for the windows stand-alone version.

The python script has a number of requirements.

It has been tested in Python 2.7, but may run with Python 3. The following
packages are required: mcstatus, cue_sdk and enum34. (enum34 not required for
Python 3.) Assumning you have pip installed you can get the submodules like:
pip install mcstatus cue_sdk enum34

If you are using the python version and want the corsair features, you will
need the SDK dll. This is CUESDK.x64_2013.dll for 64-bit systems and
CUESDK_2013.dll for 32-bit. You can obtain it from the Corsair CUE SDK here:
http://www.corsair.com/en/support/downloads
