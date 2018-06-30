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
        return session.query(func.count(conn.Patent.publicate_number)).filter(conn.Patent.publicate_date.like(year + '%')).scalar()
    except Exception as e:
        # 待指定error规则
        # print("Exception: " + repr(e))
        session.rollback()
        return "<@Error@>"
    finally:
        pass