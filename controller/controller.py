'''
@author: Anakin
'''

import wx
import enum

from model.image import Image
from view.appFrame import Frame
from view.appPanel import Panel
from view.mdfDialog import MdfDialog

from wx.lib.pubsub import Publisher as pub

class Controller:
    dir = 'C:\Users\Anakin\Documents\GitHub\CS555\\'
    src = 'src_ascii.pgm'
    dst = 'dst.pgm'
    tmp = 'tmp.pgm'
    tmp2 = 'tmp2.pgm'
    ref = 'ref.pgm'
    #default = 'default.pgm'

    choice = None

    opt_01_width    = 60
    opt_01_height   = 80

    opt_02_width    = 60
    opt_02_height   = 80
    opt_02_selection= enum.ZOOM_BILINEAR

    def __init__(self, app):
        self.src_image = Image()
        self.dst_image = None

        self.frame = Frame()
        self.panel = Panel(self.frame)

        #self.panel.open.Bind(wx.EVT_BUTTON, self.OnOpen)
        self.panel.choice.Bind(wx.EVT_CHOICE, self.onChoice)
        self.panel.go.Bind(wx.EVT_BUTTON, self.onGo)
        self.panel.mdf_param.Bind(wx.EVT_BUTTON, self.onModify)

        pub.subscribe(self.displayLeft, "LEFT IMAGE LOADED")
        pub.subscribe(self.displayRight, "RIGHT IMAGE CHANGED")

        ''' Load left image '''
        self.loadLeft(self.dir + self.src)

        ''' Shrink left image to 60x80 and display on the right '''
        #self.shrinkRight(self.dir + self.dst)

        self.frame.Show(True)

    def onChoice(self, event):
        self.choice = event.GetString()
        print("choose: %s" % self.choice)

    def onGo(self, event):
        if self.choice == enum.OPT_01_SHRINK:
            print enum.OPT_01_SHRINK
            self.shrinkRight(self.dir + self.dst)
        elif self.choice == enum.OPT_02_ZOOM_OUT:
            print enum.OPT_02_ZOOM_OUT
            self.zoomBackRight(self.dir + self.dst)
        elif self.choice == enum.OPT_03_REDUCE_GL:
            print enum.OPT_03_REDUCE_GL
        elif self.choice == enum.OPT_04_TRANSFORM:
            print enum.OPT_04_TRANSFORM
        elif self.choice == enum.OPT_05_HISTO_EQ:
            print enum.OPT_05_HISTO_EQ
        elif self.choice == enum.OPT_06_HISTO_MAT:
            print enum.OPT_06_HISTO_MAT
        else:
            print "Do nothing"

    def onModify(self, event):
        if self.choice is not None:
            useMetal = False
            if 'wxMac' in wx.PlatformInfo:
                useMetal = self.cb.IsChecked()

            dlg = MdfDialog(self.panel, -1, self.choice, size=(350, 200),
                            style=wx.DEFAULT_DIALOG_STYLE,
                            useMetal=useMetal)
            dlg.CenterOnScreen()

            val = dlg.ShowModal()
            if val == wx.ID_OK:
                if self.choice == enum.OPT_01_SHRINK:
                    self.opt_01_width   = int(dlg.opt_01_text1.GetValue())
                    self.opt_01_height  = int(dlg.opt_01_text2.GetValue())
                elif self.choice == enum.OPT_02_ZOOM_OUT:
                    self.opt_02_width   = int(dlg.opt_02_text1.GetValue())
                    self.opt_02_height  = int(dlg.opt_02_text2.GetValue())
                    if dlg.opt_02_choice1.GetValue() is True:
                        self.opt_02_selection = enum.ZOOM_REPLIC
                    elif dlg.opt_02_choice2.GetValue() is True:
                        self.opt_02_selection = enum.ZOOM_NEAR_NGHR
                    elif dlg.opt_02_choice3.GetValue() is True:
                        self.opt_02_selection = enum.ZOOM_BILINEAR
                    print self.opt_02_selection
            else:
                print "Cancelled..."

            dlg.Destroy()
        else:
            print "Not exist"


    def loadLeft(self, path):
        self.src_image.readContent(path)
        self.src_image.loadLeft(self.src_image,
                                enum.DEFAULT_WIDTH,
                                enum.DEFAULT_HEIGHT,
                                self.dir + self.tmp)

    def shrinkRight(self, path):
        self.dst_image = Image(self.src_image.magic_word,
                               self.src_image.width,
                               self.src_image.height,
                               self.src_image.maxV,
                               self.src_image.pixel)
        self.dst_image.shrinkRight(self.dst_image,
                                   self.opt_01_width,
                                   self.opt_01_height,
                                   path)

    def zoomBackRight(self, path):
        self.dst_image = Image(self.src_image.magic_word,
                               self.src_image.width,
                               self.src_image.height,
                               self.src_image.maxV,
                               self.src_image.pixel)
        self.dst_image.zoomBack(self.dst_image,
                                self.opt_02_selection,
                                self.opt_02_width,
                                self.opt_02_height,
                                self.dir + self.tmp2,
                                enum.DEFAULT_WIDTH,
                                enum.DEFAULT_HEIGHT,
                                path)

    def displayLeft(self, message):
        self.panel.setLeftImage(message.data)

    def displayRight(self, message):
        self.panel.setRightImage(message.data)



