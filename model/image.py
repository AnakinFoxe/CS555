'''
@author: Anakin
'''

from wx.lib.pubsub import Publisher as pub

class Image():

    magic_word  = 0
    width       = 0
    height      = 0
    maxV        = 0
    pixel       = []

    def __init__(self, magic_word = 0, width = 0, height = 0, maxV = 0, pixel = []):
        self.magic_word = magic_word
        self.width      = width
        self.height     = height
        self.maxV       = maxV
        self.pixel      = pixel

    def readContent(self, path):
        with open(path, 'r') as f:
            magic_word = f.readline()
            f.readline()
            width, height = [int(x) for x in f.readline().split()]
            maxV = int(f.readline())
            pixel = [[0 for x in xrange(width)] for x in xrange(height)]
            w = 0
            h = 0
            for line in f:
                for x in line.split():
                    pixel[h][w] = int(x)
                    w += 1
                    if w >= width:
                        w = 0
                        h += 1
                        if h >= height:
                            h = 0
            f.close()
            self.__init__(magic_word, width, height, maxV, pixel)
            #pub.sendMessage("IMAGE LOADED", path)

    def writeContent(self, path):
        magic_word  = self.magic_word
        width       = self.width
        height      = self.height
        maxV        = self.maxV
        pixel       = self.pixel

        s = str(magic_word) + '# ' + str(path) + '\n'
        s += str(width) + '  ' +  str(height) + '\n'
        s += str(maxV) + '\n'
        n = 0
        for h in range(height):
            for w in range(width):
                s += str(pixel[h][w]) + ' '
                n += 1
                if n >= 12:
                    s += '\n'
                    n = 0
        with open(path, 'w') as f:
            f.write(s)
            #pub.sendMessage("IMAGE SAVED", path)

    def genDefault(self, dst_width, dst_height, path):
        maxV = 55
        dst_pixel = [[maxV for w in xrange(dst_width)] for h in xrange(dst_height)]

        self.__init__('P2', dst_width, dst_height, maxV, dst_pixel)
        self.writeContent(path)


    def shrink(self, src_image, dst_width, dst_height, path):
        src_width   = src_image.width
        src_height  = src_image.height
        src_pixel   = src_image.pixel
        dst_maxV    = 0
        dst_pixel   = [[0 for w in xrange(dst_width)] for h in xrange(dst_height)]

        for h in range(dst_height):
            for w in range(dst_width):
                x = min(int(h * src_height / dst_height), src_height-1)
                y = min(int(w * src_width / dst_width), src_width-1)
                dst_pixel[h][w] = src_pixel[x][y]
                if dst_maxV < dst_pixel[h][w]:
                    dst_maxV = dst_pixel[h][w]

        self.__init__(src_image.magic_word,
                      dst_width,
                      dst_height,
                      dst_maxV,
                      dst_pixel)
        self.writeContent(path)
        #pub.sendMessage("IMAGE CHANGED", path)

    def loadLeft(self, src_image, dst_width, dst_height, path):
        self.shrink(src_image, dst_width, dst_height, path)
        pub.sendMessage("LEFT IMAGE LOADED", path)

    def shrinkRight(self, src_image, dst_width, dst_height, path):
        self.shrink(src_image, dst_width, dst_height, path)
        pub.sendMessage("RIGHT IMAGE CHANGED", path)

