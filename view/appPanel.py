'''
@author: Anakin
'''

import wx


class Panel(wx.Panel):

    def __init__(self, parent):
        super(Panel, self).__init__(parent, -1)

        self.open = wx.Button(self, label="&Open")
        self.close = wx.Button(self, label="&Close")

        self.sizer_left = wx.BoxSizer(wx.VERTICAL)
        self.sizer_left.Add(self.open, 0, wx.EXPAND)
        #self.sizer_left.Add(self.close, 0, wx.EXPAND)


        self.sizer_right = wx.BoxSizer(wx.VERTICAL)
        self.sizer_right.Add(self.close, 0, wx.EXPAND)


        self.sizer_all = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer_all.Add(self.sizer_left, 1, wx.EXPAND)
        self.sizer_all.Add(self.sizer_right, 1, wx.EXPAND)
        self.SetSizer(self.sizer_all)
        self.SetAutoLayout(True)
        self.sizer_all.Fit(self)

    def setLeftImage(self, path):
        self.left_bitmap = wx.Bitmap(path)
        self.left_bitmap = wx.StaticBitmap(self, -1, self.left_bitmap)

        self.sizer_left.Add(self.left_bitmap, 1, wx.EXPAND)
        self.sizer_left.Fit(self)

    def setRightImage(self, path):
        self.right_bitmap = wx.Bitmap(path)
        self.right_bitmap = wx.StaticBitmap(self, -1, self.right_bitmap)

        self.sizer_right.Add(self.right_bitmap, 1, wx.EXPAND)
        self.sizer_right.Fit(self)




