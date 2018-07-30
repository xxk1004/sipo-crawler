import json
import os
import random
import time
import traceback
from lxml import etree
import requests
import conn
import database
import sys
from multiprocessing import Process, Pool, Lock, Manager

POLLING_NUM = 50

TOTAL_RECORD_DICT = {
    '2017': 1270363,
    '2016': 1045720,
    '2015': 955350,
    '2014': 777340,
    '2013': 632590,
    '2012': 543300,
    '2011': 368440
}

def get_response(payload_publicate, ip_ports, proxies, retries):
    url = 'http://epub.sipo.gov.cn/patentoutline.action'
    #    payload_publicate = {'showType': '1', 'strSources': 'pip', 'strWhere': r'OPD=2012.01.18',
    #                         'numSortMethod': '4', 'numIp': '0', 'numIpc': '0', 'pageSize': '20', 'pageNow':'1'}
    # 经过测试发现, pageSize最大可以取到20
    USER_AGENTS = [
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
        "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
        "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
        "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
        "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
        "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
        "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
        "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
        "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10"
    ]
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'keep-alive',
        'User-Agent': random.choice(USER_AGENTS),
        'Origin': 'http://epub.sipo.gov.cn',
        'Referer': 'http://epub.sipo.gov.cn/',
        'Host': 'epub.sipo.gov.cn'
    }
    try:
        if retries == 5:
            response = requests.post(url, data=payload_publicate, headers=headers, timeout=60)
        else:
            response = requests.post(url, data=payload_publicate, headers=headers, timeout=60, proxies=proxies)
        if response.status_code == 200:
            response = etree.HTML(response.content)
            return response
        elif retries > 0:
            retries = retries - 1
            time.sleep(10)
            index = random.choice(range(70))
            ip = ip_ports[index][0]
            port = ip_ports[index][1]
            proxies = {
                'http': 'http://%s:%s' % (ip, port),
                'https': 'http://%s:%s' % (ip, port)
            }
            return get_response(payload_publicate, ip_ports, proxies, retries)
        else:
            return '<@Error@>'
    except requests.exceptions.Timeout:
        print(u'请求超时，正在重试...')
        if retries > 0:
            retries = retries - 1
            return get_response(payload_publicate, ip_ports, proxies, retries)
        else:
            return '<@Error@>'
    except requests.exceptions.ConnectionError:
        print(u'网络连接失败，正在重试...')
        if retries > 0:
            retries = retries - 1
            return get_response(payload_publicate, ip_ports, proxies, retries)
        else:
            return '<@Error@>'
    except Exception as e:
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " " + " occured exception:" + traceback.format_exc())
        if retries > 0:
            retries = retries - 1
            return get_response(payload_publicate, ip_ports, proxies, retries)
        else:
            return '<@Error@>'


def parse(response, payload_publicate):
    # print("crawling page ", self.pageNow) response里不可能得到当前页码
    # print("start_parse")
    cp_linrs = response.xpath("//div[@class='main']//div[@class='cp_box']//div[@class='cp_linr']")
    flag = 1
    for cp_linr in cp_linrs:
        # item['title'] = cp_linr.xpath("./h1/text()").extract()[0]
        # extract出来是一个list
        item = {}
        item['publicate_number'] = str(cp_linr.xpath("./ul/li[1]/text()")[0][6:])  # 第一个元素
        item['publicate_date'] = str(cp_linr.xpath("./ul/li[2]/text()")[0][6:])
        item['applicate_number'] = str(cp_linr.xpath("./ul/li[3]/text()")[0][4:])
        item['applicate_date'] = str(cp_linr.xpath("./ul/li[4]/text()")[0][4:])
        item['applicate_person'] = str(cp_linr.xpath("./ul/li[5]/text()")[0][4:])
        item['inventor'] = str(cp_linr.xpath("./ul/li[6]/text()")[0][4:])
        item['address'] = str(cp_linr.xpath("./ul/li[8]/text()")[0][3:])
        item['classification'] = str(cp_linr.xpath("./ul/li[9]/text()")[0][4:])  # 这样只会返回紧跟的分类号
        detail = cp_linr.xpath("./ul/li[9]/div/ul/li")
        if (detail):
            for li in detail:
                text = li.xpath("./text()")[0]
                if text[0] == u"专":
                    item['ipproxy'] = str(text[7:])
                elif text[0] == u"代":
                    item['proxy_person'] = str(text[4:])
                elif text[0] == u"优":
                    item['priority'] = str(text[4:])
                elif text[:4] == u"PCT进":
                    item['PCT_in_date'] = str(text[11:])
                elif text[:4] == u"PCT申":
                    item['PCT_applicate'] = str(text[8:])
                elif text[:4] == u"PCT公":
                    item['PCT_publicate'] = str(text[8:])
                else:
                    # print(text.encode("utf8")) # 不知道是不是除了上面的几个字段之外还有没有其他的字段..应该这里是分类号
                    item['classification'] += str(text)
        # 将数据提交给模块pipelines处理
        #        return item
        # with open('data.txt', 'a') as f:
        #     f.write(json.dumps(item) + '\n')
        # print('Raw: ' + item['applicate_person'])
        # print('After string: ' + str(item['applicate_person']))
        # print('After encode: ' + str(item['applicate_person']).encode('utf8'))
        # print(str(item['applicate_person']).encode('utf8'))
        # for v, k in item.items():
        #     print('{v}:{k}'.format(v=v, k=k))
        result = database.insertToDb(item)
        if (result == "<@Error@>"):
            flag = 0
    # if flag == 1:
    #     database.addPageCrawled(payload_publicate)
        # if (result == "<@Error@>"):
        #     print("Database exception")


# %%


def crawl(payload_publicate, pids, lock, cnt, ip_ports):
    pid = os.getpid()
    with lock:
        if pid not in pids:
            pids.append(pid)
            conn.engine.dispose()
            fs = open(logFile, "a+")
            fs.write('Invoked Engine.dispose()\n')
            fs.close()
    try:
        index = random.choice(range(70))
        ip = ip_ports[index][0]
        port = ip_ports[index][1]
        proxies = {
            'http': 'http://%s:%s' % (ip, port),
            'https': 'http://%s:%s' % (ip, port)
        }
        # with lock:
        #     fs = open(logFile, "a+")
        #     fs.write("cnt: " + str(cnt) + '\n')
        #     fs.write("pid: " + str(pid) + '\n')
        #     for v, k in proxies.items():
        #         fs.write('{v}:{k}'.format(v=v, k=k) + '\n')
        #     for v, k in payload_publicate.items():
        #         fs.write('{v}:{k}'.format(v=v, k=k) + '\n')
        #     fs.write('\n')
        #     fs.close()
        response = get_response(payload_publicate, ip_ports, proxies, 5)
        if response != '<@Error@>':
            parse(response, payload_publicate)
    except:
        with lock:
            fs = open(logFile, "a+")
            fs.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " " + str(cnt) + " in PID" + str(
                pid) + " occured exception:" + '\n')
            fs.write(traceback.format_exc())
            fs.close()

    time.sleep(5)

if __name__ == '__main__':
    currentPath = os.path.split(os.path.realpath(__file__))[0]
    if not os.path.exists(currentPath + "/log/completion/"):
        os.makedirs(currentPath + "/log/completion/")
    year = sys.argv[1]
    logFile = currentPath + "/log/completion/" + sys.argv[1] + ".log"
    total_record = TOTAL_RECORD_DICT[year]

    with Manager() as manager:
        pool = Pool(POLLING_NUM)
        cnt = 0
        pids = manager.list()
        lock = manager.Lock()
        for start in range(int(total_record / 10000) + 1):
            r = requests.get('http://127.0.0.1:8000/?types=0&count=70')
            ip_ports = json.loads(r.text)
            uncrawledPublicateNumberList = database.getUncrawledPublicateNumber(year, start * 10000, 10000)
            for uncrawledPublicateNumber in uncrawledPublicateNumberList:
                payload_publicate = {'showType': '1', 'strSources': '', 'strWhere': r'PN=' + uncrawledPublicateNumber,
                                     'numSortMethod': '', 'numIp': '', 'numIpc': '', 'pageSize': '3',
                                     'pageNow': '1'}
                with lock:
                    fs = open(logFile, "a+")
                    fs.write(payload_publicate['strWhere'] + '\n')
                    fs.write('\n')
                    fs.close()
                pool.apply_async(func=crawl, args=(payload_publicate, pids, lock, cnt, ip_ports,))
                cnt = cnt + 1
        pool.close()
        fs = open(logFile, "a+")
        fs.write('Pool has been closed.\n')
        fs.close()
        pool.join()
        for worker in pool._pool:
            assert not worker.is_alive()