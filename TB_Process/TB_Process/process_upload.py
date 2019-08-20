#!/usr/bin/python
#coding:utf-8

from TB_Process.unpack import unzip_file
from TB_Process import app

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
    unzip_file(system_zip_floder ,  app.config['EXTRACT_FOLDER'])
    
    return 

class process_upload(object):
    '''  
    this module is used as a adater pattern. one side is analyse module, another side is TB_process views module
    '''
    

