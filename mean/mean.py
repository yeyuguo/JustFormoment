##stat PD-mean
# -*- coding:utf-8 -*-
from netCDF4 import Dataset
import pandas
from pandas import DataFrame
from .datas_listFile import *
from .formulas import *
import os

# year = '2013'
# domain = '3'
# level = '10'

class mean_PD_PM_PY():
    def __init__(self,year,domain,level):
        self.year = year
        self.domain = domain
        self.level = level
        # self.in_dir = "/mnt/data1/huima/extract_data/gw_hunan_1/xy_data"
        # self.out_dir = "/mnt/data1/yeyuguo/program/cargo2"
        self.in_dir = "xy_data"
        self.out_dir = "cargo2"
        self.get_npy_data = get_pmpd_data(self.in_dir,self.year,self.domain,self.level)
        self.jy,self.ix = latlon_data_struct(self.in_dir,domain)['xlon'].shape


    # def latlon_data_struct(self,latlon_file = 'xlat_xlon.npy'):
    #     get_latlon =  "%s/d0%s/%s"%(self.in_dir,self.domain,latlon_file);
    #     get_latlon_data = np.load(get_latlon).tolist()
    #     return get_latlon_data


    #return data.shape=(12*31*24,48,48)
    def handle_py(self):
        crude_data = self.get_npy_data
        varnames = crude_data.keys()
        py_data = {}
        for varname in varnames:
            py_data[varname] = crude_data[varname].reshape(-1,self.jy,self.ix);
        return py_data

    def pdpmpy_mean(self):
        print 'pdpmpy_mean start'
        subsets = ['PD','PM','PY']
        # self.get_npy_data = get_pmpd_data(self.year,self.domain,self.level)

        pd_data = {}
        pm_data = {}
        py_data = {}

        for subset in subsets:
            varnames = self.get_npy_data.keys()
            lat = latlon_data_struct(self.in_dir,self.domain)['xlat']
            lon = latlon_data_struct(self.in_dir,self.domain)['xlon']
            jy, ix = lon.shape

            # pd_counts = []
            # pm_counts = []
            # for i in range(0,24):
            #     pd_counts_data = self.get_npy_data['wspd']['pd'][:,i,0,0].size
            #     pd_counts.append(pd_counts_data)
            # for j in range(0,12):
            #     pm_counts_data = self.get_npy_data['wspd']['pm'][:,j,0,0].size
            #     pm_counts.append(pm_counts_data)

            # print pd_data['wdir'].shape


            if subset =='PD':
                tags = np.array(['%s__%02d' % (self.year, hour) for hour in range(24)])
            elif subset =='PM':
                tags = np.array(['%s%02d' % (self.year, month) for month in range(1, 13)])
            elif subset =='PY':
                tags = np.array(['%s' % (self.year,)])

            if os.path.exists("%s/%s/mean/%s/%s/%s/"%(self.out_dir,subset,self.year,self.domain,self.level))==False:
                os.makedirs("%s/%s/mean/%s/%s/%s/"%(self.out_dir,subset,self.year,self.domain,self.level))
            out_path = "%s/%s/mean/%s/%s/%s/ALL.nc"%(self.out_dir,subset,self.year,self.domain,self.level)
            nc_file = Dataset(out_path,'w')
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
                if subset =='PD':
                    pd_data[varname] = self.get_npy_data[varname].reshape(-1,24,self.jy,self.ix)
                    var_data[:,:,:] = np.nanmean(pd_data[varname],axis=0)
                    var_data_std[:,:,:] = np.nanstd(pd_data[varname],axis=0)
                elif subset =='PM':
                    pm_data[varname] = self.get_npy_data[varname].reshape(12,-1,self.jy,self.ix)
                    # print 'PM:'
                    # np.set_printoptions(threshold='nan')
                    var_data[:,:,:] = np.nanmean(pm_data[varname],axis=1)
                    var_data_std[:,:,:] = np.nanstd(pm_data[varname],axis=1)

                    # print self.year,self.domain,self.level
                    # print var_data[:,:,:]
                    # print var_data[3,:,:]
                    # print var_data.shape
                    # return 0


                elif subset =='PY':
                    py_data[varname] = self.get_npy_data[varname].reshape(-1,self.jy,self.ix)
                    py_data[varname] = np.expand_dims(py_data[varname],axis=0)
                    var_data[:,:,:] = np.nanmean(py_data[varname],axis=1)
                    var_data_std[:,:,:] = np.nanstd(py_data[varname],axis=1)


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

            pd_data['wdir'] = self.get_npy_data['wdir'].reshape(-1,24,self.jy,self.ix)
            pm_data['wdir'] = self.get_npy_data['wdir'].reshape(12,-1,self.jy,self.ix)
            py_data['wdir'] = self.get_npy_data['wdir'].reshape(1,-1,self.jy,self.ix)
            # py_data['wdir'] = np.expand_dims(py_data['wdir'],axis=0)

            pd_counts = np.array([np.ma.masked_invalid(pd_data['wdir'][:, i, 0, 0]).count() for i in range(pd_data['wdir'].shape[1])])
            pm_counts = np.array([np.ma.masked_invalid(pm_data['wdir'][j, :, 0, 0]).count() for j in range(pm_data['wdir'].shape[0])])
            # py_counts = np.array([np.ma.masked_invalid(py_data['wdir'][ :, 0, 0]).count()])
            py_counts = np.array([np.ma.masked_invalid(py_data['wdir'][ 0,:, 0, 0]).count()])

            if subset =='PD':
                nc_file.createVariable('count', 'i8', ('tag', ))[:] = pd_counts
            elif subset =='PM':
                nc_file.createVariable('count', 'i', ('tag', ))[:] = pm_counts
            elif subset =='PY':
                # print type(py_counts)
                # print type(nc_file.createVariable('count', 'i8', ('tag', )))
                v_count = nc_file.createVariable('count', 'i', ('tag', ))
                # v_count[:] = py_counts.size()
                v_count[:] = py_counts

            nc_file.dataset = 'china_9km_anl'
            nc_file.subset = subset
            nc_file.varname = 'mean'
            nc_file.domain = '%s' % self.domain
            nc_file.year = '%s' % self.year
            nc_file.level = '%s' % self.level
            # print nc_file.variables['wdir'][:]
            nc_file.close()

    def rose_dist_mean(self):
        print 'start rose_dist'
        rose_path = "%s/PY/rose/%s/%s/%s/ALL.nc"%(self.out_dir,self.year,self.domain,self.level)
        dist_path = "%s/PY/dist/%s/%s/%s/ALL.nc"%(self.out_dir,self.year,self.domain,self.level)
        # WSBINS = np.arange(1.0, 50.1, 1.0, dtype='f4')
        # WSBINSTRS = np.array(['%g' % v for v in WSBINS])
        # N_WD = 16
        # WD0 = 0.0
        # CALM_THRES = 0.3
        # N_WS = len(WSBINS)
        # N_WDC = N_WD + 1
        # WDBINS = np.fmod((np.arange(N_WD) * (360.0 / N_WD) + WD0), 360.0)

        # 应该读取年平均值的数据

        # self.get_npy_data = get_pmpd_data(self.year,self.domain,self.level)

        # self.get_npy_data = np.load("xy_data/d03/70/all.npy").tolist()
        # self.get_npy_data = np.load("xy_data/d03/70/all.npy").tolist()
        py_data = self.handle_py()
        ws = py_data['wspd']
        wd = py_data['wdir']
        counts  = np.ma.masked_invalid(ws[:, 0, 0]).count()
        # counts = wd[:,0,0].size

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

        # v_a = dist_Dataset.createVariable('a', 'f4', ('tag', 'jy', 'ix'))
        # v_k = dist_Dataset.createVariable('k', 'f4', ('tag', 'jy', 'ix'))
        # N_JY = ws.shape[1]
        # N_IX = ws.shape[2]
        # for jy, ix in np.ndindex(N_JY, N_IX):
        #     a, k = get_ak_gamma(ws[:, jy, ix], 'raw')
        #     v_a[0, jy, ix] = a
        #     v_k[0, jy, ix] = k

        rose_Dataset.varname = 'rose'
        dist_Dataset.varname = 'dist'
        # print rose_Dataset.variables['rose'][:]
        rose_Dataset.close()
        dist_Dataset.close()

    def wpdrose_mean(self):
        print 'start wpdrose'
        wpdrose_path = "%s/PY/wpdrose/%s/%s/%s/ALL.nc"%(self.out_dir,self.year,self.domain,self.level)

        # 应该读取年平均值的数据
        # self.get_npy_data = get_pmpd_data(self.year,self.domain,self.level)

        py_data = self.handle_py()
        # print self.get_npy_data
        ws = py_data['wspd']
        wd = py_data['wdir']
        wpd = py_data['wpd']


        # print 'wd:'
        # print wd[:0,0]
        # print 'wpd:'
        # print wpd[:0,0]
        # print ws[:0,0]

        # counts = self.get_npy_data['wdir']
        counts  = np.ma.masked_invalid(ws[:, 0, 0]).count()
        # counts = wpd[:,0,0].size
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
        saveFile = '%s/d0%s/%s/%s_%s.npy'%(self.in_dir,self.domain,self.level,self.domain,self.level)
        print saveFile
        print '1'
        if os.path.isfile(saveFile) == False:
            get_dict_data(self.in_dir,self.domain,self.level)
        get_data = np.load(saveFile).tolist()
        varnames = get_data.keys()
        x = 10
        y = 10
        column = ['wdir_10','wdir_70','wdir_80','wdir_100', 'psfc_10','psfc_70', 'psfc_80','psfc_100','rhoair_10','rhoair_70','rhoair_80','rhoair_100',
                'wspd_10','wspd_70','wspd_80','wspd_100', 'wpd_10','wpd_70','wpd_80','wpd_100', 'td_10','td_70','td_80','td_100', 'rh_10','rh_70','rh_80','rh_100']
        for i in range(x):
            for j in range(y):
                ix = "%03d"%i
                jy = "%03d"%j
                for varname in varnames:
                    data_col = []
                    new_index = []
                    for time in get_data[varname].keys():
                        # data.ix[time,varname+"_"+level] = get_data[varname][time][i,j]
                        if self.year == time[0:4]:
                            new_index.append(time)
                            data_col.append(get_data[varname][time][i,j])
                    if os.path.isfile("%s/PT/ALL/%s/%s/ALL/%s_%s.h5"%(self.out_dir,self.year,self.domain,ix,jy)):
                        hdf = pandas.HDFStore("%s/PT/ALL/%s/%s/ALL/%s_%s.h5"%(self.out_dir,self.year,self.domain,ix,jy));
                        data_newIndex = hdf.select('df')
                    else:
                        if os.path.exists("%s/PT/ALL/%s/%s/ALL/"%(self.out_dir,self.year,self.domain)):
                            pass
                        else:
                           os.makedirs("%s/PT/ALL/%s/%s/ALL/"%(self.out_dir,self.year,self.domain))
                        hdf = pandas.HDFStore("%s/PT/ALL/%s/%s/ALL/%s_%s.h5"%(self.out_dir,self.year,self.domain,ix,jy));
                        data = DataFrame(columns = column)
                        data.index.name='datatime'
                        data_newIndex = data.reindex(index=new_index)
                    data_newIndex.loc[:,varname+"_"+self.level] = data_col
                    data_newIndex  = data_newIndex.sort_index()
                    hdf.put('df',data_newIndex,format='table')
                    hdf.close()
