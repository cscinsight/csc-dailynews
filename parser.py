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

class MyHTMLParser(HTMLParser):
    
    contentstr = str()
    def handle_data(self, data):
        if self.lasttag == 'p':
            #print(data)
            self.contentstr += data
            return self.contentstr

db = MySQLdb.connect('localhost','root','123','huginn_production')
cursor1 = db.cursor()
cursor2 = db.cursor()
#cursor1.execute("select payload,created_at from mydaily where agent_id in (10,19,22,35,38,46,49,69,71,93,96,99) and DATE_FORMAT(created_at,'%Y-%m-%d') = date_format(now(),'%Y-%m-%d');")
cursor1.execute("select payload,created_at,id from mydaily where agent_id in (10,19,22,35,38,46,49,69,71,93,96,99);")
#cursor2.execute("select count(*) from mydaily where agent_id in (10,19,22,35,38,46,49,69,71,93,96,99) and DATE_FORMAT(created_at,'%Y-%m-%d') = date_format(now(),'%Y-%m-%d');")
cursor2.execute("select count(*) from mydaily where agent_id in (10,19,22,35,38,46,49,69,71,93,96,99);")
num = cursor2.fetchone()
num = int(num[0])
print(num)


title_list = []
parser = MyHTMLParser()
keyword_processor = flashtext_keyword.KeywordProcessor()
keyword_processor.add_keyword_from_file('keywords.txt')

for i in range(num):
    result = cursor1.fetchone()
    time = str(result[1])
    print(time)
    newsid = str(result[2])
    result = str(result[0])
    #print chardet.detect(time)
    #print chardet.detect(newsid)
    result = result.decode("ISO-8859-2")
    result = result.encode("utf-8")
    #print chardet.detect(result)
    url = re.search('(?<="url":").*?(?=")',result).group(0)
    title = re.search('(?<="title":").*?(?=")',result).group(0)
    titlename = title.lower()
    #titlename = titlename.replace(' ','-')
    #titlename = titlename.replace('\\','-')
    #titlename = titlename.replace('/','-')
    #titlename = titlename.replace(':','-')
    #titlename = titlename.replace("'",'')
    #titlename = titlename.replace('.','')
    #titlename = titlename.replace(',','')
    #titlename = titlename.replace('?','')
    #titlename = titlename.replace('#','')
    if title in title_list:
        continue
    else: 
        title_list.append(title)
    print(titlename)
    print(title)
    content = re.search('(?<="quanwen":").*?(?=>")',result).group(0)
    content = content+">"
    parser.feed(content)
    content = parser.contentstr
    parser.contentstr = ""
    #print(content1)
    contentnew = content.replace('\\n','')
    contentnew1 = contentnew.replace('\\r','')
    contentnew2 = contentnew1.replace('\\','')
    contentnew3 = contentnew2.replace('  ','')
    #print(contentnew)
    #print chardet.detect(contentnew3)
    #trans1 = contentnew3.decode("ISO-8859-2")
    #trans2 = trans1.encode("utf-8")
    #trans3 = trans2[0:5000]
    #print(trans3)
    #translate = translate_baidu_api.baidu_translate(trans3)
    #print(translate)
    keywords_found = keyword_processor.extract_keywords(content)
    new_keywords = []
    score = 0

    for kw in keywords_found:
        if kw not in new_keywords:
            new_keywords.append(kw)
            score = score+1

    if not new_keywords:
        continue
    name = "./newsmarkdown/"+time[0:10]+"-"+newsid+".markdown"
    #print(name)
    keystr = ""
    for k in new_keywords:
        keystr = keystr + "," + str(k)
    #keystr = " ".join(new_keywords)
    writestr = "---\nlayout: post\n"+"title: "+title+"\ndate: "+time+"\ntourl: "+url+"\ntags: ["+keystr[1:]+"]\n"+"---\n"+contentnew3
    #print chardet.detect(writestr)
    f = open(name, 'w')
    f.write(writestr)
    f.close()

cursor1.close()
cursor2.close()

db.close()
