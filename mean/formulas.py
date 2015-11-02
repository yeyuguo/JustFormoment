# -*- coding:utf-8 -*-
from scipy.special import gamma
from dist_parameter import *


def calc_wpd(ws, rhoair=1.125):
    return 0.5 * rhoair * ws * ws * ws

def return_as_needed(count, total_count, return_type='percent'):
    if return_type == 'count':
        return count
    else:
        ratio = count / float(total_count)
        if return_type == 'ratio':
            return ratio
        elif return_type == 'permill':
            return ratio * 1000.0
        else:
            return ratio * 100.0


def get_wind_rose(ws, wd, return_type='percent'):
    """
    :param ws: 1维的风速数组
    :param wd: 1维的风向数组
    :param return_type: 返回类型: 'count': 数量 'ratio': 小数值, 'percent': 百分比, 'permill': 千分比
    :return:
    """
    stacker = np.zeros((len(ws), N_WS, N_WD), dtype='i4')
    ws_binned = ws2wsbin(ws)
    wd_binned = wd2wdbin(wd)
    stacker[(np.arange(len(ws)), ws_binned, wd_binned)] = 1
    stacker[np.where(ws_binned<0)] = 0  # 对付掉nan导致的ws_binned中的负值
    squeezed = np.sum(stacker, axis=0)

    return return_as_needed(squeezed, np.ma.masked_invalid(ws).count(), return_type=return_type)


def get_wind_rose_2d(ws, wd, return_type='percent'):
    res_dtype = 'i4' if return_type == 'count' else 'f4'
    N_JY = ws.shape[1]
    N_IX = ws.shape[2]
    res_array = np.zeros((N_JY, N_IX, N_WS, N_WD), dtype=res_dtype)
    for jy, ix in np.ndindex(N_JY, N_IX):
        res_array[jy, ix] = get_wind_rose(ws[:, jy, ix], wd[:, jy, ix], return_type=return_type)
    return res_array


def get_wpd_rose(ws, wd, wpd=None, rhoair=1.125):
    stacker = np.zeros((len(ws), N_WS, N_WD), dtype='f8')
    if wpd is None:
        wpd = calc_wpd(ws, rhoair=rhoair)
    ws_binned = ws2wsbin(ws)
    wd_binned = wd2wdbin(wd)
    stacker[(np.arange(len(ws)), ws_binned, wd_binned)] = 1.0
    stacker[np.where(ws_binned<0)] = 0
    stacker *= wpd[:, np.newaxis, np.newaxis]
    res = np.nansum(stacker, axis=0)
    return res


def get_wpd_rose_2d(ws, wd, wpd=None, rhoair=1.125):
    N_JY = ws.shape[1]
    N_IX = ws.shape[2]
    res_array = np.zeros((N_JY, N_IX, N_WS, N_WD), dtype='f4')
    for jy, ix in np.ndindex(N_JY, N_IX):
        if wpd is None:
            wpd_one = None
        else:
            wpd_one = wpd[:, jy, ix]
        # todo: handle rhoair array
        res_array[jy, ix] = get_wpd_rose(ws[:, jy, ix], wd[:, jy, ix], wpd=wpd_one, rhoair=rhoair)
    return res_array


def get_wsdist(ws, return_type='percent'):
    stacker = np.zeros((len(ws), N_WS), dtype='i4')
    ws_binned = ws2wsbin(ws)
    stacker[(np.arange(len(ws)), ws_binned)] = 1
    stacker[np.where(ws_binned<0)] = 0
    squeezed = np.sum(stacker, axis=0)
    return return_as_needed(squeezed, np.ma.masked_invalid(ws).count(), return_type=return_type)

def get_wsdist_2d(ws, return_type='percent'):
    N_JY = ws.shape[1]
    N_IX = ws.shape[2]
    res_array = np.zeros((N_JY, N_IX, N_WS), dtype='f4')
    for jy, ix in np.ndindex(N_JY, N_IX):
        res_array[jy, ix] = get_wsdist(ws[:, jy, ix], return_type=return_type)
    return res_array

def get_wddist(wd, return_type='percent'):
    stacker = np.zeros((len(wd), N_WD), dtype='i4')
    wd_binned = wd2wdbin(wd)
    stacker[(np.arange(len(wd)), wd_binned)] = 1
    stacker[np.where(~np.isfinite(wd))] = 0
    squeezed = np.sum(stacker, axis=0)
    return return_as_needed(squeezed, np.ma.masked_invalid(wd).count(), return_type=return_type)

def get_wddist_2d(wd, return_type='percent'):
    N_JY = wd.shape[1]
    N_IX = wd.shape[2]
    res_array = np.zeros((N_JY, N_IX, N_WD), dtype='f4')
    for jy, ix in np.ndindex(N_JY, N_IX):
        res_array[jy, ix] = get_wddist(wd[:, jy, ix], return_type=return_type)
    return res_array

def get_wdcdist(wd, ws, return_type='percent'):
    w_calm = np.where(ws < CALM_THRES)
    w_active = np.where(~(ws < CALM_THRES))  # 把nan归到这一类里, 让get_wddist处理
    wd_active = wd[w_active]
    wddist_count = get_wddist(wd_active, return_type='count')
    calm_count = len(w_calm[0])
    wdcdist_count = np.zeros(N_WDC, 'i4')
    wdcdist_count[:N_WD] = wddist_count
    wdcdist_count[-1] = calm_count
    return return_as_needed(wdcdist_count, np.ma.masked_invalid(wd).count(), return_type=return_type)

def get_wdcdist_2d(wd, ws, return_type='percent'):
    N_JY = wd.shape[1]
    N_IX = wd.shape[2]
    res_array = np.zeros((N_JY, N_IX, N_WDC), dtype='f4')
    for jy, ix in np.ndindex(N_JY, N_IX):
        res_array[jy, ix] = get_wdcdist(wd[:, jy, ix], ws[:, jy, ix], return_type=return_type)
    return res_array

def get_ak_gamma(wsdist, dist_type='percent'):
    """
    由王瑞明提供的方法
    :param wsdist:
    :param dist_type:
    :return:
    """
    if dist_type == 'raw':
        ws = wsdist
        ws = np.ma.masked_invalid(ws)
        k = (ws.std() / ws.mean()) ** -1.086
        a = ((ws*ws*ws).mean() / gamma(3.0 / k + 1.0)) ** (1.0/3)
    else:
        if dist_type == 'count':
            wsdist_ratio = wsdist / float(wsdist.sum())
        elif dist_type == 'percent':
            wsdist_ratio = wsdist / 100.0
        elif dist_type == 'permill':
            wsdist_ratio = wsdist / 1000.0
        else:
            wsdist_ratio = wsdist
        WSBINS_0 = np.concatenate(([0.0], WSBINS))
        wsmid = (WSBINS_0[:-1] + WSBINS_0[1:]) / 2.0
        ws_mean = np.sum(wsdist_ratio * wsmid)
        ws_std = np.sqrt(np.sum(wsdist_ratio * np.square(wsmid - ws_mean)))
        ws3_mean = np.sum(wsdist_ratio * wsmid * wsmid * wsmid)
        k = (ws_std / ws_mean) ** -1.086
        a = (ws3_mean / gamma(3.0 / k + 1.0)) ** (1.0/3)
    return a, k

