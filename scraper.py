import requests
from bs4 import BeautifulSoup
import json

# URL страницы
BASE_URL = "http://quotes.toscrape.com/page/{}/"

# Списки для хранения цитат и авторов
quotes_data = []
authors_data = []

# Функция для скрапинга данных
def scrape_quotes(page_num):
    url = BASE_URL.format(page_num)
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Находим все контейнеры с цитатами
        quotes = soup.find_all("div", class_="quote")
        
        for quote in quotes:
            text = quote.find("span", class_="text").get_text()
            author_name = quote.find("small", class_="author").get_text()
            tags = [tag.get_text() for tag in quote.find_all("a", class_="tag")]
            
            # Добавляем цитату в список
            quotes_data.append({
                "tags": tags,
                "author": author_name,
                "quote": text
            })
            
            # Сбор информации об авторе
            if author_name not in [author['fullname'] for author in authors_data]:
                author_url = quote.find("a")["href"]
                author_info = get_author_info(author_url)
                authors_data.append(author_info)

# Функция для получения информации об авторе
def get_author_info(author_url):
    author_base_url = "http://quotes.toscrape.com"
    response = requests.get(author_base_url + author_url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        
        fullname = soup.find("h3", class_="author-title").get_text().strip()
        born_date = soup.find("span", class_="author-born-date").get_text()
        born_location = soup.find("span", class_="author-born-location").get_text()
        description = soup.find("div", class_="author-description").get_text().strip()
        
        return {
            "fullname": fullname,
            "born_date": born_date,
            "born_location": born_location,
            "description": description
        }

# Пагинация: собираем данные с каждой страницы
page_num = 1
while True:
    scrape_quotes(page_num)
    page_num += 1
    
    # Проверяем, есть ли следующая страница
    next_page = BeautifulSoup(requests.get(BASE_URL.format(page_num)).text, "html.parser").find("li", class_="next")
    if not next_page:
        break

# Сохраняем в JSON файлы
with open('quotes.json', 'w', encoding='utf-8') as f:
    json.dump(quotes_data, f, ensure_ascii=False, indent=4)

with open('authors.json', 'w', encoding='utf-8') as f:
    json.dump(authors_data, f, ensure_ascii=False, indent=4)

print("Данные успешно собраны и сохранены в файлы.")
