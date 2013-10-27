'''
@author: Anakin
'''

import wx
import enum


class Panel(wx.Panel):

    def __init__(self, parent):
        super(Panel, self).__init__(parent, -1)

        ''' Left '''
        sizer_left = wx.BoxSizer(wx.VERTICAL)

        ''' Left Top '''
        lefttop_title = wx.StaticBox(self, -1, "")
        self.sizer_lefttop = wx.StaticBoxSizer(lefttop_title, wx.HORIZONTAL)

        self.open = wx.Button(self, label="&Open")
        self.sizer_lefttop.Add(self.open, 0, wx.ALIGN_LEFT|wx.ALIGN_CENTER)

        ''' Left Bottom '''
        leftbtm_title = wx.StaticBox(self, -1, "Original Image")
        self.sizer_leftbtm = wx.StaticBoxSizer(leftbtm_title, wx.VERTICAL)

        bmp = wx.EmptyBitmap(enum.DEFAULT_WIDTH, enum.DEFAULT_HEIGHT)
        self.left_bitmap = wx.StaticBitmap(self, -1, bmp)

        self.sizer_leftbtm.Add(self.left_bitmap, 1, wx.ALIGN_CENTER)

        sizer_left.Add(self.sizer_lefttop, 0, wx.EXPAND)
        sizer_left.Add(self.sizer_leftbtm, 1, wx.EXPAND)



        ''' Right '''
        sizer_right = wx.BoxSizer(wx.VERTICAL)

        ''' Right Top '''
        righttop_title = wx.StaticBox(self, -1, "")
        self.sizer_righttop = wx.StaticBoxSizer(righttop_title, wx.HORIZONTAL)

        choice_list = enum.CHOICE_LIST
        self.choice = wx.Choice(self, -1, choices = choice_list)

        self.go = wx.Button(self, label="&GO!")
        self.mdf_param = wx.Button(self, label="Modify Default Parameters...")

        self.sizer_righttop.Add(self.choice, 0, wx.ALIGN_LEFT|wx.ALIGN_CENTER)
        self.sizer_righttop.Add(self.go, 0, wx.ALIGN_LEFT|wx.ALIGN_CENTER)
        self.sizer_righttop.Add(self.mdf_param, 0, wx.ALIGN_LEFT|wx.ALIGN_CENTER)

        ''' Right Center '''
        rightctr_title = wx.StaticBox(self, -1, "Processed Image")
        self.sizer_rightctr = wx.StaticBoxSizer(rightctr_title, wx.VERTICAL)

        bmp = wx.EmptyBitmap(0, 0)
        self.right_bitmap = wx.StaticBitmap(self, -1, bmp)

        self.sizer_rightctr.Add(self.right_bitmap, 1,
                                wx.ALIGN_CENTER)#_HORIZONTAL | wx.ALL | wx.ADJUST_MINSIZE)

        ''' Right Bottom '''
        rightbtm_title = wx.StaticBox(self, -1, "")
        self.sizer_rightbtm = wx.StaticBoxSizer(rightbtm_title, wx.HORIZONTAL)

        sizer_right.Add(self.sizer_righttop, 0, wx.EXPAND)
        sizer_right.Add(self.sizer_rightctr, 1, wx.EXPAND)
        sizer_right.Add(self.sizer_rightbtm, 0, wx.EXPAND)


        ''' All '''
        self.sizer_all = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer_all.Add(sizer_left, 1, wx.EXPAND)
        self.sizer_all.Add(sizer_right, 1, wx.EXPAND)
        self.SetSizer(self.sizer_all)
        self.SetAutoLayout(True)
        self.sizer_all.Fit(self)

    def setLeftImage(self, path):
        bmp = wx.Bitmap(path)
        '''if not bmp.Ok():
            bmp = wx.EmptyBitmap(enum.DEFAULT_WIDTH, enum.DEFAULT_HEIGHT)
            self.clearImage(bmp)'''
        self.left_bitmap.SetBitmap(bmp)

    def setRightImage(self, path):
        bmp = wx.Bitmap(path)
        '''if not bmp.Ok():
            bmp = wx.EmptyBitmap(60, 80)
            self.clearImage(bmp)'''
        self.right_bitmap.SetBitmap(bmp)
        ''' Still got problem with Fit, don't know how to put it into the middle '''
        #self.sizer_rightctr.FitInside(self)
        self.Refresh()

    def clearImage(self, bmp):
        dc = wx.MemoryDC()
        dc.SelectObject(bmp)
        dc.SetBackground(wx.Brush("white"))
        dc.Clear()


