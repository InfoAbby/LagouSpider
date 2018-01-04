import json
import random
import queue
import threading
import time
from multiprocessing.pool import Pool
from http.cookies import SimpleCookie
import requests
import xlwt
from fake_useragent import UserAgent


# 获取数据 存储
def get_json(url, datas):
    tag = ['positionId', 'language', 'companyFullName', 'city', 'education', 'positionName', 'salary', 'workYear',
           'companySize']
    ua = UserAgent()

    ip_list = ['219.155.10.242', '117.92.178.89', '123.149.160.164', '180.118.242.248', '219.138.58.219',
               '119.29.12.129', '14.112.76.25']
    proxies = {
        "http": "http://" + random.choice(ip_list),

    }
    headers = {
        'User-Agent': ua.random,
        'Host': 'www.lagou.com',
        'Referer': 'https://www.lagou.com/jobs/list_Java?px=default&city=%E5%8C%97%E4%BA%AC',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Origin': 'https://www.lagou.com'
    }

    cookies = {
        'Cookies': 'JSESSIONID=ABAAABAAAFCAAEG67DB1C45FDFE668CCB5868146EF8DA6C; user_trace_token=20180102145412-b0a98c1d-f845-420d-8c23-6715b8f5dd07; LGUID=20180102145413-be0b6658-ef89-11e7-b9ca-525400f775ce; index_location_city=%E5%85%A8%E5%9B%BD; TG-TRACK-CODE=index_navigation; _gid=GA1.2.1882972898.1514876055; _ga=GA1.2.1050735134.1514876055; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1514876054,1514878270,1514879661; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1514879731; LGRID=20180102155529-4d2fe487-ef92-11e7-b9df-525400f775ce; SEARCH_ID=568433a750894f13a817dca5bc1ef830'
    }

    # 获取到的内容
    content = requests.post(url=url, headers=headers, data=datas, cookies=cookies, proxies=proxies)
    result = content.json()

    if result['success'] == True:
        info = result['content']['positionResult']['result']
        info_list = []
        for job in info:
            information = []
            for t in tag:
                if t == 'language':
                    information.append(datas['kd'])
                else:
                    information.append(job[t])
            info_list.append(information)
        # 将列表对象进行json格式的编码转换,其中indent参数设置缩进值为2
        json.dumps(info_list, ensure_ascii=False, indent=2)
        print(info_list)
        time.sleep(8 + random.randint(3, 5))
        return info_list


def main(kd, city):
    page = 15
    info_result = []

    title = ['岗位id', '语言', '公司全名', '工作地点', 'a学历要求', '职位名称', '薪资', '工作年限', '公司规模']

    info_result.append(title)
    for x in range(1, page + 1):
        if x == 1:
            boo = 'true'
        else:
            boo = 'false'
        url = 'https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false&isSchoolJob=0'
        datas = {
            'first': boo,
            'pn': x,
            'kd': kd,
            'city': city
        }
        info = get_json(url, datas)
        info_result = info_result + info
        # 创建workbook,即excel
        workbook = xlwt.Workbook(encoding='utf-8')
        # 创建表,第二参数用于确认同一个cell单元是否可以重设值
        worksheet = workbook.add_sheet('lagouzp', cell_overwrite_ok=True)
        for i, row in enumerate(info_result):
            for j, col in enumerate(row):
                worksheet.write(i, j, col)
            workbook.save('F:\\Data\\lagouzp.xls')


if __name__ == '__main__':
    kd = ['Java', 'Python', 'PHP', 'C++', 'C#', 'Ruby']
    place = ['北京', '上海', '广州', '长沙', '深圳', '杭州', '成都', '武汉', '苏州']

    ip_list = ['119.6.136.122', '114.106.77.14']
    pool = Pool()

    for k in kd:
        for city in place:
            pool.apply(main, (k, city,))
