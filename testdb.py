import database

# item = {}
# item['publicate_number'] = 'sss'
# item['publicate_date'] = 'ss'
#
# database.insertToDb(item)

# print(str(database.countRecords('2012')))

payload_publicate = {'showType': '1', 'strSources': 'pip', 'strWhere': r"OPD=BETWEEN['2014.09.01', '2014.09.10']",
                     'numSortMethod': '4', 'numIp': '0', 'numIpc': '0', 'pageSize': '20',
                     'pageNow': '1'}
# database.addPageCrawled(payload_publicate)
# print(str(database.isCrawled(payload_publicate)))
# print(database.getUncrawledPageList("OPD=BETWEEN['2013.04.11', '2013.04.20']", '20', range(1, 30)))
# database.addTrace('2015', '2018-07-02 16:05:40', '2')
# print(str(database.getMaxPages("OPD=BETWEEN['2011.01.01', '2011.01.10']", '20')))
# database.addMaxPages("OPD=BETWEEN['2011.01.01', '2011.01.10']", '20', 1111)
database.getUncrawledPublicateNumber('2016', 100000, 10000)