import os
import re

from database import create_connection
from database.db_view import get_record_list, update_record, delete_record, get_related_pict_list, PROD_FEATURES
from settings import CATALOGS_PATH, PRODUCTS_PATH, IMG_PATH, MAIN_URL, create_logs

connection = create_connection()


def database_cleaning():
  #  pict_db_clean()
  #  prod_db_clean()
  #clean_features()
  add_prints()

def pict_db_clean():
    record_list = get_record_list(table = 'picture', connection = connection)
    for enum, record in enumerate(record_list):
        temp_id = record[0]
        temp_prod_id = record[1]
        temp_file =record[2].split('/')[-1].split('\\')[-1]
        temp_path =  IMG_PATH + temp_file
        temp_path = temp_path.replace('\\', '/')
        if record[2].find('media') >= 0:
            if os.path.exists(temp_path):
                if temp_path != record[2]:
                    ans = update_record(table='picture', table_id=temp_id,
                                    connection=connection, update_list=['pict_path', temp_path])
            else:
                create_logs(f'нет {temp_path}')
                ans = delete_record(table='picture', table_id=temp_id, connection=connection)
                with open('check_db.txt', 'a', encoding='utf-8') as f:
                    f.write(f'{temp_path}\n')
                create_logs(f'нет {temp_path}')

def prod_db_clean():
    pr_record_list = get_record_list(table='product', connection=connection)
    for enum, record in enumerate(pr_record_list):
        temp_id = record[0]
        picts = get_related_pict_list(connection, pr_id=temp_id)
        if len(picts) == 0:
            ans = delete_record(table='product', table_id=temp_id, connection=connection)
            print(str(ans) + ' ' + str(temp_id))


def clean_features():
    pr_record_list = get_record_list(table='product', connection=connection)
    for record in pr_record_list:
        temp_id = record[0]

        temp_collection = record[4] # collection
        new_collection = del_digit(temp_collection).strip()
        if new_collection != temp_collection:
            ans = update_record(table='product', table_id=temp_id,
                                connection=connection, update_list=['collection', new_collection])

        temp_fabric = clean_fabric(record[5])
        if temp_fabric != record[5]:
            ans = update_record(table='product', table_id=temp_id,
                                connection=connection, update_list=['fabric', temp_fabric])



def clean_fabric(inbound_string:str) -> str:


    old_string = inbound_string.strip().replace(' %', '%').\
        replace('п/э', 'пэ').replace('/', ',').\
        replace('.', ' ').replace('  ', ' ').replace(' и ', ' ')
    result = ''
    if old_string.find('%') < 0:

        if old_string.find(',') >= 0:
            result = old_string.split(',')[0].strip()
        elif old_string.find(';') >= 0:
            result = old_string.split(';')[0].strip()

        else:
            result = old_string.strip()
    else:
        percent = 0
        if old_string[0] == '%':
            old_string = old_string.replace('%', ' ')
        old_string = old_string.replace('%', '% ').replace('  ', ' ').strip()
        if len(old_string.split()) == 1:
            result = del_digit(old_string).replace('%', '')

        if old_string.find(',') > 0 or old_string.find(';') > 0:
            temp_list = re.split(",|;", old_string)
            num = -1
            for i, temp_str in enumerate(temp_list):
                if int(get_digit(temp_str)) > percent:
                    percent = int(get_digit(temp_str))
                    num = i

            result = del_digit(temp_list[num]).strip()
            result = result.replace('%', '').strip()

        else:
            percent = 0
            temp_string = old_string.replace('основной материал 1: ', '')
            temp_list = re.split(" - | |-", temp_string)

            if len(temp_list) == 3:
                dig_line = ''.join(get_digit(x) for x in temp_list)
                str_line = ''.join(del_digit(x) + ' ' for x in temp_list)
                str_line = str_line.replace('%', '').strip()
                temp_list = [str_line, dig_line]

                with open('wrong_line.txt', 'a', encoding='utf-8') as f:
                    f.write(str(temp_list) + '\n')

            for i in range(len(temp_list) // 2):
                if get_digit(temp_list[i * 2]) != '':
                    temp_num = int(get_digit(temp_list[i * 2]))
                    if temp_num > percent:
                        temp_fab = del_digit(temp_list[i * 2 + 1])
                        percent = temp_num
                else:
                    try:
                        temp_num = int(get_digit(temp_list[i * 2 + 1]))
                    except Exception as ex:
                        print(ex)
                    if temp_num > percent:
                        temp_fab = del_digit(temp_list[i * 2])
                        percent = temp_num
            result = temp_fab

    out_result = result.replace('-', '').replace('  ', ' ').replace(':', '')\
        .replace('п/э', 'полиэстер').replace('полиэстер вискоза эластан', 'полиэстер')\
        .replace('пэ', 'полиэстер').replace('полиэстр', 'полиэстер')\
        .replace('viscose', 'вискоза').replace('полиэстера', 'полиэстер')\
        .replace('100 полиэстер', 'полиэстер').replace('металлизированное', 'металлизированное волокно')\
        .replace('ткань трикотаж (состав хлопок', 'хлопок').replace('подкладка', 'полиэстер')\
        .replace('крепшифон', 'креп-шифон').replace('бархатстрейч', 'бархат-стрейч').strip()
    return out_result


def del_digit(old_string:str) -> str:
    return ''.join(lett if not lett.isdigit() else '' for lett in old_string)


def get_digit(old_string:str) -> str:
    temp_res = ''.join(lett if lett.isdigit() else '' for lett in old_string)
    return temp_res


def clean_color(old_color:str) -> str:

    result = del_digit(old_color).strip().strip('-')

    result = result.replace('о - ', 'о-').replace('.', ' ').replace('  ', ' ')\
    .replace('о ','о-').replace('меланж','').strip().replace('цвет','').replace('принт','')\
    .replace('пепельно', 'серо').replace('св. ', 'светло-').replace('св.', 'светло-')\
    .replace('ярко-', '').replace('дэним','').replace('деним','').replace('платье','').strip()

    result = result.replace('изумрудный', 'зеленый')

    result = result.split(' c ')[0]

    if result[-2:] == 'ee':
        result = result[:-2] + 'ий'
    elif result == 'голубое':
        result = 'голубой'
    elif result[-2:] == 'ое':
        result = result[:-2] + 'ый'


    if result.find(';') >= 0:
        result = result.split(';')[0]
    return result


def add_prints():
    pr_record_list = get_record_list(table='product', connection=connection)
    for record in pr_record_list:
        temp_id = record[0]

        temp_colors = record[PROD_FEATURES.index('color')] # color
        temp_print = record[PROD_FEATURES.index('pr_print')]  # print
        if temp_colors.find('горох') >= 0 or temp_colors.find('горошек') >= 0 or temp_colors.find('горощек') >= 0:
            if len(temp_print) == 0:
                create_logs(f'добавляем горох в {temp_id}', True)
                ans = update_record(table='product', table_id=temp_id,
                                connection=connection, update_list=['pr_print', 'горох'])
        elif temp_colors.find('принт') >= 0:
            if len(temp_print) == 0:
                create_logs(f'добавляем принт в {temp_id}', True)
                ans = update_record(table='product', table_id=temp_id,
                                connection=connection, update_list=['pr_print', 'принт'])

        elif temp_colors.find('лапк') >= 0:
            if len(temp_print) == 0:
                create_logs(f'добавляем лапка в {temp_id}', True)
                ans = update_record(table='product', table_id=temp_id,
                                connection=connection, update_list=['pr_print', 'лапка'])

        elif temp_colors.find('цветок') >= 0:
            if len(temp_print) == 0:
                create_logs(f'добавляем цветок в {temp_id}', True)
                ans = update_record(table='product', table_id=temp_id,
                                connection=connection, update_list=['pr_print', 'цветок'])

        elif temp_colors.find('геометрический') >= 0:
            if len(temp_print) == 0:
                create_logs(f'добавляем геометрический в {temp_id}', True)
                ans = update_record(table='product', table_id=temp_id,
                                connection=connection, update_list=['pr_print', 'геометрический'])

        elif temp_colors.find('абстракция') >= 0:
            if len(temp_print) == 0:
                create_logs(f'добавляем абстракция в {temp_id}', True)
                ans = update_record(table='product', table_id=temp_id,
                                connection=connection, update_list=['pr_print', 'абстракция'])

        elif temp_colors.find('полоск') >= 0:
            if len(temp_print) == 0:
                create_logs(f'добавляем полоска в {temp_id}', True)
                ans = update_record(table='product', table_id=temp_id,
                                connection=connection, update_list=['pr_print', 'полоска'])

