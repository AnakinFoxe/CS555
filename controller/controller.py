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
    dir = 'C:\Users\Anakin\Documents\GitHub\CS555\image\\'
    #src = 'src_ascii.pgm'
    #src = 'moon_ascii.pgm'
    #src = 'Fig0507_a__ckt_board_orig__tif_ascii.pgm'
    src = 'Fig0507_b__ckt_board_gauss_var_400__tif_ascii.pgm'
    #src = 'Fig0508_a__circuit_board_pepper_prob_pt1__tif_ascii.pgm'
    #src = 'Fig0508_b__circuit_board_salt_prob_pt1__tif_ascii.pgm'
    #src = 'Fig0510_a__ckt_board_saltpep_prob_pt05__tif_ascii.pgm'
    #src = 'Fig0512_a__ckt_uniform_var_800__tif_ascii.pgm'
    #src = 'Fig0512_b__ckt_uniform_plus_saltpepr_prob_pt1__tif_ascii.pgm'
    #src = 'Fig0513_a__ckt_gaussian_var_1000_mean_0__tif_ascii.pgm'
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

    opt_03_gray_lvl     = enum.DEFAULT_GRAY_LEVEL
    opt_03_sgn          = enum.DEFAULT_SIGN

    opt_04_selection    = enum.DEFAULT_TRANS
    opt_04_c            = enum.DEFAULT_C
    opt_04_gamma        = enum.DEFAULT_GAMMA

    opt_05_selection    = enum.DEFAULT_HIST_EQ
    opt_05_resolution   = enum.DEFAULT_RESLTN_MIN

    opt_07_resolution   = enum.DEFAULT_RESLTN_MIN
    opt_07_selection    = enum.SP_FLT_SMOOTH
    opt_07_laplacian    = enum.DEFAULT_LAPLACIAN
    opt_07_k            = enum.DEFAULT_K

    opt_08_bits         = 64

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

        ''' Load Reference image '''
        self.loadRef(self.dir + self.ref)

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
            self.reduceGrayLevel(self.dir + self.dst)
        elif self.choice == enum.OPT_04_TRANSFORM:
            print enum.OPT_04_TRANSFORM
            self.transform(self.dir + self.dst)
        elif self.choice == enum.OPT_05_HISTO_EQ:
            print enum.OPT_05_HISTO_EQ
            self.histogramEQ(self.dir + self.dst)
        elif self.choice == enum.OPT_06_HISTO_MAT:
            print enum.OPT_06_HISTO_MAT
            self.histogramMatch(self.dir + self.dst)
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
                elif self.choice == enum.OPT_03_REDUCE_GL:
                    self.opt_03_gray_lvl = int(dlg.opt_03_text1.GetValue())
                    if self.opt_03_gray_lvl < 1:
                        self.opt_03_gray_lvl = 1
                    elif self.opt_03_gray_lvl > 8:
                        self.opt_03_gray_lvl = 8
                    if dlg.opt_03_choice1.GetValue() is True:
                        self.opt_03_sgn = enum.REDUCE_GL_LEAST
                    elif dlg.opt_03_choice2.GetValue() is True:
                        self.opt_03_sgn = enum.REDUCE_GL_MOST
                    print("%s %d" % (self.opt_03_sgn, self.opt_03_gray_lvl))
                elif self.choice == enum.OPT_04_TRANSFORM:
                    if dlg.opt_04_choice1.GetValue() is True:
                        self.opt_04_selection = enum.TRANS_LOG
                        self.opt_04_c = float(dlg.opt_04_text1.GetValue())
                        print("%s %d %d" % (self.opt_04_selection,
                                        self.opt_04_c,
                                        self.opt_04_gamma))
                    elif dlg.opt_04_choice2.GetValue() is True:
                        self.opt_04_selection = enum.TRANS_POW
                        self.opt_04_c = float(dlg.opt_04_text2.GetValue())
                        self.opt_04_gamma = float(dlg.opt_04_text3.GetValue())
                        print("%s %d %d" % (self.opt_04_selection,
                                        self.opt_04_c,
                                        self.opt_04_gamma))
                elif self.choice == enum.OPT_05_HISTO_EQ:
                    if dlg.opt_05_choice1.GetValue() is True:
                        self.opt_05_selection = enum.HIST_EQ_GLOBAL
                    elif dlg.opt_05_choice2.GetValue() is True:
                        self.opt_05_selection = enum.HIST_EQ_LOCAL
                        self.opt_05_resolution = int(dlg.opt_05_text1.GetValue())
                elif self.choice == enum.OPT_07_SPATIAL_FLT:
                    if dlg.opt_07_choice1.GetValue() is True:
                        self.opt_07_resolution = int(dlg.opt_07_text1.GetValue())
                        self.opt_07_selection = enum.SP_FLT_SMOOTH
                    elif dlg.opt_07_choice2.GetValue() is True:
                        self.opt_07_resolution = int(dlg.opt_07_text1.GetValue())
                        self.opt_07_selection = enum.SP_FLT_MEDIAN
                    elif dlg.opt_07_choice3.GetValue() is True:
                        self.opt_07_laplacian = int(dlg.opt_07_text2.GetValue())
                        self.opt_07_selection = enum.SP_FLT_LAPLACIAN
                    elif dlg.opt_07_choice4.GetValue() is True:
                        self.opt_07_k = int(dlg.opt_07_text3.GetValue())
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

    def loadRef(self, path):
        self.opt_06_ref_image = Image()
        self.opt_06_ref_image.readContent(path)

    def reload(self):
        if self.dst_image is None:
            self.dst_image = Image()
        self.dst_image.__init__(self.src_image.magic_word,
                                self.src_image.width,
                                self.src_image.height,
                                self.src_image.maxV,
                                self.src_image.pixel)

    def shrinkRight(self, path):
        self.reload(self.src_image, self.dst_image)
        self.dst_image.shrinkRight(self.dst_image,
                                   self.opt_01_width,
                                   self.opt_01_height,
                                   path)

    def zoomBackRight(self, path):
        self.reload(self.src_image, self.dst_image)
        self.dst_image.zoomBack(self.dst_image,
                                self.opt_02_selection,
                                self.opt_02_width,
                                self.opt_02_height,
                                self.dir + self.tmp2,
                                enum.DEFAULT_WIDTH,
                                enum.DEFAULT_HEIGHT,
                                path)

    def reduceGrayLevel(self, path):
        self.reload()
        self.dst_image.reduceGrayLevel(self.dst_image,
                                       self.opt_03_gray_lvl,
                                       self.opt_03_sgn,
                                       path)

    def transform(self, path):
        self.reload()
        self.dst_image.transform(self.src_image,
                                 self.opt_04_selection,
                                 self.opt_04_c,
                                 self.opt_04_gamma,
                                 path)

    def histogramEQ(self, path):
        self.reload()
        self.dst_image.histogramEQ(self.src_image,
                                   self.opt_05_selection,
                                   self.opt_05_resolution,
                                   path)

    def histogramMatch(self, path):
        self.reload()
        self.dst_image.histogramMatch(self.src_image,
                                      self.opt_06_ref_image,
                                      path)

    def spatialFilterRight(self, path):
        self.reload()
        self.dst_image.spatialFilter(self.dst_image,
                                     self.opt_07_selection,
                                     self.opt_07_resolution,
                                     self.opt_07_laplacian,
                                     self.opt_07_k,
                                     path)

    def bitPlaneRight(self, path):
        self.reload()
        self.dst_image.bitPlane(self.dst_image,
                                self.opt_08_bits,
                                path)

    def restoreImage(self, path):
        self.reload()
        self.dst_image.restoreImage(self.dst_image,
                                    self.opt_09_selection,
                                    self.opt_09_resolution,
                                    path)

    def displayLeft(self, message):
        self.panel.setLeftImage(message.data)

    def displayRight(self, message):
        self.panel.setRightImage(message.data)



