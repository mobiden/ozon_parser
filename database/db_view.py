from database import execute_query
from database import create_connection
from settings import create_logs
from pars import Product_class



def _execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Exception as e:
        print(f"Произошла ошибка '{e}'")
        create_logs(f"Произошла ошибка '{e}'")


def create_product_record(new_record:Product_class, connection):
  #  connection = create_connection()
    new_record.prod_id = int(new_record.prod_id)
    sql = "INSERT INTO product_table (title, prod_num, description, brand, collection, " \
          "fabric, dress_type, clasp_type, color, pr_style, season, country," \
          " pr_print, sleeve_length, sleeve_type, waistline, hem_length,  interior_material," \
          " details, holiday) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
          " %s, %s, %s, %s, %s, %s, %s, %s, %s)"

    val = (new_record.title, new_record.prod_id,
           new_record.description, new_record.brand, new_record.collection,
           new_record.fabric, new_record.dress_type, new_record.clasp_type,
           new_record.color, new_record.pr_style, new_record.season, new_record.country,
           new_record.pr_print, new_record.sleeve_length, new_record.sleeve_type,
           new_record.waistline, new_record.hem_length, new_record.interior_material,
           new_record.details, new_record.holiday)

    cursor = connection.cursor()
    cursor.execute(sql, val)
    connection.commit()
    create_logs(f'В базу записали {new_record}')


def create_pict_record(pict_list: list, pr_id: int, connection):
    val_list = []
    #connection = create_connection()

    for pict in pict_list:
        temp_tuple = (pr_id, pict)
        val_list.append(temp_tuple)

    sql = "INSERT INTO picture_table (prod_num, pict_path)  VALUES ( %s, %s)"
    val = val_list

    cursor = connection.cursor()
    cursor.executemany(sql, val)
    connection.commit()
    create_logs(f'В базу записали фото для {pr_id}')

def get_record_list(table:str, pr_id: -1, connection):

    select_line, where_line = '', ''
    if table.lower() == "product" or table.lower() == 'product_table':
        select_line = 'SELECT * FROM product_table'
        if int(pr_id) >= 0:
            where_line = f' WHERE product_table.prod_num = {pr_id}'
    elif table.lower() in["picture","pict_table", "picture_table"]:
        select_line = 'SELECT * FROM picture_table'
        if pr_id >= 0:
            where_line = f' WHERE picture_table.prod_num = {pr_id}'
    assert len(select_line + where_line) > 0

    return  _execute_read_query(connection, select_line + where_line)




def delete_record(id:int, connection):
    pass

