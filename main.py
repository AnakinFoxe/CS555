'''
@author: Anakin
'''
import wx

from controller import controller

class WxApp(wx.App):
    app_controller = None

    def OnInit(self):
        self.app_controller = controller.Controller(self)
        return True


if __name__ == '__main__':
    wxApp = WxApp(False)
    wxApp.MainLoop()