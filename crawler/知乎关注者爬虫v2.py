import requests,json,csv,time,execjs,hashlib
from lxml import etree




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
    res = requests.get(fullurl,headers=headers)
    res.encoding = 'utf-8'
    print(res.status_code)

    print('-'*100)
    print(res.url)
    try:
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
    except:
        print('none')

#保存数
def saveData(datas,ii):
    # 输出文件目录
    with open(r'C:\Users\ZeYun-Shi\Desktop\info.csv','a+',newline="") as f:
        writer = csv.writer(f)
        if ii==1:
            writer.writerow(['用户昵称','地址','性别','回答数','视频数','提问数','文章数','专栏数','想法数','关注数','被关注数','被赞同数'])
        for i in datas:
            #print(i)
            writer.writerow(i)
'''
参考：https://blog.csdn.net/Jines__lizhishi/article/details/109272786?utm_medium=distribute.pc_relevant.none-task-blog-BlogCommendFromMachineLearnPai2-4.compare&depth_1-utm_source=distribute.pc_relevant.none-task-blog-BlogCommendFromMachineLearnPai2-4.compare
refer，baseurl 需要修改
f变量后面的一串字符在cookies  d_c0里面
另外需要js代码g_encrypt.js
需要安装jsdom,
cmd下面运行
npm i jsdom -g 
'''
if __name__ == '__main__':
    for ii in range(1,5):#要爬取的页数范围
        url0 = 'https://www.zhihu.com'
        baseurl = r'/api/v4/members/shi-zy-43/followers?include=data%5B*%5D.answer_count%2Carticles_count%2' \
                  r'Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5' \
                  r'D.topics&offset={}&limit=20'.format(20*ii)
        referer = "https://www.zhihu.com/people/shi-zy-43/followers"
        f = "+".join(["3_2.0", baseurl, referer, '"AHBX5N3pBxKPTv1gBCzBG87E0eHEP-SuiOo=|1602548714"'])
        fmd5 = hashlib.new('md5', f.encode()).hexdigest()
        with open('g_encrypt.js', 'r', encoding='utf-8') as w:
            ctx1 = execjs.compile(w.read(), cwd=r'C:\Users\ZeYun-Shi\AppData\Roaming\npm\node_modules')
        encrypt_str = ctx1.call('b', fmd5)
        print('encrypt_str\n', encrypt_str)
        # 1.0_aXOB66H068OfUBF0yqtqNJ98QTxYn9F0M_tyr0uqeRYf

        # 1.0_aRt0QiuyUwFpHuFqBLtyoH9qbL2XgC20K7FqFveqNgYp

        headers = {
            'cookie': '_zap=f169ec50-82f6-4d5b-a41d-e95d4fd1a544; d_c0="AHBX5N3pBxKPTv1gBCzBG87E0eHEP-SuiOo=|1602548714"; capsion_ticket="2|1:0|10:1602582562|14:capsion_ticket|44:N2NkNTQ5OTE1ODQwNDJlNTg5ZTdiNmEzOTBiOTA2Yjg=|faf1fafe0d7b7547207b1ec021e564d906fe99404032a13e71e221f5321f6eeb"; z_c0="2|1:0|10:1602582563|4:z_c0|92:Mi4xZGhMMUFRQUFBQUFBY0ZmazNla0hFaVlBQUFCZ0FsVk5JOFp5WUFBby1ESzJTcTM5WnI1NEpONzBOZERrSHZNa25B|5ae727b00fbc1e137112add3d79addd8bb9fa9253121f64586c4f5341dac001b"; tst=h; tshl=; q_c1=36a71808665343be8adb56fc1ab2ddcf|1602582583000|1602582583000; ff_supports_webp=1; _ga=GA1.2.2114222068.1604826726; _gid=GA1.2.1915507277.1604826726; _xsrf=38ee37b6-ea8f-4226-baef-bbedc39b2138; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1604797790,1604826495,1604827446,1604829559; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1604831379; KLBRSID=4843ceb2c0de43091e0ff7c22eadca8c|1604831388|1604829557',
            'referer': 'https://www.zhihu.com/people/shi-zy-43/followers',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36',
            'x-zse-83': '3_2.0',
            'x-zse-86': '1.0_' + encrypt_str,
            # 'x-zst-81': '3_2.0ae3TnRUTEvOOUCNMTQnTSHUZo02p-HNMZBO8YDQ06XtuQ_F0K6P0EQuy-LS9-hp1DufI-we8gGHPgJO1xuPZ0GxCTJHR7820XM20cLRGDJXfgGCBxupMuD_Ie8FL7AtqM6O1VDQyQ6nxrRPCHukMoCXBEgOsiRP0XL2ZUBXmDDV9qhnyTXFMnXcTF_ntRueTh7CYVbrMk7x9uDHB2vxm8bc0khpVQBNLZcXCpGNO-CpODgp9RhpOxUVBSGCPv_21YUVCIq9yS7NOSDC8RhtfcQwObup_EU39tBOOgb3BbDxp6X39gqeVVrw9QGesrbxCGhpMkJ3MyrOp_wCBMGXMS_XKjq38EGt0pJxKCbXYECX1V9tm5qfzWwLKSLep68Fq6h3MxJC1kTopcwCG1DSMiJU1BgcVfhOGlGtyprxLxDOsSgLq88wGEuLKSwtffhp1xBYfqvHGyCY8JhFKhBH1EvNmW9SsFceq-hXB-r3C'
        }
        fullurl = url0+baseurl
        datas = findAllInfo(fullurl)
        saveData(datas,ii)
        # print(fullurl)
        # rs = requests.get(fullurl,headers=headers)
        # print(rs.status_code)
