import ConfigParser
from os import path
from cue_lookup import cue_lookup

class config():
    _cp = None
    
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
        # Read the optionals
        self.corsairkeyindicator = self.getbool('CorsairKeyIndicator', section='corsair', default = False)
        self.corsairkeyname = self.get('CorsairKeyName', section='corsair', default = 'PauseBreak')
        # Validate the key
        if (self.corsairkeyindicator == True):
            if (self.corsairkeyname not in cue_lookup):
                return self.return_error(self.corsairkeyname + " is not a valid key. See corsair_keylist.txt for list of keys.")
        return True

    # Config get helper function
    def get(self, key, type = 'string', default = None, section = 'mcsystray'):
        try:
            if type == 'int':
                return self._cp.getint(section, key)
            elif type == 'bool':
                return self._cp.getboolean(section, key)
            else:
                return self._cp.get(section, key)
        except:
            return default
                
    # Convenience
    def getint(self, key, default = None, section = 'mcsystray'):
        return self.get(key, type = 'int', default = default, section = section)

    def getbool(self, key, default = None, section = 'mcsystray'):
        return self.get(key, type = 'bool', default = default, section = section)
                
    def return_error(self,errormsg):
        self.errormsg = errormsg
        return False