'''
@author: Anakin
'''

import wx
import enum

class Frame(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, None, -1,
                          title = enum.WINDOW_TITLE,
                          size = enum.WINDOW_SIZE)   # 480 x 640 => (480x2=960) x (640 + 60)