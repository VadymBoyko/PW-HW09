import requests
import json
from bs4 import BeautifulSoup

url = 'https://quotes.toscrape.com/'


def get_author_info(author_url) -> dict:
    result = dict()
    author_response = requests.get(author_url)
    author_soup = BeautifulSoup(author_response.text, 'lxml')
    result['fullname'] = author_soup.find_all('h3', class_='author-title')[0].text.strip()
    result['born_date'] = author_soup.find_all('span', class_='author-born-date')[0].text.strip()
    result['born_location'] = author_soup.find_all('span', class_='author-born-location')[0].text.strip()
    result['description'] = author_soup.find_all('div', class_='author-description')[0].text.strip()
    return result


def pars_quotes() -> None:
    authors_list = list()
    result_authors = list()
    result_quotes = list()

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    quote_div = soup.find_all('div', class_="quote")
    quotes = soup.find_all('span', class_='text')
    authors = soup.find_all('small', class_='author')
    tags = soup.find_all('div', class_='tags')

    for i in range(0, len(quote_div)):
        quote = dict()
        author_name = authors[i].text
        quote['quote'] = quotes[i].text
        quote['author'] = author_name
        quote['tags'] = tags[i].find_all('meta', class_='keywords')[0].attrs['content'].split(',')
        result_quotes.append(quote)
        if author_name not in authors_list:  # якщо автора ще нема, то заповнюємо інфу про нього, та додаеємо у список
            result_authors.append(get_author_info(url + quote_div[i].find('a')['href']))
            authors_list.append(author_name)

    with open(r'data\authors.json', 'w', encoding='utf-8') as fd:
        json.dump(result_authors, fd, ensure_ascii=False)

    with open(r'data\qoutes.json', 'w', encoding='utf-8') as fd:
        json.dump(result_quotes, fd, ensure_ascii=False)


if __name__ == '__main__':
    pars_quotes()
