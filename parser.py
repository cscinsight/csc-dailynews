# coding: utf8
import MySQLdb
import re
from HTMLParser import HTMLParser
import flashtext_keyword
import sys
import translate_baidu_api
import chardet

reload(sys)
sys.setdefaultencoding('utf8')

contents = []

class MyHTMLParser(HTMLParser): #解析html类
    
    contentstr = str()
    def handle_data(self, data):
        if self.lasttag == 'p':
            #print(data)
            self.contentstr += data
            return self.contentstr

db = MySQLdb.connect('localhost','root','123','huginn_production') #创建一个连接到数据库的接口
cursor1 = db.cursor()
cursor2 = db.cursor()
#cursor1.execute("select payload,created_at from mydaily where agent_id in (10,19,22,35,38,46,49,69,71,93,96,99) and DATE_FORMAT(created_at,'%Y-%m-%d') = date_format(now(),'%Y-%m-%d');")  只生成当天新闻
cursor1.execute("select payload,created_at,id,agent_id from mydaily where agent_id in (10,19,22,35,38,46,49,69,71,75,78,81,84,90,93,96,99,102,105,111,114,117,120,123,125);")  #生成所有新闻
#cursor2.execute("select count(*) from mydaily where agent_id in (10,19,22,35,38,46,49,69,71,93,96,99) and DATE_FORMAT(created_at,'%Y-%m-%d') = date_format(now(),'%Y-%m-%d');")
cursor2.execute("select count(*) from mydaily where agent_id in (10,19,22,35,38,46,49,69,71,75,78,81,84,90,93,96,99,102,105,111,114,117,120,123,125);")#获取新闻总数
num = cursor2.fetchone()
num = int(num[0])#新闻总数
print(num)

def keyscore(filename):  #读出所有关键词
    keys = []
    with open(filename,'r') as f:
        for line in f:
            line = line.lower()
            keys.append(line)
    return keys

def readdict():  #按照分值从不同的文件中读出关键词，并与分值一起放入字典中
    score1 = keyscore('keyscore1.txt')
    score2 = keyscore('keyscore2.txt')
    score3 = keyscore('keyscore3.txt')
    score4 = keyscore('keyscore4.txt')
    score5 = keyscore('keyscore5.txt')
    scdic = {}
    for s in score1:
        scdic[s[:-2]] = 1#存入字典，去掉最后的换行符
    for s in score2:
        scdic[s[:-2]] = 2
    for s in score3:
        scdic[s[:-2]] = 3
    for s in score4:
        scdic[s[:-2]] = 4
    for s in score5:
        scdic[s[:-2]] = 5
    return scdic

def calcscore(newkeywords,scdic):#计算从新闻中取出的关键词的总分
    score = 0
    for keyword in newkeywords:
        keyword = keyword.lower()
        score = score+scdic[keyword]
    return score

title_list = []
agent_dict = {'19':'https://www.zdnet.com','35':'https://meduza.io'}#部分抓取url不全的agent的前缀和其agent_id
parser = MyHTMLParser()
keyword_processor = flashtext_keyword.KeywordProcessor()
keyword_processor.add_keyword_from_file('keywords.txt')

for i in range(num):
    result = cursor1.fetchone()
    time = str(result[1])
    print(time)
    newsid = str(result[2])#新闻id用于生成文章的名字
    newsagent_id = str(result[3])
    result = str(result[0])
    result = result.decode("ISO-8859-2")#对抓取的新闻重新编码
    result = result.encode("utf-8")
    url = re.search('(?<="url":").*?(?=")',result).group(0)
    if newsagent_id in agent_dict.keys():
        url = agent_dict[newsagent_id]+url
        
    title = re.search('(?<="title":").*?(?=")',result).group(0)
    titlename = title.lower()
    if title in title_list:#用于查看是否已经有重复新闻
        continue
    else: 
        title_list.append(title)
    print(titlename)
    print(title)
    try:
        content = re.search('(?<="quanwen":").*?(?=>")',result).group(0)
    except:
        continue
    content = content+">"
    #content = content.decode("ISO-8859-2")
    #content = content.encode("utf-8")
    parser.feed(content)
    content = parser.contentstr
    parser.contentstr = ""
    #print(content1)
    contentnew = content.replace('\\n','')
    contentnew1 = contentnew.replace('\\r','')
    contentnew2 = contentnew1.replace('\\','')
    contentnew3 = contentnew2.replace('  ','')#替换掉文中特殊字符
    #trans = contentnew3[0:5000]调用翻译api
    #print(trans)
    #translate = translate_baidu_api.baidu_translate(trans)
    #print(translate)
    keywords_found = keyword_processor.extract_keywords(content)#返回文中提取的关键字
    new_keywords = []

    for kw in keywords_found:
        if kw not in new_keywords:
            new_keywords.append(kw)

    if not new_keywords:
        continue

    scoredict = readdict() #返回关键字字典
    #score = calcscore(new_keywords,scoredict)
    name = "./newsmarkdown/"+time[0:10] + "-" + newsid+".markdown"
    keystr = ""
    timescore = time
    newer_keywords = []
    for k in new_keywords:
        keystr = keystr + "," + str(k)
        k = k.encode('utf-8')
        newer_keywords.append(k)
    print(new_keywords)
    score = calcscore(new_keywords,scoredict)
    print(score)
    #keystr = " ".join(new_keywords)
    timescore = timescore[0:11] + "00:02:" + str(score)#将分数加到时间里
    writestr = "---\nlayout: post\n"+"title: "+title+"\ndate: "+timescore+"\ntourl: "+url+"\ntags: ["+keystr[1:]+"]\n"+"---\n"+contentnew3#写入文档的内容
    #print chardet.detect(writestr)
    f = open(name, 'w')
    f.write(writestr)
    f.close()

cursor1.close()
cursor2.close()

db.close()
