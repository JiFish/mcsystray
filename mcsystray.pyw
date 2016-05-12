import wx, threading, ConfigParser
from mcstatus import MinecraftServer
from os import path

# Icon files
TRAY_ICON_ONLINE = 'icon_green.png'
TRAY_ICON_OFFLINE = 'icon_red.png'
TRAY_ICON_INUSE = 'icon_blue.png'
TRAY_ICON_DISABLED = 'icon_grey.png'

# Create menu convenience function
def create_menu_item(menu, label, func):
    item = wx.MenuItem(menu, -1, label)
    menu.Bind(wx.EVT_MENU, func, id=item.GetId())
    menu.AppendItem(item)
    return item

class TaskBarIcon(wx.TaskBarIcon):
    def __init__(self):
        super(TaskBarIcon, self).__init__()
        self.set_icon(TRAY_ICON_DISABLED, 'Enabling...')
        self.Bind(wx.EVT_TASKBAR_LEFT_DOWN, self.on_disable_enable)

    def CreatePopupMenu(self):
        menu = wx.Menu()
        create_menu_item(menu, 'Disable/Enable', self.on_disable_enable)
        create_menu_item(menu, 'Exit', self.on_exit)
        return menu

    def set_icon(self, path, title = '...'):
        icon = wx.IconFromBitmap(wx.Bitmap(path))
        self.SetIcon(icon, title)

    def on_exit(self, event):
        self.RemoveIcon()
        wx.CallAfter(self.Destroy)

    def on_disable_enable(self, event):
        global enabled
        enabled = not enabled
        if enabled:
            checkServer()
        else:
            self.set_icon(TRAY_ICON_DISABLED,"Disabled")
            
class config():
    address = "127.0.0.1:25565"
    frequency = 180
    
    def __init__(self, confile="config.ini"):
        # Test File exists
        if (path.isfile(confile) == False):
            fatal_error(confile+" does not exist.")
        # Parse file
        cp = ConfigParser.ConfigParser()
        try:
            cp.read('config.ini')
        except:
            self.fatal_error("Invalid ini file.")
        try:
            self.address = cp.get('mcsystray','Address')
        except:
            self.fatal_error("Could not read address from config file.")
        try:
            self.frequency = cp.getint('mcsystray','Frequency')
        except:
            self.fatal_error("Could not read frequency from config file.")
        # Sanity check frequency
        if (self.frequency < 30 or self.frequency > 1000000):
            self.fatal_error("Check frequency should be between 30 and 1,000,000 seconds.")
        
    def fatal_error(self,message):
        wx.MessageBox(message, 'Error', wx.OK | wx.ICON_WARNING)
        wx.CallAfter(self.Destroy)
    
        
def checkServer():
    if not enabled:
        return
    t = threading.Timer(conf.frequency, checkServer)
    # Setting as daemon ensures the thread exits with the program. This is
    # probably a bad way to do this, because it might leave resources locked.
    t.daemon = True
    t.start()
    server = MinecraftServer.lookup(conf.address)
    try:
        status = server.status()
    except:
        tbi.set_icon(TRAY_ICON_OFFLINE,"Server not found.")
        return
    # For debugging
    # print("The server has {0} players and replied in {1} ms".format(status.players.online, status.latency))
    if status.players.online < 1:
        tbi.set_icon(TRAY_ICON_ONLINE,"No Players. "+str(status.latency)+" ms")
    elif status.players.online == 1:
        tbi.set_icon(TRAY_ICON_INUSE,"1 Player. "+str(status.latency)+" ms")
    elif status.players.online > 1:
        tbi.set_icon(TRAY_ICON_INUSE,str(status.players.online)+" Players. "+str(status.latency)+" ms")


def main():
    # Globals are for the weak
    global tbi, enabled, conf
    enabled = True
    app = wx.App(False)
    conf = config()
    tbi = TaskBarIcon()
    checkServer()
    app.MainLoop()


if __name__ == '__main__':
    main()