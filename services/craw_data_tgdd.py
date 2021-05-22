from common_services import *
import threading

domain_url = 'https://www.thegioididong.com'
output_path = '..\\comment_tgdd.json'


def get_categories():
    soup = get_soup(domain_url)
    links = soup.find(class_='wrap-nav').find_all('a')
    categories = []
    for link in links:
        uri = link.get('href')
        if uri != '/phu-kien' and uri != '/tien-ich/thanh-toan-tra-gop':
            title = link.get('title')
            if title is None:
                h3 = link.find('h3')
                if h3 is not None:
                    title = h3.getText()
            categories.append({'link': domain_url + uri, 'title': title})
    return categories


def get_product(items, product):
    for item in items:
        a = item.find('a')
        link = a.get('href')
        url = domain_url + link
        h3 = a.find('h3')
        if h3 is not None:
            product_title = h3.getText()
            product['title'] = product_title
        product['link'] = url
        try:
            soup = get_soup(url + '/danh-gia')
        except:
            print('url error: ' + url)
        ratings = []
        ratings.extend(get_ratings(url + '/danh-gia'))
        paging = soup.find('div', class_='pgrc')
        if paging is not None:
            pageNum = soup.find('div', class_='pgrc').findAll('a')
            if pageNum is not None:
                for i in range(2, len(pageNum) + 1):
                    ratings.extend(get_ratings(url + '/danh-gia?p=' + str(i)))

        product['rating'] = ratings
        product['questions'] = get_question(get_soup(domain_url + link))
        print(product)


def get_question(soup):
    questions = soup.findAll('div', class_="question")
    comment_questions = []
    for question in questions:
        comment_questions.append(question.getText())
    return comment_questions


def get_ratings(url):
    comments = []
    try:
        soup = get_soup(url)
        ratings = soup.find('ul', class_='ratingLst')
        if ratings is not None:
            rating_comments = ratings.findAll('div', class_='rc')
            for rating in rating_comments:
                star = rating.findAll('i', class_='iconcom-txtstar')
                rating_star = 0 if star is None else len(star)
                rating_text = rating.find(lambda tag: tag.name == 'i' and not tag.attrs).getText()
                comments.append({'rating_star': rating_star, 'rating_text': rating_text})
    except:
        print('error url:' + url)
    return comments


def get_data():
    threads = []
    products = []
    for category in get_categories():
        print(category['link'] + '#i:20')
        soup = get_soup(category.get('link'))
        items = soup.find_all(class_='item')
        product = {'category': category['title']}
        products.append(product)
        thread = threading.Thread(target=get_product, args=(items, product,))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
    write_file_json(output_path, products)
    return products


def get_dat_no_thread():
    products = []
    for category in get_categories():
        print(category['link'] + '#i:20')
        soup = get_soup(category.get('link'))
        items = soup.find_all(class_='item')
        product = {'category': category['title']}
        products.append(product)
        get_product(items, product)
    write_file_json(output_path, products)
    return products


get_data()
