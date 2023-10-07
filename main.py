from datetime import datetime
from pars.selenium_parser import cataloge_page_parser


dress_page = 'https://www.ozon.ru/category/platya-zhenskie-7502/'


def create_logs(string: str):
    with open("logs.txt", "a") as l:
        string = str(datetime.now()) + ": " + string
        l.write(str(string) + "\n")



if __name__ == '__main__':
    cataloge_page_parser()