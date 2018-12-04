import numpy as np
import imageio
import scipy.ndimage


np.seterr(divide='ignore', invalid='ignore')

def grayscale(rgb):
    return np.dot(rgb[...,:3], [0.299, 0.587, 0.114])

def dodge(front,back):
    result=front*255/(255-back)
    result[result>255]=255
    result[back==255]=255
    return result.astype('uint8')

def convert(image):
    s = imageio.imread(image)
    g = grayscale(s)
    i = 255-g
    b = scipy.ndimage.filters.gaussian_filter(i,sigma=5)
    r = dodge(b,g)
    return r
