#!/usr/bin/env python
import os,sys
import numpy as np
import glob

root_dir = '/mnt/data1/tengyao/data'
root_out = '/mnt/data1/huima/data'
def get_csv_data(file='latitude.txt'):
  fid = open(file,'r')
  data=[]
  for line in fid.readlines():
    tmp = line.strip()
    if len(tmp) >0:
      list = tmp.split(',')
      t1=[]
      for dd in list:
        val = float(dd)
        t1.append(val)
      t1 = np.array(t1,dtype=np.float32)
      data.append(t1)
  fid.close()
  data = np.array(data,dtype=np.float32)
  data = np.transpose(data)
  return(data)
def get_latlon():
  latfile = '%s/latitude.txt' % root_dir
  lonfile = '%s/longitude.txt' % root_dir
  xlat = get_csv_data(file=latfile)
  xlon = get_csv_data(file=lonfile)
  return(xlat,xlon)

def get_data(model='CAMX',var='PM2.5',init='2015013012'):
  file_flag = '%s/%s_2D_OUTPUT/%s/%s/%s/%s_%s_*.csv' % (root_dir,model,init[0:4],init[0:6],init[0:10],var,model)
  re =  glob.glob(file_flag)
  data={}
  for file in re:
    tmp =  os.path.basename(file).replace('.csv','').split('_')
    fcdt = tmp[-1]
    td = get_csv_data(file=file)
    data[fcdt]= td
  newdata=[]
  fcdtlist=[]
  for fcdt in sorted(data.keys()):
    fcdtlist.append(fcdt)
    newdata.append(data[fcdt])
  newdata = np.array(newdata,dtype=np.float32)
  return(newdata,fcdtlist) 

def get_latest_init(model='CAMX'):
  cmd1 = '%s/%s_2D_OUTPUT/*' % (root_dir,model)
  year_list=[]
  for line in glob.glob(cmd1):
     year= os.path.basename(line.strip())
     year_list.append(year)
  year = sorted(year_list,reverse=True)[0]
  cmd2 = '%s/%s_2D_OUTPUT/%s/*' % (root_dir,model,year)
  month_list = []
  for line in glob.glob(cmd2):
    mo = os.path.basename(line.strip())
    month_list.append(mo)
  month = sorted(month_list,reverse=True)[0]
  cmd3 = '%s/%s_2D_OUTPUT/%s/%s/*' % (root_dir,model,year,month)
  init_list=[]
  for line in glob.glob(cmd3):
    init = os.path.basename(line.strip())
    init_list.append(init)
  init_dt = sorted(init_list,reverse=True)[0] 
  return(init_dt)
 

def run_main(model='CAMX'):
  init_dt = get_latest_init(model=model)
  print init_dt
  cmd1 =  '%s/%s_2D_OUTPUT/%s/%s/%s/*' % (root_dir,model,init_dt[0:4],init_dt[0:6],init_dt[0:10])
  re = glob.glob(cmd1)
  print len(re)
  if len(re) <= 670:
    return
  out_dir  = '%s/%s' % (root_out,model)
  if os.path.exists(out_dir)==False: os.makedirs(out_dir)
  outfile = '%s/%s.npy' % (out_dir,init_dt)
  #if os.path.isfile(outfile): return
  varlist = ['PM2.5','PM10','O3','NO2','SO2','CO','VIS']
  fdata={}  
  xlat,xlon=get_latlon()
  for var in varlist:
    tmp,dtlist = get_data(model=model,var=var,init=init_dt)
    fdata[var]=tmp
  fdata['xlat']=xlat
  fdata['xlon']=xlon
  fdata['times']=dtlist
  print dtlist
  np.save(outfile,fdata)
  
if __name__ == "__main__":
  run_main()
  #get_latlon()
