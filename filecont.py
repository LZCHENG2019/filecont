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

def un_tar(fname,dirs):#解压tar文件
    t = tarfile.open(fname)
    t.extractall(path = dirs)
    t.close()

def un_zip(file,dirs):#解压zip文件
    z = zipfile.is_zipfile(file)
    if z:
        fz = zipfile.ZipFile(file,'r')
        for filen in fz.namelist():
            fz.extractall(filen,dirs)
    else:
        print(file + '不是zip文件')

def un_compress(file):#识别压缩包类型并解压
    if os.path.exists(file):
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
    else:
        print('%s 文件错误或不存在' % file)
        quit()
        # return

def write_excel_xls(path, sheet_name, value):#创建结果输出文件表
    index = len(value)  # 获取需要写入数据的行数
    workbook = xlwt.Workbook()  # 新建一个工作簿
    sheet = workbook.add_sheet(sheet_name)  # 在工作簿中新建一个表格
    for i in range(0, index):
        for j in range(0, len(value[i])):
            sheet.write(i, j, value[i][j])  # 像表格中写入数据（对应的行和列）
    workbook.save(path)  # 保存工作簿
    print("输出文件创建成功！")

def write_excel_xls_append(path, value):#在输出结果中追加内容，一行一行追加
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

def fileguess(file):#获取文件类型
    if os.path.exists(file):
        fg = filetype.guess(file)
        if fg is None:
            fg1 = os.path.splitext(file)[1]
            # print('文件类型：%s' % fg1)
        else:
            fg1 = fg.extension
            # print('文件类型: %s' % fg1)
        return fg1
        #return fg.extension
    else:
        fg1 = '/'
        return fg1

def filesize(file):#获取文件尺寸，以字节（b）为单位
    if os.path.exists(file):
        fs = os.path.getsize(file)
        return fs
    else:
        fs = '/'
        return fs

def getMd5(file):#获取MD5值
    if (os.path.exists(file)):

        m = hashlib.md5()
        f = open(file,'rb')
        str = f.read()
        m.update(str)
        return m.hexdigest()
    else:
        m = file
        print(file + '文件错误或不存在')
        return m

def comparMd5(file1,file2,m1,m2):#对比MD5值
    fail_num = 0
    suc_num = 0
    no_file = 0
    nofile = '/'
    fbiger = '/' #如果此处不写此变量，则报错：local variable 'fbiger' referenced before assignment
    morefile = '/'
    con = '/'
    if m2 == file2:
    # if m2 == 'none':
        # print(file1 + '-不存在')
        nofile = file2
        no_file=1
        # return nofile,no_file
    else:
        if m1==m2:
            # print (file1 + '-文件一致')
            suc_num = 1
            con = '文件一致'
            # con = file1+ '-文件一致'
        else:
            if os.path.exists(file1) & os.path.exists(file2):
                # print (file1 + '-文件不一致')
                con = file1+ '-文件不一致'
                size1 = filesize(file1)
                size2 = filesize(file2)

                # print(file1 + '-文件不一致')
                fail_num = 1
                if size1 > size2:

                    fbiger = '%s 文件较大' %file1

                else:

                    fbiger ='%s 文件较大' % file2

    return no_file,fail_num,suc_num,con,fbiger,nofile,morefile

def cmparFile(path1,path2,book_name_xls):#对比文件夹内文件差异，并输出结果
    files_num = 0
    fail_num = 0
    suc_num = 0
    no_file = 0
    # lackf  = 0
    moref = 0
    for root,dirs,files in os.walk(path1):

        for name1 in files:

            basefile = os.path.join(path1,name1)
            testfile = os.path.join(path2,name1)
            m1 = getMd5(basefile)
            m2 = getMd5(testfile)

            l, m, n, co, fb, nf, mf = comparMd5(basefile, testfile, m1, m2)

            fgb = fileguess(basefile)  # 输出文件类型
            fsb = filesize(basefile)
            fgt = fileguess(testfile)  #输出文件类型
            fst = filesize(testfile)

            no_file+=l
            fail_num+=m
            suc_num+=n
            files_num+=1

            # if nf == '/':
            #     lackf = lackf
            # else:
            #     lackf += 1
            if mf:
                moref = moref
            else:
                moref += 1


            RESULT = [basefile, fgb, fsb, testfile, fgt, fst,co,fb,nf,mf]
            write_excel_xls_append(book_name_xls, RESULT)

    for root,dirs,files in os.walk(path2):

        for name2 in files:

            basefile = os.path.join(path1,name2)
            testfile = os.path.join(path2,name2)
            m1 = getMd5(basefile)
            m2 = getMd5(testfile)

            if m1== basefile:
                mf = testfile
                moref += 1
                basefile, fgb, fsb, testfile, fgt, fst, co, fb, nf=\
                    '/','/','/','/','/','/','/','/','/'
                RESULT = [basefile, fgb, fsb, testfile, fgt, fst, co, fb, nf, mf]
                write_excel_xls_append(book_name_xls, RESULT)
    return files_num, fail_num, suc_num, no_file,moref

def Main(file1,file2,book_name_xls):
    m1 = getMd5(file1)
    m2 = getMd5(file2)

    if m1 == m2:
        print('压缩包文件无差异')
    else:

        fname11 = un_compress(file1)
        fname22 = un_compress(file2)

        try:
            file1path = fname11
            file2path = fname22

            x,y,z,q,v = cmparFile(file1path,file2path,book_name_xls)

            allf = '共比对文件：%s ' %x
            diff = '不一致文件：%s ' %y
            conf = '一致文件：%s ' %z
            notf = '缺少文件：%s ' %q
            moref = '多余文件：%s ' %v

            RESULT = [allf, diff,conf,notf,moref]
            write_excel_xls_append(book_name_xls, RESULT)
            # print('共比对文件[', x, '],不一致文件[', y, '],一致文件[', z, '],文件不存在[', q, ']')
            num_alt = int(input('请输入报警阈值：'))
            if y > num_alt:
                print('差异较大！请查看输出文件')
            else:
                print('文件差异在允许范围内')
        except:
            traceback.print_exc()

if __name__=='__main__':

    book_name_xls = input('请输入结果文件路径及文件名：') + '.xls'
    sheet_name_xls = '文件差异对比结果显示'
    value_title = [["基准文件",  "基准文件类型","基准文件大小(b)", "受试文件",
                    "受试文件类型","受试文件大小(b)","文件一致性", "大小对比", "缺少文件","多余文件"], ]
    write_excel_xls(book_name_xls, sheet_name_xls, value_title)

    Main(input('基准文件:'), input('受试文件:'),book_name_xls)

