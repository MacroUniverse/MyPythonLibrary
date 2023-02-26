import requests
import json
import csv
import datetime

# 打开专栏找到这个地址，多个专栏就手动修改这个，
baseUrl = r'https://zhuanlan.zhihu.com/api/columns/zyshiqq2254461992/' \
          r'articles?include=data%5B%2A%5D.admin_closed_comment%2Ccomment_count%2C' \
          r'suggest_edit%2Cis_title_image_full_screen%2Ccan_comment%2Cupvote' \
          r'd_followees%2Ccan_open_tipjar%2Ccan_tip%2Cvoteup_count%2Cvoting%2' \
          r'Ctopics%2Creview_info%2Cauthor.is_following%2Cis_labeled%2Clabel_in' \
          r'fo&limit=10&offset='

cookies = ''# cookie information


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                         '(KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
           'cookie':cookies}

def findAllInfo(fullurl):
    res = requests.get(fullurl, headers=headers)
    res.encoding = 'utf-8'
    html = res.text
    # print(html)
    data = json.loads(html)
    lists =[]
    for i in range(10):
         try:
            title = data['data'][i]['title']
            times = data['data'][i]['created']
            times = datetime.datetime.fromtimestamp(int(times))
            lists.append([title,times])
            print(title, times)
         except:
            pass
    return  lists




#保存数
def saveData(datas,filename):
    with open(filename,'a+',newline="") as f:
        writer = csv.writer(f)
        for data in datas:
            writer.writerow(data)


if __name__ == '__main__':
    filename = 'C:\\Users\\shizy\\Desktop\\info.csv'
    with open(filename, 'a+', newline="") as f:
        writer = csv.writer(f)
        writer.writerow(['title', 'time'])
    for i in range(4):
        url = baseUrl+str(10*i)
        datas = findAllInfo(url)
        saveData(datas,filename)
