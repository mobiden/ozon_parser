from database import execute_query
from database import create_connection
from parsing import record_class


def create_record(new_record:record_class):
    connection = create_connection()
    sql = "INSERT INTO likes (current_date, cb_dollar, cb_euro, cb_yuan, birzh_dollar," \
          " birzh_euro, birzh_yuan, buy_dollar, sell_dollar, buy_euro, sell_euro)" \
          " VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s )"

    val = [
        (new_record.current_date, new_record.cb_dollar, new_record.cb_euro, new_record.cb_yuan,
            new_record.birzh_dollar, new_record.birzh_euro, new_record.birzh_yuan,
            new_record.buy_dollar, new_record.sell_dollar, new_record.buy_euro, new_record.sell_euro)
                    ]
    cursor = connection.cursor()
    cursor.executemany(sql, val)
    connection.commit()


def delete_record(id:int):
    pass

