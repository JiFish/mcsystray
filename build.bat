pyinstaller.exe -F --noconsole --icon=redstonelamp.ico --onefile mcsystray.pyw
copy /b /y icon_*.png dist\icon_*.png
copy /b /y config.ini dist\config.ini
copy /b /y corsair_keylist.txt dist\corsair_keylist.txt
TYPE README.md | FIND "" /V >dist\readme.txt
