##stat PD-mean
# -*- coding:utf-8 -*-
import os
import pandas
from netCDF4 import Dataset
from pandas import DataFrame
from .datas_listFile import *
from .formulas import *


from metlib.datetime import *

class mean_PD_PM_PY():
    def __init__(self,year,domain,level):
        self.year = year
        self.domain = domain
        self.level = level
        # self.in_dir = "/mnt/data1/huima/extract_data/gw_hunan_1/xy_data"
        # self.out_dir = "/mnt/data1/yeyuguo/program/cargo2"
        self.in_dir = "xy_data"
        self.out_dir = "cargo2"
        get_npy = foreach(self.in_dir,self.domain,self.level,self.year)
        self.get_npy_data = get_npy['data']
        self.get_npy_time = get_npy['times']
        self.jy,self.ix = latlon_data_struct(self.in_dir,domain)['xlon'].shape

    def pdpmpy_mean(self):
        print 'pdpmpy_mean start'
        subsets = ['PD','PM','PY']
        # self.get_npy_data = get_pmpd_data(self.year,self.domain,self.level)
        index_list = np.arange(len(self.get_npy_time))
        varnames = self.get_npy_data.keys()[1:]     #['psfc', 'rhoair', 'wspd', 'wpd', 'td', 'rh']
        for subset in subsets:
            lat = latlon_data_struct(self.in_dir,self.domain)['xlat']
            lon = latlon_data_struct(self.in_dir,self.domain)['xlon']
            jy, ix = lon.shape

            if subset =='PD':
                tags = np.array(['%s__%02d' % (self.year, hour) for hour in range(24)])
            elif subset =='PM':
                tags = np.array(['%s%02d' % (self.year, month) for month in range(1, 13)])
            elif subset =='PY':
                tags = np.array(['%s' % (self.year,)])
            if os.path.exists("%s/%s/mean/%s/%s/%s/"%(self.out_dir,subset,self.year,self.domain,self.level))==False:
                os.makedirs("%s/%s/mean/%s/%s/%s/"%(self.out_dir,subset,self.year,self.domain,self.level))
            out_path = "%s/%s/mean/%s/%s/%s/ALL.nc"%(self.out_dir,subset,self.year,self.domain,self.level)
            nc_file = Dataset(out_path,'w',format='NETCDF4')
            # creat dimensions
            nc_file.createDimension('jy',jy)
            nc_file.createDimension('ix',ix)
            nc_file.createDimension('tag',len(tags))

            # creat variables
            nc_file.createVariable('lat','f8',('jy','ix'))[:] = lat
            nc_file.createVariable('lon','f8',('jy','ix'))[:] = lon
            nc_file.createVariable('tag',str,('tag',))[:] = tags

            for varname in varnames:
                var_data = nc_file.createVariable(varname,'f4',('tag','jy','ix'))
                var_data_std = nc_file.createVariable(varname+"_std",'f4',('tag','jy','ix'))

                if varname == 'wspd':
                    var_data.units = 'm/s'
                    var_data_std.units ='m/s'
                elif varname =='wpd':
                    var_data.units = 'W/m²'
                    var_data_std.units ='W/m²'
                elif varname =='psfc':
                    var_data.units = 'hPa'
                    var_data_std.units ='hPa'
                elif varname =='std':
                    var_data.units = '°C'
                    var_data_std.units ='°C'
                elif varname =='rhoair':
                    var_data.units = 'kg/m³'
                    var_data_std.units ='kg/m³'
                elif varname =='rh':
                    var_data.units = '%'
                    var_data_std.units ='%'

                p_data = self.get_npy_data[varname]
                if subset =='PD':
                    d_splits = split_hour(index_list,self.get_npy_time)
                    p_counts = np.array([np.ma.masked_invalid(d_splits[i]).count() for i in range(var_data.shape[0])])
                    var_data[:] = np.zeros((24,self.jy,self.ix))
                    var_data_std[:] = np.zeros((24,self.jy,self.ix))
                    var_data[:] = np.nan
                    var_data_std[:] = np.nan
                    for d in range(24):
                        d_indice = d_splits[d]
                        var_data[d,:,:] = np.nanmean(p_data[d_indice],axis=0)
                        var_data_std[d,:,:] = np.nanstd(p_data[d_indice],axis=0)
                    # print var_data[:]
                elif subset =='PM':
                    m_splits = split_month(index_list,self.get_npy_time)
                    p_counts = np.array([np.ma.masked_invalid(m_splits[i]).count() for i in range(var_data.shape[0])])
                    var_data[:] = np.zeros((12,self.jy,self.ix))
                    var_data_std[:] = np.zeros((12,self.jy,self.ix))
                    var_data[:] = np.nan
                    var_data_std[:] = np.nan
                    for m in range(12):
                        m_indice = m_splits[m]
                        var_data[m,:,:] = np.nanmean(p_data[m_indice],axis=0)
                        var_data_std[m,:,:] = np.nanstd(p_data[m_indice],axis=0)
                    # print var_data[:]
                elif subset =='PY':
                    p_counts = np.array([len(self.get_npy_time)])
                    var_data[:] = np.zeros((1,self.jy,self.ix))
                    var_data_std[:] = np.zeros((1,self.jy,self.ix))
                    var_data[:] = np.nan
                    var_data_std[:] = np.nan
                    var_data[0,:,:] = np.nanmean(p_data,axis=0)
                    var_data_std[0,:,:] = np.nanstd(p_data,axis=0)
            # print p_counts
            print 'yes'
            nc_file.createVariable('count', 'i8', ('tag', ))[:] = p_counts
            nc_file.dataset = 'china_9km_anl'
            nc_file.subset = subset
            nc_file.varname = 'mean'
            nc_file.domain = '%s' % self.domain
            nc_file.year = '%s' % self.year
            nc_file.level = '%s' % self.level
            # print nc_file.variables['psfc'][:]
            nc_file.close()

    def rose_dist_mean(self):
        print 'start rose_dist'
        rose_path = "%s/PY/rose/%s/%s/%s/ALL.nc"%(self.out_dir,self.year,self.domain,self.level)
        dist_path = "%s/PY/dist/%s/%s/%s/ALL.nc"%(self.out_dir,self.year,self.domain,self.level)

        py_data = self.get_npy_data
        ws = py_data['wspd']
        wd = py_data['wdir']
        counts  = np.array([np.ma.masked_invalid(ws[:, 0, 0]).count()])
        tags = np.array(['%s' % self.year])
        lat = latlon_data_struct(self.in_dir,self.domain)['xlat']
        lon = latlon_data_struct(self.in_dir,self.domain)['xlon']
        jy, ix = lon.shape
        if os.path.exists("%s/PY/rose/%s/%s/%s/"%(self.out_dir,self.year,self.domain,self.level))==False:
            os.makedirs("%s/PY/rose/%s/%s/%s/"%(self.out_dir,self.year,self.domain,self.level))
        if os.path.exists("%s/PY/dist/%s/%s/%s/"%(self.out_dir,self.year,self.domain,self.level))==False:
            os.makedirs("%s/PY/dist/%s/%s/%s/"%(self.out_dir,self.year,self.domain,self.level))
        rose_Dataset = Dataset(rose_path,'w')
        dist_Dataset = Dataset(dist_path,'w')

        for nc_file in (rose_Dataset,dist_Dataset):
            nc_file.createDimension('jy',jy)
            nc_file.createDimension('ix',ix)
            nc_file.createDimension('tag',len(tags))
            nc_file.createDimension('ws',N_WS)
            nc_file.createDimension('wd',N_WD)
            nc_file.createDimension('wdc',N_WDC)

            nc_file.createVariable('lat', 'f8', ('jy', 'ix'))[:] = lat
            nc_file.createVariable('lon', 'f8', ('jy', 'ix'))[:] = lon
            nc_file.createVariable('tag', str, ('tag', ))[:] = tags

            nc_file.createVariable('wsbin', str, ('ws', ))[:] = WSBINSTRS
            nc_file.createVariable('wdbin', 'f8', ('wd', ))[:] = WDBINS
            nc_file.createVariable('count', 'i8', ('tag', ))[:] = counts

            nc_file.dataset = 'china_9km_anl'
            nc_file.subset = 'PY'
            nc_file.domain = '%s' % self.domain
            nc_file.year = '%s' % self.year
            nc_file.level = '%s' % self.level
            nc_file.wsbinnum = N_WS
            nc_file.wdbinnum = N_WD
            nc_file.wdbin0 = WD0
            nc_file.calm_thres = CALM_THRES

        # rose's variables
        rose_data = rose_Dataset.createVariable('rose', 'f4', ('tag', 'jy', 'ix', 'ws', 'wd'))
        rose_data[0,:,:,:] = get_wind_rose_2d(ws, wd, 'permill')
        rose_data.units = 'permill'

        # dist's variables
        wsdist_data = dist_Dataset.createVariable('wsdist', 'f4', ('tag', 'jy', 'ix', 'ws'))
        wddist_data = dist_Dataset.createVariable('wddist', 'f4', ('tag', 'jy', 'ix', 'wd'))
        wdcdist_data = dist_Dataset.createVariable('wdcdist', 'f4', ('tag', 'jy', 'ix', 'wdc'))

        wsdist_data[0, :, :, :] = get_wsdist_2d(ws, 'percent')
        wddist_data[0, :, :, :] = get_wddist_2d(wd, 'percent')
        wdcdist_data[0, :, :, :] = get_wdcdist_2d(wd, ws, 'percent')
        for v in [wsdist_data, wddist_data, wdcdist_data]:
            v.units = 'percent'

        rose_Dataset.varname = 'rose'
        dist_Dataset.varname = 'dist'
        # print rose_Dataset.variables['count'][:]
        rose_Dataset.close()
        dist_Dataset.close()

    def wpdrose_mean(self):
        print 'start wpdrose'
        wpdrose_path = "%s/PY/wpdrose/%s/%s/%s/ALL.nc"%(self.out_dir,self.year,self.domain,self.level)

        # 应该读取年平均值的数据
        # self.get_npy_data = get_pmpd_data(self.year,self.domain,self.level)

        py_data = self.get_npy_data
        ws = py_data['wspd']
        wd = py_data['wdir']
        wpd = py_data['wpd']


        # print 'wd:'
        # print wd[:0,0]
        # print 'wpd:'
        # print wpd[:0,0]
        # print ws[:0,0]


        counts  = np.ma.masked_invalid(ws[:, 0, 0]).count()

        tags = np.array(['%s' % self.year])
        lat = latlon_data_struct(self.in_dir,self.domain)['xlat']
        lon = latlon_data_struct(self.in_dir,self.domain)['xlon']
        jy, ix = lon.shape

        if os.path.exists("%s/PY/wpdrose/%s/%s/%s/"%(self.out_dir,self.year,self.domain,self.level))==False:
            os.makedirs("%s/PY/wpdrose/%s/%s/%s/"%(self.out_dir,self.year,self.domain,self.level))
        nc_file = Dataset(wpdrose_path,'w')


        nc_file.createDimension('jy',jy)
        nc_file.createDimension('ix',ix)
        nc_file.createDimension('tag',len(tags))
        nc_file.createDimension('ws',N_WS)
        nc_file.createDimension('wd',N_WD)

        nc_file.createVariable('lat', 'f8', ('jy', 'ix'))[:] = lat
        nc_file.createVariable('lon', 'f8', ('jy', 'ix'))[:] = lon
        nc_file.createVariable('tag', str, ('tag', ))[:] = tags

        nc_file.createVariable('wsbin', str, ('ws', ))[:] = WSBINSTRS
        nc_file.createVariable('wdbin', 'f8', ('wd', ))[:] = WDBINS
        nc_file.createVariable('count', 'i8', ('tag', ))[0] = counts

        nc_file.dataset = 'china_9km_anl'
        nc_file.subset = 'PY'
        nc_file.domain = '%s' % self.domain
        nc_file.year = '%s' % self.year
        nc_file.level = '%s' % self.level
        nc_file.wsbinnum = N_WS
        nc_file.wdbinnum = N_WD
        nc_file.wdbin0 = WD0
        nc_file.calm_thres = CALM_THRES

        rose_data = nc_file.createVariable('wpdrose', 'f4', ('tag', 'jy', 'ix', 'ws', 'wd'))
        rose_data[0,:,:,:] = get_wpd_rose_2d(ws, wd, wpd)
        # print get_wpd_rose(ws[:, 0, 0], wd[:, 0, 0], wpd[:, 0, 0])
        # print rose_data[0,:,:,:]
        rose_data.units = u'W/m²'
        nc_file.varname = 'wpdrose'
        nc_file.close()

    def hdf5(self):
        print 'start hdf5 .....'
        get_data = self.get_npy_data
        varnames = get_data.keys()
        print varnames
        # x = self.ix
        # y = self.jy
        x = 3
        y = 3
        column = ['wdir_10','wdir_70','wdir_80','wdir_100', 'psfc_10','psfc_70', 'psfc_80','psfc_100','rhoair_10','rhoair_70','rhoair_80','rhoair_100',
                'wspd_10','wspd_70','wspd_80','wspd_100', 'wpd_10','wpd_70','wpd_80','wpd_100', 'td_10','td_70','td_80','td_100', 'rh_10','rh_70','rh_80','rh_100']
        for j in range(y):
            for i in range(x):
                ix = "%03d"%i
                jy = "%03d"%j
                for varname in varnames:
                    if not os.path.exists("%s/PT/ALL/%s/%s/ALL/"%(self.out_dir,self.year,self.domain)):
                        os.makedirs("%s/PT/ALL/%s/%s/ALL/"%(self.out_dir,self.year,self.domain))
                    if os.path.exists("%s/PT/ALL/%s/%s/ALL/%s_%s.h5"%(self.out_dir,self.year,self.domain,jy,ix)):
                        hdf = pandas.HDFStore("%s/PT/ALL/%s/%s/ALL/%s_%s.h5"%(self.out_dir,self.year,self.domain,jy,ix))
                        data = hdf['df']
                    else:
                        hdf = pandas.HDFStore("%s/PT/ALL/%s/%s/ALL/%s_%s.h5"%(self.out_dir,self.year,self.domain,jy,ix))
                        data = DataFrame(columns = column,index = self.get_npy_time)
                        data.index.name='datatime'
                    data.loc[:,varname+"_"+self.level] = self.get_npy_data[varname][:,jy,ix]
                    hdf.put('df',data,format='table')
                    hdf.close()


