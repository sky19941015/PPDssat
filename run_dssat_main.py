# coding=utf-8
import os, sys, subprocess
import numpy as np
import re
from pro_cli_to_dssat import clm_list, read_clm, write_clm
from pro_soil import write_soil
from pro_rix import write_rix
from pro_batch import write_batch


def read_latlon(_file = './latlon.csv'):
    _lat_lon = np.loadtxt(_file, dtype=np.str, delimiter=",")
    _lat_lon = _lat_lon[1:]
    #_lat = _lat_lon[1:,0].astype(np.float)
    #_lon = _lat_lon[1:,1].astype(np.float)
    return _lat_lon


def create_name(_latloni, _gen_path = './'):
    #_latloni is number, return is str like 'AAAA'
    _gen_path = os.getcwd() + '/'
    _words = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    aaa = []
    for i in xrange(len(_words)):
        for j in xrange(len(_words)):
            for k in xrange(len(_words)):
                for l in xrange(len(_words)):
                    aaa.append(_words[i]+_words[j] + _words[k] + _words[l])

    _path_full = _gen_path + aaa[_latloni]
    if os.path.exists(_path_full):
        _file_exsit = raw_input("Already have path: %s! Want to rewrite? y/n: " % _path_full)
        if _file_exsit == 'y' or _file_exsit == 'Y':
            subprocess.call('rm -rf ' + _path_full, shell = True)
    os.mkdir(_path_full)
    return aaa[_latloni]


# _lat_lon are list, each_lat_lon is a lat lon group, _clm_list is list
def run_dssat_main(_lat_lon, _begin_year, _end_year, _climate_path = './', _run_path = './', _dssat_exe= './'):

    # Loop each point
    for _latloni in xrange(len(_lat_lon)):
        _name_AAAA = create_name(_latloni)
        _site_path = _run_path + _name_AAAA + '/'

        _lat_in = float(_lat_lon[_latloni][0])
        _lon_in = float(_lat_lon[_latloni][1])

        # TEST!
        _lat_in =  32.00
        _lon_in = 118.29

        #write .SOL
        _soil_name = write_soil(_lat_in, _lon_in, _name_AAAA, _run_path, _site_path)

        _rix_list = []
        # Loop year for .WTH
        for _year in xrange(_begin_year, _end_year):
            print 'Processing year: ', _year
            _list_year = list(str(_year))
            _last_two_num = str(_list_year[2]) + str(_list_year[3])
            _site_name = _name_AAAA + _last_two_num + '01'

            #find clm list
            _wea_list = clm_list(_year, _climate_path)

            #read clm vars
            _clm_dic = read_clm(_year, _wea_list, _lat_in, _lon_in, _climate_path)
       
            #write clm vars .WTH
            write_clm(_lat_in, _lon_in, _year, _clm_dic, _site_name, _site_path)

            #write .RIX
            _rix_name = write_rix(_year, _site_name, _soil_name, _site_path)
            _rix_list.append(_rix_name)
        print 'Finised writing all year between %s and %s' % (_begin_year, _end_year)
            
        #write DSSBatch.v47
        write_batch(_site_path)

        #link some needed files and run dssat
        _ln_dssat_exe           = subprocess.call('ln -sf %s/buid/bin/dscsm047.exe %s/.' % (_dssat_exe_path, _site_path),       shell=True)
        _ln_dssat_linux         = subprocess.call('ln -sf %s/DSSATPRO.L47 %s/.' % (_run_path, _site_path),                      shell=True)
        _ln_rice_gene           = subprocess.call('ln -sf %s/RICER047.CUL %s' % (_run_path, _site_path),                        shell=True)
        _ln_dssat_model_err     = subprocess.call('ln -sf %s/Data/MODEL.ERR %s/.' % (_run_path, _site_path),                    shell=True)
        _ln_dssat_cde           = subprocess.call('ln -sf %s/Data/*CDE %s/.' % (_dssat_exe_path, _site_path),                   shell=True)

        _run_dssat              = subprocess.call('cd %s; ./dscsm047.exe RICER047 B DSSBatch.v47' % _site_path,                 shell=True)

        return
        #post process Summary.out
        pro_summary()

        #plot
            




# LETS ROCK!!!
_climate_path = '/Users/qingsun/GGCM/run_dssat/GFDL_RCP2.6/'
_run_path = '/Users/qingsun/GGCM/run_dssat/'
_dssat_exe_path = '/Users/qingsun/GGCM/dssat-csm/'

# Read _lat _lon, first col is lat, second col is lon, first row is 'lat, lon' 
_lat_lon = read_latlon(_run_path + '/latlon.csv')

# run main loop
run_dssat_main(_lat_lon, 1951, 1960, _climate_path, _run_path, _dssat_exe_path)






'''
def file_name(file_dir):  
    ls = [] 
    for root, dirs, files in os.walk(file_dir):  
        #print(root) 
        #print(dirs)
        ls.append(files) 
    ls = ls[0]
    print ls
    print root
file_name('/Users/qingsun/GGCM/run_dssat/GFDL_RCP2.6')

   for _wea in xrange(len(_clm_list)):
        f = Dataset(wea_list[_wea], 'r')
        # exact first strings before '_' as variable name
        _var = wea_list[_wea][0:wea_list[_wea].rfind('_', 0, 7)]

'''