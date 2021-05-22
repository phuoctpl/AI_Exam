from common_services import *
from selenium import webdriver
from bs4 import BeautifulSoup
from jsonpath_ng import jsonpath, parse
import requests
import time

domain_url = 'https://fptshop.com.vn'
cag_urls = ['https://fptshop.com.vn/dien-thoai?sort=ban-chay-nhat&trang=20',
            'https://fptshop.com.vn/may-tinh-xach-tay?sort=ban-chay-nhat&trang=20']
output_comment_file = '..\\comment_fpt.txt'
output_question_file = '..\\question_fpt.txt'


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
    reviews = []
    jsonpath_expression = parse('$..listItems[*].commentCustomer')
    try:
        prod_id = soup.find('input', id='id-product').get('value')
        req1 = requests.get(f'https://fptshop.com.vn/apiFPTShop/Product/GetReviewAndRateByProduct?ProductId={prod_id}&PageIndex=1&PageSize=100&sortId=3')
        for match in jsonpath_expression.find(req1.json()):
            reviews.append(match.value)
        print(reviews)
        write_file_text(output_question_file, extract_question(soup), '1')
        while True:
            element0 = driver.find_element_by_id('f-comment-root')
            element = element0.find_element_by_xpath(".//i[@class='demo-icon icon-angle-right']")
            if element is None:
                break
            element.click()
            time.sleep(2)
            html = driver.page_source
            soup = BeautifulSoup(html, "html.parser")
            write_file_text(output_question_file, extract_question(soup), '1')
    except:
        print('incorrect link: ' + link)
    driver.close()
    write_file_text(output_comment_file, reviews, '0')


def extract_question(soup):
    list_comment = soup.find('div', id='listComment')
    question_text_list = []
    if list_comment is None:
        list_comment = soup.find('div', id='f-comment-root')
        contents = set(list_comment.findAll('div', class_='c-comment-box'))
        answers = set(list_comment.findAll('div', class_='level2'))
        questions = contents - answers
        for question in questions:
            q_text = question.find('div', class_='c-comment-text').getText()
            question_text_list.append(q_text)
            print(q_text)
    else:
        questions = list_comment.findAll('div', class_='f-cmt-ask', recursive=False)
        for question in questions:
            q_text = question.find('div', class_='f-cmmain').getText()
            print(q_text)

    return question_text_list


get_products()
