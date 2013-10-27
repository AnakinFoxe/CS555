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
        elif title == enum.OPT_02_ZOOM_OUT:
            self.opt02ZoomOut()


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
        label = wx.StaticText(self, -1, "Width")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.opt_01_text1 = wx.TextCtrl(self, -1, str(enum.DEFAULT_WIDTH_MIN), size=(80,-1))
        box.Add(self.opt_01_text1, 1, wx.ALIGN_CENTRE|wx.ALL, 5)

        self.sizer_main.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "Height")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.opt_01_text2 = wx.TextCtrl(self, -1, str(enum.DEFAULT_HEIGHT_MIN), size=(80,-1))
        box.Add(self.opt_01_text2, 1, wx.ALIGN_CENTRE|wx.ALL, 5)

        self.sizer_main.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

    def opt02ZoomOut(self):
        label = wx.StaticText(self, -1, "Zoom Out Operation")
        self.sizer_main.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "Width")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.opt_02_text1 = wx.TextCtrl(self, -1, str(enum.DEFAULT_WIDTH_MIN), size=(80,-1))
        box.Add(self.opt_02_text1, 1, wx.ALIGN_CENTRE|wx.ALL, 5)

        self.sizer_main.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "Height")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.opt_02_text2 = wx.TextCtrl(self, -1, str(enum.DEFAULT_HEIGHT_MIN), size=(80,-1))
        box.Add(self.opt_02_text2, 1, wx.ALIGN_CENTRE|wx.ALL, 5)

        self.sizer_main.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

