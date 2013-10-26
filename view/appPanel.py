'''
@author: Anakin
'''

import wx


class Panel(wx.Panel):

    def __init__(self, parent):
        super(Panel, self).__init__(parent, -1)

        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.SetSizer(self.sizer)
        self.SetAutoLayout(True)
        self.sizer.Fit(self)


    def setLeftImage(self, path):
        self.left_bitmap = wx.Bitmap(path)
        self.left_bitmap = wx.StaticBitmap(self, -1, self.left_bitmap)

        self.sizer.Add(self.left_bitmap, 1, wx.ALIGN_LEFT)
        self.sizer.Fit(self)

    def setRightImage(self, path):
        self.right_bitmap = wx.Bitmap(path)
        self.right_bitmap = wx.StaticBitmap(self, -1, self.right_bitmap)

        self.sizer.Add(self.right_bitmap, 1, wx.ALIGN_RIGHT)
        self.sizer.Fit(self)




