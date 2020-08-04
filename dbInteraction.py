import cx_Oracle
from pandas import DataFrame


userName = 'dte'
password = 'Utx_qtf3TYIZ7O'
dbDetails = 'annold02.ae.ge.com:1540/annold02.ae.ge.com'


def connect_db():
    attempts = 0
    print("Connecting to Oracle Database")
    pool = None
    while True:
        try:
            pool = cx_Oracle.SessionPool(userName, password, dbDetails,min=2, max=5, increment=1, encoding="UTF-8")
        except (cx_Oracle.DatabaseError, cx_Oracle.InterfaceError,
                cx_Oracle.OperationalError, cx_Oracle.DataError) as e:
            if attempts < 0:
                connection, attempts = reconnect_db(connection, attempts)
                continue
            else:
                print(type(e).__name__, ':', e.__str__())
                exit(0)
        break
    print("Connected to Oracle Db")
    return pool


def reconnect_db(connection, attempt):
    print('Trying to reconnect..')
    connection = cx_Oracle.connect(userName, password, dbDetails, encoding="UTF-8")
    print('Attempt #' + str(attempt + 1) + '..')
    attempt += 1
    return connection, attempt

def disconnect_pool(connection, pool):
    try:
        connection.commit()
        pool.release(connection)
        print("connection released")
    except cx_Oracle.DatabaseError:
        pass

def disconnect_db(connection, pool):
    try:
        connection.commit()
        pool.release(connection)
        pool.close()
        print("Disconnected from Oracle Database")
    except cx_Oracle.DatabaseError:
        pass


def select_doc_all(cursor):
    sql = "select Doc_id, doc_description, doc_closure_note from DTS_DOCUMENT"
    cursor.execute(sql)
    get_data = cursor.fetchall()
    df = DataFrame(get_data)
    del get_data
    return df


def select_cat_all(cursor):
    sql = "select cat_name from DTS_CATEGORY"
    cursor.execute(sql)
    get_data = cursor.fetchall()
    df = DataFrame(get_data)
    del get_data
    return df


def select_app_all(cursor):
    sql = "select app_name, app_fullname from DTS_APPLICATION"
    cursor.execute(sql)
    get_data = cursor.fetchall()
    df = DataFrame(get_data)
    del get_data
    return df


def select_note_all(cursor):
    sql = "select note_id, note_text, DOC_ID from DTS_NOTE"
    cursor.execute(sql)
    get_data = cursor.fetchall()
    df = DataFrame(get_data)
    del get_data
    return df


def select_atc_all(cursor):
    sql = "select atc_id, atc_name, DOC_ID, cms_uuid from DTS_ATTACHMENT"
    cursor.execute(sql)
    get_data = cursor.fetchall()
    df = DataFrame(get_data)
    del get_data
    return df


def insert_dts_document(cursor, desc, closure_note, CAT_ID):
    sql = "insert into DTS_DOCUMENT(DOC_DESCRIPTION, DOC_CLOSURE_NOTE, CAT_ID) values (:mybv1, :mybv2, :mybv3)"
    cursor.execute(sql, mybv1=desc, mybv2=closure_note, mybv3=CAT_ID)


def insert_dts_note(cursor, text, DOC_ID):
    sql = "insert into DTS_NOTE(NOTE_TEXT, DOC_ID) values (:mybv1, :mybv2)"
    cursor.execute(sql, mybv1=text, mybv2=DOC_ID)


def insert_dts_belongs_to(cursor, DOC_ID, APP_ID):
    sql = "insert into DTS_BELONGS_TO(DOC_ID, APP_ID) values (:mybv1, :mybv2)"
    cursor.execute(sql, mybv1=DOC_ID, mybv2=APP_ID)


def insert_dts_application(cursor, appMap):
    for key, value in appMap.items():
        sql = "insert into DTS_APPLICATION(APP_NAME, APP_FULLNAME) values (:mybv1, :mybv2)"
        cursor.execute(sql, mybv1=value, mybv2=key)


def insert_dts_attachment(cursor, name, uuid, doc_id):
    sql = "insert into DTS_ATTACHMENT(ATC_NAME, CMS_UUID, DOC_ID) values (:mybv1, :mybv2, :mybv3)"
    cursor.execute(sql, mybv1=name, mybv2=uuid, mybv3=doc_id)


def insert_dts_category(cursor, categoryList):
    for name in categoryList:
        sql = "insert into DTS_CATEGORY(CAT_NAME) values (:mybv1)"
        cursor.execute(sql, mybv1=name)


def select_doc_id(cursor):
    sql = "select max(DOC_ID) from DTS_DOCUMENT"
    cursor.execute(sql)
    return cursor.fetchone()[0]


def select_cat_id(cursor, category):
    sql = "select CAT_ID from DTS_CATEGORY where CAT_NAME = :mybv"
    cursor.execute(sql, mybv=category)
    return cursor.fetchone()[0]


def select_app_id(cursor, app):
    sql = "select APP_ID from DTS_APPLICATION where APP_NAME = :mybv"
    if app == 'unknown':
        cursor.execute(sql, mybv='general')
    else:
        cursor.execute(sql, mybv=app)
    return cursor.fetchone()[0]


def select_atc_id(cursor, uuid):
    sql = "select ATC_ID from DTS_ATTACHMENT where CMS_UUID = :mybv"
    cursor.execute(sql, mybv=uuid)
    return cursor.fetchone()[0]


def select_note_id(cursor):
    sql = "select max(NOTE_ID) from DTS_NOTE"
    cursor.execute(sql)
    return cursor.fetchone()[0]


def update_doc_closure_note(cursor, DOC_ID, closure_note):
    sql = "UPDATE dts_document SET doc_closure_note = :mybv1 WHERE doc_id = :mybv2"
    cursor.execute(sql, mybv1=closure_note, mybv2=DOC_ID)


def delete_doc_by_id(cursor, doc_id):
    sql = "Delete dts_attachment where DOC_ID = :mybv1"
    cursor.execute(sql, mybv1=doc_id)
    sql = "Delete dts_note where DOC_ID = :mybv1"
    cursor.execute(sql, mybv1=doc_id)
    sql = "Delete dts_belongs_to where DOC_ID = :mybv1"
    cursor.execute(sql, mybv1=doc_id)
    sql = "Delete DTS_DOCUMENT where DOC_ID = :mybv1"
    cursor.execute(sql, mybv1=doc_id)


def insertAppAndCatTables(connection, cursor, categoryList, appMap):
    print("insert_dts_category")
    insert_dts_category(cursor, categoryList)
    print("insert_dts_application")
    insert_dts_application(cursor, appMap)
    disconnect_db(connection, cursor)
    print("data insertion complete")
    exit(0)


def pushData(cursor, category, app, desc, closure_note):
    print('Cat: ', category)
    CAT_ID = select_cat_id(cursor, category)
    print('CAT_ID: ', CAT_ID)
    print('App: ', app)
    APP_ID = select_app_id(cursor, app)
    print('APP_ID: ', APP_ID)
    insert_dts_document(cursor, desc, closure_note, CAT_ID)
    print("insert_dts_document")
    print(closure_note)
    DOC_ID = select_doc_id(cursor=cursor)
    print('DOC_ID: ', DOC_ID)
    insert_dts_belongs_to(cursor, DOC_ID, APP_ID)
    print("insert_dts_belongs_to")
    return DOC_ID
