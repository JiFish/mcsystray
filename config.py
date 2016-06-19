import ConfigParser
from os import path
from cue_lookup import cue_lookup
from traystatus import *

class config():
    _cp = None
    trayicon = {}
    keycol = {}
    
    def __init__(self):
        self._cp = ConfigParser.ConfigParser()
    
    def load(self, file = 'config.ini'):
        # Test File exists
        if (path.isfile(file) == False):
            return self.return_error(file+" does not exist.")
        # Open file
        try:
            self._cp.read(file)
        except:
            return self.return_error(file+" is an invalid ini file.")
        # Read the basics
        self.address = self.get('Address')
        if (self.address == None):
            return self.return_error("Could not read address from config file")
        self.frequency = self.getint('Frequency')
        if (self.frequency == None):
            return self.return_error("Could not read frequency from config file.")
        # Sanity check frequency
        if (self.frequency < 30 or self.frequency > 1000000):
            return self.return_error("Check frequency should be between 30 and 1,000,000 seconds.")
        # Read the optional corsair values
        self.corsairkeyindicator = self.getbool('CorsairKeyIndicator', section='corsair', default = False)
        self.corsairkeyname = self.get('CorsairKeyName', section='corsair', default = 'PauseBreak')
        self.keycol[STATUS_DISABLED] = self.gethex('DisabledColor', section='corsair', default = (128,128,128))
        self.keycol[STATUS_OFFLINE] = self.gethex('OfflineColor', section='corsair', default = (255,0,0))
        self.keycol[STATUS_ONLINE] = self.gethex('OnlineColor', section='corsair', default = (0,255,0))
        self.keycol[STATUS_INUSE] = self.gethex('InUseColor', section='corsair', default = (0,0,255))
        # Validate the key
        if (self.corsairkeyindicator == True):
            if (self.corsairkeyname not in cue_lookup):
                return self.return_error(self.corsairkeyname + " is not a valid key. See corsair_keylist.txt for list of keys.")
        # Read the optional icon files
        self.trayicon[STATUS_DISABLED] = self.get('DisabledIcon', section='icons', default = 'icon_grey.png')
        self.trayicon[STATUS_OFFLINE] = self.get('OfflineIcon', section='icons', default = 'icon_red.png')
        self.trayicon[STATUS_ONLINE] = self.get('OnlineIcon', section='icons', default = 'icon_green.png')
        self.trayicon[STATUS_INUSE] = self.get('InUseIcon', section='icons', default = 'icon_blue.png')
        # Validate icon files existance
        for i in self.trayicon.values():
            if (path.isfile(i) == False):
                return self.return_error(i+" does not exist.")
        return True

    # Config get helper function
    def get(self, key, type = 'string', default = None, section = 'mcsystray'):
        try:
            if type == 'int':
                return self._cp.getint(section, key)
            elif type == 'bool':
                return self._cp.getboolean(section, key)
            elif type == 'hex':
                t = self._cp.get(section, key)
                return tuple(ord(c) for c in t.decode('hex'))
            else:
                return self._cp.get(section, key)
        except:
            return default
                
    # Convenience
    def getint(self, key, default = None, section = 'mcsystray'):
        return self.get(key, type = 'int', default = default, section = section)

    def getbool(self, key, default = None, section = 'mcsystray'):
        return self.get(key, type = 'bool', default = default, section = section)
                
    def gethex(self, key, default = None, section = 'mcsystray'):
        return self.get(key, type = 'hex', default = default, section = section)

    def return_error(self,errormsg):
        self.errormsg = errormsg
        return False