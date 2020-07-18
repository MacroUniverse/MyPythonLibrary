# 把代码粘贴到 Anaconda 的 Spyder 中即可运行
# baseurl 的来源见 "知乎关注着爬虫.png"， 注意 "offset=" 后面的东西要删掉（程序会自动补上）
# headers 中的 'cookie' 也需要替换， 向下拉就可以找到
# 在主函数的 for 循环中 0 代表关注列表的第一页，每页 20 个用户数据如果中途网络断开会自动继续
# 输出文件目录在 saveData() 函数中改
import requests
from lxml import etree
import json
import csv
import time
baseurl = r'https://www.zhihu.com/api/v4/members/MacroUniverse/followers?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset='

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
           'cookie':'_zap=aeeb0acd-c135-4f1f-8a99-bd94753d1ea5; _xsrf=1fppdHKMlZiojzd4EYp5d6zr4epM44tO; _ga=GA1.2.740748297.1590598624; d_c0="ADDXMObXVRGPTjgdnu6zw0qE3VFFbCH1bCA=|1590598626"; z_c0="2|1:0|10:1590598634|4:z_c0|92:Mi4xYlFjMEFBQUFBQUFBTU5jdzV0ZFZFU1lBQUFCZ0FsVk42dW03WHdBSU01eV9nekE3UFBpMnZ1YjJWUlN4Um51b19n|2443bd9f2f01ad03815efe70ced7b22bd8943f8f08b3363e78129fa1cdefeca4"; tst=f; q_c1=5ccd71cafb4446e192d75bd97be4ae45|1593279101000|1590645471000; __utmv=51854390.100-1|2=registration_date=20140204=1^3=entry_date=20140204=1; _gid=GA1.2.1831438759.1594188689; __utma=51854390.740748297.1590598624.1594498592.1594630978.3; __utmz=51854390.1594630978.3.3.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/question/405776597; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1594668638,1594672833,1594690031,1594699194; SESSIONID=IlMea59OQ5Cj5b7Co3P1K8MbkqtFUhQlns3S7eMizDM; JOID=VVAUC0qYFIqfyvFObZcdUjqUMdV63nHO863LfivPLsD89pV2J9xSh8_D905t__lDVStLT1Uzv2tlF_apoUFrXnk=; osd=V18VAU2aG4uVzfNBbJ0aUDWVO9J40XDE9K_EfyHILM_9_JJ0KN1YgM3M9kRq_fZCXyxJQFQ5uGlqFvyuo05qVH4=; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1594706268; KLBRSID=53650870f91603bc3193342a80cf198c|1594706840|1594699193; _gat_gtag_UA_149949619_1=1'}


#h获取一页的信息
def findOneInfo(url):
    res = requests.get(url, headers=headers)
    res.encoding = 'utf-8'
    data = res.text
    data2 =  etree.HTML(data)
    data3 = data2.xpath("//div[@class='ProfileMain-header']//span[@class='Tabs-meta']")
    data4 = data2.xpath("//strong[@class='NumberBoard-itemValue']")

    #print(data5)
    try:
         data5 = data2.xpath("//div[@class='css-vurnku']")[0].text
         data6 = data5.split()[1]
    except:
        data6 = 0
    #print('当前url为：  ',url)
    dicts ={}
    try:
        dicts['AnswerNumber'] = data3[0].text
    except:
        dicts['AnswerNumber'] =0
    try:
        dicts['videoNumber'] = data3[1].text
    except:
        dicts['videoNumber'] = 0
    try:
        dicts['QuestionNumber'] = data3[2].text
    except:
        dicts['QuestionNumber'] = 0
    try:
        dicts['ArticleNumber']= data3[3].text
    except:
        dicts['ArticleNumber']= 0
    try:
        dicts['TabsNumber'] = data3[4].text
    except:
        dicts['TabsNumber'] = 0
    try:
        dicts['ThinkNumber'] = data3[5].text
    except:
        dicts['ThinkNumber'] = 0
    try:
        dicts['num1'] = data4[0].text
    except:
        dicts['num1'] = 0
    try:
        dicts['num2'] = data4[1].text
    except:
        dicts['num2'] = 0
    try:
        dicts['num3'] = data6
    except:
        dicts['num3'] = 0
    return dicts

#获取所有信息
def findAllInfo(fullurl):
    res = requests.get(fullurl, headers=headers)
    res.encoding = 'utf-8'
    data1 = res.text
    data2 = json.loads(data1)
    lists = []
    iii=0
    for i in data2['data']:
        print('iii=',iii)
        iii += 1
        info = {}
        info['name'] = i['name']
        info['url'] = i['url']
        info['xb'] = i['gender']
        # lists.append(info)
        ll = info['url'].split('/')
        newurl = 'https://www.zhihu.com/people/' + ll[-1]
        for j in range(0, 1000):
            try:
                dicts = findOneInfo(newurl)
            except:
                print('exception found, might be network issue, trying again...')
                time.sleep(5)
                continue
            break
        info2 = [info['name'], info['url'], info['xb']]
        for k, v in dicts.items():
            info2.append(dicts[k])
        # print(info)
        lists.append(info2)

    return lists

#保存数
def saveData(datas,ii):
    # 输出文件目录
    with open('C:\\Users\\addis\\Desktop\\info.csv','a+',newline="") as f:
        writer = csv.writer(f)
        if ii==0:
            writer.writerow(['用户昵称','地址','性别','回答数','视频数','提问数','文章数','专栏数','想法数','关注数','被关注数','被赞同数'])
        for i in datas:
            #print(i)
            writer.writerow(i)
# if __name__ == '__main__':
for ii in range(0,404):#要爬取的页数范围
    print('第%d页'%ii)
    fullurl =   baseurl    +str(ii*20)+'&limit=20'
    datas = findAllInfo(fullurl)
    saveData(datas,ii)
