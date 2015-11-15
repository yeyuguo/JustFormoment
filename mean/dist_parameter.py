# -*- coding:utf-8 -*-

import numpy as np

WSBINS = np.arange(1.0, 50.1, 1.0, dtype='f4')   # 风速段
WSBINSTRS = np.array(['%g' % v for v in WSBINS])  # 字符串表示的风速段
N_WD = 16   # 风向扇区数
WD0 = 0.0   # 第一个风向扇区的中心角度
CALM_THRES = 0.3  # 静风风速阈值 (m/s)
N_WS = len(WSBINS)   # 风速段数
N_WDC = N_WD + 1    # 风向扇区数(带上静风)
WDBINS = np.fmod((np.arange(N_WD) * (360.0 / N_WD) + WD0), 360.0)  # (风向扇区)

# 将风速数组的值转换为在风速段中的下标
# 该函数需要随WSBINS的不同而手动修改, 以实现高效的转换
def ws2wsbin(ws):
    res = ws.astype('i4')
    res[res>49] = 49
    res[res<0] = -1
    return res

def wd2wdbin(wd):
    binsize = 360.0 / N_WD
    offsetted_wd = wd + binsize/2.0 - WD0 + 360.0  # TODO 检查 WD0 是否合理
    return np.array(offsetted_wd / binsize).astype('i4') % N_WD



