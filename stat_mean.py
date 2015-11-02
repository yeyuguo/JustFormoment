from mean.mean import mean_PD_PM_PY as nc_h5
def stat_mean(argList):
    for year, domain, level in argList:
        print year, domain, level
        try:
            mean_pt = nc_h5(year,domain,level)
            # mean_pt.pdpmpy_mean()
            # mean_pt.rose_dist_mean()
            # mean_pt.wpdrose_mean()
            mean_pt.hdf5()
            print 'ok'
        except Exception as e:
            print e

if __name__ =="__main__":
    argList = []
    for year in ['2013', '2014']:
        for domain in ['3','4','5','6','7']:
            for level in ['10','70','80','100']:
                argList.append((year, domain, level))
    # for year in ['2013']:
    #     for domain in ['3']:
    #         for level in ['10', '70']:
    stat_mean(argList)