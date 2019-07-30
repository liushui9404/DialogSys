# coding:utf-8
import numpy as np
import matplotlib.pylab as plt
from PIL import Image

im = Image.open('./test.png')
L = im.convert('L')
a = np.asarray(L)
