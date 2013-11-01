'''
@author: Anakin
'''

import wx
import enum


class MdfDialog(wx.Dialog):
    def __init__(self, parent, ID, title,
                 size=wx.DefaultSize, pos=wx.DefaultPosition,
                 style=wx.DEFAULT_DIALOG_STYLE,
                 useMetal=False):

        pre = wx.PreDialog()
        pre.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
        pre.Create(parent, ID, title, pos, size, style)

        self.PostCreate(pre)

        if 'wxMac' in wx.PlatformInfo and useMetal:
            self.SetExtraStyle(wx.DIALOG_EX_METAL)

        self.sizer_main = wx.BoxSizer(wx.VERTICAL)

        if title == enum.OPT_01_SHRINK:
            self.opt01Shrink()
        elif title == enum.OPT_02_ZOOM_BACK:
            self.opt02ZoomOut()
        elif title == enum.OPT_03_REDUCE_GL:
            self.opt03reduceGrayLevel()
        elif title == enum.OPT_04_TRANSFORM:
            self.opt04transform()
        elif title == enum.OPT_05_HISTO_EQ:
            self.opt05histogramEQ()
        elif title == enum.OPT_06_HISTO_MAT:
            self.opt06histogramMatch()
        elif title == enum.OPT_07_SPATIAL_FLT:
            self.opt07SpatialFilter()
        elif title == enum.OPT_08_BIT_PLANE:
            self.opt08BitPlane()
        elif title == enum.OPT_09_RESTORE:
            self.opt09RestoreImage()


        sizer_btn = wx.StdDialogButtonSizer()

        if wx.Platform != "__WXMSW__":
            btn = wx.ContextHelpButton(self)
            sizer_btn.AddButton(btn)

        btn = wx.Button(self, wx.ID_OK)
        btn.SetDefault()
        sizer_btn.AddButton(btn)

        btn = wx.Button(self, wx.ID_CANCEL)
        sizer_btn.AddButton(btn)
        sizer_btn.Realize()

        self.sizer_main.Add(sizer_btn, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        self.SetSizer(self.sizer_main)
        self.sizer_main.Fit(self)

    def opt01Shrink(self):
        label = wx.StaticText(self, -1, "Shring Operation")
        self.sizer_main.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "Shrink2Width")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.opt_01_text1 = wx.TextCtrl(self, -1, str(enum.DEFAULT_WIDTH_MIN), size=(80,-1))
        box.Add(self.opt_01_text1, 1, wx.ALIGN_CENTRE|wx.ALL, 5)

        self.sizer_main.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "Shrink2Height")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.opt_01_text2 = wx.TextCtrl(self, -1, str(enum.DEFAULT_HEIGHT_MIN), size=(80,-1))
        box.Add(self.opt_01_text2, 1, wx.ALIGN_CENTRE|wx.ALL, 5)

        self.sizer_main.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

    def opt02ZoomOut(self):
        label = wx.StaticText(self, -1, "Zoom Back Operation")
        self.sizer_main.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "Shrink2Width")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.opt_02_text1 = wx.TextCtrl(self, -1, str(enum.DEFAULT_WIDTH_MIN), size=(80,-1))
        box.Add(self.opt_02_text1, 1, wx.ALIGN_CENTRE|wx.ALL, 5)

        self.sizer_main.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "Shrink2Height")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.opt_02_text2 = wx.TextCtrl(self, -1, str(enum.DEFAULT_HEIGHT_MIN), size=(80,-1))
        box.Add(self.opt_02_text2, 1, wx.ALIGN_CENTRE|wx.ALL, 5)

        self.sizer_main.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        choice_title = wx.StaticBox(self, -1, "")
        sizer_choice = wx.StaticBoxSizer(choice_title, wx.VERTICAL)

        self.opt_02_choice1 = wx.RadioButton(self, -1, enum.ZOOM_REPLIC)
        self.opt_02_choice2 = wx.RadioButton(self, -1, enum.ZOOM_NEAR_NGHR)
        self.opt_02_choice3 = wx.RadioButton(self, -1, enum.ZOOM_BILINEAR)

        sizer_choice.Add(self.opt_02_choice1, wx.ALIGN_LEFT)
        sizer_choice.Add(self.opt_02_choice2, wx.ALIGN_LEFT)
        sizer_choice.Add(self.opt_02_choice3, wx.ALIGN_LEFT)

        self.sizer_main.Add(sizer_choice, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

    def opt03reduceGrayLevel(self):
        label = wx.StaticText(self, -1, "Reduce Gray Level Operation")
        self.sizer_main.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "Gray Level (1-8)")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.opt_03_text1 = wx.TextCtrl(self, -1, str(enum.DEFAULT_GRAY_LEVEL), size=(80,-1))
        box.Add(self.opt_03_text1, 1, wx.ALIGN_CENTRE|wx.ALL, 5)

        self.sizer_main.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        choice_title = wx.StaticBox(self, -1, "Significance")
        sizer_choice = wx.StaticBoxSizer(choice_title, wx.VERTICAL)

        self.opt_03_choice1 = wx.RadioButton(self, -1, enum.REDUCE_GL_LEAST)
        self.opt_03_choice2 = wx.RadioButton(self, -1, enum.REDUCE_GL_MOST)

        sizer_choice.Add(self.opt_03_choice1, wx.ALIGN_LEFT)
        sizer_choice.Add(self.opt_03_choice2, wx.ALIGN_LEFT)

        self.sizer_main.Add(sizer_choice, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

    def opt04transform(self):
        label = wx.StaticText(self, -1, "Transformation Operation")
        self.sizer_main.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

        ''' Log Transformation '''
        choice_title = wx.StaticBox(self, -1, "")
        sizer_choice1 = wx.StaticBoxSizer(choice_title, wx.VERTICAL)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "Constant C")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.opt_04_text1 = wx.TextCtrl(self, -1, str(enum.DEFAULT_C), size=(80,-1))
        box.Add(self.opt_04_text1, 1, wx.ALIGN_CENTRE|wx.ALL, 5)

        sizer_choice1.Add(box, wx.ALIGN_LEFT)

        self.opt_04_choice1 = wx.RadioButton(self, -1, enum.TRANS_LOG)

        sizer_choice1.Add(self.opt_04_choice1, wx.ALIGN_LEFT)

        ''' Power Transformation '''
        choice_title = wx.StaticBox(self, -1, "")
        sizer_choice2 = wx.StaticBoxSizer(choice_title, wx.VERTICAL)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "Constant C")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.opt_04_text2 = wx.TextCtrl(self, -1, str(enum.DEFAULT_C), size=(80,-1))
        box.Add(self.opt_04_text2, 1, wx.ALIGN_CENTRE|wx.ALL, 5)

        sizer_choice2.Add(box, wx.ALIGN_LEFT)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "Gamma")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.opt_04_text3 = wx.TextCtrl(self, -1, str(enum.DEFAULT_GAMMA), size=(80,-1))
        box.Add(self.opt_04_text3, 1, wx.ALIGN_CENTRE|wx.ALL, 5)

        sizer_choice2.Add(box, wx.ALIGN_LEFT)

        self.opt_04_choice2 = wx.RadioButton(self, -1, enum.TRANS_POW)

        sizer_choice2.Add(self.opt_04_choice2, wx.ALIGN_LEFT)

        self.sizer_main.Add(sizer_choice1, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.sizer_main.Add(sizer_choice2, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)


    def opt05histogramEQ(self):
        label = wx.StaticText(self, -1, "Histogram Equalization")
        self.sizer_main.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

        ''' Global '''
        choice_title = wx.StaticBox(self, -1, "")
        sizer_choice1 = wx.StaticBoxSizer(choice_title, wx.VERTICAL)

        self.opt_05_choice1 = wx.RadioButton(self, -1, enum.HIST_EQ_GLOBAL)

        sizer_choice1.Add(self.opt_05_choice1, wx.ALIGN_LEFT)

        ''' Local '''
        choice_title = wx.StaticBox(self, -1, "")
        sizer_choice2 = wx.StaticBoxSizer(choice_title, wx.VERTICAL)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "Resolution")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.opt_05_text1 = wx.TextCtrl(self, -1, str(enum.DEFAULT_RESLTN_MIN), size=(80,-1))
        box.Add(self.opt_05_text1, 1, wx.ALIGN_CENTRE|wx.ALL, 5)

        sizer_choice2.Add(box, wx.ALIGN_LEFT)

        self.opt_05_choice2 = wx.RadioButton(self, -1, enum.HIST_EQ_LOCAL)

        sizer_choice2.Add(self.opt_05_choice2, wx.ALIGN_LEFT)

        self.sizer_main.Add(sizer_choice1, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.sizer_main.Add(sizer_choice2, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

    def opt06histogramMatch(self):
        label = wx.StaticText(self, -1, "Histogram Match")
        self.sizer_main.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

        label = wx.StaticText(self, -1, "No Parameter Change Supported")
        self.sizer_main.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)


    def opt07SpatialFilter(self):
        label = wx.StaticText(self, -1, "Spatial Filter Operation")
        self.sizer_main.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

        #self.sizer_main.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        ''' Sizer Choice 1 '''
        choice_title = wx.StaticBox(self, -1, "")
        sizer_choice1 = wx.StaticBoxSizer(choice_title, wx.VERTICAL)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "Resolution")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.opt_07_text1 = wx.TextCtrl(self, -1, str(enum.DEFAULT_RESLTN_MIN), size=(80,-1))
        box.Add(self.opt_07_text1, 1, wx.ALIGN_CENTRE|wx.ALL, 5)

        self.opt_07_choice1 = wx.RadioButton(self, -1, enum.SP_FLT_SMOOTH)
        self.opt_07_choice2 = wx.RadioButton(self, -1, enum.SP_FLT_MEDIAN)

        sizer_choice1.Add(box, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL)
        sizer_choice1.Add(self.opt_07_choice1, wx.ALIGN_LEFT)
        sizer_choice1.Add(self.opt_07_choice2, wx.ALIGN_LEFT)

        ''' Sizer Choice 2 '''
        choice_title = wx.StaticBox(self, -1, "")
        sizer_choice2 = wx.StaticBoxSizer(choice_title, wx.VERTICAL)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "Laplacian")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.opt_07_text2 = wx.TextCtrl(self, -1, str(enum.DEFAULT_LAPLACIAN), size=(80,-1))
        box.Add(self.opt_07_text2, 1, wx.ALIGN_CENTRE|wx.ALL, 5)

        self.opt_07_choice3 = wx.RadioButton(self, -1, enum.SP_FLT_LAPLACIAN)

        sizer_choice2.Add(box, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL)
        sizer_choice2.Add(self.opt_07_choice3, wx.ALIGN_LEFT)

        ''' Sizer Choice 3 '''
        choice_title = wx.StaticBox(self, -1, "")
        sizer_choice3 = wx.StaticBoxSizer(choice_title, wx.VERTICAL)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "k")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.opt_07_text3 = wx.TextCtrl(self, -1, str(enum.DEFAULT_K), size=(80,-1))
        box.Add(self.opt_07_text3, 1, wx.ALIGN_CENTRE|wx.ALL, 5)

        self.opt_07_choice4 = wx.RadioButton(self, -1, enum.SP_FLT_H_BOOST)

        sizer_choice3.Add(box, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL)
        sizer_choice3.Add(self.opt_07_choice4, wx.ALIGN_LEFT)

        self.sizer_main.Add(sizer_choice1, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.sizer_main.Add(sizer_choice2, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.sizer_main.Add(sizer_choice3, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

    def opt08BitPlane(self):
        label = wx.StaticText(self, -1, "Bit Plane Operation")
        self.sizer_main.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

        choice_title = wx.StaticBox(self, -1, "")
        sizer_choice = wx.StaticBoxSizer(choice_title, wx.VERTICAL)

        self.opt_08_check1 = wx.CheckBox(self, -1, "bit-1 (lowest)")
        self.opt_08_check2 = wx.CheckBox(self, -1, "bit-2")
        self.opt_08_check3 = wx.CheckBox(self, -1, "bit-3")
        self.opt_08_check4 = wx.CheckBox(self, -1, "bit-4")
        self.opt_08_check5 = wx.CheckBox(self, -1, "bit-5")
        self.opt_08_check6 = wx.CheckBox(self, -1, "bit-6")
        self.opt_08_check7 = wx.CheckBox(self, -1, "bit-7")
        self.opt_08_check8 = wx.CheckBox(self, -1, "bit-8 (highest)")

        sizer_choice.Add(self.opt_08_check1, wx.ALIGN_LEFT)
        sizer_choice.Add(self.opt_08_check2, wx.ALIGN_LEFT)
        sizer_choice.Add(self.opt_08_check3, wx.ALIGN_LEFT)
        sizer_choice.Add(self.opt_08_check4, wx.ALIGN_LEFT)
        sizer_choice.Add(self.opt_08_check5, wx.ALIGN_LEFT)
        sizer_choice.Add(self.opt_08_check6, wx.ALIGN_LEFT)
        sizer_choice.Add(self.opt_08_check7, wx.ALIGN_LEFT)
        sizer_choice.Add(self.opt_08_check8, wx.ALIGN_LEFT)

        self.sizer_main.Add(sizer_choice, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

    def opt09RestoreImage(self):
        label = wx.StaticText(self, -1, "Restore Image Operation")
        self.sizer_main.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "Resolution")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.opt_09_text1 = wx.TextCtrl(self, -1, str(enum.DEFAULT_RESLTN_MIN), size=(80,-1))
        box.Add(self.opt_09_text1, 1, wx.ALIGN_CENTRE|wx.ALL, 5)

        self.sizer_main.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        choice_title = wx.StaticBox(self, -1, "")
        sizer_choice = wx.StaticBoxSizer(choice_title, wx.VERTICAL)

        self.opt_09_choice1 = wx.RadioButton(self, -1, enum.RESTORE_ARITHMETIC)
        self.opt_09_choice2 = wx.RadioButton(self, -1, enum.RESTORE_GEOMETRIC)
        self.opt_09_choice3 = wx.RadioButton(self, -1, enum.RESTORE_HARMONIC)
        self.opt_09_choice4 = wx.RadioButton(self, -1, enum.RESTORE_CONTRAHARM)
        self.opt_09_choice5 = wx.RadioButton(self, -1, enum.RESTORE_MAX)
        self.opt_09_choice6 = wx.RadioButton(self, -1, enum.RESTORE_MIN)
        self.opt_09_choice7 = wx.RadioButton(self, -1, enum.RESTORE_MIDPOINT)
        self.opt_09_choice8 = wx.RadioButton(self, -1, enum.RESTORE_ALPHA_TRIM)

        sizer_choice.Add(self.opt_09_choice1, wx.ALIGN_LEFT)
        sizer_choice.Add(self.opt_09_choice2, wx.ALIGN_LEFT)
        sizer_choice.Add(self.opt_09_choice3, wx.ALIGN_LEFT)
        sizer_choice.Add(self.opt_09_choice4, wx.ALIGN_LEFT)
        sizer_choice.Add(self.opt_09_choice5, wx.ALIGN_LEFT)
        sizer_choice.Add(self.opt_09_choice6, wx.ALIGN_LEFT)
        sizer_choice.Add(self.opt_09_choice7, wx.ALIGN_LEFT)
        sizer_choice.Add(self.opt_09_choice8, wx.ALIGN_LEFT)

        self.sizer_main.Add(sizer_choice, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
