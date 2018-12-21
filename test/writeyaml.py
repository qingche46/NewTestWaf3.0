import xlrd
import xlwt
import os
import sys
import yaml
import urllib.parse
from datetime import datetime

date=datetime.now().strftime("%Y%m%d.%H:%M:%S")

data = xlrd.open_workbook("sql_xss.xls")
table = data.sheets()[0]
nrows = table.nrows

for i in range(0,nrows ):

    sql=urllib.parse.quote(table.cell(i,0).value)#第1列第i行，获取payload,（urllib.parse.quote对payload编码）
    #sql=urllib.parse.unquote(table.cell(i,0).value)#第1列第i行，获取payload,（urllib.parse.unquote对payload解码）
    num=int(table.cell(i,1).value) #第2列第i行,注入攻击编号

    fname="D:\\Python\\NewTestWaf\\yaml\\%s.txt"%num
    try:
        fobj=open(fname,'a')                 # 这里的a意思是追加，这样在加了之后就不会覆盖掉源文件中的内容，如果是w则会覆盖。
    except IOError:
        print ('*** file open error:')
    else:


        fobj.write('---')   #  这里的\n的意思是在源文件末尾换行，即新加内容另起一行插入。
        fobj.write('\n'+'  meta:')
        fobj.write('\n'+'    author: "zfz_%s"'%date)
        fobj.write('\n'+'    description: "SQL"')
        fobj.write('\n'+'    enabled: true')
        fobj.write('\n'+'    name: "%s.yaml"'%num)
        #时间修改
        fobj.write('\n'+'  tests:')
        #修改等级
        fobj.write('\n'+'  -')
        fobj.write('\n'+'    test_title: %s_%s'%(num,date))
        fobj.write('\n'+'    desc: "SQL"')
        fobj.write('\n'+'    stages:')
        fobj.write('\n'+'    -')
        fobj.write('\n'+'      stage:')
        fobj.write('\n'+'        input:')
        fobj.write('\n'+'#          dest_addr: 192.168.77.111')
        fobj.write('\n'+'          headers:')
        fobj.write('\n'+'            Host:')
        fobj.write('\n'+'          method: GET')
        fobj.write('\n'+'#          port: 80')
        fobj.write('\n'+'          uri: "?%s"'%sql)
        fobj.write('\n'+'          version: HTTP/1.0')
        fobj.write('\n'+'        output:')
        fobj.write('\n'+'          log_contains: id "%s"'%num)
        fobj.write('\n'+'          status: 200')
        fobj.write('\n'+'          response_contains: "safedog.cn/images/safedogsite/broswer_logo.jpg"')

        fobj.close()                              #   特别注意文件操作完毕后要close


# 列出当前目录下所有的文件
files = os.listdir("D:\\Python\\NewTestWaf\\yaml")

#files = os.listdir('.')
#print('files',files)

for filename in files:
    portion = os.path.splitext(filename)
    # 原來的后缀名
    if portion[1] == ".txt":
        newname = portion[0] + ".yaml"# 重新组合文件名和后缀名
        #切换文件路径,如无路径则要新建或者路径同上,做好备份
        os.chdir("D:\\Python\\NewTestWaf\\yaml")
        os.rename(filename,newname)
