# coding: utf8
import MySQLdb
import json
import flashtext_keyword
import chardet
import sys
from parser import keyscore,readdict,calcscore
reload(sys)
sys.setdefaultencoding("utf8")

keyword_processor = flashtext_keyword.KeywordProcessor()
keyword_processor.add_keyword_from_file('keywords.txt')
db = MySQLdb.connect('localhost','root','123','huginn_production')
cursor = db.cursor()
cursor1 = db.cursor()
sql = "select id,payload,created_at from mydaily where agent_id in (60);"
sql1 = "select count(*) from mydaily where agent_id in (60);"
cursor.execute(sql)
cursor1.execute(sql1)
num = int(cursor1.fetchone()[0])
print(num)

#从文章中find关键词
def findwords(content):
    keywords_found = keyword_processor.extract_keywords(content)
    new_keywords = []
    score = 0

    for kw in keywords_found:
        if kw not in new_keywords:
            new_keywords.append(kw)
            score = score + 1
    return new_keywords

#制作markdown
def makemd(time,newsid,score,keywords,author,url,content):
    name = './newsmarkdown/'+time[0:10]+'-'+newsid+'.markdown'
    print(name)
    keystr = ''
    score = score + 10
    timescore = time[0:11] + '00:00:' + str(score)
    for k in keywords:
        keystr = keystr + ',' + str(k)
    if not url:
        url = 'www.baidu.com'
    writestr = "---\nlayout: post\n"+"title: "+author+"\ndate: "+timescore+"\ntourl: "+url+"\ntags: ["+keystr[1:]+"]\n"+"---\n"+content
    f = open(name, 'w')
    f.write(writestr)
    f.close()

for i in range(num):
    result = cursor.fetchone()
    ids = str(result[0])
    payloads = result[1]
    payloads = payloads.decode("ISO-8859-2")
    payloads = payloads.encode("utf-8")
    created_at = str(result[2]) 
    text = json.loads(payloads)#直接将数据用json解析
    print(text['full_text'])
    content = text['full_text']
    time = str(created_at)
    author = text['user']['name']
    url = text['user']['url']
    scoredict = readdict()
    keywords = findwords(content)
    score = calcscore(keywords,scoredict)
    score = score + 10
    makemd(time,ids,score,keywords,author,url,content)
    

cursor.close()
cursor1.close()
db.close()
