# The mcstatus module is in a subdirectory of it's repo. This is a work-
# around to allow it to still import without altering the file structure.
# TODO: Find a better way to do this
from sys import path
path.insert(0, './mcstatus')

import wx
import threading
from mcstatus import MinecraftServer

# Set the server address and port
SERVER_ADD = "127.0.0.1:25565"

# Set the check frequency (seconds)
CHECK_FREQ = 180

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
        wx.CallAfter(self.Destroy)

    def on_disable_enable(self, event):
        global enabled
        enabled = not enabled
        if enabled:
            checkServer()
        else:
            self.set_icon(TRAY_ICON_DISABLED,"Disabled")
        
def checkServer():
    if not enabled:
        return
    t = threading.Timer(CHECK_FREQ, checkServer)
    # Setting as daemon ensures the thread exits with the program. This is
    # probably a bad way to do this, because it might leave resources locked.
    t.daemon = True
    t.start()
    server = MinecraftServer.lookup(SERVER_ADD)
    try:
        status = server.status()
    except:
        tbi.set_icon(TRAY_ICON_OFFLINE,"No Server")
        print "No server"
        return
    # For debugging
    #print("The server has {0} players and replied in {1} ms".format(status.players.online, status.latency))
    if status.players.online < 1:
        tbi.set_icon(TRAY_ICON_ONLINE,"No Players. "+str(status.latency)+" ms")
    elif status.players.online == 1:
        tbi.set_icon(TRAY_ICON_INUSE,"1 Player. "+str(status.latency)+" ms")
    elif status.players.online > 1:
        tbi.set_icon(TRAY_ICON_INUSE,str(status.players.online)+" Players. "+str(status.latency)+" ms")


def main():
    # Globals are for the weak
    global tbi, enabled
    enabled = True
    app = wx.PySimpleApp()
    tbi = TaskBarIcon()
    checkServer()
    app.MainLoop()
    
# Toggle the check. The global enabled bool will be checked during the
# next loop.
def disable_enable():
    global enabled
    enabled = not enabled
    if enabled:
        checkServer()
    else:
        tbi.set_icon(TRAY_ICON_DISABLED,"Disabled")


if __name__ == '__main__':
    main()