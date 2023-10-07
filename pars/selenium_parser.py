import json

from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
import random
from pars.proxy_agent_config import USER_AGENTS_PROXY_LIST
from fake_useragent import UserAgent
from webdriver_manager.chrome import ChromeDriverManager

from settings import CATALOGS_PATH, PRODUCTS_PATH, MAIN_URL
from bs4 import BeautifulSoup
import os
import re



class Selenium_Class:
    def __init__(self, url: str, filename: str):
        self.url = url
        self.filename = filename
        self.option = None
        self.service = None
        self.sel_options = None

    def get_driver(self):
        persona = self.__get_headers_proxy()

        self.option = webdriver.ChromeOptions()
        self.option.add_argument(f"user-agent={persona['user-agent']}")
        self.option.add_argument("--disable-blink-features=AutomationControlled")
        self.option.add_argument("--headless")

        options_proxy = {
            'proxy': {
                'https': persona['http_proxy'],
                'no_proxy': 'localhost,127.0.0.1:8080'
                        }
                            }
        self.service = Service(executable_path="chromedriver")
      #  driver = webdriver.Chrome(ChromeDriverManager().install())
        driver = webdriver.Chrome(options=self.option, service=self.service) # seleniumwire_options=options_proxy)
        return driver



    def reset_driver(self, driver):
        handle = driver.current_window_handle
        driver.service.stop()
        time.sleep(6)
        driver.webdriver.Chrome(options=self.option, service=self.service,
                                seleniumwire_options=self.sel_options)
        driver.switch_to.window(handle)


    def save_page(self):
        driver = self.get_driver()

        try:
            driver.get(self.url)
            time.sleep(3)
            driver.execute_script("window.scrollTo(5,4000);")
            time.sleep(5)
            html = driver.page_source
            with open(CATALOGS_PATH + self.filename, 'w', encoding='utf-8') as f:
                f.write(html)
        except Exception as ex:
            print(ex)
        finally:
            driver.close()
            driver.quit()


    def save_product(self):
        driver = self.get_driver()

        try:
            driver.get(self.url)
            time.sleep(3)
            temp = driver.find_element(By.TAG_NAME, "body")
            text = temp.find_element(By.TAG_NAME, 'pre')
            json_text = text.text
            html = driver.page_source
            with open(PRODUCTS_PATH + self.filename + '.html', 'w', encoding='utf-8') as f:
                f.write(html)
        except Exception as ex:
            print(ex)
        finally:
            driver.close()
            driver.quit()
        return  json_text #PRODUCTS_PATH + self.filename



    def __get_headers_proxy(self) -> dict:
      #    The config file must have dict:
      #       {'http_proxy':'http://user:password@ip:port',
      #          'user-agent': 'user_agent name'     }

        try:
            users = USER_AGENTS_PROXY_LIST
            persona = random.choice(users)
        except ImportError:
            persona = None
        return persona


def get_cataloge_pages(url:str):
    #url = "https://www.ozon.ru/category/kompasy-11461/"


    MAX_PAGE = 1000 # Ограничим парсинг первыми 1000 страницами
    i = 50
    while i <= MAX_PAGE:
        filename = f'page_' + str(i) + '.html'
        if i == 1:
            Selenium_Class(url, filename).save_page()
        else:
            url_param = url + '?page=' + str(i)
            Selenium_Class(url_param, filename).save_page()

        i += 1


def add_product_to_base(product_json:dict):
    product_descr = json.loads(product_json['webCharacteristics-939965-pdpApparelPage2-2'])
    print(product_descr)



def product_page2_parser(url:str):
    #https://www.ozon.ru/api/entrypoint-api.bx/page/json/v2?url=/product/plate-sinelia-1153394934/?layout_container=pdpApparelPage2&layout_page_index=2
    add_url0 = 'api/entrypoint-api.bx/page/json/v2?url=/'
    add_url1 = '?layout_container=pdpApparelPage2&layout_page_index=2'
    ch_url = url.replace('/', '-') + '2'
    resp = (MAIN_URL + add_url0 + url + add_url1)
    print(f'начинаем сохранять изделие {ch_url}')
    product = (Selenium_Class(resp, ch_url).save_product())
    product_json = json.loads(product)
    with open (PRODUCTS_PATH + ch_url + '.json', 'w', encoding='utf-8') as f:
        json.dump(product_json, f, ensure_ascii=False)
    #print(product_json)
    add_product_to_base(product_json['widgetStates'])
    print('stop')


def cataloge_page_parser():
    file_list = os.listdir(CATALOGS_PATH)
    for html_file in file_list:
        if html_file[-4:] != 'html':
            continue

        with open(CATALOGS_PATH + html_file, 'r', encoding='utf-8') as f:
            html = f.read()
        soup = BeautifulSoup(html, 'lxml')
        prod_hrefs = soup.find_all(href=re.compile("product"))
        for p_href in prod_hrefs:
            p_href = p_href.get('href')
            p_href = p_href.strip().split('/')
            url = p_href[1] + '/' + p_href[2] + '/'
            product_page2_parser(url)
