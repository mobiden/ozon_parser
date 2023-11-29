from database import execute_query
from database import create_connection
from settings import create_logs
from pars import Product_class

PROD_FEATURES_LIST = ['id', 'title',  'description', 'brand', 'collection',
          'fabric', 'dress_type', 'clasp_type', 'color', 'pr_style', 'season', 'country',
          'pr_print', 'sleeve_length', 'sleeve_type', 'waistline', 'hem_length',
          'interior_material','details', 'holiday', 'prod_num',
                 ]


def _execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        return True

    except Exception as e:
        print(f"Произошла ошибка '{e}'")
        create_logs(f"Произошла ошибка '{e}'")
        return False



def _execute_read_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        return cursor.fetchall()
    except Exception as e:
        print(f"Произошла ошибка '{e}'")
        create_logs(f"Произошла ошибка '{e}'")
        return None


def create_product_record(new_record:Product_class, connection):
  #  connection = create_connection()
    new_record.prod_id = int(new_record.prod_id)
    #TODO: переделать из листа фич
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


def get_record_list(table:str, connection, pr_num =  -1):
    select_line, where_line = '', ''
    if table.lower() == "product" or table.lower() == 'product_table':
        select_line = 'SELECT * FROM product_table'
        if int(pr_num) >= 0:
            where_line = f' WHERE product_table.prod_num = {pr_num}'
    elif table.lower() in["picture","pict_table", "picture_table"]:
        select_line = 'SELECT * FROM picture_table'
        if pr_num >= 0:
            where_line = f' WHERE picture_table.prod_num = {pr_num}'
    assert len(select_line + where_line) > 0
    return  _execute_read_query(connection, select_line + where_line)



def delete_record(table:str, table_id:int, connection):
    assert table_id >= 0
    select_line = ''
    if table.lower() == "product" or table.lower() == 'product_table':
        select_line = f'DELETE FROM product_table WHERE product_table.id = {table_id}'

    elif table.lower() in ["picture", "pict_table", "picture_table"]:
        select_line = f'DELETE FROM picture_table WHERE picture_table.id = {table_id}'

    assert len(select_line) > 0

    return _execute_query(connection, select_line)


def update_record(table:str, table_id:int, connection, update_list = []):
    assert table_id >= 0 and len(update_list) != 0
    field = update_list[0]
    data = update_list[1]
    select_line = ''
    if table.lower() == "product" or table.lower() == 'product_table':
        select_line = f'UPDATE product_table SET {field} = "{data}" WHERE product_table.id = {table_id}'

    elif table.lower() in ["picture", "pict_table", "picture_table"]:
        select_line = f'UPDATE picture_table SET {field} = "{data}" WHERE picture_table.id = {table_id}'

    assert len(select_line) > 0

    return _execute_query(connection, select_line)



def get_related_pict_list(connection, pr_num =  -1, pr_id = -1):
    assert pr_num >= 0 or pr_id >=0
    assert pr_num * pr_id <= 0
    select_line = 'SELECT * FROM picture_table as pi LEFT JOIN product_table as pr ON' \
                  ' pi.prod_num = pr.prod_num where '
    where_line = ''
    if pr_num >= 0:
        where_line = f'pr.prod_num = {pr_num}'
    else:
        where_line = f'pr.id = {pr_id}'

    assert len(where_line) > 0
    return  _execute_read_query(connection, select_line + where_line)