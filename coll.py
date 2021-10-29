import sqlite3
import mconfig
import mfilters
import mgeneric

TABLE_NAME="coll"
COL_ID="id"
COL_NAME="name"
COL_GENDER="gender"
COL_AGE="age"

def drop_coll_table(db=mconfig.DB_NAME):
    mgeneric.drop_table(TABLE_NAME,db)

def create_coll_table(db=mconfig.DB_NAME):
    print("create_coll_table()")
    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    sql = f"""
    create table if not exists {TABLE_NAME} (
        {COL_ID} integer primary key,
        {COL_NAME} text not null,
        {COL_GENDER} text not null,
        {COL_AGE} integer not null
    )
    """
    print("sql=" + sql)
    cursor.execute(sql)
    connection.commit()
    connection.close()


def insert_coll(values,db=mconfig.DB_NAME):
    print(f"insert_coll(values={values},db={db})")
    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    sql = f"""
      insert into {TABLE_NAME} ({COL_NAME}, {COL_GENDER}, {COL_AGE})
      values (:{COL_NAME}, :{COL_GENDER}, :{COL_AGE})
      """
    params = {COL_NAME: mfilters.dbString(values[COL_NAME]), 
        COL_GENDER: mfilters.dbString(values[COL_GENDER]), 
        COL_AGE: mfilters.dbInteger(values[COL_AGE])}
    cursor.execute(sql,params)
    connection.commit()
    connection.close()
    return cursor.lastrowid

def select_coll_by_id(id,db=mconfig.DB_NAME):
    print("select_coll_by_id()")
    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    sql = f"""
      select {COL_NAME}, {COL_GENDER}, {COL_AGE} from {TABLE_NAME}
      where ({COL_ID} = :{COL_ID})
      """

    print('sql='+sql)
    params = {COL_ID: mfilters.dbInteger(id)}
    cursor.execute(sql,params)
    response=cursor.fetchone()
    connection.close()
    if response != None:
        return {
            COL_ID : mfilters.dbInteger(id),
            COL_NAME: response[0],
            COL_GENDER: response[1],
            COL_AGE: response[2]
        }
    else:
        return None


def select_coll_by_name(name,db=mconfig.DB_NAME):
    print("select_collector_by_name()")
    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    sql = f"""
      select {COL_ID}, {COL_NAME} from {TABLE_NAME}
      where ({COL_NAME} = :{COL_NAME})
      """

    print('sql='+sql)
    params = {COL_NAME: mfilters.dbString(name)}
    cursor.execute(sql,params)
    response=cursor.fetchone()
    connection.close()
    if response != None:
        return {
            COL_ID : response[0],
            COL_NAME: response[1]
        }
    else:
        return None

def test_coll():
    db=mconfig.DB_TEST_NAME
    drop_coll_table(db)
    create_coll_table(db)
    id1=insert_coll({
        'name': 'mike', 
        'gender': 'm', 
        'age': 49},db) 
    id2=insert_coll({
        'name': 'sally', 
        'gender': 'f', 
        'age': 33},db)
    row1=select_coll_by_id(id1,db)
    row2=select_coll_by_id(id2,db)
    rowNone=select_coll_by_id(32984057,db)
    if rowNone != None:
        raise ValueError('not none')
    if row1['id'] != id1:
        raise ValueError('id1 id wrong:' + str(row1['ID']))
    if row1['name'] != 'mike':
        raise ValueError('id1 name wrong.')
    if row2['gender'] != 'f':
        raise ValueError('id2 gender wrong.')
    if row2['age'] != 33:
        raise ValueError('id2 age wrong.')