from typing import Optional
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
import random
from pars.proxy_agent_config import USER_AGENTS_PROXY_LIST
from settings import CATALOGS_PATH, PRODUCTS_PATH, MAIN_URL, create_logs
import undetected_chromedriver as uc




class Product_class:
    def __init__(self):

       self.title = ''
       self.pictures_path = []
       self.prod_id = -1
       self.description = ''
       self.brand = ''
       self.collection = ''
       self.fabric = ''
       self.dress_type = ''   #Вид одежды
       self.clasp_type = ''
       self.link = ''
       self.color = ''
       self.pr_style = ''
       self.season = ''
       self.country = ''
       self.pr_print = ''
       self.sleeve_length = ''
       self.sleeve_type = ''
       self.waistline = ''
       self.hem_length = ''  #Длина платья
       self.interior_material = ''
       self.details = ''  #Детали: Манжеты, Разрезы
       self.holiday = ''
    

     #  self.sell_euro: Optional[float] = 0
    def __str__(self):
       return f'Product {self.title}'



class Selenium_Class:
    count = 0

    def __init__(self):
        self.option = None
        self.service = None
        self.sel_options = None
        self.__class__.count += 1

    def get_driver(self):

        persona = self.__get_headers_proxy()
        #self.option = uc.ChromeOptions()
        self.option = webdriver.ChromeOptions()
        self.option.add_argument(f"user-agent={persona['user-agent']}")
        self.option.add_argument("--disable-blink-features=AutomationControlled")
        self.option.add_argument('--no-first-run --no-service-autorun --password-store=basic')
        self.option.add_argument("--headless")

        options_proxy = {
         'proxy': {
            'https': persona['http_proxy'],
            'no_proxy': 'localhost,127.0.0.1:8080'
               }
               }
        self.service = Service(executable_path= "chromedriver.exe")
      #driver = webdriver.Chrome(ChromeDriverManager().install())

        driver = webdriver.Chrome(options=self.option, service=self.service)  # seleniumwire_options=options_proxy)
        create_logs(f'driver count {self.count}', True)
        return driver

    def get_undetcted_driver(self):

        persona = self.__get_headers_proxy()
        self.option = uc.ChromeOptions()
        self.option.add_argument(f"user-agent={persona['user-agent']}")
        self.option.add_argument("--disable-blink-features=AutomationControlled")
        self.option.add_argument('--no-first-run --no-service-autorun --password-store=basic')
        self.option.add_argument("--headless")
      #  self.option.add_argument("--user-data-dir=H:/temp")
      #  self.option.add_argument("--disable-gpu")
      #  self.option.add_argument("--no-sandbox")
      #  self.option.add_argument("--disable-setuid-sandbox")

        options_proxy = {
         'proxy': {
            'https': persona['http_proxy'],
            'no_proxy': 'localhost,127.0.0.1:8080'
               }
               }
  #      self.service = Service(executable_path= "chromedriver.exe")
        driver = uc.Chrome(
                          headless=False,
                          use_subprocess=False,
                          driver_executable_path="C:/Python/my_projects/ozon_parser/chromedriver.exe",
                          version_main=109,

                          options=self.option,
                           # service=self.service
                           )

        create_logs(f'driver count {self.count}')
        return driver



    def reset_driver(self, driver):
        handle = driver.current_window_handle
        driver.service.stop()
        time.sleep(6)
        driver.webdriver.Chrome(options=self.option, service=self.service,
                                 seleniumwire_options=self.sel_options)
        driver.switch_to.window(handle)


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

