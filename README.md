# NewTestWaf3.0
## 修改开源Framework for Testing WAFs (FTW)为Python3
主要用于测试WAF产品累积更新是否遗漏之前绕过行为，分为get和post请求，
这边编写了sql，xss，scanner，struts2，upload等yaml模式进行分类，具体的payload可以通过不断积累进行添加


## 安装
* `下载https://github.com/qingche46/NewTestWaf3.0.git`
* `cd NewTestWaf`
* pip is installed `apt-get install python-pip`
* `pip install -r requirements.txt`

## 结果通过pytest-HTML的页面显示，通过把大量的payload放到yaml文件中 --destaddr是搭建的目标地址，port是站点端口
* `cd NewTestWaf3.0`
* `py.test test/test_default.py -s -v --destaddr 192.168.88.244 --port 80 --rule yaml/sql.yaml --html sql.html`

