import crawl

payload_publicate = {'showType': '1', 'strSources': 'pip', 'strWhere': r'OPD=2012.01', 'numSortMethod': '4', 'numIp': '0',
                     'numIpc': '0', 'pageSize': '20', 'pageNow': '1'}
response = crawl.get_response(payload_publicate)
print(response.text)