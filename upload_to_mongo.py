from pymongo import MongoClient
import json

# Подключение к базе данных MongoDB Atlas
client = MongoClient("mongodb+srv://goitlearn:KAh-N7y7xnT6%3AkW@cluster0.vxppp.mongodb.net/?retryWrites=true&w=majority")
db = client["quotes_db"]

# Импорт данных в коллекции
with open('quotes.json', 'r', encoding='utf-8') as f:
    quotes = json.load(f)
    db.quotes.insert_many(quotes)

with open('authors.json', 'r', encoding='utf-8') as f:
    authors = json.load(f)
    db.authors.insert_many(authors)

print("Данные успешно импортированы в MongoDB.")
