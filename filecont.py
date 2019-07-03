#!/usr/bin/env python3
# -*- coding: utf-8 -*
import hashlib,os,tarfile,subprocess
def un_tar(file,dirs):#解压tar文件
    t = tarfile.open(file)
    t.extractall(path = dirs)
    t.close()
def un_compress(file):#识别压缩包类型并解压，可能不用
    if os.path.exists(file):
        kind = fileguess(file)#filetype.guess(file)
        path = os.path.split(file)[0]#获取文件路径，例：/root/demo
        if kind == 'XZ compressed data':#.xz文件解压
            dirnm = subprocess.getstatusoutput("tar Jxvf %s -C %s | xargs awk 'BEGIN{print ARGV[1]}'" % (file, path))
            print('%s 解压完成' %file)
        elif kind == 'POSIX tar archive (GNU)':#tar包解压
            dirnm = subprocess.getstatusoutput("tar xvf %s -C %s | xargs awk 'BEGIN{print ARGV[1]}'" %(file,path))
            print('%s 解压完成' % file)
        elif kind == 'gzip compressed data':#.gz文件解压
            dirnm = subprocess.getstatusoutput("tar zxvf %s -C %s | xargs awk 'BEGIN{print ARGV[1]}'" % (file, path))
            print('%s 解压完成' % file)
        else:
            print('未知文件类型')

        dirname = path + '/'+dirnm[1].split('/')[0]
        return dirname

def fileguess(file):#获取文件类型
    if os.path.exists(file):
        filttyp = subprocess.getstatusoutput('file %s -b' %file)
        fg = filttyp[1].split(',')[0]
        return fg
    else:
        fg = '/'
        return fg
def filesize(file):#获取文件尺寸，以字节（b）为单位
    if os.path.exists(file):
        fs = os.path.getsize(file)
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

def comparfile(file1,file2):#对比文件
    result = True
    file1tp = fileguess(file1)
    file2tp = fileguess(file2)
    if file1tp == file2tp:        #先判断文件类型，若相同则继续对比，若不同则直接退出对比
        size1 = filesize(file1)
        size2 = filesize(file2)
        sizevalue = 1 #此处用来定义文件大小阈值，单位是字节（B），可设置
        if size1 == size2:#先判断文件尺寸，若相同则对比MD5值
            file1md5 = getMd5(file1)
            file2md5 = getMd5(file2)
            if file1md5 == file2md5:
                print('%s 和%s 大小、内容均无差异' %(file1,file2))#大小内容均相同
                return result
            else:
                result = False
                print('%s 和%s 大小相同，内容不同' % (file1, file2))#大小一样，内容不一样
                return result

        elif abs(size1-size2)  > sizevalue:#文件大小差距过大,自动判定内容不同
            result = False
            print('%s 和 %s 文件大小差距过大' % (file1, file2))
            return result
        elif abs(size1-size2) < sizevalue:#大小差异较小，进一步判断文件内容差异
            file1md5 = getMd5(file1)
            file2md5 = getMd5(file2)
            if file1md5 == file2md5:
                print('%s 和%s 大小差异小、内容无差异' % (file1, file2))
                # 大小差异小，内容无差异
            else:
                print('%s 和%s 大小差异小、内容有差异' % (file1, file2))
                # 大小差异小，内容有差异 （即内容不一样，大小一样）
                result = False
                return result
        # return result
    else:
        print(' %s 和 %s 类型不同，不进行对比' %(file1,file2))
        result = False
        return result

def compardirs(path1,path2):#对比文件夹内容
    file1m = 0
    file2m = 0
    diff = []
    diffdirs = 1
    diffnum = 2
    print('文件夹%s 和文件夹 %s 对比内容如下：' %(path1,path2))
    for root, dirs, files in os.walk(path1):
        for name in files:
            file1 = os.path.join(path1, name)
            file2 = os.path.join(path2, name)
            if os.path.exists(file1) and os.path.exists(file2):#如果AB两个文件都存在，则进一步对比
                result = comparfile(file1,file2)
                # print(result)
                if result is True:#如果对比结果一致则返回True
                    finresult = True
                else:
                    file1path = un_compress(file1)  # filepath是解压后文件所在目录
                    file2path = un_compress(file2)
                    compardirs2(file1path, file2path)
                    diff.append(name)
            elif os.path.exists(file1):#任何一个文件不存在则，输出一个数值
                file1m +=1
                print('%s 不存在' %file2)
            elif os.path.exists(file2):
                file2m +=1
                print('%s 不存在' % file1)
    if abs(file1m-file2m) > diffdirs:#此阈值是个可调值。用来显示文件夹内文件缺少/增多数量差距过大时报警
        print('文件夹内文件数量差距过多')
        finresult = False
        return finresult
    if len(diff) > diffnum:#此阈值是个可调值。用来显示文件夹内文件不同数据过大时报警
        print('%s 和 %s 文件夹内部差异文件数大于阈值' %(path1,path2))
        finresult = False
        return finresult
    return finresult

def compardirs2(path1,path2):#对比文件夹内容
    file1m = 0
    file2m = 0
    diff = []
    diffdirs = 1
    diffnum = 2
    print('文件夹%s 和文件夹 %s 对比内容如下：' %(path1,path2))
    for root, dirs, files in os.walk(path1):
        for name in files:
            file1 = os.path.join(path1, name)
            file2 = os.path.join(path2, name)
            if os.path.exists(file1) and os.path.exists(file2):#如果AB两个文件都存在，则进一步对比
                result = comparfile(file1,file2)
                # print(result)
                if result is True:#如果对比结果一致则返回True
                    # nonlocal finresult
                    finresult = True
                else:
                    diff.append(name)
            elif os.path.exists(file1):#任何一个文件不存在则，输出一个数值
                file1m +=1
                print('%s 不存在' %file2)
            elif os.path.exists(file2):
                file2m +=1
                print('%s 不存在' % file1)
    if abs(file1m-file2m) > diffdirs:#此阈值是个可调值。用来显示文件夹内文件缺少/增多数量差距过大时报警
        print('文件夹内文件数量差距过多')
        finresult = False
        return finresult
    if len(diff) > diffnum:#此阈值是个可调值。用来显示文件夹内文件不同数据过大时报警
        print('%s 和 %s 文件夹内部差异文件数大于阈值' % (path1, path2))
        finresult = False
        return finresult
    return finresult

def Main(file1,file2):#,book_name_xls):
    if os.path.exists(file1) and os.path.exists(file2):
        size1 = filesize(file1)#文件1的大小
        size2 = filesize(file2)#文件2的大小
        if size1 == size2:     #首先对比文件大小，若文件大小一样，则继续对比MD5值
            m1 = getMd5(file1)
            m2 = getMd5(file2)
            if m1 == m2:
                print('压缩包文件无差异')
                return
            else:
                file1path = un_compress(file1)#filepath是解压后文件所在目录
                file2path = un_compress(file2)
                if compardirs(file1path,file2path):
                    print('最终结果：结果无差异')
                else:
                    print('最终结果：结果有差异请查看！')
        elif abs(size1-size2) > 10:#此处阈值可调，当文件差异过大时，继续对比
            file1path = un_compress(file1)  # filepath是解压后文件所在目录
            file2path = un_compress(file2)
            if compardirs(file1path, file2path):
                print('最终结果：结果无差异')
            else:
                print('最终结果：结果有差异请查看！')
        else:
            print('最终结果：文件差异在允许范围内')
    else:
        print('文件不存在，请重新输入')
if __name__=='__main__':
    Main(input('基准文件:'), input('受试文件:'))