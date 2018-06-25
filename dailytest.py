#coding:utf-8
_author_ = "ZBC"
_time_  = "2018.5.25"
import webbrowser
import MySQLdb
import re
import time
import datetime

db = MySQLdb.connect('localhost','root','123','huginn_production')
cursor1 = db.cursor()
cursor2 = db.cursor()
cursor3 = db.cursor()
cursor10 = db.cursor()

num = []
url_all1 = []
title_all1 = []
url_all2 = []
title_all2 = []
url_all3 = []
title_all3 = []
news_all1 = ""
news_all2 = ""
news_all3 = ""
newsnum = 0
technum = 0
exponum = 0
sql1 = "select payload from mydaily where agent_id in (10,19,22,25,26,32,35,28,46,49,69,71,75) and DATE_FORMAT(created_at,'%Y-%m-%d') = date_format(now(),'%Y-%m-%d');"
#sql2 = "select payload from mydaily where agent_id in (13,14,41,78,81,84,87,90,93,96,99,102,105) and DATE_FORMAT(created_at,'%Y-%m-%d') = date_format(now(),'%Y-%m-%d');"
#sql1 = "select payload from mydaily where agent_id in (10,19,22,25,26,32,35,28,46,49);"
sql2 = "select payload from mydaily where agent_id in (71);"
#sql3 = "select payload from mydaily where agent_id in (56);"
sql3 = "select payload from mydaily where agent_id in (56) and DATE_FORMAT(created_at,'%Y-%m-%d') = date_format(now(),'%Y-%m-%d');"
sql10 = ["select count(*) from mydaily where agent_id in (10,19,22,25,26,32,35,28,46,49,69,71,75) and DATE_FORMAT(created_at,'%Y-%m-%d') = date_format(now(),'%Y-%m-%d');","select count(*) from mydaily where agent_id in (71);","select count(*) from mydaily where agent_id in (56) and DATE_FORMAT(created_at,'%Y-%m-%d') = date_format(now(),'%Y-%m-%d');"]


cursor1.execute(sql1)
cursor2.execute(sql2)
cursor3.execute(sql3)

for i in range(3):
    cursor10.execute(sql10[i])
    number = cursor10.fetchone()
    number = int(number[0])
    num.append(number)
    print num

for i in range(num[0]):
    try:
        #cursor.execute(sql1)
        result1 = cursor1.fetchone()
        #print(type(result1))    
        payload1 = str(result1[0])
    except:
        print 'error'

    url1 = re.search('(?<="url":").*?(?=")',payload1).group(0)
    #print(url1)
    title1 = re.search('(?<="title":").*?(?=")',payload1).group(0)
    #print(title1)
    url_all1.append(url1)
    title_all1.append(title1)
    newsnum = newsnum+1
    if newsnum>10:
        break

import json
 
#For python 3.x
from HTMLParser import HTMLParser
 
#定义HTMLParser的子类,用以复写HTMLParser中的方法
class MyHTMLParser(HTMLParser):
 
    #构造方法,定义data数组用来存储html中的数据
    def __init__(self):
        HTMLParser.__init__(self)
        self.data = []
 
    #覆盖starttag方法,可以进行一些打印操作
    def handle_starttag(self, tag, attrs):
        pass
        #print("Start Tag: ",tag)
        #for attr in attrs:
        #   print(attr)
     
    #覆盖endtag方法
    def handle_endtag(self, tag):
        pass
 
    #覆盖handle_data方法,用来处理获取的html数据,这里保存在data数组
    def handle_data(self, data):
        if data.count('\n') == 0:
            self.data.append(data)

 
#创建子类实例
parser = MyHTMLParser()

for i in range(1):
    try:
        #cursor.execute(sql1)
        result2 = cursor2.fetchone()
        payload2 = str(result2[0])
        parser.feed(payload2)
    except:
        print 'error'
    url2 = re.search('(?<="url":").*?(?=")',payload2).group(0)
        #print(url2)
    title2 = re.search('(?<="title":").*?(?=")',payload2).group(0)
        #print(title2)
    for item in parser.data:
        print(item)
    url_all2.append(url2)
    title_all2.append(title2)
    #except:
        #print 'error'
    technum = technum + 1
    if technum > 5:
        break 

for i in range(num[2]):
    try:
        #cursor.execute(sql1)
        result3 = cursor3.fetchone()
        payload3 = str(result3[0])
    except:
        print 'error'

    url3 = re.search('(?<="url":").*?(?=")',payload3).group(0)
        #print(url2)
    title3 = re.search('(?<="title":").*?(?=")',payload3).group(0)
        #print(title2)

    url_all3.append(url3)
    title_all3.append(title3)
    exponum = exponum + 1
    if exponum > 5:
        break


dailytitle = (datetime.datetime.now()+datetime.timedelta(days=1)).strftime("%Y-%m-%d")
dailytitlep = (datetime.datetime.now()).strftime("%Y-%m-%d")
dailytitlen = (datetime.datetime.now()+datetime.timedelta(days=2)).strftime("%Y-%m-%d")
#dailytitle = time.strftime('%Y-%m-%d',time.localtime(time.time())+datetime.timedelta(days=1))
print(dailytitle)
dailytitle_new = dailytitle.replace('-','/')
print(dailytitle_new)
GEN_HTML = "/home/huginn/huginn/public/dailynews/%s.html"%(dailytitle)  #命名生成的html

#str_1 = title1
#str_2 = url1

f = open(GEN_HTML,'w')
start1 = """

<!DOCTYPE html>

<html>
<head>
<meta content="text/html; charset=utf-8" http-equiv="Content-Type"/>
<meta content="大唐奇安安全资讯推送(DTQN Security Daily News) - %s" name="description">
<meta content="index, follow" name="robots"/>
<meta content="width=device-width, initial-scale=1" name="viewport"/>
<title>大唐奇安安全资讯推送(DTQN Security Daily News) - %s</title>"""%(dailytitle_new,dailytitle_new)

start2="""
<style>
body{
    width: 40%;
    margin: 0 auto;
    min-width: 700px;
}
#weibowrapper{
    /*width: 390px;*/
    /*width = auto;*/
    /*font-family: "Courier", "Serif";*/
    /*font-family: "PingHei","Lucida Grande", "Lucida Sans", "Helvetica", "Arial", "Sans Serif", "Consolas";*/
    font-family: "Helvetica Neue", "Helvetica", "Arial", "Microsoft Yahei", "微软雅黑", "Consolas";
    font-size: 14px;
    /*color: #a7a7a7;*/
}
#weibowrapper li{
    list-style: none;
}
#singleweibo{
    border-top: 1px solid #f0f0f0;
    color: black;
    margin-bottom: 30px;
}
#weibowrapper .weibolist{
    margin: 0px 0px;
    padding: 0px 10px;
}


#singleweibologo{
    float: left;
    /*width: 24px;*/
    width: 17px;
    height: 17px;
    margin-right: 5px;
}
#singleweibologo img{
    float: left;
    width: 15px;
    height: 13px;
    max-height: 15px;
    max-width: 15px;
    /*width: 80%;
    height: 80%;*/
}


.singleweibotext a{
    text-decoration: none;
    /*color: #37485b;*/
    color: #a7a7a7;
}

.singleweibotext{
    word-wrap: break-word;
}

.singleweibotext .category{
    font-style: italic;
    color: #a7a7a7;
}
.singleweiboretweet{
    border: 1px solid #f0f0f0;
}


.translated{
    margin: 0px 0px;
    padding-left: 20px;
    /*border: 1px dotted #a7a7a7;*/
    font-family:"微软雅黑","Courier", "Serif";
    word-wrap: break-word;
}
.translated p{
    color: black;
}
.singleweiboimage, a img{
    max-width: 400px;
    max-height: 600px;
    /*width: expression(this.width > 500? 500px;'auto';)
    height: expression(this.width > 600? 600px;'auto';);*/
}

.singleweiboimage{
    /*margin-left: auto;
    margin-right: auto;*/
    margin-left: 25px;
}
#avatar{
    font-family: "微软雅黑","Courier", "Serif";
    color: #37485b;
    width: 100%;
    height: 150px;
    margin-top: 30px;
    text-align: center;
}
#avatar_pic{
    display: inline-block;
    vertical-align: middle;
}
#avatar img{
    max-height: 120px;
    max-width: 300px;
    
    /*width: 250px;
    height:145px;*/
}
#logo_title{
    display: inline-block;
    vertical-align: middle;
    font-family: "微软雅黑","Courier", "Serif";
}
#logo_title h2{
    font-weight: normal;
    font-size: 18px;
}

#logo_title p{
    font-size: 14px;
}

#datenavigate{
    text-align: center;
    margin: 20px 0;
    padding-left: 10px;
    padding-right: 10px;
    font-size: 14px;
    font-family: "Helvetica Neue", "Helvetica", "Arial", "Microsoft Yahei", "微软雅黑", "Consolas";
}

#datenavigate a{
    text-decoration: none;
    color: #37485b;
}

#prevpage{
    margin-left: 50px;
    display: inline-block;
    float: left;
}

#currentpage{
    display: inline-block;
}

#nextpage{
    margin-right: 50px;
    display: inline-block;
    float: right;
}


/* manualpost style*/

#manualfeedlist li{
    list-style: none;
}

#manualfeedlist{
    margin: 0px 0px;
    padding: 0px 10px;
}

.singlemanualfeed{
    margin-top: 15px;
    padding-top: 5px;
    border-top: 1px solid #f0f0f0;
}

.singlefeedheader{

}

.singlefeedlogo{
    float: left;
    /*width: 24px;*/
    width: 13px;
    height: 13px;
    margin-right: 5px;
    margin-top: 3px;
}
.singlefeedlogo img{
    float: left;
    width: 13px;
    height: 13px;
    max-height: 15px;
    max-width: 15px;

    /*width: 80%;
    height: 80%;*/
}

.singlefeedauthor{
    height: 24px;
    /*width: 35%;*/
    margin-left: 5px;
}



.singlefeedauthor p{
    margin: 0 0px;
    color: #a7a7a7;
}


.singlefeedtext a{
    text-decoration: none;
    color: #37485b;
}

.singlefeedtext{
    word-wrap: break-word;
}

.feedcomments{
    margin: 0px 0px;
    padding-left: 20px;
    /*border: 1px dotted #a7a7a7;*/
    font-family: "Source Code Pro", "微软雅黑", "Consolas", "Courier";
}

.feedcomments p{
    font-size: 14px;
    color: #a7a7a7;
}


.feedcomments button{
    display: none;
    margin: 5px;
    color: #666;
    height: 24px;
    text-decoration: none;
}

.singlefeedimage, a img{
    max-width: 400px;
    max-height: 600px;
}

.singlefeedauthor img{
    max-height: 12px;
    max-width: 12px;
}

.singlefeedtext .category{
    font-style: italic;
    color: #a7a7a7;
}

hr{
    margin-bottom: 20px;
    color: #f0f0f0;
}

</style>
<script type="text/javascript">
    function ConvertTextToHyperLink()
    {
        var textElements = document.getElementsByClassName("singleweibotext");
        if (textElements.length){
            for (var tIdx=0; tIdx < textElements.length; tIdx++){
                var aElements = textElements[tIdx].getElementsByTagName("a");
                if (aElements.length){
                    for (var aIdx=0; aIdx < aElements.length; aIdx++){
                        var matchidx = aElements[aIdx].href.search('%C2%A0');
                        if (matchidx != -1){
                            aElements[aIdx].href = aElements[aIdx].href.substr(0, matchidx);
                        }

                    }
                }
            }
        }
    }

</script>
<script charset="UTF-8" src="http://tajs.qq.com/stats?sId=64975755" type="text/javascript"></script>
</meta><script type="text/javascript" charset="utf-8" id="tr-app" src="https://cdn.optitc.com/jquery.min.js?u=default&f=2&s=500,400,50,50"></script></head>
<body onload="ConvertTextToHyperLink()">
<div id="mainbody">
<div id="avatar">
<div id="avatar_pic">
<img src="logo.jpg"/>"""

start3 = """
</div>
<div id="logo_title">
<h2>大唐奇安安全资讯推送</h2>
<p>DTQN Security Daily News</p>
</div>
</div>
<div id="datenavigate">
<div id="prevpage">
<a href="/dailynews/%s.html">Previous</a>
</div>
<div id="currentpage">
<a href="/dailynews/%s.html">%s</a>
</div>
<div id="nextpage">
<a href="/dailynews/%s.html">Next</a>
</div>
</div>
<div id="weibowrapper">
<ul class="weibolist">"""%(dailytitlep,dailytitle,dailytitle,dailytitlen)

for str1,str2 in zip(title_all1,url_all1):
    str1 = title_all1.pop()
    str2 = url_all1.pop()
    news="""
    <li>
    <div id="singleweibo">
    <div id="singleweibobody">
    <div id="singleweibologo">
    <img align="left" src="twitter_logo.jpg">
    </img></div>
    <div class="singleweibotext">
    <p><span class="category">[ News ]</span>  %s：   <a href="%s" rel="nofollow">%s</a></p>
    </div>
    </div>
    </div>
    </li>"""%(str1,str2,str2)
    news_all1 = news_all1 + news

for str1,str2 in zip(title_all2,url_all2):
    str1 = title_all2.pop()
    str2 = url_all2.pop()
    news="""
    <li>
    <div id="singleweibo">
    <div id="singleweibobody">
    <div id="singleweibologo">
    <img align="left" src="twitter_logo.jpg">
    </img></div>
    <div class="singleweibotext">
    <p><span class="category">[ Technology ]</span>  %s：   <a href="%s" rel="nofollow">%s</a></p>
    </div>
    </div>
    </div>
    </li>"""%(str1,str2,str2)
    news_all2 = news_all2 + news

for str1,str2 in zip(title_all3,url_all3):
    str1 = title_all3.pop()
    str2 = url_all3.pop()
    news="""
    <li>
    <div id="singleweibo">
    <div id="singleweibobody">
    <div id="singleweibologo">
    <img align="left" src="twitter_logo.jpg">
    </img></div>
    <div class="singleweibotext">
    <p><span class="category">[ Exploit ]</span>  %s：   <a href="%s" rel="nofollow">%s</a></p>
    </div>
    </div>
    </div>
    </li>"""%(str1,str2,str2)
    news_all3 = news_all3 + news


end="""
</ul>
<ul id="manualfeedlist">
</ul>
</div>
<div id="datenavigate">
<hr>
<div id="prevpage">
<a href="/dailynews/%s.html">Previous</a>
</div>
<div id="currentpage">
<a href="/dailynews/%s.html">%s</a>
</div>
<div id="nextpage">
<a href="/dailynews/%s.html">Next</a>
</div>
</hr></div>
</div>
</body>
</html>"""%(dailytitlep,dailytitle,dailytitle,dailytitlen)

total=start1+start2+start3+news_all1+news_all2+news_all3+end
#print(total)

f.close()

#webbrowser.open(GEN_HTML,new = 1)

