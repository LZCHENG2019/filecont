import os
import sys
import commands
import argparse
sys.setrecursionlimit(100000)

parser=argparse.ArgumentParser()
parser.add_argument("file1")
parser.add_argument("file2")
parser.add_argument("-o","--option",type=int,choices=[0,1],default=0,help="default 0,not show extracting information")
args=parser.parse_args()
count=0

def process(filename):#解压文件
   # print("extracting file "+filename+"......")
    if args.option==0:
        os.system("tar xf "+filename)
    elif args.option==1:
        os.system("tar xvf "+filename)
    topdir = filename.split(".tar")[0]
    #print("topdir:%s"%topdir)
    #os.system("cd "+topdir)

    pwd=os.getcwd()+'/'+topdir
    os.chdir(pwd)
    files = os.listdir(pwd)
#    os.system("cd ..")

    for file in files:#解压xz和gz文件
        if "tar" in file:
            if "xz" in file:
                os.system("xz -d "+file)
                if args.option==0:
                    os.system("tar xf "+file.strip(".xz"))
                elif args.option==1:
                    os.system("tar xvf "+file.strip(".xz"))
            elif "gz" in file:
                if args.option==0:
                    os.system("tar zxf "+file)
                elif args.option==1:
                    os.system("tar zvxf "+file)
    os.system("rm -rf *.tar*")#解压后删除所有的压缩文件
    files1=os.listdir(pwd)
    #print("files1:%s"%files1)
    for file in files1:
        if "parastor-" in file and os.path.isdir(pwd+'/'+file):
            #print(pwd+'/'+file)
            #print("mv "+file+" parastor-3.0.0")
            os.system("mv "+file+" parastor-3.0.0")#更改文件夹名字
    os.chdir('..')

def check(dir11,dir22):#对比文件内容
    #print("checking direcory %s and %s start...."%(dir11,dir22))
    redir1=dir11.replace(dir1,"./1")
    redir2=dir22.replace(dir2,"./2")
    #print(dir1)
    #print(dir2)
    #topdir = os.getcwd()
    pwd1=os.listdir(dir11)#给文件夹内文件排序
    pwd2=os.listdir(dir22)
    len1=len(pwd1)#判断文件数量
    len2=len(pwd2)
    #print("pwd1:%s" % pwd1)
    #print("pwd2:%s" % pwd2)
    #print("dirlen1:%s" % len1)
    #print("dirlen2:%s" % len2)
    pwd1.sort()
    pwd2.sort()
    global count
    if len1!=len2:#如果文件数不同
        count +=1
        print("Failed: the file number is different!")
        print("The number of files in %s is %d"%(redir1,len1))
        print("The number of files in %s is %d"%(redir2,len2))
        samelist=[x for x in pwd1 if x in pwd2]#两个文件夹内均有的文件
        difflist1=[y for y in (pwd1+pwd2) if y not in samelist and y not in pwd2]
        #只有文件夹1内有的文件
        difflist2=[y for y in (pwd1+pwd2) if y not in samelist and y not in pwd1]
        #只有文件夹2内有的文件
        if len(difflist1) !=0:
           print("The unexpected files in %s are: %s"%(redir1,difflist1))
        if len(difflist2) !=0:
           print("The unexpected files in %s are: %s"%(redir2,difflist2))
        #print("the diff files are:%s"%difflist)
        #exit("failed")
    if len1==len2 and pwd1!=pwd2:
        #文件夹内文件数一样，但是文件夹内文件名称不一样
        count +=1
        #print("files in %s are %s"%(dir11,pwd1))
        #print("files in %s are %s"%(dir22,pwd2))
        print("Failed:  the files are different!")
        samelist=[x for x in pwd1 if x in pwd2]
        difflist1=[y for y in (pwd1+pwd2) if y not in samelist and y not in pwd2]
        difflist2=[y for y in (pwd1+pwd2) if y not in samelist and y not in pwd1]
        if len(difflist1) !=0:
            print("The unexpected files in %s are: %s"%(redir1,difflist1))
        if len(difflist2) !=0:
            print("The unexpected files in %s are: %s"%(redir2,difflist2))
        #print("failed:  the files are different!" %(pwd1,pwd2))
        #print("the diff files are:%s"%difflist)
        #exit("failed")
    for item in pwd1:
        path1=dir11+'/'+item
        path2=dir22+'/'+item
        respath1=redir1+'/'+item
        respath2=redir2+'/'+item
        if os.path.isfile(path1) and os.path.isfile(path2):
            filetype1=commands.getoutput("file -b "+path1)
            filetype2=commands.getoutput("file -b "+path2)
            #print("filetype1:%s"%filetype1)
            #print("filetype2:%s"%filetype2)
            if filetype1 != filetype2:#文件类型不同的情况
                count +=1
                print("Failed:the file type is different!")
                print("the filetype of %s is:%s"%(respath1,filetype1))
                print("the filetype of %s is:%s"%(respath2,filetype2))
                #exit("the file type is different!")
            size1=os.path.getsize(path1)
            size2=os.path.getsize(path2)
            if size1!=0 and size2!=0:
                diff1=1.0*abs(size1-size2)/size2#文件不同的数量不能超过10%
                diff2=1.0*abs(size1-size2)/size1
                if diff1>0.1 or diff2>0.1:
                    count +=1
                    print("Failed:the diff size is more than 10% ")
                    print("The size of %s is %s:" %(respath1,size1))
                    print("The size of %s is %s:" %(respath2,size2))
                    #exit("failed:the diff size is more than 10% ")
            elif (size1==0 and size2!=0) or (size1!=0 and size2==0):
                    count +=1
                    print("the file size of %s and %s,one is zero, another is not zero. "%(respath1,respath2))
                    #exit("the file size of %s and %s,one is zero, another is not zero. "%(respath1,respath2))            
        elif os.path.isdir(path1) and os.path.isdir(path2):
            check(path1, path2,)
            #else:
            #    exit("failed")
        #print("checking finished, result: pass")

if __name__ == '__main__':
    #tar1 = sys.argv[1]
    #tar2 = sys.argv[2]
    tar1 = args.file1
    tar2 = args.file2
    #count=0
    process(tar1)
    process(tar2)#分别解压两个文件
    rootpwd=os.getcwd()
    dir1=rootpwd+'/'+tar1.split('.tar')[0]
    dir2=rootpwd+'/'+tar2.split('.tar')[0]#获取文件路径
    #print("rootpwd: %s" %rootpwd)
    check(dir1,dir2)
    if count==0:#按照计数来进行对比，
        print("total checking finished, result: pass")
    else:
        print("total checking finished, result:failed")
    #check(rootpwd+'/1',rootpwd+'/2')


