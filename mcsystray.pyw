import wx
import threading
import platform
from sys import argv
from config import config
from mcstatus import MinecraftServer
from socket import gaierror
from cue_sdk import *
from traystatus import *

# Create menu convenience function


def create_menu_item(menu, label, func):
    item = wx.MenuItem(menu, -1, label)
    menu.Bind(wx.EVT_MENU, func, id=item.GetId())
    menu.AppendItem(item)
    return item


class mcsystray(wx.TaskBarIcon):
    timingThread = None
    config = None
    enabled = True
    cue = None

    def __init__(self):
        super(mcsystray, self).__init__()
        if (len(argv) > 1):
            config_file = argv[1]
        else:
            config_file = 'config.ini'
        self.config = config()
        if (self.config.load(config_file) == False):
            self.fatal_error(self.config.errormsg)
            return
        self.update_status(STATUS_DISABLED, 'Enabling...')
        self.Bind(wx.EVT_TASKBAR_LEFT_DOWN, self.on_disable_enable)
        self.checkServer()

    def init_corsair(self):
        if platform.system() != "Windows":
            return self.fatal_error("Corsair mode is only supported on Windows.")
        if (platform.architecture()[0] == '64bit'):
            cue_dll = "CUESDK.x64_2013.dll"
        else:
            cue_dll = "CUESDK_2013.dll"
        try:
            self.cue = CUE(cue_dll)
        except:
            return False
        return True

    def CreatePopupMenu(self):
        menu = wx.Menu()
        create_menu_item(menu, 'Disable/Enable', self.on_disable_enable)
        create_menu_item(menu, 'Exit', self.on_exit)
        return menu

    def set_icon(self, path, title='...'):
        icon = wx.IconFromBitmap(wx.Bitmap(path))
        self.SetIcon(icon, title)

    def on_exit(self, event):
        self.exit()

    def on_disable_enable(self, event):
        self.enabled = not self.enabled
        if self.enabled:
            self.checkServer()
        else:
            self.update_status(STATUS_DISABLED, "Disabled")
            self.stopTimer()

    def stopTimer(self):
        if self.timingThread != None:
            self.timingThread.cancel()

    def checkServer(self):
        if not self.enabled:
            return
        self.timingThread = threading.Timer(
            self.config.frequency, self.checkServer)
        self.timingThread.start()
        server = MinecraftServer.lookup(self.config.address)
        try:
            status = server.status()
        except gaierror:
            self.update_status(STATUS_OFFLINE, "Server not found.")
        except:
            self.update_status(STATUS_OFFLINE, "Unknown error.")
        else:
            if status.players.online < 1:
                self.update_status(
                    STATUS_ONLINE, "No Players. %dms" % (status.latency))
            elif status.players.online == 1:
                self.update_status(
                    STATUS_INUSE, "1 Player. %dms" % (status.latency))
            elif status.players.online > 1:
                self.update_status(STATUS_INUSE, "%d Players. %dms" % (
                    status.players.online, status.latency))

    def update_status(self, status, message):
        if (self.config.corsairkeyindicator):
            self.update_corsair_key(status)
        self.set_icon(self.config.trayicon[status], message)
        
    def update_corsair_key(self, status):
        # Try to init CUE if not initialised.
        # If it's still not initialised, skip setting the key this time
        if (self.cue == None):
            if (self.init_corsair() == False):
                return
        self.cue.SetLedsColors(CorsairLedColor(
                CLK[self.config.corsairkeyname], *self.config.keycol[status]))
        

    def fatal_error(self, message):
        wx.MessageBox(message, 'Error', wx.OK | wx.ICON_WARNING)
        self.exit()

    def exit(self):
        self.stopTimer()
        self.RemoveIcon()
        wx.CallAfter(self.Destroy)


def main():
    app = wx.App(False)
    mcsystray()
    app.MainLoop()


if __name__ == '__main__':
    main()
