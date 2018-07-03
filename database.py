import conn
from sqlalchemy import func

def insertToDb(patent):
    try:
        session = conn.Session()
        p = conn.Patent(publicate_number=patent['publicate_number'],
                        publicate_date=patent['publicate_date'],
                        applicate_number=patent['applicate_number'],
                        applicate_date=patent['applicate_date'],
                        applicate_person=patent['applicate_person'],
                        inventor=patent['inventor'],
                        address=patent['address'],
                        classification=patent['classification'],
                        ipproxy="" if ('ipproxy' not in patent) else patent['ipproxy'],
                        proxy_person="" if ('proxy_person' not in patent) else patent['proxy_person'],
                        priority="" if ('priority' not in patent) else patent['priority'],
                        PCT_in_date="" if ('PCT_in_date' not in patent) else patent['PCT_in_date'],
                        PCT_applicate="" if ('PCT_applicate' not in patent) else patent['PCT_applicate'],
                        PCT_publicate="" if ('PCT_publicate' not in patent) else patent['PCT_publicate'])
        session.add(p)
        # commit操作
        session.commit()
        session.close()
    except Exception as e:
        # 待指定error规则
        print("Exception: " + repr(e))
        session.rollback()
        return "<@Error@>"
    finally:
        pass

def countRecords(year):
    try:
        session = conn.Session()
        result = session.query(func.count(conn.Patent.publicate_number)).filter(conn.Patent.publicate_date.like(year + '%')).scalar()
        session.close()
        return result
    except Exception as e:
        # 待指定error规则
        # print("Exception: " + repr(e))
        session.rollback()
        return "<@Error@>"
    finally:
        pass

def addPageCrawled(payload_publicate):
    try:
        session = conn.Session()
        page = conn.Page(strWhere=payload_publicate['strWhere'],
                         pageSize=payload_publicate['pageSize'],
                         pageNow=payload_publicate['pageNow'])
        session.add(page)
        # commit操作
        session.commit()
        session.close()
    except Exception as e:
        # 待指定error规则
        print("Exception: " + repr(e))
        session.rollback()
        return "<@Error@>"
    finally:
        pass

def isCrawled(payload_publicate):
    try:
        session = conn.Session()
        result = session.query(func.count('*')).\
            filter(conn.Page.strWhere == payload_publicate['strWhere']). \
            filter(conn.Page.pageSize == payload_publicate['pageSize']). \
            filter(conn.Page.pageNow == payload_publicate['pageNow']).\
            scalar()
        session.close()
        return result
    except Exception as e:
        # 待指定error规则
        print("Exception: " + repr(e))
        session.rollback()
        return "<@Error@>"
    finally:
        pass

def getUncrawledPageList(strWhere, pageSize, pageNowList):
    crawledPageList = []
    unCrawledPageList = []
    try:
        session = conn.Session()
        query = session.query(conn.Page.pageNow).\
            filter(conn.Page.strWhere == strWhere).\
            filter(conn.Page.pageSize == pageSize)
        for page in query.all():
            crawledPageList.append(page[0])
        print(crawledPageList)
        for item in pageNowList:
            if str(item) not in crawledPageList:
                unCrawledPageList.append(str(item))
        session.close()
        return unCrawledPageList
    except Exception as e:
        # 待指定error规则
        session.rollback()
        return "<@Error@>"
    finally:
        pass

def addTrace(year, time, count):
    try:
        session = conn.Session()
        trace = conn.Trace(year=year,
                          time=time,
                          count=count)
        session.add(trace)
        # commit操作
        session.commit()
        session.close()
    except Exception as e:
        # 待指定error规则
        print("Exception: " + repr(e))
        session.rollback()
        return "<@Error@>"
    finally:
        pass

def getMaxPages(strWhere, pageSize):
    try:
        session = conn.Session()
        result = session.query(conn.MaxPages.maxPages).filter(conn.MaxPages.strWhere == strWhere).\
            filter(conn.MaxPages.pageSize == pageSize).\
            first()
        session.close()
        if result is not None:
            return result[0]
        else:
            return result
    except Exception as e:
        # 待指定error规则
        # print("Exception: " + repr(e))
        session.rollback()
        return "<@Error@>"
    finally:
        pass

def addMaxPages(strWhere, pageSize, maxPages):
    try:
        session = conn.Session()
        maxPages = conn.MaxPages(strWhere=strWhere,
                                 pageSize=pageSize,
                                 maxPages=maxPages)
        session.add(maxPages)
        # commit操作
        session.commit()
        session.close()
    except Exception as e:
        # 待指定error规则
        # print("Exception: " + repr(e))
        session.rollback()
        return "<@Error@>"
    finally:
        pass