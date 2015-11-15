#__author__ = '30213'
# -*- coding:utf-8 -*-
import os
import math
import  numpy as np
# from .formulas import *

def latlon_data_struct(in_dir,domain,latlon_file = 'xlat_xlon.npy'):
        get_latlon =  "%s/d0%s/%s"%(in_dir,domain,latlon_file);
        get_latlon_data = np.load(get_latlon).tolist()
        return get_latlon_data

def read_file(path,name):
    f = file(path+name,"rb")
    fileData = np.load(f).tolist()
    # fileData = np.load(path+name).tolist()
    # print fileData['times']
    f.close()
    return fileData


#get file's all  data  => data.keys() = ['data','times']        data['data'][varname]    data['data'][varname].shape=(n,48,48)
def foreach(path,domain,level):
    print 'foreach start:'
    file_path = "%s/d0%s/%s/"%(path,domain,level)
    varnames = ['wdir', 'psfc', 'rhoair', 'wspd', 'wpd', 'td', 'rh']
    files = os.listdir(file_path)
    all_datas = {}
    all_datas['data'] = {}
    jy,ix = latlon_data_struct(path,domain)['xlon'].shape
    print 'jy:::::::::::::',jy
    count = len(files)*72+7
    for varname in varnames:
        all_datas['times'] = []
        all_datas['data'][varname] = np.zeros((0,jy,ix))
        for fileName in files:
            file_data = read_file(file_path,fileName)
            if fileName != files[-1]:
                for k in range(len(file_data['times'][0:-7])):
                    all_datas['times'].append(file_data['times'][k]);
                timeLen = len(all_datas['times'])
                # all_datas['data'][varname][timeLen-72:timeLen,:,:] = file_data['data'][varname][0:-7,:,:]
                if fileName != files[0]:
                    all_datas['data'][varname] = np.append(all_datas['data'][varname][:,:,:],file_data['data'][varname][0:-7,:,:],axis=0)
                else:
                    all_datas['data'][varname] = np.append(all_datas['data'][varname][:,:,:],file_data['data'][varname][0:-7,:,:],axis=0)
                    # all_datas['data'][varname] = np.delete(all_datas['data'][varname],0,0)
            else:
                for k in range(len(file_data['times'])):
                    all_datas['times'].append(file_data['times'][k]);
                timeLen = len(all_datas['times'])
                # all_datas['data'][varname][-80:-1,:,:] = file_data['data'][varname][:,:,:]
                all_datas['data'][varname] = np.append(all_datas['data'][varname][:,:,:],file_data['data'][varname][:,:,:],axis=0)
        if varname == varnames[-1]:
            return all_datas


# data's type is data[varname][time] = >  shape = (48,48)
def get_dict_data(path,domain,level):
    get_data = foreach(path,domain,level)
    varnames = get_data['data'].keys()
    # print len(get_data['times'])
    new_data = {}
    for varname in varnames:
        new_data[varname] = {}
        for i in get_data['times']:
            new_data[varname][i] = get_data['data'][varname][get_data['times'].index(i),:,:]
    # print new_data['wspd'].keys()
    # print new_data['wdir']['20140220140000']
    saveFile = '%s/d0%s/%s/%s_%s.npy'%(path,domain,level,domain,level)
    np.save(saveFile,new_data)
    # return new_data

#get py pm pd's data     data[varname].keys() = 'pd','pm','py'     data[varname]['pd'][n] => type=list  (n=24,12,1) py=> 2010,2011,2012,2014
def get_pmpd_data(path,year,domain,level):
    saveFile = '%s/d0%s/%s/%s_%s.npy'%(path,domain,level,domain,level)
    # jy = meanClass.latlon_data_struct()['xlat']
    # ix = meanClass.latlon_data_struct()['xlon']
    if os.path.isfile(saveFile) == False:
        get_dict_data(path,domain,level)
    dict_data = np.load(saveFile).tolist()
    varnames = dict_data.keys()
    py_pd_data = {}
    year = int(year)
    jy,ix = latlon_data_struct(path,domain)['xlon'].shape
    for varname in varnames:
        py_pd_data[varname] = []
        py_pd_data[varname] = np.zeros((12,31,24,jy,ix))
        py_pd_data[varname][:] = np.nan
        for time in dict_data[varname].keys():
            #pd
            if time[0:4] =="%04d"%year :
                for m in range(1,13):
                    if "%02d"%m == time[4:6]:
                        for d in range(1,31):
                            if "%02d"%d == time[6:8]:
                                for h in range(0,24):
                                    if "%02d"%h == time[8:10]:
                                        m = m-1
                                        d = d-1
                                        py_pd_data[varname][m,d,h,:,:] = dict_data[varname][time]
            else:
                pass
        if varname == varnames[-1]:
            return  py_pd_data

# if __name__ == "__main__":
#     get_dict_data(path='xy_data',year='2013',domain='3',level='70')

