'''
@author: Anakin
'''

import wx


class Panel(wx.Panel):

    def __init__(self, parent):
        super(Panel, self).__init__(parent, -1)

        self.open = wx.Button(self, label="&Open")
        self.close = wx.Button(self, label="&Close")

        """ Left """
        sizer_left = wx.BoxSizer(wx.VERTICAL)

        """ Left Top """
        lefttop_title = wx.StaticBox(self, -1, "")
        self.sizer_lefttop = wx.StaticBoxSizer(lefttop_title, wx.HORIZONTAL)
        self.sizer_lefttop.Add(self.open, 0, wx.EXPAND)

        """ Left Bottom """
        leftbtm_title = wx.StaticBox(self, -1, "Original Image")
        self.sizer_leftbtm = wx.StaticBoxSizer(leftbtm_title, wx.VERTICAL)

        sizer_left.Add(self.sizer_lefttop, 0, wx.EXPAND)
        sizer_left.Add(self.sizer_leftbtm, 1, wx.EXPAND)

        """ Right """
        sizer_right = wx.BoxSizer(wx.VERTICAL)

        """ Right Top """
        righttop_title = wx.StaticBox(self, -1, "")
        self.sizer_righttop = wx.StaticBoxSizer(righttop_title, wx.HORIZONTAL)
        self.sizer_righttop.Add(self.close, 0, wx.EXPAND)

        """ Right Center """
        rightctr_title = wx.StaticBox(self, -1, "Processed Image")
        self.sizer_rightctr = wx.StaticBoxSizer(rightctr_title, wx.VERTICAL)

        """ Right Bottom """
        rightbtm_title = wx.StaticBox(self, -1, "")
        self.sizer_rightbtm = wx.StaticBoxSizer(rightbtm_title, wx.HORIZONTAL)

        sizer_right.Add(self.sizer_righttop, 0, wx.EXPAND)
        sizer_right.Add(self.sizer_rightctr, 1, wx.EXPAND)
        sizer_right.Add(self.sizer_rightbtm, 0, wx.EXPAND)


        """ All """
        sizer_all = wx.BoxSizer(wx.HORIZONTAL)
        sizer_all.Add(sizer_left, 1, wx.EXPAND)
        sizer_all.Add(sizer_right, 1, wx.EXPAND)
        self.SetSizer(sizer_all)
        self.SetAutoLayout(True)
        sizer_all.Fit(self)

    def setLeftImage(self, path):
        self.left_bitmap = wx.Bitmap(path)
        self.left_bitmap = wx.StaticBitmap(self, -1, self.left_bitmap)

        self.sizer_leftbtm.Add(self.left_bitmap, 1, wx.ALIGN_CENTER)
        self.sizer_leftbtm.Fit(self)

    def setRightImage(self, path):
        self.right_bitmap = wx.Bitmap(path)
        self.right_bitmap = wx.StaticBitmap(self, -1, self.right_bitmap)

        self.sizer_rightctr.Add(self.right_bitmap, 1, wx.ALIGN_CENTER)
        self.sizer_rightctr.Fit(self)




