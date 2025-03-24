from pymongo import MongoClient
from pymongo.server_api import ServerApi

# Подключаемся к Mongo
try:
    client = MongoClient(
        "mongodb+srv://goitlearn:KAh-N7y7xnT6%3AkW@cluster0.vxppp.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
        server_api=ServerApi('1')
    )
    db = client.homework3
    print("Успешное подключение к MongoDB")
except Exception as e:
    print(f"Ошибка подключения: {e}")
    exit()  # Если нет подключения, завершаем программу 


def get_all_cats():
    """Получаем список всех котов в базе"""
    try:
        for cat in db.cats.find():
            print(cat)
    except Exception as e:
        print(f"Ошибка при получении списка котов: {e}")


def get_cat_by_name(name):
    """Ищем кота по имени"""
    try:
        cat = db.cats.find_one({"name": name})
        if cat:
            print(cat)
        else:
            print("Кіт не знайдений")
    except Exception as e:
        print(f"Ошибка при поиске кота: {e}")


def update_cat_age(name, new_age):
    """Обновляем возраст кота"""
    try:
        result = db.cats.update_one({"name": name}, {"$set": {"age": new_age}})
        print(f"Оновлено {result.modified_count} записів")
    except Exception as e:
        print(f"Ошибка при обновлении возраста кота: {e}")


def add_feature_to_cat(name, feature):
    """Добавляем новую характеристику коту"""
    try:
        result = db.cats.update_one({"name": name}, {"$push": {"features": feature}})
        print(f"Оновлено {result.modified_count} записів")
    except Exception as e:
        print(f"Ошибка при добавлении характеристики: {e}")


def delete_cat_by_name(name):
    """Удаляем кота по имени"""
    try:
        result = db.cats.delete_one({"name": name})
        print(f"Видалено {result.deleted_count} записів")
    except Exception as e:
        print(f"Ошибка при удалении кота: {e}")


def delete_all_cats():
    """Удаляем всех котов в базе"""
    try:
        result = db.cats.delete_many({})
        print(f"Видалено {result.deleted_count} записів")
    except Exception as e:
        print(f"Ошибка при удалении всех котов: {e}")


if __name__ == "__main__":
    print("\n Очищаем базу перед добавлением кота")
    delete_all_cats()

    print("\n Добавляем нового кота 'barsik'")
    try:
        result_one = db.cats.insert_one(
            {
                "name": "barsik",
                "age": 3,
                "features": ["ходить в капці", "дає себе гладити", "рудий"],
            }
        )
        print(f"Добавлен кот с ID: {result_one.inserted_id}")
    except Exception as e:
        print(f"Ошибка при добавлении кота: {e}")

    print("\n Все коты в базе:")
    get_all_cats()

    print("\n Ищем кота 'barsik':")
    get_cat_by_name("barsik")

    print("\n Оновлюємо вік 'barsik' до 5 років:")
    update_cat_age("barsik", 5)

    print("\n Додаємо характеристику 'любить рибу' до 'barsik':")
    add_feature_to_cat("barsik", "любить рибу")

    print("\n Шукаємо оновленого 'barsik':")
    get_cat_by_name("barsik")

    print("\n Видаляємо 'barsik':")
    delete_cat_by_name("barsik")

    print("\n Всі коти після видалення:")
    get_all_cats()