from datetime import datetime

from create_finish_dataset.f_d_creating import f_d_createing
from pars.selenium_parser import cataloge_page_parser, get_cataloge_pages
from dataset_cleaning.database_cleaning import database_cleaning
from settings import create_logs

dress_page = 'https://www.ozon.ru/category/platya-zhenskie-7502/'

def parser_start():
    while True:
        try:
            get_cataloge_pages()
            cataloge_page_parser()
        except Exception as ex:
            create_logs(f'exception: {ex}', True)


if __name__ == '__main__':
    # parser_start()
    database_cleaning()
    f_d_createing()