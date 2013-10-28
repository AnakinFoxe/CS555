'''
@author: Anakin
'''

import enum

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

        print "shrink"
        self.__init__(src_image.magic_word,
                      dst_width,
                      dst_height,
                      dst_maxV,
                      dst_pixel)
        self.writeContent(path)


    def zoomBack_Replic(self, src_image, dst_width, dst_height, path):
        ratioW = dst_width / src_image.width
        ratioH = dst_height / src_image.height
        dst_maxV = 0
        dst_pixel = [[0 for w in xrange(dst_width)] for h in xrange(dst_height)]

        for h in range(dst_height):
            src_h = min(int(h/ratioH), src_image.height-1)
            for w in range(dst_width):
                src_w = min(int(w/ratioW), src_image.width-1)
                dst_pixel[h][w] = src_image.pixel[src_h][src_w]
                if dst_maxV < dst_pixel[h][w]:
                    dst_maxV = dst_pixel[h][w]

        self.__init__(src_image.magic_word,
                      dst_width,
                      dst_height,
                      dst_maxV,
                      dst_pixel)
        self.writeContent(path)

    def zoomBack_NearNghr(self, src_image, dst_width, dst_height, path):
        ratioW = dst_width / src_image.width
        ratioH = dst_height / src_image.height
        dst_maxV = 0
        dst_pixel = [[0 for w in xrange(dst_width)] for h in xrange(dst_height)]

        for h in range(dst_height):
            left = (h/ratioH)*ratioH
            right = (1+h/ratioH)*ratioH
            if h - left <= right -h:
                closestH = left
            else:
                closestH = right
            closestH = min(closestH/ratioH, src_image.height-1)
            for w in range(dst_width):
                up = (w/ratioW)*ratioW
                down = (1+w/ratioW)*ratioW
                if w - up <= down - w:
                    closestW = up
                else:
                    closestW = down
                closestW = min(closestW/ratioW, src_image.width-1)
                dst_pixel[h][w] = src_image.pixel[closestH][closestW]
                if dst_maxV < dst_pixel[h][w]:
                    dst_maxV = dst_pixel[h][w]

        self.__init__(src_image.magic_word,
                      dst_width,
                      dst_height,
                      dst_maxV,
                      dst_pixel)
        self.writeContent(path)

    def zoomBack_Bilinear(self, src_image, dst_width, dst_height, path):
        width = src_image.width
        height = src_image.height
        pixel = src_image.pixel
        ratioW = dst_width / width
        ratioH = dst_height / height
        dst_maxV = 0
        dst_pixel = [[0 for w in xrange(dst_width)] for h in xrange(dst_height)]

        for h in range(dst_height):
            mapH = h / ratioH
            left = int(h / ratioH)
            right = min((1 + int(h / ratioH)), height -1)
            for w in range(dst_width):
                mapW = w / ratioW
                up = int(w / ratioW)
                down = min((1 + int(w / ratioW)), width - 1)
                dst_pixel[h][w] = int(((height - mapH) * (width - mapW) * pixel[left][up] \
                                + (height - mapH) * mapW * pixel[left][down] \
                                + mapH * (width - mapW) * pixel[right][up]  \
                                + mapH * mapW * pixel[right][down]) \
                                / (width * height))
                if dst_maxV < dst_pixel[h][w]:
                    dst_maxV = dst_pixel[h][w]

        self.__init__(src_image.magic_word,
                      dst_width,
                      dst_height,
                      dst_maxV,
                      dst_pixel)
        self.writeContent(path)

    def zoomBack(self, src_image, selection,
                in_width, in_height, in_path,
                out_width, out_height, out_path):
        self.shrink(src_image, in_width, in_height, in_path)

        if selection == enum.ZOOM_REPLIC:
            self.zoomBack_Replic(self, out_width, out_height, out_path)
            pub.sendMessage("RIGHT IMAGE CHANGED", out_path)
        elif selection == enum.ZOOM_NEAR_NGHR:
            self.zoomBack_NearNghr(self, out_width, out_height, out_path)
            pub.sendMessage("RIGHT IMAGE CHANGED", out_path)
        elif selection == enum.ZOOM_BILINEAR:
            self.zoomBack_Bilinear(self, out_width, out_height, out_path)
            pub.sendMessage("RIGHT IMAGE CHANGED", out_path)

    def loadLeft(self, src_image, dst_width, dst_height, path):
        self.shrink(src_image, dst_width, dst_height, path)
        pub.sendMessage("LEFT IMAGE LOADED", path)

    def shrinkRight(self, src_image, dst_width, dst_height, path):
        self.shrink(src_image, dst_width, dst_height, path)
        pub.sendMessage("RIGHT IMAGE CHANGED", path)

