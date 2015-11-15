#__author__ = '30213'
# -*- coding:utf-8 -*-
import os
import math
import numpy as np

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
def foreach(path,domain,level,year):
    saveFile = '%s/d0%s/%s/%s_%s_%s.npy'%(path,domain,level,year,domain,level)
    print saveFile
    if os.path.exists(saveFile):
        return np.load(saveFile).tolist()
    else:
        file_path = "%s/d0%s/%s/"%(path,domain,level)
        varnames = ['wdir', 'psfc', 'rhoair', 'wspd', 'wpd', 'td', 'rh']
        all_file = os.listdir(file_path)
        files = []
        for x in all_file:
            if x[0:4] == year:
                files.append(x)
        all_datas = {}
        all_datas['data'] = {}
        jy,ix = latlon_data_struct(path,domain)['xlon'].shape
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
                # return all_datas
                np.save(saveFile,all_datas)
                return all_datas




