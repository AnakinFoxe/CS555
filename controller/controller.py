'''
@author: Anakin
'''

from model.image import Image
from view.appFrame import Frame
from view.appPanel import Panel

from wx.lib.pubsub import Publisher as pub

class Controller:
    dir = 'C:\Work\Python\workspace\CS555\\'
    src = 'src_ascii.pgm'
    dst = 'dst.pgm'
    tmp = 'tmp.pgm'
    ref = 'ref.pgm'
    #default = 'default.pgm'

    def __init__(self, app):
        self.src_image = Image()
        self.dst_image = None

        self.frame = Frame()
        self.panel = Panel(self.frame)

        pub.subscribe(self.displayLeft, "LEFT IMAGE LOADED")
        pub.subscribe(self.displayRight, "RIGHT IMAGE CHANGED")

        ''' Load left image '''
        self.loadLeft(self.dir + self.src)

        ''' Shrink left image to 60x80 and display on the right '''
        self.shrinkRight(self.dir + self.dst)

        self.frame.Show(True)

    def loadLeft(self, path):
        self.src_image.readContent(path)
        self.src_image.loadLeft(self.src_image,
                                480, 640,
                                self.dir + self.tmp)

    def shrinkRight(self, path):
        self.dst_image = Image(self.src_image.magic_word,
                               self.src_image.width,
                               self.src_image.height,
                               self.src_image.maxV,
                               self.src_image.pixel)
        self.dst_image.shrinkRight(self.dst_image,
                                   60, 80,
                                   path)

    def displayLeft(self, message):
        self.panel.setLeftImage(message.data)

    def displayRight(self, message):
        self.panel.setRightImage(message.data)



