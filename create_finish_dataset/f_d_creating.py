import os
import pandas as pd  # pip install pandas
from database import create_connection
from database.db_view import get_record_list, PROD_FEATURES_LIST
from dataset_cleaning.database_cleaning import clean_color
from settings import WORK_PATH, IMG_PATH, create_logs
import shutil
import zipfile

DATASET_PATH = WORK_PATH + 'dataset\\'
connection = create_connection()


def to_zip (folder_path:str, zip_path:str):
    folder_to_zip = folder_path
    zip_file = zip_path

    with zipfile.ZipFile(zip_file, 'w') as archive:
        for root, dirs, files in os.walk(folder_to_zip):
            for file in files:
                file_path = os.path.join(root, file)
                archive.write(file_path, arcname=file_path.replace(folder_to_zip, ''))

    print(f'Папка {folder_to_zip} добавлена в архив {zip_file}')




def f_d_creating():  # создание датасета и его архивация
    prod_list = get_record_list(table='product', connection=connection) # все товары в списке

    os.makedirs(DATASET_PATH, exist_ok=True)
    feat_dict = get_features_dict(prod_list)
    if len(feat_dict) > 0:
        to_zip(folder_path=DATASET_PATH, zip_path=WORK_PATH + 'dress_dataset.zip')





def get_features_dict(prod_list:list) -> dict:  # создание словаря признаков
    all_feat_dict = {}
    exclude_list = ['id', 'title', 'description', 'brand', 'fabric', 'country', #создание списка исключений полей
                    'prod_num',
                                        ]

    for x in PROD_FEATURES_LIST: # создание пустого словаря словарей признаков
        if x not in exclude_list:  # создание исключений полей
            all_feat_dict.update({x: {}})

    columns = ['Feature', 'Name']


    for enum0, prod in enumerate(prod_list):
        if enum0 % 1000 == 0:
            print(f'обрабатывается {enum0} из {prod_list_count} \r', end='')
        data = []
        prod_list_count = len(prod_list)

        for enum1, item in enumerate(prod):
            if PROD_FEATURES_LIST[enum1] in exclude_list:
                continue

            if enum1 == PROD_FEATURES_LIST.index('color'):
                item =  clean_color(item)
            data.append([PROD_FEATURES_LIST[enum1], item]) # prepares data for csv

            # блок создания списков словарей

            temp_feat_dict = all_feat_dict[PROD_FEATURES_LIST[enum1]]
            if item in temp_feat_dict.keys():
                all_feat_dict[PROD_FEATURES_LIST[enum1]][item] += 1
            else:
                all_feat_dict[PROD_FEATURES_LIST[enum1]].update({item: 1})


        df = pd.DataFrame(data, columns=columns)
        pictures = get_record_list('picture', connection, prod[-1])
        total_pict = len(pictures)
        for i, pict in enumerate(pictures):
            temp_name = f'{DATASET_PATH}item{prod[-1]}-{i}.'
            if os.path.exists(pict[2]):
                if not os.path.exists(temp_name+'jpg'):
                    shutil.copyfile(pict[2], temp_name+'jpg')
                df.to_csv(temp_name +'csv')


    with open(DATASET_PATH+'feat_list.txt', 'a', encoding='utf-8') as f:
        for fea in all_feat_dict.items():
            f.write(f'{fea[0]} ---- {fea[1]}\n')

    return all_feat_dict



