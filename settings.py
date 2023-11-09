import yaml
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) + '\\'
#загрузка конфиг файла
with open(os.path.join(
       os.path.dirname(os.path.abspath(__file__)), 'config.yml'), "r") as f:
    APP_CONFIG = yaml.safe_load(f)

    current_db = APP_CONFIG['database']['db']
    db_config =  APP_CONFIG[current_db]


def create_logs(string: str, printing = False):
    with open("logs.txt", "a", encoding='utf-8') as l:
        string = str(datetime.now()) + ": " + string
        l.write(str(string) + "\n")
    if printing:
        print(string)


CATALOGS_PATH = 'C:\\Python\\my_projects\\Work\\cataloges\\'
PRODUCTS_PATH = 'C:\\Python\\my_projects\\Work\products\\'
IMG_PATH = 'C:\\Python\\my_projects\\Work\\img\\'
WORK_PATH = 'C:\\Python\\my_projects\\Work\\'
MAIN_URL = 'https://www.ozon.ru/'


