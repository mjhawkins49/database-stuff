import sqlite3
import score
import hood
import mfilters
import mconfig

def select_score_id_by_hood_name(hood_name, db=mconfig.DB_NAME):
    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    sql="""
      select score.id, score.hoodID, score.lscore from 
      score inner join hood on 
      (score.hoodID = hood.id) where (hood.name = :hood_name)
      """
    params = {'hood_name': mfilters.dbString(hood_name)}
    cursor.execute(sql,params)
    response=cursor.fetchall()
    connection.close()
    if response != None:
        print(response)
        return response
    else:
        print(f"no records at location {hood_name}.")
        return None



def before_data(tablename, db=mconfig.DB_NAME):
    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    sql=f"""
      select * from {tablename}
      """
    params = {'tablename': mfilters.dbString(tablename)}
    cursor.execute(sql,params)
    response=cursor.fetchall()
    connection.close()
    print(response)
