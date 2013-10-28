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

    opt_01_width        = enum.DEFAULT_WIDTH_MIN
    opt_01_height       = enum.DEFAULT_HEIGHT_MIN

    opt_02_width        = enum.DEFAULT_WIDTH_MIN
    opt_02_height       = enum.DEFAULT_HEIGHT_MIN
    opt_02_selection    = enum.ZOOM_BILINEAR

    opt_07_resolution   = enum.DEFAULT_RESLTN_MIN
    opt_07_selection    = enum.SP_FLT_SMOOTH

    opt_08_bits         = 64 # top 3 set to zero

    opt_09_resolution   = enum.DEFAULT_RESLTN_MIN
    opt_09_selection    = enum.RESTORE_ARITHMETIC

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

        self.dst_image = Image(self.src_image.magic_word,
                               self.src_image.width,
                               self.src_image.height,
                               self.src_image.maxV,
                               self.src_image.pixel)

        self.frame.Show(True)

    def onChoice(self, event):
        self.choice = event.GetString()
        print("choose: %s" % self.choice)

    def onGo(self, event):
        if self.choice == enum.OPT_01_SHRINK:
            print enum.OPT_01_SHRINK
            self.shrinkRight(self.dir + self.dst)
        elif self.choice == enum.OPT_02_ZOOM_BACK:
            print enum.OPT_02_ZOOM_BACK
            self.zoomBackRight(self.dir + self.dst)
        elif self.choice == enum.OPT_03_REDUCE_GL:
            print enum.OPT_03_REDUCE_GL
        elif self.choice == enum.OPT_04_TRANSFORM:
            print enum.OPT_04_TRANSFORM
        elif self.choice == enum.OPT_05_HISTO_EQ:
            print enum.OPT_05_HISTO_EQ
        elif self.choice == enum.OPT_06_HISTO_MAT:
            print enum.OPT_06_HISTO_MAT
        elif self.choice == enum.OPT_07_SPATIAL_FLT:
            print enum.OPT_07_SPATIAL_FLT
            self.spatialFilterRight(self.dir + self.dst)
        elif self.choice == enum.OPT_08_BIT_PLANE:
            print enum.OPT_08_BIT_PLANE
            self.bitPlaneRight(self.dir + self.dst)
        elif self.choice == enum.OPT_09_RESTORE:
            print enum.OPT_09_RESTORE
            self.restoreImage(self.dir + self.dst)
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
                elif self.choice == enum.OPT_02_ZOOM_BACK:
                    self.opt_02_width   = int(dlg.opt_02_text1.GetValue())
                    self.opt_02_height  = int(dlg.opt_02_text2.GetValue())
                    if dlg.opt_02_choice1.GetValue() is True:
                        self.opt_02_selection = enum.ZOOM_REPLIC
                    elif dlg.opt_02_choice2.GetValue() is True:
                        self.opt_02_selection = enum.ZOOM_NEAR_NGHR
                    elif dlg.opt_02_choice3.GetValue() is True:
                        self.opt_02_selection = enum.ZOOM_BILINEAR
                    print self.opt_02_selection
                elif self.choice == enum.OPT_07_SPATIAL_FLT:
                    self.opt_07_resolution = int(dlg.opt_07_text1.GetValue())
                    if dlg.opt_07_choice1.GetValue() is True:
                        self.opt_07_selection = enum.SP_FLT_SMOOTH
                    elif dlg.opt_07_choice2.GetValue() is True:
                        self.opt_07_selection = enum.SP_FLT_MEDIAN
                    elif dlg.opt_07_choice3.GetValue() is True:
                        self.opt_07_selection = enum.SP_FLT_LAPLACIAN
                    elif dlg.opt_07_choice4.GetValue() is True:
                        self.opt_07_selection = enum.SP_FLT_H_BOOST
                    print self.opt_07_selection
                elif self.choice == enum.OPT_08_BIT_PLANE:
                    self.opt_08_bits = 0
                    if dlg.opt_08_check1.GetValue() is True:
                        self.opt_08_bits |= 1
                    if dlg.opt_08_check2.GetValue() is True:
                        self.opt_08_bits |= 1 << 1
                    if dlg.opt_08_check3.GetValue() is True:
                        self.opt_08_bits |= 1 << 2
                    if dlg.opt_08_check4.GetValue() is True:
                        self.opt_08_bits |= 1 << 3
                    if dlg.opt_08_check5.GetValue() is True:
                        self.opt_08_bits |= 1 << 4
                    if dlg.opt_08_check6.GetValue() is True:
                        self.opt_08_bits |= 1 << 5
                    if dlg.opt_08_check7.GetValue() is True:
                        self.opt_08_bits |= 1 << 6
                    if dlg.opt_08_check8.GetValue() is True:
                        self.opt_08_bits |= 1 << 7
                    print self.opt_08_bits
                elif self.choice == enum.OPT_09_RESTORE:
                    self.opt_09_resolution = int(dlg.opt_09_text1.GetValue())
                    if dlg.opt_09_choice1.GetValue() is True:
                        self.opt_09_selection = enum.RESTORE_ARITHMETIC
                    elif dlg.opt_09_choice2.GetValue() is True:
                        self.opt_09_selection = enum.RESTORE_GEOMETRIC
                    elif dlg.opt_09_choice3.GetValue() is True:
                        self.opt_09_selection = enum.RESTORE_HARMONIC
                    elif dlg.opt_09_choice4.GetValue() is True:
                        self.opt_09_selection = enum.RESTORE_CONTRAHARM
                    elif dlg.opt_09_choice5.GetValue() is True:
                        self.opt_09_selection = enum.RESTORE_MAX
                    elif dlg.opt_09_choice6.GetValue() is True:
                        self.opt_09_selection = enum.RESTORE_MIN
                    elif dlg.opt_09_choice7.GetValue() is True:
                        self.opt_09_selection = enum.RESTORE_MIDPOINT
                    elif dlg.opt_09_choice8.GetValue() is True:
                        self.opt_09_selection = enum.RESTORE_ALPHA_TRIM
                    print self.opt_09_selection
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
        self.dst_image.shrinkRight(self.dst_image,
                                   self.opt_01_width,
                                   self.opt_01_height,
                                   path)

    def zoomBackRight(self, path):
        self.dst_image.zoomBack(self.dst_image,
                                self.opt_02_selection,
                                self.opt_02_width,
                                self.opt_02_height,
                                self.dir + self.tmp2,
                                enum.DEFAULT_WIDTH,
                                enum.DEFAULT_HEIGHT,
                                path)

    def spatialFilterRight(self, path):
        self.dst_image.spatialFilter(self.src_image,
                                     self.opt_07_selection,
                                     self.opt_07_resolution,
                                     path)

    def bitPlaneRight(self, path):
        self.dst_image.bitPlane(self.src_image,
                                self.opt_08_bits,
                                path)

    def restoreImage(self, path):
        self.dst_image.restoreImage(self.src_image,
                                    self.opt_09_selection,
                                    self.opt_09_resolution,
                                    path)

    def displayLeft(self, message):
        self.panel.setLeftImage(message.data)

    def displayRight(self, message):
        self.panel.setRightImage(message.data)



