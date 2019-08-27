#!/usr/bin/python
#coding:utf-8

from    TB_Process.unpack import unzip_file
from    TB_Process import app
import  os
from    os.path import join, getsize, splitext
from    analyse_html.analyse_html_matrix import process_metrix_repot
from    docx import Document

class Process_Html_Report(object):
    url_type = 'file:///'

    def __init__(self):
        self.metricsfile_path = ""
        self.htmlfile_path = ""
        self.metrics_result_report = ""
        

    @staticmethod
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
            return Process_Html_Report.find_metrix_result_file(finale_floder)

    def get_metrix_result_path(self):
        return os.path.basename(self.metrics_result_report)

    def process_tb_system(self, system_zip_floder, path):
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

        dst_floder = unzip_file(system_zip_floder, path.extract)
        #dst_floder = unzip_file(system_zip_floder ,  app.config['EXTRACT_FOLDER'])
        self.metrix_filename , self.rule_filename = Process_Html_Report.find_metrix_result_file(dst_floder)

        report = process_metrix_repot()
        filename = ''.join((Process_Html_Report.url_type, self.metrix_filename)) 
        report.analyse_html(filename)

        #以模板为基础，生成度量结果文档
        template_file = os.path.join(app.config['METRICS_REPORT_PATH'],app.config['METRICS_REPORT_TEMPLATE'])
        document = Document(template_file)

        result_file = 'demo.docx'
        #self.metrics_result_report = os.path.join(app.config['RESULT_FOLDER'],result_file)
        self.metrics_result_report = os.path.join(path.project_result, result_file)

        report.store_matrix_to_docx(document, self.metrics_result_report)

        return 

    

