import sqlite3
import mconfig
import mfilters
import mgeneric

TABLE_NAME="hood"
COL_ID="id"
COL_NAME="name"

def drop_hood_table(db=mconfig.DB_NAME):
    mgeneric.drop_table(TABLE_NAME,db)

def create_hood_table(db=mconfig.DB_NAME):
    print("create_hood_table()")
    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    sql = f"""
    create table if not exists {TABLE_NAME} (
        {COL_ID} integer primary key,
        {COL_NAME} text not null
    )
    """
    print("sql=" + sql)
    cursor.execute(sql)
    connection.commit()
    connection.close()


def insert_hood(values,db=mconfig.DB_NAME):
    print(f"insert_hood(values={values},db={db})")
    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    sql = f"""
      insert into {TABLE_NAME} ({COL_NAME})
      values (:{COL_NAME})
      """
    params = {COL_NAME: mfilters.dbString(values[COL_NAME])}
    cursor.execute(sql,params)
    connection.commit()
    connection.close()
    return cursor.lastrowid

def select_hood_by_id(id,db=mconfig.DB_NAME):
    print("select_hood_by_id()")
    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    sql = f"""
      select name from {TABLE_NAME}
      where (ID = :ID)
      """
    params = {'ID': mfilters.dbInteger(id)}
    cursor.execute(sql,params)
    response=cursor.fetchone()
    connection.close()
    if response != None:
        return {
            'ID' : mfilters.dbInteger(id),
            'name': response[0]
        }
    else:
        return None

def select_hood_by_name(name,db=mconfig.DB_NAME):
    print("select_hood_by_name()")
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
        
def test_hood():
    db=mconfig.DB_TEST_NAME
    drop_hood_table(db)
    create_hood_table(db)
    id1=insert_hood({
        'name': 'clifton'},db)
    id2=insert_hood({
        'name': 'redlands'},db)
    row1=select_hood_by_id(id1,db)
    row2=select_hood_by_id(id2,db)
    rowNone=select_hood_by_id(32984057,db)
    if rowNone != None:
        raise ValueError('not none')
    if row1['ID'] != id1:
        raise ValueError('id1 id wrong:' + str(row1['ID']))
    if row2['name'] != 'redlands':
        raise ValueError('id2 hood wrong.')
