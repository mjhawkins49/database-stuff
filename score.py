import sqlite3
import mconfig
import mfilters
import mgeneric

TABLE_NAME="score"
COL_ID='id'
COL_SCORE='lscore'
COL_SEX='sex'
COL_AGE='age'
COL_HOOD_ID='hoodID'
COL_COLL_ID='collID'

def drop_score_table(db=mconfig.DB_NAME):
    mgeneric.drop_table(TABLE_NAME,db)

def create_score_table(db=mconfig.DB_NAME):
    print("create_score_table()")
    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    sql = f"""
    create table if not exists {TABLE_NAME}(
        {COL_ID} integer primary key,
        {COL_SCORE} integer not null,
        {COL_SEX} text not null,
        {COL_AGE} integer not null,
        {COL_HOOD_ID} integer not null,
        {COL_COLL_ID} integer not null
    )
    """
    cursor.execute(sql)
    connection.commit()
    connection.close()

def insert_score(values,db=mconfig.DB_NAME):
    print("insert_score()")
    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    sql = f"""
      insert into {TABLE_NAME} ({COL_SCORE}, {COL_SEX}, {COL_AGE}, {COL_HOOD_ID}, {COL_COLL_ID})
      values (:{COL_SCORE}, :{COL_SEX}, :{COL_AGE}, :{COL_HOOD_ID}, :{COL_COLL_ID})
      """
    params = {COL_SCORE: mfilters.dbInteger(values[COL_SCORE]), 
        COL_SEX: mfilters.dbString(values[COL_SEX]), 
        COL_AGE: mfilters.dbInteger(values[COL_AGE]),
        COL_HOOD_ID: mfilters.dbString(values[COL_HOOD_ID]), 
        COL_COLL_ID: mfilters.dbInteger(values[COL_COLL_ID])}
    cursor.execute(sql,params)
    connection.commit()
    connection.close()
    return cursor.lastrowid

def select_score_by_id(id,db=mconfig.DB_NAME):
    print("select_score_by_id()")
    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    sql = f"""
      select {COL_COLL_ID}, {COL_HOOD_ID}, {COL_SCORE} from {TABLE_NAME}
      where ({COL_ID} = :{COL_ID})
      """
    params = {COL_ID: mfilters.dbInteger(id)}
    cursor.execute(sql,params)
    response=cursor.fetchone()
    connection.close()
    if response != None:
        return {
            COL_ID: mfilters.dbInteger(id),
            COL_COLL_ID: response[0],
            COL_HOOD_ID: response[1],
            COL_SCORE: response[2]
        }
    else:
        return None

def test_score():
    db=mconfig.DB_TEST_NAME
    drop_score_table(db)
    create_score_table(db)
    id1=insert_score({'lscore': 3, 'hoodID': 1, 'collID': 2},db)
    id2=insert_score({'lscore': 5, 'hoodID': 2, 'collID': 1},db)
    row1=select_score_by_id(id1,db)
    row2=select_score_by_id(id2,db)
    rowNone=select_score_by_id(32984057,db)
    if rowNone != None:
        raise ValueError('not none')
    if row1['id'] != id1:
        raise ValueError('id1 id wrong:' + str(row1['id']))
    if row1['lscore'] != 3:
        raise ValueError('id1 lscore wrong.')
    if row2['hoodID'] != 2:
        raise ValueError('id2 hoodID wrong.')
    if row2['collID'] != 1:
        raise ValueError('id2 collID wrong.')