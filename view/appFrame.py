'''
@author: Anakin
'''

import wx

class Frame(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, None, -1,
                          title = "Digital Image Processing (CS 555)",
                          size = (1024, 600))