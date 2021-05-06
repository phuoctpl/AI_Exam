from common_services import *
import threading

domain_url = 'https://fptshop.com.vn/'
output_path = '..\\comment_fpt.json'


def get_categories():
    soup = get_soup(domain_url)
    links = soup.find('nav', class_='fs-menu').find_all('a', class_='sax')
    indexs = [0, 1, 3, 4, 6, 7]
    categories = []
    if len(links) > 7:
        for i in indexs:
            uri = links[i].get('href')
            title = links[i].get('title')
            if title is None:
                h3 = find('h3')
                if h3 is not None:
                    title = h3.getText()
                categories.append({'link': domain_url + uri, 'title': title})
    return categories


get_categories()
