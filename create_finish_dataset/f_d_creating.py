import os

from database import create_connection
from database.db_view import get_record_list, PROD_FEATURES
from settings import WORK_PATH, IMG_PATH, create_logs

connection = create_connection()

def f_d_createing():
    prod_list = get_record_list(table='product', connection=connection)
    os.makedirs(WORK_PATH + 'photo\\', exist_ok=True)
    feat_dict = get_features_dict(prod_list)

    for product in prod_list:
        pass


def get_features_dict(prod_list):
    feat_list = []
    for x in range(len(PROD_FEATURES)):
        feat_list.append([])
    for enum0, prod in enumerate(prod_list):


        for enum1, item in enumerate(prod):
            if enum1 in [0, 1, 2, len(prod) - 1]:
                continue
            if item == '':
                continue

            if item not in feat_list[enum1 - 3]:
                feat_list[enum1 - 3].append(item)


    with open('feat_list.txt', 'a', encoding='utf-8') as f:
        for fea in feat_list:
            f.write(str(fea) + '\n')



