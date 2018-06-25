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
url_all = []
title_all = []
news_all1 = """ """
news_all2 = """ """
news_all3 = """ """
newsnum = 0
technum = 0
exponum = 0
gradescores = [1,2,3,4]
keywords = [['DNS','SSRF','exploitation','0day','exploit','hack','attack','GDPR','AWS','APT','National Security Agency','NSA','DHS','Department of Homeland Security','NPPD','National Security Council','CIO Council','American Technology Council','ICI-IPC','CTS','Office of Cyber Affairs','Office of International Communications and Information Policy','Cyber Security Division','The Office of the Director of National Intelligence','CTIIC','NIST','GAO','Office of the Cyber Policy','DoD Cyber Crime Center','Cyber Command','CIO','CISO','White House Cybersecurity Coordinator','The Coordinator for Cyber Issues','law','act','bill','draft','regulations','military exercise'],['DOD','NIPRNEet','Biometric','China','crowdstrike','WhatsApp','McBee Strategic Consulting','eck Madigan Jones','Van Scoyoc Associates','Franklin Square Group','Monument Policy Group','Ogilvy Government Relations','CSIS','CNAS','Atlantic Council','Brookings Institution','Council on Foreign Relations','EastWest Institute','Wilson Center','Cato Institute','ITIF','CDI'],['TLS','WebAuthn','Breaking CFI','Scanning Activity','vincentyiu','Falcon X','Cybersecurity Tech Accord'],['user to system EoP','MikroTik','Telegram']]
sql1 = "select payload from mydaily where agent_id in (10,19,22,25,26,32,35,28,46,49,69,71,75) and DATE_FORMAT(created_at,'%Y-%m-%d') = date_format(now(),'%Y-%m-%d');"
sql2 = "select payload from mydaily where agent_id in (13,14,41,78,81,84,87,90,93,96,99,102,105) and DATE_FORMAT(created_at,'%Y-%m-%d') = date_format(now(),'%Y-%m-%d');"
#sql1 = "select payload from mydaily where agent_id in (10,19,22,25,26,32,35,28,46,49,69,71,75);"
#sql2 = "select payload from mydaily where agent_id in (13,14,41,78,81,84,87,90,93,96,99,102,105);"
#sql3 = "select payload from mydaily where agent_id in (56);"
sql3 = "select payload from mydaily where agent_id in (56) and DATE_FORMAT(created_at,'%Y-%m-%d') = date_format(now(),'%Y-%m-%d');"
sql10 = ["select count(*) from mydaily where agent_id in (10,19,22,25,26,32,35,28,46,49,69,71,75) and DATE_FORMAT(created_at,'%Y-%m-%d') = date_format(now(),'%Y-%m-%d');","select count(*) from mydaily where agent_id in (13,14,41,78,81,84,87,90,93,96,99,102,105) and DATE_FORMAT(created_at,'%Y-%m-%d') = date_format(now(),'%Y-%m-%d');","select count(*) from mydaily where agent_id in (56) and DATE_FORMAT(created_at,'%Y-%m-%d') = date_format(now(),'%Y-%m-%d');"]


cursor1.execute(sql1)
cursor2.execute(sql2)
cursor3.execute(sql3)

for i in range(3):
    cursor10.execute(sql10[i])
    number = cursor10.fetchone()
    number = int(number[0])
    num.append(number)
    print num

def score(payload):#根据关键词对新闻进行打分
    j=3
    payloadscore=0
    for keyword in keywords:
        gradescore = gradescores[j]
        j = j-1
        for k in keyword:
            keywordnum = payload.count(k)
            payloadscore = keywordnum*gradescore + payloadscore
    print payloadscore
    return payloadscore

def genpayload(numcan,cursor):#从数据库中取出当天新闻进行分析打分，将排序后的数据送出
    dict1 = {}
    title_all = []
    url_all = []
    for i in range(numcan):
    #try:
    #cursor.execute(sql1)
        result = cursor.fetchone()
        #print(type(result1))
        payload = str(result[0])
        payload1score = score(payload)
        title = re.search('(?<="title":").*?(?=")',payload).group(0)
        print(title)
        dict1[payload] = payload1score
    #except:
     #   print 'error'

    listdict = zip(dict1.values(), dict1.keys())
    listdict = sorted(listdict,key=lambda x:x[0])
    newsnum = 0
    for i in range(numcan):
        scoreword,payload = listdict.pop()
        print("asdhfaiuhsdfkasdfjaldsfjajdsfasdfasdfasdfalkfjlknlnkv;adijfwowerqewopp")
        url = re.search('(?<="url":").*?(?=")',payload).group(0)
    #print(url1)
        title = re.search('(?<="title":").*?(?=")',payload).group(0)
        print(title)
        print(scoreword)
        url_all.append(url)
        title_all.append(title)
        #print(title_all)
        newsnum = newsnum+1
        if newsnum>10:
            break
    title_all.reverse()
    url_all.reverse()
    return title_all, url_all

title_all1, url_all1 = genpayload(num[0],cursor1)
title_all2, url_all2 = genpayload(num[1],cursor2)
title_all3, url_all3 = genpayload(num[2],cursor3)


dailytitle = (datetime.datetime.now()+datetime.timedelta(days=1)).strftime("%Y-%m-%d")#生成当天时间
dailytitlep = (datetime.datetime.now()).strftime("%Y-%m-%d")
dailytitlen = (datetime.datetime.now()+datetime.timedelta(days=2)).strftime("%Y-%m-%d")
#dailytitle = time.strftime('%Y-%m-%d',time.localtime(time.time())+datetime.timedelta(days=1))
print(dailytitle)
dailytitle_new = dailytitle.replace('-','/')
print(dailytitle_new)
GEN_HTML = "/home/cscinsight.github.io/%s.html"%(dailytitle)  #命名生成的html

#str_1 = title1
#str_2 = url1

f = open(GEN_HTML,'w')
start1 = """

<!DOCTYPE html>

<html>
<head>
<meta content="text/html; charset=utf-8" http-equiv="Content-Type"/>
<meta content="CSC Security Daily News - %s" name="description">
<meta content="index, follow" name="robots"/>
<meta content="width=device-width, initial-scale=1" name="viewport"/>
<title>CSC Security Daily News - %s</title>"""%(dailytitle_new,dailytitle_new)

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
<h2>CSCINSIGHT</h2>
<p>Security Daily News</p>
</div>
</div>
<div id="datenavigate">
<div id="prevpage">
<a href="/%s.html">Previous</a>
</div>
<div id="currentpage">
<a href="/%s.html">%s</a>
</div>
<div id="nextpage">
<a href="/%s.html">Next</a>
</div>
</div>
<div id="weibowrapper">
<ul class="weibolist">"""%(dailytitlep,dailytitle,dailytitle,dailytitlen)

for str1,str2 in zip(title_all1,url_all1):
    str1 = title_all1.pop()
    str2 = url_all1.pop()
    if re.search(str1, news_all1) is not None:#检查是否有重复
        continue 
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
    if re.search(str1, news_all2) is not None:
        continue
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
    if re.search(str1, news_all3) is not None:
        continue
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
<a href="/%s.html">Previous</a>
</div>
<div id="currentpage">
<a href="/%s.html">%s</a>
</div>
<div id="nextpage">
<a href="/%s.html">Next</a>
</div>
</hr></div>
</div>
</body>
</html>"""%(dailytitlep,dailytitle,dailytitle,dailytitlen)

total=start1+start2+start3+news_all1+news_all2+news_all3+end
#print(total)

f.write(total)
f.close()

webbrowser.open(GEN_HTML,new = 1)

