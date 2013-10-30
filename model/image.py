'''
@author: Anakin
'''

import enum
import math

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

    def genSquareMask(self, width, height, h, w, pixel, sft):
        square_mask = []
        for i in range(-sft, sft+1):
            for j in range(-sft, sft+1):
                x = h + i
                y = w + j
                if x < 0: x = 0
                if x >= height: x = height - 1
                if y < 0: y = 0
                if y >= width: y = width - 1
                square_mask.append(pixel[x][y])
        return square_mask

    def probability_count(self, width, height, pixel):
        prob = [0 for w in range(255)]
        for h in range(height):
            for w in range(width):
                prob[pixel[h][w]] += 1
        return prob

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

    def reduceGrayLevel_Least(self, src_image, gray_lvl, path):
        src_pixel = src_image.pixel
        dst_width = src_image.width
        dst_height = src_image.height
        dst_maxV = 0
        dst_pixel = [[0 for w in xrange(dst_width)] for h in xrange(dst_height)]

        for h in range(dst_height):
            for w in range(dst_width):
                dst_pixel[h][w] = src_pixel[h][w] >> (8 - gray_lvl)
                if dst_maxV < dst_pixel[h][w]:
                    dst_maxV = dst_pixel[h][w]

        self.__init__(src_image.magic_word,
                      dst_width,
                      dst_height,
                      dst_maxV,
                      dst_pixel)
        self.writeContent(path)

    def reduceGrayLevel_Most(self, src_image, gray_lvl, path):
        src_pixel = src_image.pixel
        dst_width = src_image.width
        dst_height = src_image.height
        dst_maxV = 0
        dst_pixel = [[0 for w in xrange(dst_width)] for h in xrange(dst_height)]

        for h in range(dst_height):
            for w in range(dst_width):
                dst_pixel[h][w] = src_pixel[h][w] & (1 << gray_lvl)
                if dst_maxV < dst_pixel[h][w]:
                    dst_maxV = dst_pixel[h][w]

        self.__init__(src_image.magic_word,
                      dst_width,
                      dst_height,
                      dst_maxV,
                      dst_pixel)
        self.writeContent(path)

    def transform_Log(self, src_image, c, path):
        src_pixel = src_image.pixel
        dst_width = src_image.width
        dst_height = src_image.height
        dst_maxV = 0
        dst_pixel = [[0 for w in xrange(dst_width)] for h in xrange(dst_height)]

        for h in range(dst_height):
            for w in range(dst_width):
                dst_pixel[h][w] = int(c * math.log(1 + src_pixel[h][w], 2) * 255 / math.log(256, 2))
                if dst_maxV < dst_pixel[h][w]:
                    dst_maxV = dst_pixel[h][w]

        self.__init__(src_image.magic_word,
                      dst_width,
                      dst_height,
                      dst_maxV,
                      dst_pixel)
        self.writeContent(path)

    def transform_Pow(self, src_image, c, gamma, path):
        src_pixel = src_image.pixel
        dst_width = src_image.width
        dst_height = src_image.height
        dst_maxV = 0
        dst_pixel = [[0 for w in xrange(dst_width)] for h in xrange(dst_height)]

        for h in range(dst_height):
            for w in range(dst_width):
                dst_pixel[h][w] = int(c * math.pow(src_pixel[h][w], gamma) * 255 / math.pow(255, gamma))
                if dst_maxV < dst_pixel[h][w]:
                    dst_maxV = dst_pixel[h][w]

        self.__init__(src_image.magic_word,
                      dst_width,
                      dst_height,
                      dst_maxV,
                      dst_pixel)
        self.writeContent(path)

    def histogramEQ_Global(self, src_image, path):
        pixel = src_image.pixel
        dst_width = src_image.width
        dst_height = src_image.height
        dst_maxV = 0
        prob = self.probability_count(dst_width, dst_height, pixel)
        dst_pixel = [[0 for w in xrange(dst_width)] for h in xrange(dst_height)]

        num_pixel = dst_width * dst_height
        hist = [0 for w in range(255)]
        sumH = 0
        for x in range(255):
            sumH += prob[x]
            hist[x] = int((sumH * 254 + 0.5) / num_pixel)
        for h in range(dst_height):
            for w in range(dst_width):
                dst_pixel[h][w] = hist[pixel[h][w]]
                if dst_maxV < dst_pixel[h][w]:
                    dst_maxV = dst_pixel[h][w]

        self.__init__(src_image.magic_word,
                      dst_width,
                      dst_height,
                      dst_maxV,
                      dst_pixel)
        self.writeContent(path)

    def histogramEQ_Local(self, src_image, resolution, path):
        sft = resolution / 2
        pixel = src_image.pixel
        dst_width = src_image.width
        dst_height = src_image.height
        dst_maxV = 0
        prob = self.probability_count(dst_width, dst_height, pixel)
        dst_pixel = [[0 for w in xrange(dst_width)] for h in xrange(dst_height)]

        num_pixel = (2*sft+1) * (2*sft+1)
        for h in range(dst_height):
            for w in range(dst_width):
                square_mask = self.genSquareMask(dst_width, dst_height, h, w, pixel, sft)
                prob = [0 for x in range(255)]
                for x in range(len(square_mask)):
                    prob[square_mask[x]] += 1
                hist = []
                hist_prob = []
                hist_final = []
                m = 0
                for x in range(255):
                    if prob[x] != 0:
                        hist.append(x)
                        hist_prob.append(prob[x])
                        m += 1
                sumH = 0
                for x in range(m):
                    sumH += hist_prob[x]
                    hist_final.append(int((sumH * 254 + 0.5) / num_pixel))

                for x in range(m):
                    if hist[x] == pixel[h][w]:
                        dst_pixel[h][w] = hist_final[x]
                        if dst_maxV < dst_pixel[h][w]:
                            dst_maxV = dst_pixel[h][w]

        self.__init__(src_image.magic_word,
                      dst_width,
                      dst_height,
                      dst_maxV,
                      dst_pixel)
        self.writeContent(path)

    def spatialFilter_Smooth(self, src_image, resolution, path):
        sft = int(resolution / 2)
        dst_width = src_image.width
        dst_height = src_image.height
        dst_maxV = 0
        dst_pixel = [[0 for w in xrange(dst_width)] for h in xrange(dst_height)]

        for h in range(dst_height):
            for w in range(dst_width):
                square_mask = self.genSquareMask(dst_width,
                                                 dst_height,
                                                 h, w,
                                                 src_image.pixel, sft)
                pixel_value = 0
                for x in square_mask:
                    pixel_value += x
                pixel_value /= len(square_mask)
                dst_pixel[h][w] = pixel_value
                if dst_maxV < pixel_value: dst_maxV = pixel_value

        self.__init__(src_image.magic_word,
                      dst_width,
                      dst_height,
                      dst_maxV,
                      dst_pixel)
        self.writeContent(path)

    def spatialFilter_Median(self, src_image, resolution, path):
        sft = int(resolution / 2)
        dst_width = src_image.width
        dst_height = src_image.height
        dst_maxV = 0
        dst_pixel = [[0 for w in xrange(dst_width)] for h in xrange(dst_height)]

        for h in range(dst_height):
            for w in range(dst_width):
                square_mask = self.genSquareMask(dst_width,
                                                 dst_height,
                                                 h, w,
                                                 src_image.pixel, sft)
                sorted_square_mask = sorted(square_mask)
                pixel_value = sorted_square_mask[int(len(square_mask)/2)]
                dst_pixel[h][w] = pixel_value
                if dst_maxV < pixel_value: dst_maxV = pixel_value

        self.__init__(src_image.magic_word,
                      dst_width,
                      dst_height,
                      dst_maxV,
                      dst_pixel)
        self.writeContent(path)

    def spatialFilter_Laplacian(self, src_image, resolution, path):
        sft = int(resolution / 2)
        dst_width = src_image.width
        dst_height = src_image.height
        dst_maxV = 0
        dst_pixel = [[0 for w in xrange(dst_width)] for h in xrange(dst_height)]

        lap1 = [0, 1, 0,
                1,-4, 1,
                0, 1, 0]
        lap2 = [1, 1, 1,
                1,-8, 1,
                1, 1, 1]
        lap3 = [0,-1, 0,
                -1,4,-1,
                0,-1, 0]
        lap4 = [-1,-1,-1,
                -1, 8,-1,
                -1,-1,-1]

        for h in range(dst_height):
            for w in range(dst_width):
                square_mask = self.genSquareMask(dst_width,
                                                 dst_height,
                                                 h, w,
                                                 src_image.pixel, sft)
                pixel_value = 0
                for x in range(len(square_mask)):
                    pixel_value += lap4[x] * square_mask[x]
                dst_pixel[h][w] = pixel_value
                if dst_maxV < pixel_value: dst_maxV = pixel_value

        self.__init__(src_image.magic_word,
                      dst_width,
                      dst_height,
                      dst_maxV,
                      dst_pixel)
        self.writeContent(path)

    def spatialFilter_HighBoost(self, src_image, resolution, path):
        sft = int(resolution / 2)
        dst_width = src_image.width
        dst_height = src_image.height
        dst_maxV = 0
        dst_pixel = [[0 for w in xrange(dst_width)] for h in xrange(dst_height)]

        gaussian = [1, 2, 1,
                    2, 4, 2,
                    1, 2, 1]
        k = 2

        for h in range(dst_height):
            for w in range(dst_width):
                square_mask = self.genSquareMask(dst_width,
                                                 dst_height,
                                                 h, w,
                                                 src_image.pixel, sft)
                pixel_value = 0
                for x in range(len(square_mask)):
                    pixel_value += gaussian[x] * square_mask[x]
                pixel_value /= 16
                dst_pixel[h][w] = src_image.pixel[h][w] * (k + 1) - k * pixel_value
                if dst_maxV < dst_pixel[h][w]: dst_maxV = dst_pixel[h][w]

        self.__init__(src_image.magic_word,
                      dst_width,
                      dst_height,
                      dst_maxV,
                      dst_pixel)
        self.writeContent(path)

    def restoreImage_Arithmetic(self, src_image, resolution, path):
        sft = int(resolution / 2)
        dst_width = src_image.width
        dst_height = src_image.height
        dst_maxV = 0
        dst_pixel = [[0 for w in xrange(dst_width)] for h in xrange(dst_height)]

        for h in range(dst_height):
            for w in range(dst_width):
                square_mask = self.genSquareMask(dst_width,
                                                 dst_height,
                                                 h, w,
                                                 src_image.pixel, sft)
                pixel_value = 0
                for x in square_mask:
                    pixel_value += x
                pixel_value /= len(square_mask)
                dst_pixel[h][w] = pixel_value
                if dst_maxV < pixel_value: dst_maxV = pixel_value

        self.__init__(src_image.magic_word,
                      dst_width,
                      dst_height,
                      dst_maxV,
                      dst_pixel)
        self.writeContent(path)

    def restoreImage_Geometric(self, src_image, resolution, path):
        sft = int(resolution / 2)
        dst_width = src_image.width
        dst_height = src_image.height
        dst_maxV = 0
        dst_pixel = [[0 for w in xrange(dst_width)] for h in xrange(dst_height)]

        for h in range(dst_height):
            for w in range(dst_width):
                square_mask = self.genSquareMask(dst_width,
                                                 dst_height,
                                                 h, w,
                                                 src_image.pixel, sft)
                pixel_value = 1
                for x in square_mask:
                    pixel_value *= x
                pixel_value = int(math.pow(pixel_value, float(1) / (resolution * resolution)))
                dst_pixel[h][w] = pixel_value
                if dst_maxV < pixel_value: dst_maxV = pixel_value

        self.__init__(src_image.magic_word,
                      dst_width,
                      dst_height,
                      dst_maxV,
                      dst_pixel)
        self.writeContent(path)

    def restoreImage_Harmonic(self, src_image, resolution, path):
        sft = int(resolution / 2)
        dst_width = src_image.width
        dst_height = src_image.height
        dst_maxV = 0
        dst_pixel = [[0 for w in xrange(dst_width)] for h in xrange(dst_height)]

        for h in range(dst_height):
            for w in range(dst_width):
                square_mask = self.genSquareMask(dst_width,
                                                 dst_height,
                                                 h, w,
                                                 src_image.pixel, sft)
                pixel_value = 0
                for x in square_mask:
                    pixel_value += float(1) / x
                pixel_value = (resolution * resolution) / pixel_value
                dst_pixel[h][w] = pixel_value
                if dst_maxV < pixel_value: dst_maxV = pixel_value

        self.__init__(src_image.magic_word,
                      dst_width,
                      dst_height,
                      dst_maxV,
                      dst_pixel)
        self.writeContent(path)

    def restoreImage_ContraHarmonic(self, src_image, resolution, path):
        sft = int(resolution / 2)
        dst_width = src_image.width
        dst_height = src_image.height
        dst_maxV = 0
        dst_pixel = [[0 for w in xrange(dst_width)] for h in xrange(dst_height)]

        q = 1

        for h in range(dst_height):
            for w in range(dst_width):
                square_mask = self.genSquareMask(dst_width,
                                                 dst_height,
                                                 h, w,
                                                 src_image.pixel, sft)
                numerator = 0
                denominator = 0
                for x in square_mask:
                    numerator += math.pow(x, q+1)
                    denominator += math.pow(x, q)
                pixel_value = numerator / denominator
                dst_pixel[h][w] = pixel_value
                if dst_maxV < pixel_value: dst_maxV = pixel_value

        self.__init__(src_image.magic_word,
                      dst_width,
                      dst_height,
                      dst_maxV,
                      dst_pixel)
        self.writeContent(path)

    def restoreImage_Max(self, src_image, resolution, path):
        sft = int(resolution / 2)
        dst_width = src_image.width
        dst_height = src_image.height
        dst_maxV = 0
        dst_pixel = [[0 for w in xrange(dst_width)] for h in xrange(dst_height)]

        for h in range(dst_height):
            for w in range(dst_width):
                square_mask = self.genSquareMask(dst_width,
                                                 dst_height,
                                                 h, w,
                                                 src_image.pixel, sft)
                sorted_square_mask = sorted(square_mask)
                pixel_value = sorted_square_mask[len(sorted_square_mask)-1]
                dst_pixel[h][w] = pixel_value
                if dst_maxV < pixel_value: dst_maxV = pixel_value

        self.__init__(src_image.magic_word,
                      dst_width,
                      dst_height,
                      dst_maxV,
                      dst_pixel)
        self.writeContent(path)

    def restoreImage_Min(self, src_image, resolution, path):
        sft = int(resolution / 2)
        dst_width = src_image.width
        dst_height = src_image.height
        dst_maxV = 0
        dst_pixel = [[0 for w in xrange(dst_width)] for h in xrange(dst_height)]

        for h in range(dst_height):
            for w in range(dst_width):
                square_mask = self.genSquareMask(dst_width,
                                                 dst_height,
                                                 h, w,
                                                 src_image.pixel, sft)
                sorted_square_mask = sorted(square_mask)
                pixel_value = sorted_square_mask[0]
                dst_pixel[h][w] = pixel_value
                if dst_maxV < pixel_value: dst_maxV = pixel_value

        self.__init__(src_image.magic_word,
                      dst_width,
                      dst_height,
                      dst_maxV,
                      dst_pixel)
        self.writeContent(path)

    def restoreImage_Midpoint(self, src_image, resolution, path):
        sft = int(resolution / 2)
        dst_width = src_image.width
        dst_height = src_image.height
        dst_maxV = 0
        dst_pixel = [[0 for w in xrange(dst_width)] for h in xrange(dst_height)]

        for h in range(dst_height):
            for w in range(dst_width):
                square_mask = self.genSquareMask(dst_width,
                                                 dst_height,
                                                 h, w,
                                                 src_image.pixel, sft)
                sorted_square_mask = sorted(square_mask)
                pixel_value = (sorted_square_mask[0]
                            + sorted_square_mask[len(sorted_square_mask)-1]) / 2
                dst_pixel[h][w] = pixel_value
                if dst_maxV < pixel_value: dst_maxV = pixel_value

        self.__init__(src_image.magic_word,
                      dst_width,
                      dst_height,
                      dst_maxV,
                      dst_pixel)
        self.writeContent(path)

    def restoreImage_AlphaTrim(self, src_image, resolution, path):
        sft = int(resolution / 2)
        dst_width = src_image.width
        dst_height = src_image.height
        dst_maxV = 0
        dst_pixel = [[0 for w in xrange(dst_width)] for h in xrange(dst_height)]

        d = 2

        for h in range(dst_height):
            for w in range(dst_width):
                square_mask = self.genSquareMask(dst_width,
                                                 dst_height,
                                                 h, w,
                                                 src_image.pixel, sft)
                sorted_square_mask = sorted(square_mask)
                pixel_value = 0
                for x in range(d/2, len(sorted_square_mask)-d/2):
                    pixel_value += sorted_square_mask[x]
                pixel_value /= len(sorted_square_mask) - d
                dst_pixel[h][w] = pixel_value
                if dst_maxV < pixel_value: dst_maxV = pixel_value

        self.__init__(src_image.magic_word,
                      dst_width,
                      dst_height,
                      dst_maxV,
                      dst_pixel)
        self.writeContent(path)

    def restoreImage(self, src_image, selection, resolution, path):
        if selection == enum.RESTORE_ARITHMETIC:
            self.restoreImage_Arithmetic(src_image, resolution, path)
            pub.sendMessage("RIGHT IMAGE CHANGED", path)
        elif selection == enum.RESTORE_GEOMETRIC:
            self.restoreImage_Geometric(src_image, resolution, path)
            pub.sendMessage("RIGHT IMAGE CHANGED", path)
        elif selection == enum.RESTORE_HARMONIC:
            self.restoreImage_Harmonic(src_image, resolution, path)
            pub.sendMessage("RIGHT IMAGE CHANGED", path)
        elif selection == enum.RESTORE_CONTRAHARM:
            self.restoreImage_ContraHarmonic(src_image, resolution, path)
            pub.sendMessage("RIGHT IMAGE CHANGED", path)
        elif selection == enum.RESTORE_MAX:
            self.restoreImage_Max(src_image, resolution, path)
            pub.sendMessage("RIGHT IMAGE CHANGED", path)
        elif selection == enum.RESTORE_MIN:
            self.restoreImage_Min(src_image, resolution, path)
            pub.sendMessage("RIGHT IMAGE CHANGED", path)
        elif selection == enum.RESTORE_MIDPOINT:
            self.restoreImage_Midpoint(src_image, resolution, path)
            pub.sendMessage("RIGHT IMAGE CHANGED", path)
        elif selection == enum.RESTORE_ALPHA_TRIM:
            self.restoreImage_AlphaTrim(src_image, resolution, path)
            pub.sendMessage("RIGHT IMAGE CHANGED", path)

    def bitPlane(self, src_image, bits, path):
        dst_width = src_image.width
        dst_height = src_image.height
        dst_maxV = 0
        dst_pixel = [[0 for w in xrange(dst_width)] for h in xrange(dst_height)]

        for h in range(dst_height):
            for w in range(dst_width):
                dst_pixel[h][w] = src_image.pixel[h][w] & bits
                if dst_maxV < dst_pixel[h][w]: dst_maxV = dst_pixel[h][w]

        self.__init__(src_image.magic_word,
                      dst_width,
                      dst_height,
                      dst_maxV,
                      dst_pixel)
        self.writeContent(path)
        pub.sendMessage("RIGHT IMAGE CHANGED", path)


    def spatialFilter(self, src_image, selection, resolution, path):
        if selection == enum.SP_FLT_SMOOTH:
            self.spatialFilter_Smooth(src_image, resolution, path)
            pub.sendMessage("RIGHT IMAGE CHANGED", path)
        elif selection == enum.SP_FLT_MEDIAN:
            self.spatialFilter_Median(src_image, resolution, path)
            pub.sendMessage("RIGHT IMAGE CHANGED", path)
        elif selection == enum.SP_FLT_LAPLACIAN:
            self.spatialFilter_Laplacian(src_image, 3, path)
            pub.sendMessage("RIGHT IMAGE CHANGED", path)
        elif selection == enum.SP_FLT_H_BOOST:
            self.spatialFilter_HighBoost(src_image, 3, path)
            pub.sendMessage("RIGHT IMAGE CHANGED", path)

    def histogramEQ(self, src_image, selection, resolution, path):
        if selection == enum.HIST_EQ_GLOBAL:
            self.histogramEQ_Global(src_image, path)
            pub.sendMessage("RIGHT IMAGE CHANGED", path)
        elif selection == enum.HIST_EQ_LOCAL:
            self.histogramEQ_Local(src_image, resolution, path)
            pub.sendMessage("RIGHT IMAGE CHANGED", path)

    def transform(self, src_image, selection, c, gamma, path):
        print("transform")
        if selection == enum.TRANS_LOG:
            self.transform_Log(src_image, c, path)
            pub.sendMessage("RIGHT IMAGE CHANGED", path)
        elif selection == enum.TRANS_POW:
            self.transform_Pow(src_image, c, gamma, path)
            pub.sendMessage("RIGHT IMAGE CHANGED", path)

    def reduceGrayLevel(self, src_image, gray_lvl, sgn, path):
        print("reduceGrayLevel: %s GL: %d" % (sgn, gray_lvl))
        if sgn == enum.REDUCE_GL_LEAST:
            self.reduceGrayLevel_Least(src_image, gray_lvl, path)
            pub.sendMessage("RIGHT IMAGE CHANGED", path)
        elif sgn == enum.REDUCE_GL_MOST:
            self.reduceGrayLevel_Most(src_image, gray_lvl, path)
            pub.sendMessage("RIGHT IMAGE CHANGED", path)

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

    def shrinkRight(self, src_image, dst_width, dst_height, path):
        self.shrink(src_image, dst_width, dst_height, path)
        pub.sendMessage("RIGHT IMAGE CHANGED", path)

    def loadLeft(self, src_image, dst_width, dst_height, path):
        self.shrink(src_image, dst_width, dst_height, path)
        pub.sendMessage("LEFT IMAGE LOADED", path)

