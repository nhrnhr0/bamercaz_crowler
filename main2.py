
import csv
from bs4 import BeautifulSoup
import requests
import re
from csv import writer
import datetime
import xlsxwriter

def clean_location_from_url(url):
    if url.count('/') > 3:
        reg = '(https:\/\/www\.bamercaz\.co\.il\/.+)\/.+\/'
        url = re.sub(reg, '\\1/', url)
    return url
def get_urls():
    # read urls.txt and remove duplicates
    with open('urls.txt', 'r', encoding="utf-8") as f:
        urls = f.readlines()
    urls = map(clean_location_from_url, urls)
    urls = list(set(urls))
    return urls


def load_url_info(url, pagenum=1, last_page_results=None):
    request_url = url + str(pagenum) if pagenum > 1 else url
    if request_url.endswith('/') == False:
        request_url += '/'
    soup = BeautifulSoup(requests.get(request_url).text, 'lxml')
    # save soup to temp.html
    with open('temp.html', 'w', encoding="utf-8") as f:
        f.write(soup.prettify())
        
    page_content = soup.find('div', {'id': 'page_content'})
    content = page_content.find('div', {'class': 'content'})
    ret = []
    spans = content.find_all('span')
    # itemprop="itemListElement"
    spans = [span for span in spans if span.get('itemprop') == 'itemListElement']
    for span in spans:
        href = span.find('a', {'class': 'title'})
        link = href.get('href')
        name = href.text
        ret.append((name, link))
    print(request_url, ' => ', len(ret))
    if last_page_results and ret == last_page_results:
        return []
    if (len(ret) != 0):
        ret.extend(load_url_info(url, pagenum + 1, ret))
        return ret
    return ret

def main2():
    # open places.csv and append to it [url, name, link]
    filename = 'places' + datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S') + '.csv'
    with  open(filename, 'w', newline='', encoding="utf-8") as csvfile:
        pass
    
    urls = get_urls()
    xl_row_count = 1
    for url in urls:
        if url.endswith('\n'):
            url = url[:-1]
            
        # remove the secound slash with the location if exists
        if url.count('/') > 3:
            reg = '(https:\/\/www\.bamercaz\.co\.il\/.+)\/.+\/'
            url = re.sub(reg, '\\1/', url)

        
        res = load_url_info(url)
        print('done', url, '=>', len(res))
        with  open(filename, 'a', newline='', encoding="utf-8") as csvfile:
        #with  open('places.csv', 'a', newline='', encoding="utf-8") as csvfile:
            csvwriter = csv.writer(csvfile)
            for contact in res:
                name, link = contact
                csvwriter.writerow([url,name, link])
                # worksheet.write(xl_row_count, 0, url)
                # worksheet.write(xl_row_count, 1, name)
                # worksheet.write(xl_row_count, 2, link)
                xl_row_count+=1
            print('saved')
if __name__ == '__main__':
    main2()