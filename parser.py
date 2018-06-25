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
#cursor1.execute("select payload,created_at from mydaily where agent_id in (10,19,46,35,93,96,99) and DATE_FORMAT(created_at,'%Y-%m-%d') = date_format(now(),'%Y-%m-%d');")
cursor1.execute("select payload,created_at from mydaily where agent_id in (10,19,46,35,93,96,99);")
#cursor2.execute("select count(*) from mydaily where agent_id in (10,19,46,35,93,96,99) and DATE_FORMAT(created_at,'%Y-%m-%d') = date_format(now(),'%Y-%m-%d');")
cursor2.execute("select count(*) from mydaily where agent_id in (10,19,46,35,93,96,99);")
num = cursor2.fetchone()
num = int(num[0])


title_list = []
parser = MyHTMLParser()
keyword_processor = flashtext_keyword.KeywordProcessor()
keyword_processor.add_keyword_from_file('keywords.txt')

for i in range(1):
    result = cursor1.fetchone()
    time = str(result[1])
    result = str(result[0])
    url = re.search('(?<="url":").*?(?=")',result).group(0)
    title = re.search('(?<="title":").*?(?=")',result).group(0)
    if title in title_list:
        continue
    else: 
        title_list.append(title)
    #time = re.search('(?<="created_at":").*?(?=")',result).group(0)
    content = re.search('(?<="quanwen":").*?(?=>")',result).group(0)
    content = content+">"
    parser.feed(content)
    content = parser.contentstr
    #print(content1)
    contentnew = content.replace('\\n','')
    contentnew1 = contentnew.replace('\\r','')
    contentnew2 = contentnew1.replace('\\','')
    contentnew3 = contentnew2.replace('  ','')
    print(contentnew)
    print chardet.detect(contentnew3)
    trans1 = contentnew3.decode("ISO-8859-2")
    trans2 = trans1.encode("utf-8")
    translate = translate_baidu_api.baidu_translate(trans2)
    print(translate)
    keywords_found = keyword_processor.extract_keywords(content)
    new_keywords = []
    score = 0

    for kw in keywords_found:
        if kw not in new_keywords:
            new_keywords.append(kw)
            score = score+1

    if not new_keywords:
        continue
    name = "./newsmarkdown/"+time+".markdown"
    keystr = ""
    for k in new_keywords:
        keystr = keystr + "," + str(k)
    #keystr = " ".join(new_keywords)
    #print(keystr)
    writestr = "---\n"+"title:"+title+"\ndate:"+time+"\ntourl:"+url+"\ntags:["+keystr[1:]+"]\n"+"---\n"+contentnew
    #print(writestr)
    f = open(name, 'w')
    f.write(writestr)
    f.close()

cursor1.close()
cursor2.close()
