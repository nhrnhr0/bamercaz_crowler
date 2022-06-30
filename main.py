from bs4 import BeautifulSoup
import requests

def get_all_categories_urls():
    cateogies_urls = []
    url = f'https://www.bamercaz.co.il/sitemap.aspx'
    soup = BeautifulSoup(requests.get(url).text, 'lxml')
    sitemapTags = soup.find_all("sitemap")
    #print(soup.prettify())
    xmlDict = {}
    
    for sitemap in sitemapTags:
        cateogies_urls.append(sitemap.findNext("loc").text)

    #print(len(cateogies_urls))
    cateogies_urls = list(filter(lambda x: x.startswith('https://www.bamercaz.co.il/sitemap/categories/'),cateogies_urls))
    #print(len(cateogies_urls))
    
    #cateogies_urls = ['https://www.bamercaz.co.il/sitemap/categories/1/1/','https://www.bamercaz.co.il/sitemap/categories/2/1/','https://www.bamercaz.co.il/sitemap/categories/3/1/','https://www.bamercaz.co.il/sitemap/categories/4/1/','https://www.bamercaz.co.il/sitemap/categories/5/1/','https://www.bamercaz.co.il/sitemap/categories/6/1/','https://www.bamercaz.co.il/sitemap/categories/8/1/','https://www.bamercaz.co.il/sitemap/categories/9/1/','https://www.bamercaz.co.il/sitemap/categories/10/1/,''https://www.bamercaz.co.il/sitemap/categories/11/1/',]
    
    return cateogies_urls

def get_urls_from_category(url):
    entries = []
    soup = BeautifulSoup(requests.get(url).text, 'lxml')
    links = soup.find_all("url")
    for link in links:
        entries.append(link.text)
    return entries

def main():
    full_entries = []
    urls = get_all_categories_urls()
    i = 0
    for url in urls:
        entries = get_urls_from_category(url)
        print(i, url, ' => ', len(entries))
        #print(entries)
        full_entries.extend(entries)
        i+=1
    #print(urls)

    # write full_entries to file
    with open('urls.txt', 'w', encoding="utf-8") as f:
        for url in full_entries:
            f.write(url + '\n')
if __name__ == '__main__':
    main()