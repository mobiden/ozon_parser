import io
import json
from selenium.webdriver.common.by import By
import time

from database import create_connection
from database.db_view import get_record_list, create_product_record, create_pict_record
from pars import Selenium_Class, Product_class
from settings import CATALOGS_PATH, PRODUCTS_PATH, MAIN_URL, IMG_PATH, create_logs
from bs4 import BeautifulSoup as bs
import os
import re
import requests
from PIL import Image

connection = create_connection()

def save_page(url:str, filename: str):
    selen = Selenium_Class()
    driver = selen.get_driver()
    try:
        driver.get(url)
        time.sleep(3)
        driver.execute_script("window.scrollTo(5,4000);")
        time.sleep(5)
        html = driver.page_source
        with open(CATALOGS_PATH + filename, 'w', encoding='utf-8') as f:
            f.write(html)
    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()


def save_product(url:str, filename: str) -> str:
    # сохраняет страницу, передает json в тексте
    if os.path.exists(PRODUCTS_PATH + filename + '.html'):
        with open(PRODUCTS_PATH + filename + '.html', encoding='utf-8') as f:
            html = f.read()
    else:
        selen = Selenium_Class()
        driver = selen.get_driver()

        try:
            driver.get(url)
            time.sleep(6)
            html = driver.page_source
            with open(PRODUCTS_PATH + filename + '.html', 'w', encoding='utf-8') as f:
                f.write(html)


        except Exception as ex:
            create_logs(f'save product {filename} rised exception {ex}')
            print(ex)
        finally:
            driver.close()
            driver.quit()

    return  html,  PRODUCTS_PATH + filename




def save_pict(url, filename):
    if os.path.exists(filename):
        return True
    else:
        try:
            response = requests.get(url)
            image_file = io.BytesIO(response.content)
            image = Image.open(image_file).convert('RGB')
            with open(filename, 'wb') as file:
                image.save(file, "JPEG", quality=100)
        except Exception as ex:
            create_logs(f'save pict {filename} created errors {ex}')
            print(ex)
            return False
        finally:
            return True



def get_cataloge_pages(url:str, filename:str):
    #url = "https://www.ozon.ru/category/kompasy-11461/"
    selen = Selenium_Class()

    MAX_PAGE = 1000 # Ограничим парсинг первыми 1000 страницами
    i = 50
    while i <= MAX_PAGE:
        filename = f'page_' + str(i) + '.html'
        if i != 1:
            url = url + '?page=' + str(i)
        save_page(url, filename)
        i += 1



def add_product_to_base(pictures_path: list, product_json:dict, prod_id:int) -> Product_class:
    adding = True
    if len(pictures_path) == 0:
        return None
    try:
        product_descr = json.loads(product_json['webCharacteristics-939965-pdpApparelPage2-2'])
    except Exception as e:
        print(e)
        return None
    product = Product_class()
    product.prod_id = prod_id
    product.pictures_path = pictures_path
    product.link = product_descr['link']
    product.title = product_descr['productTitle'].split(': ')[1]
    temp_dict = product_descr['characteristics'][0]['short']
    for item in temp_dict:
        key = item['key'].lower()
        text = item['values'][0]['text'].lower()

        if key == 'type':
            if text.lower() != 'платье':
                adding = False
                break
        elif key == 'season':
            product.season = text
        elif len(product.fabric) == 0 and key == 'composition':
            product.fabric = text
        elif key == 'styleapparel':
            product.pr_style = text
        elif key == 'brand':
            product.brand = text
        elif key == 'country':
            product.country = text
        elif key == 'typeprinttshirt':
            product.pr_print = text
        elif key == 'innermaterial':
            product.interior_material = text
        elif key == 'modelclothing':
            product.dress_type = text
        elif key == 'collection':
            product.collection = text #TODO: убрать цифры
        elif key == 'typeclasp':
            product.clasp_type = text
        elif key == 'typesleeve':
            product.sleeve_type = text
        elif key == 'sleevelength':
            product.sleeve_length = text
        elif key == 'waist':
            product.waistline = text
        elif key == 'color':
            product.color = text
        elif key == 'material':
            product.fabric = text
        elif key == 'detailsclothes':
            product.details = text
        elif key == 'holidays':
            product.holiday = text
        elif key == 'dresslength':
            product.hem_length = text

        else:
            if key not in ['sizem', 'heightm', 'settingsm', 'russiansizeclothes',
                           'sexmaster', 'instruction', 'packing', 'numitemsdcml',
                           'setapparel', 'sizemanufacturer', 'isadult', 'sizeheight',
                           'lenghtclothing', 'trucode', 'patternbust', 'temprange',
                           'compressionclass', 'composition']:
                with open('unknown_feature.txt', 'a', encoding='utf-8') as f:
                    f.write(f'неизвестный признак: {key} -  {text} \n')


    rec = get_record_list('product', product.prod_id, connection)
    if (not rec or len(rec) == 0) and adding:
        create_product_record(product, connection)
        create_pict_record(pict_list = product.pictures_path, pr_id = product.prod_id,
                           connection=connection)

    return product


def product_page1_parser(url:str, tempfile = ''):
    pict_path_list = []
    ch_url = url.replace('/', '-') + '1'
    create_logs(f'обработка page1 {ch_url} ')
    if len(tempfile) == 0:
        ch_url = url.replace('/', '-') + '1'
        resp = (MAIN_URL + url)
        print(f'начинаем сохранять изделие {ch_url}')
        html, filename = save_product(url=resp, filename=ch_url)
    else:
        with open(tempfile, 'r', encoding='utf-8') as f:
            html = f.read()
    soup = bs(html, 'lxml')
    div_jm5 = soup.find_all(class_='jm5')
    for enum, jm5 in enumerate(div_jm5):
        j = jm5.contents[0]
    #    pict_url1 = j.get('src')
    #    save_pict(pict_url1, IMG_PATH + ch_url + str(enum) + '.jpg' )
        pict_url2 = j.get('srcset').split()[0]
        answer = save_pict(pict_url2, IMG_PATH + ch_url + '-' + str(enum) + '.jpg' )
        if answer:
            pict_path_list.append(IMG_PATH + ch_url + '-' + str(enum) + '.jpg')
    #time.sleep(6)
    return pict_path_list



def product_page2_parser(url:str):
    #https://www.ozon.ru/api/entrypoint-api.bx/page/json/v2?url=/product/plate-sinelia-1153394934/?layout_container=pdpApparelPage2&layout_page_index=2
    add_url0 = 'api/entrypoint-api.bx/page/json/v2?url=/'
    add_url1 = '?layout_container=pdpApparelPage2&layout_page_index=2'
    ch_url = url.replace('/', '-') + '2'
    resp = (MAIN_URL + add_url0 + url + add_url1)
    print(f'начинаем сохранять вторую страницу {ch_url}')
    html, _ = save_product(url=resp, filename=ch_url)
    soup = bs(html, 'lxml')
    json_text = soup.find('pre').text
    product_json = json.loads(json_text)
    with open (PRODUCTS_PATH + ch_url + '.json', 'w', encoding='utf-8') as f:
        json.dump(product_json, f, ensure_ascii=False)
    #print(product_json)
    time.sleep(6)
    return product_json['widgetStates']


def cataloge_page_parser():
    file_list = os.listdir(CATALOGS_PATH)
    done_file = []
    if os.path.exists(CATALOGS_PATH + 'page_done.txt'):
        with open(CATALOGS_PATH + 'page_done.txt', 'r', encoding='utf-8') as f:
            done_file = [line.strip() for line in f.readline()]
    for html_file in file_list:
        if os.path.exists(CATALOGS_PATH + 'page_done.txt'):
            if html_file in done_file:
                continue
        if html_file[-4:] != 'html':
            continue

        with open(CATALOGS_PATH + html_file, 'r', encoding='utf-8') as f:
            html = f.read()
        soup = bs(html, 'lxml')
        prod_hrefs = soup.find_all(href=re.compile("product"))
        for p_href in prod_hrefs:
            p_href = p_href.get('href')
            p_href = p_href.strip().split('/')
            url = p_href[1] + '/' + p_href[2] + '/'
            prod_id = url.split('-')[-1].replace('/', '')
            prod_id = ''.join(let if let.isdigit() else '' for let in prod_id)
            check_rec = get_record_list('product', prod_id, connection)
            if check_rec:
                if len(check_rec) > 0:
                    continue
            product_json1 = product_page1_parser(url)
            if len(product_json1) > 0:
                product_json2 = product_page2_parser(url)
                product = add_product_to_base(product_json1, product_json2 , prod_id)
                if product is not None:
                    print(product)
                else:
                    print(f'продукт {prod_id} не сохранен')
                    create_logs(f'продукт {prod_id} не сохранен')
            else:
                print(f'нет фото у продукта {prod_id}')
                create_logs(f'нет фото у продукта {prod_id}')

        with open(CATALOGS_PATH + 'page_done.txt', 'a', encoding="utf-8") as f:
            f.write(html_file + '\n')
