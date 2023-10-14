from datetime import datetime
from pars.selenium_parser import cataloge_page_parser, get_cataloge_pages

dress_page = 'https://www.ozon.ru/category/platya-zhenskie-7502/'


def create_logs(string: str):
    with open("logs.txt", "a", encoding='utf-8') as l:
        string = str(datetime.now()) + ": " + string
        l.write(str(string) + "\n")



if __name__ == '__main__':
  #  get_cataloge_pages()
    cataloge_page_parser()