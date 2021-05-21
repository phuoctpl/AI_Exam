from common_services import *
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import time

domain_url = 'https://fptshop.com.vn'
cag_urls = ['https://fptshop.com.vn/dien-thoai?sort=ban-chay-nhat&trang=20',
            'https://fptshop.com.vn/may-tinh-xach-tay?sort=ban-chay-nhat&trang=20']
output_path = '..\\comment_fpt.json'


def get_products():
    links = []
    for cag_url in cag_urls:
        driver = webdriver.Chrome('..\\webdriver\\chromedriver.exe')
        driver.get(cag_url)
        pause = 1
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(pause)
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        driver.close()
        prod_items = soup.findAll('div', class_='cdt-product__img')
        for item in prod_items:
            a = item.find('a')
            if a is not None:
                links.append(domain_url + a.get('href'))
    for link in links:
        get_review(link)


def get_review(link):
    driver = webdriver.Chrome('..\\webdriver\\chromedriver.exe')
    driver.get(link)
    pause = 1
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(pause)
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    try:
        prod_id = soup.find('input', id='id-product').get('value')
        req1 = requests.get(f'https://fptshop.com.vn/apiFPTShop/Product/GetReviewAndRateByProduct?ProductId={prod_id}&PageIndex=1&PageSize=50&sortId=3')
        print(req1.json())
        extract_question(soup)
        while True:
            element0 = driver.find_element_by_id('f-comment-root')
            element = element0.find_element_by_xpath("//a[@class='pagination-link' and @aria-label='Next']")
            if element is None:
                break
            element.click()
            time.sleep(2)
            html = driver.page_source
            soup = BeautifulSoup(html, "html.parser")
            extract_question(soup)
    except:
        print('incorrect link: ' + link)
    driver.close()


def count_question_page(soup):
    paging = soup.find('ul', class_='pagination')
    total = int(paging.get('data-total'))
    size = int(paging.get('data-pagesize'))
    return -(-total // size)


def extract_question(soup):
    list_comment = soup.find('div', id='listComment')
    if list_comment is None:
        list_comment = soup.find('div', id='f-comment-root')
        questions = list_comment.findAll('div', class_='c-comment-text')
        for question in questions:
            ask = question.getText()
            print(ask)
    questions = list_comment.findAll('div', class_='f-cmt-ask', recursive=False)
    for question in questions:
        ask = question.find('div', class_='f-cmmain').getText()
        print(ask)


get_products()
