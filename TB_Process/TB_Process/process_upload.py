#!/usr/bin/python
#coding:utf-8

from TB_Process.unpack import unzip_file
from TB_Process import app
import os
from    os.path import join, getsize, splitext

def find_metrix_result_file(floder):
    '''
    从文件夹中找到metrix report的html文件：
    floder文件夹中可能包含子文件夹
    1.判断floder中是否存在metrix文件，如果不存在则在子文件夹中查找
    如果只有一个文件夹，那么直接进入文件夹
    
    '''
    dirs = os.listdir(floder)
    if len(dirs) != 1:
        #the last floder, contain testbed system analyse result
        for filename in dirs:
            if filename.endswith("mts.htm"):
                metrix_filename = os.path.join(floder, filename)
            elif filename.endswith('rps.htm'):
                rule_filename = os.path.join(floder, filename)

        if (metrix_filename is not None) and (rule_filename is not None):
            return (metrix_filename , rule_filename )
        else:
            return None
    else:
        finale_floder = os.path.join(floder, dirs[0])
        return find_metrix_result_file(finale_floder)

def process_tb_system(system_zip_floder):
    '''
    process a testbed system floder:
    1.make dir /user/projectx/--upload
                                         /--extract  
                                         /--result
    2.extract floder to /extract
    3.process html report, produce metrics report and GJB8114 rule report
    4.store to result floder
    5.zip result files and auto download to user
    5.store results
    ''' 

    dst_floder = unzip_file(system_zip_floder ,  app.config['EXTRACT_FOLDER'])
    metrix_filename , rule_filename = find_metrix_result_file(dst_floder)
    # to be continue
    return 

class process_upload(object):
    '''  
    this module is used as a adater pattern. one side is analyse module, another side is TB_process views module
    '''
    

