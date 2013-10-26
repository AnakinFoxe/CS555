'''
@author: Anakin
'''

import wx

class Frame(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, None, -1,
                          title = "Digital Image Processing (CS 555)",
                          size = (1000, 740))   # 480 x 640 => (480x2=960) x (640 + 60)