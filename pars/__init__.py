from typing import Optional
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
import random
from pars.proxy_agent_config import USER_AGENTS_PROXY_LIST
from settings import CATALOGS_PATH, PRODUCTS_PATH, MAIN_URL



class Record_class:
    def __init__(self):

       self.title: str
       self.id: int
       self.price: int
       self.description:str
       self.fabric: list
       self.dress_type:list
       self.clasp_type:list
       self.link: str
       self.color: list
       self.pr_style: list
       self.season: list
       self.country: str
       self.pr_print:list
       self.sleeve_length: str
       self.sleeve_type: str
       self.waistline: str
       self.hem_length: str
       self.interior_material: list
       self.details: list
       self.holiday: list
    #   self.
    #   self.
    #   self.
    #   self.
    #   self.
     #  self.sell_euro: Optional[float] = 0



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
      driver = webdriver.Chrome(options=self.option, service=self.service)  # seleniumwire_options=options_proxy)
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
      return json_text  # PRODUCTS_PATH + self.filename

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
