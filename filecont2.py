#!/usr/bin/env python3
# -*- coding: utf-8 -*

import hashlib
import os
import traceback

import tarfile
import filetype

import zipfile

import xlrd,xlwt
from xlutils.copy import copy

# global RESULT

def un_tar(fname,dirs):
    t = tarfile.open(fname)
    t.extractall(path = dirs)
    t.close()

def un_zip(file,dirs):
    z = zipfile.is_zipfile(file)
    if z:
        fz = zipfile.ZipFile(file,'r')
        for filen in fz.namelist():
            fz.extractall(filen,dirs)
    else:
        print(file + '不是zip文件')

def write_excel_xls(path, sheet_name, value):
    index = len(value)  # 获取需要写入数据的行数
    workbook = xlwt.Workbook()  # 新建一个工作簿
    sheet = workbook.add_sheet(sheet_name)  # 在工作簿中新建一个表格
    for i in range(0, index):
        for j in range(0, len(value[i])):
            sheet.write(i, j, value[i][j])  # 像表格中写入数据（对应的行和列）
    workbook.save(path)  # 保存工作簿
    print("数据表头写入成功！")


def write_excel_xls_append(path, value):
    index = len(value)  # 获取需要写入数据的行数
    workbook = xlrd.open_workbook(path)  # 打开工作簿
    sheets = workbook.sheet_names()  # 获取工作簿中的所有表格
    worksheet = workbook.sheet_by_name(sheets[0])  # 获取工作簿中所有表格中的的第一个表格
    rows_old = worksheet.nrows  # 获取表格中已存在的数据的行数
    new_workbook = copy(workbook)  # 将xlrd对象拷贝转化为xlwt对象
    new_worksheet = new_workbook.get_sheet(0)  # 获取转化后工作簿中的第一个表格
    for i in range(0,len(value)):
        new_worksheet.write(rows_old,i,value[i])
    new_workbook.save(path)  # 保存工作簿
    # print("数据已添加表格！")


def getMd5(file):
    if (os.path.exists(file)):

        m = hashlib.md5()
        f = open(file,'rb')
        str = f.read()
        m.update(str)
        return m.hexdigest()
    else:
        print(file + '文件错误或不存在，请核实后重新输入')
        exit()
        # return ''

def comparMd5(file1,file2,m1,m2):
    fail_num = 0
    suc_num = 0
    no_file = 0
    fbiger = ''
    if m2 == '':
        # print(file1 + '-不存在')
        no_file=1
        return
    else:
        if m1==m2:
            # print (file1 + '-文件一致')
            suc_num = 1
            con = '文件一致'
            fbiger = "/"
            # con = file1+ '-文件一致'
        else:

            # print (file1 + '-文件不一致')
            con = file1+ '-不文件一致'
            a = filesize(file1)
            b = filesize(file2)

            # print(file1 + '-文件不一致')
            fail_num = 1
            if a > b:

                fbiger = '%s 文件较大' %file1

                # print('%s 文件较大' %file1)

            else:

                fbiger ='%s 文件较大' % file2


                # print('%s 文件较大' %file2)

        return no_file,fail_num,suc_num,con,fbiger

def cmparFile(path1,path2):
    files_num = 0
    fail_num = 0
    suc_num = 0
    no_file = 0
    for root,dirs,files in os.walk(path1):

        for name1 in files:

            basefile = os.path.join(path1,name1)
            testfile = os.path.join(path2,name1)
            m1 = getMd5(basefile)
            m2 = getMd5(testfile)

            l, m, n, co,fb= comparMd5(basefile, testfile, m1, m2)

            # l,m,n,co,fb=comparMd5(basefile,testfile,m1,m2)

            fgb = fileguess(basefile)  # 输出文件类型
            fsb = filesize(basefile)
            fgt = fileguess(testfile)  #输出文件类型
            fst = filesize(testfile)

            no_file+=l
            fail_num+=m
            suc_num+=n
            files_num+=1
            # global RESULT
            # RESULT = [str(basefile), str(fgb), str(fsb), str(testfile), str(fgt), str(fst)]
            RESULT = [basefile, fgb, fsb, testfile, fgt, fst,co,fb]

            book_name_xls = '/root/demo/result.xls'
            write_excel_xls_append(book_name_xls, RESULT)


    return files_num,fail_num,suc_num,no_file
def fileguess(file):
    fg = filetype.guess(file)
    if fg is None:
        fg1 = os.path.splitext(file)[1]

        # print('文件类型：%s' % fg1)
    else:
        fg1 = fg.extension
        # print('文件类型: %s' % fg1)
    return fg1

    #return fg.extension

def filesize(file):
    fs = os.path.getsize(file)
    # print(fs)
    return fs
def uncompress(file):
    kind = filetype.guess(file)
    path = os.path.split(file)[0]
    fname = os.path.splitext(file)[0]
    if kind is None:
        print('未知的文件类型！！')
        return
    elif kind.extension in {'gz','tar'}:

        un_tar(file,path)
        str1 = fname.split('.')
        if str1 is None:
            return
        else:
            fname = str1[0]

        return fname

    elif kind.extension == 'zip':
        un_zip(file,path)

def Main(file1,file2):
    m1 = getMd5(file1)
    m2 = getMd5(file2)


    if m1 == m2:
        print('压缩包文件无差异')
    else:

        fname11 = uncompress(file1)
        fname22 = uncompress(file2)

        try:
            file1path = fname11
            file2path = fname22

            print(file1path)

            x,y,z,q = cmparFile(file1path,file2path)

            print('共比对文件[', x, '],不一致文件[', y, '],一致文件[', z, '],文件不存在[', q, ']')
            num_alt = int(input('请输入报警阈值：'))
            if y > num_alt:
                print('注意！！！差异文件过多请查看')
            else:
                print('文件差异在允许范围内')
        except:
            traceback.print_exc()

if __name__=='__main__':

    book_name_xls = '/root/demo/result.xls'
    sheet_name_xls = '文件差异对比结果显示'
    value_title = [["base文件",  "base文件类型","base文件大小(b)", "test文件",  "test文件类型","test文件大小(b)","文件一致性", "大小对比"], ]
    write_excel_xls(book_name_xls, sheet_name_xls, value_title)

    Main(input('base:'), input('test:'))

