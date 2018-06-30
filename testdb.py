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
print(str(database.isCrawled(payload_publicate)))
