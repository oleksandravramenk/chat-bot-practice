import telebot
from telebot import types
import datetime

BOT_TOKEN = "8230563826:AAEobaWyOejKkSH9lo8rdkSZuuNzostCTFI"

bot = telebot.TeleBot(BOT_TOKEN)

# База даних книг (розширена версія)
books_db = {
    "художня": [
        {"id": 1, "title": "Кобзар", "author": "Тарас Шевченко", "available": True, "genre": "поезія", "year": 1840},
        {"id": 2, "title": "Лісова пісня", "author": "Леся Українка", "available": True, "genre": "драма", "year": 1911},
        {"id": 3, "title": "Тіні забутих предків", "author": "Михайло Коцюбинський", "available": False, "genre": "проза", "year": 1911},
        {"id": 4, "title": "Захар Беркут", "author": "Іван Франко", "available": True, "genre": "історичний роман", "year": 1883},
        {"id": 5, "title": "Маруся Чурай", "author": "Ліна Костенко", "available": True, "genre": "історичний роман", "year": 1979},
        {"id": 6, "title": "Камінний хрест", "author": "Василь Стефаник", "available": True, "genre": "новела", "year": 1900},
        {"id": 7, "title": "Земля", "author": "Ольга Кобилянська", "available": True, "genre": "роман", "year": 1902},
        {"id": 8, "title": "Украдене щастя", "author": "Іван Франко", "available": False, "genre": "повість", "year": 1893},
    ],
    "наукова": [
        {"id": 9, "title": "Історія України", "author": "Михайло Грушевський", "available": True, "genre": "історія", "year": 1898},
        {"id": 10, "title": "Філософські твори", "author": "Григорій Сковорода", "available": True, "genre": "філософія", "year": 1790},
        {"id": 11, "title": "Енциклопедія українознавства", "author": "Колектив авторів", "available": True, "genre": "енциклопедія", "year": 1949},
        {"id": 12, "title": "Походження українського народу", "author": "Володимир Білинський", "available": False, "genre": "історія", "year": 2000},
    ],
    "дитяча": [
        {"id": 13, "title": "Дивовижна мандрівка", "author": "Всеволод Нестайко", "available": True, "genre": "пригоди", "year": 1956},
        {"id": 14, "title": "Енеїда", "author": "Іван Котляревський", "available": True, "genre": "поема", "year": 1798},
        {"id": 15, "title": "Сірко", "author": "Анатолій Дімаров", "available": True, "genre": "пригоди", "year": 1964},
        {"id": 16, "title": "Казки", "author": "Іван Франко", "available": True, "genre": "казки", "year": 1896},
        {"id": 17, "title": "Ключ до таємниці", "author": "Всеволод Нестайко", "available": False, "genre": "пригоди", "year": 1961},
    ],
    "сучасна": [
        {"id": 18, "title": "Музей покинутих секретів", "author": "Оксана Забужко", "available": True, "genre": "роман", "year": 2009},
        {"id": 19, "title": "Вогнепальні", "author": "Сергій Жадан", "available": True, "genre": "роман", "year": 2012},
        {"id": 20, "title": "Інтернат", "author": "Сергій Жадан", "available": False, "genre": "роман", "year": 2017},
        {"id": 21, "title": "Твій погляд, Сколо", "author": "Марія Матіос", "available": True, "genre": "роман", "year": 2004},
        {"id": 22, "title": "Польові дослідження", "author": "Сергій Жадан", "available": True, "genre": "поезія", "year": 2023},
    ]
}

# Новини та події бібліотеки
events_db = [
    {
        "title": "Зустріч з письменником Сергієм Жаданом",
        "date": "15 січня 2025",
        "time": "15:00",
        "description": "Презентація нової книги та автограф-сесія"
    },
    {
        "title": "Літературний вечір до Дня Соборності",
        "date": "22 січня 2025", 
        "time": "17:00",
        "description": "Читання поезій українських класиків"
    },
    {
        "title": "Книжкова виставка 'Українська сучасна література'",
        "date": "10-31 січня 2025",
        "time": "09:00-17:00",
        "description": "Презентація нових надходжень"
    }
]

# База користувачів
users_data = {}

# База бронювань
bookings = {}

# База запитів на книги
book_requests = []

# Головне меню
def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("📚 Каталог книг")
    btn2 = types.KeyboardButton("🔍 Пошук книги")
    btn3 = types.KeyboardButton("⭐ Рекомендації")
    btn4 = types.KeyboardButton("📖 Мої книги")
    btn5 = types.KeyboardButton("📰 Новини та події")
    btn6 = types.KeyboardButton("ℹ️ Інформація")
    btn7 = types.KeyboardButton("📅 Режим роботи")
    markup.row(btn1, btn2)
    markup.row(btn3, btn4)
    markup.row(btn5)
    markup.row(btn6, btn7)
    return markup

# Команда /start
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    
    if user_id not in users_data:
        users_data[user_id] = {
            "name": first_name,
            "borrowed_books": [],
            "booked_books": [],
            "favorite_genres": [],
            "reading_history": [],
            "notifications": True
        }
    
    welcome_text = f"""
🎉 Вітаємо, {first_name}!

Ласкаво просимо до бота Полтавської обласної бібліотеки для юнацтва імені Олеся Гончара! 📚

Я допоможу тобі:
✅ Знайти потрібну книгу
✅ Забронювати книгу онлайн
✅ Отримати рекомендації
✅ Дізнатися про новинки та події
✅ Замовити книгу, якої немає в каталозі

Оберіть потрібний розділ з меню нижче 👇
"""
    
    bot.send_message(message.chat.id, welcome_text, reply_markup=main_menu())

# Обробка кнопки "Каталог книг"
@bot.message_handler(func=lambda message: message.text == "📚 Каталог книг")
def catalog(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("📖 Художня література", callback_data="cat_художня")
    btn2 = types.InlineKeyboardButton("🔬 Наукова література", callback_data="cat_наукова")
    btn3 = types.InlineKeyboardButton("👶 Дитяча література", callback_data="cat_дитяча")
    btn4 = types.InlineKeyboardButton("🌟 Сучасна українська", callback_data="cat_сучасна")
    markup.add(btn1)
    markup.add(btn2)
    markup.add(btn3)
    markup.add(btn4)
    
    bot.send_message(message.chat.id, "📚 Оберіть категорію:", reply_markup=markup)

# Обробка вибору категорії
@bot.callback_query_handler(func=lambda call: call.data.startswith("cat_"))
def category_handler(call):
    category = call.data.replace("cat_", "")
    books = books_db.get(category, [])
    
    if books:
        response = f"📚 *{category.capitalize()} література:*\n\n"
        for i, book in enumerate(books, 1):
            status = "✅ Доступна" if book["available"] else "❌ Видана"
            response += f"{i}. *{book['title']}*\n"
            response += f"   👤 Автор: {book['author']}\n"
            response += f"   📊 Статус: {status}\n"
            response += f"   📑 Жанр: {book['genre']}\n"
            response += f"   📅 Рік: {book['year']}\n"
            
            # Кнопка бронювання
            if book["available"]:
                response += f"   🔖 Забронювати: /book{book['id']}\n"
            else:
                response += f"   📩 Зарезервувати: /reserve{book['id']}\n"
            response += "\n"
        
        bot.send_message(call.message.chat.id, response, parse_mode="Markdown")
    else:
        bot.send_message(call.message.chat.id, "Книги в цій категорії поки що недоступні.")

# Бронювання книги
@bot.message_handler(func=lambda message: message.text.startswith("/book"))
def book_book(message):
    try:
        book_id = int(message.text.replace("/book", ""))
        user_id = message.from_user.id
        
        # Знаходимо книгу
        book = None
        for category in books_db.values():
            for b in category:
                if b["id"] == book_id:
                    book = b
                    break
        
        if book and book["available"]:
            # Бронюємо книгу
            if user_id not in bookings:
                bookings[user_id] = []
            
            bookings[user_id].append({
                "book_id": book_id,
                "title": book["title"],
                "author": book["author"],
                "date": datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
            })
            
            users_data[user_id]["booked_books"].append(book["title"])
            
            response = f"""
✅ Книгу успішно забронювано!

📖 *{book['title']}*
👤 Автор: {book['author']}
🕐 Час бронювання: {datetime.datetime.now().strftime("%d.%m.%Y %H:%M")}

⏰ Книга чекатиме на вас протягом 3 днів.

📍 Забрати можна за адресою:
вул. Олеся Гончара, 25а, Полтава

📞 Телефон: (0532) 67-64-02

💡 Не забудьте читацький квиток!
"""
            bot.send_message(message.chat.id, response, parse_mode="Markdown")
        else:
            bot.send_message(message.chat.id, "❌ На жаль, ця книга вже недоступна для бронювання.")
    except:
        bot.send_message(message.chat.id, "❌ Помилка при бронюванні. Перевірте правильність команди.")

# Резервування виданої книги
@bot.message_handler(func=lambda message: message.text.startswith("/reserve"))
def reserve_book(message):
    try:
        book_id = int(message.text.replace("/reserve", ""))
        user_id = message.from_user.id
        
        book = None
        for category in books_db.values():
            for b in category:
                if b["id"] == book_id:
                    book = b
                    break
        
        if book:
            response = f"""
📋 Книгу зарезервовано!

📖 *{book['title']}*
👤 Автор: {book['author']}

Ця книга зараз у читача. Ми повідомимо вас, коли вона стане доступною!

📧 Очікуйте повідомлення від бота.
📞 Або зателефонуйте: (0532) 67-64-02
"""
            bot.send_message(message.chat.id, response, parse_mode="Markdown")
    except:
        bot.send_message(message.chat.id, "❌ Помилка при резервуванні.")

# Обробка кнопки "Пошук книги"
@bot.message_handler(func=lambda message: message.text == "🔍 Пошук книги")
def search_book(message):
    msg = bot.send_message(message.chat.id, "🔍 Введіть назву книги або автора:")
    bot.register_next_step_handler(msg, process_search)

def process_search(message):
    search_query = message.text.lower()
    results = []
    
    for category, books in books_db.items():
        for book in books:
            if search_query in book['title'].lower() or search_query in book['author'].lower():
                results.append(book)
    
    if results:
        response = "🔍 *Результати пошуку:*\n\n"
        for i, book in enumerate(results, 1):
            status = "✅ Доступна" if book["available"] else "❌ Видана"
            response += f"{i}. *{book['title']}*\n"
            response += f"   👤 Автор: {book['author']}\n"
            response += f"   📊 Статус: {status}\n"
            response += f"   📑 Жанр: {book['genre']}\n"
            
            if book["available"]:
                response += f"   🔖 Забронювати: /book{book['id']}\n"
            else:
                response += f"   📩 Зарезервувати: /reserve{book['id']}\n"
            response += "\n"
        
        bot.send_message(message.chat.id, response, parse_mode="Markdown")
    else:
        # Якщо не знайдено - пропонуємо замовити
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton("📝 Замовити цю книгу", callback_data=f"request_{search_query}")
        markup.add(btn)
        
        response = f"""
😔 На жаль, нічого не знайдено за запитом: "{message.text}"

💡 Ви можете замовити цю книгу, і ми спробуємо її придбати для бібліотеки!
"""
        bot.send_message(message.chat.id, response, reply_markup=markup)

# Замовлення книги
@bot.callback_query_handler(func=lambda call: call.data.startswith("request_"))
def request_book(call):
    book_name = call.data.replace("request_", "")
    user_id = call.from_user.id
    user_name = users_data.get(user_id, {}).get("name", "Користувач")
    
    book_requests.append({
        "user_id": user_id,
        "user_name": user_name,
        "book": book_name,
        "date": datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
    })
    
    response = f"""
✅ Ваш запит прийнято!

📖 Книга: *{book_name}*
👤 Замовник: {user_name}
🕐 Дата запиту: {datetime.datetime.now().strftime("%d.%m.%Y %H:%M")}

Бібліотекарі розглянуть ваш запит найближчим часом. 

📞 Для уточнення зателефонуйте: (0532) 67-64-02

Дякуємо за активність! 📚
"""
    bot.send_message(call.message.chat.id, response, parse_mode="Markdown")

# Обробка кнопки "Рекомендації"
@bot.message_handler(func=lambda message: message.text == "⭐ Рекомендації")
def recommendations(message):
    recommendations_text = """
⭐ *Рекомендації місяця:*

1. 📖 *"Кобзар"* - Тарас Шевченко
   Безсмертна класика української поезії
   🔖 Забронювати: /book1

2. 📖 *"Лісова пісня"* - Леся Українка
   Філософська драма-феєрія про кохання
   🔖 Забронювати: /book2

3. 📖 *"Захар Беркут"* - Іван Франко
   Історичний роман про боротьбу карпатців
   🔖 Забронювати: /book4

4. 📖 *"Музей покинутих секретів"* - Оксана Забужко
   Сучасний роман про пам'ять і історію
   🔖 Забронювати: /book18

5. 📖 *"Польові дослідження"* - Сергій Жадан
   Актуальна сучасна поезія
   🔖 Забронювати: /book22

💡 Використовуйте 🔍 Пошук для більш детального підбору!
"""
    bot.send_message(message.chat.id, recommendations_text, parse_mode="Markdown")

# Обробка кнопки "Мої книги"
@bot.message_handler(func=lambda message: message.text == "📖 Мої книги")
def my_books(message):
    user_id = message.from_user.id
    
    if user_id in users_data:
        borrowed = users_data[user_id].get("borrowed_books", [])
        booked = users_data[user_id].get("booked_books", [])
        
        response = "📖 *Ваші книги:*\n\n"
        
        if borrowed:
            response += "*📚 Взяті книги:*\n"
            for book in borrowed:
                response += f"• {book}\n"
            response += "\n"
        
        if booked:
            response += "*🔖 Заброньовані книги:*\n"
            for book in booked:
                response += f"• {book}\n"
            response += "\n⏰ Забрати протягом 3 днів!\n\n"
        
        if not borrowed and not booked:
            response = "📭 У вас поки що немає взятих або заброньованих книг.\n\n✨ Відвідайте наш каталог, щоб обрати щось цікаве!"
    else:
        response = "📭 У вас поки що немає взятих книг.\n\n✨ Відвідайте наш каталог!"
    
    bot.send_message(message.chat.id, response, parse_mode="Markdown")

# Новини та події
@bot.message_handler(func=lambda message: message.text == "📰 Новини та події")
def news_and_events(message):
    response = "📰 *Новини та майбутні події:*\n\n"
    
    for i, event in enumerate(events_db, 1):
        response += f"{i}. *{event['title']}*\n"
        response += f"   📅 Дата: {event['date']}\n"
        response += f"   🕐 Час: {event['time']}\n"
        response += f"   📝 {event['description']}\n\n"
    
    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton("🔔 Увімкнути нагадування", callback_data="notifications_on")
    markup.add(btn)
    
    response += "\n💡 Увімкніть нагадування, щоб не пропустити події!"
    
    bot.send_message(message.chat.id, response, parse_mode="Markdown", reply_markup=markup)

# Увімкнення нагадувань
@bot.callback_query_handler(func=lambda call: call.data == "notifications_on")
def enable_notifications(call):
    user_id = call.from_user.id
    if user_id in users_data:
        users_data[user_id]["notifications"] = True
    
    bot.send_message(call.message.chat.id, "✅ Нагадування увімкнено! Ви отримаєте повідомлення про майбутні події за день до початку.")

# Обробка кнопки "Інформація"
@bot.message_handler(func=lambda message: message.text == "ℹ️ Інформація")
def info(message):
    markup = types.InlineKeyboardMarkup()
    
    btn_site = types.InlineKeyboardButton("🌐 Веб-сайт", url="https://libgonchar.org/")
    btn_fb = types.InlineKeyboardButton("📘 Facebook", url="https://www.facebook.com/pobugonchara")
    btn_insta = types.InlineKeyboardButton("📸 Instagram", url="https://www.instagram.com/pobu_gonchara/")
    btn_youtube = types.InlineKeyboardButton("▶️ YouTube", url="https://www.youtube.com/user/LibGonchar")
    btn_tiktok = types.InlineKeyboardButton("🎵 TikTok", url="https://www.tiktok.com/@libgoncharpoltava")
    
    markup.add(btn_site)
    markup.row(btn_fb, btn_insta)
    markup.row(btn_youtube, btn_tiktok)
    
    info_text = """
ℹ️ *Полтавська обласна бібліотека для юнацтва імені Олеся Гончара*

📍 *Адреса:* 
вулиця Олеся Гончара, 25а, Полтава
Полтавська область, 36000

📞 *Контакти:*
• Телефон: (0532) 67-64-02
• Адреса: 36039, м. Полтава, вул. Олеся Гончара, 25-а

🏛️ *Дата основання:* 1976 рік

💡 *Наша місія:* надання якісних бібліотечних послуг для молоді та юнацтва Полтавщини.

📱 Підписуйтесь на наші соціальні мережі, щоб не пропустити новини та події! 👇
"""
    
    bot.send_message(message.chat.id, info_text, parse_mode="Markdown", reply_markup=markup)

# Обробка кнопки "Режим роботи"
@bot.message_handler(func=lambda message: message.text == "📅 Режим роботи")
def schedule(message):
    schedule_text = """
📅 *Режим роботи бібліотеки:*

📌 *Основний графік:*

🕐 Понеділок: 09:00 – 17:00
🕐 Вівторок: 09:00 – 17:00
🕐 Середа: 09:00 – 17:00
🕐 Четвер: 09:00 – 17:00
⚠️ *Увага! Години роботи можуть змінюватися*

🕐 П'ятниця: 09:00 – 17:00
🕐 Субота: Зачинено ❌
🕐 Неділя: 09:00 – 17:00

💡 *Корисні поради:*
• Краще приходити до 16:30, щоб встигнути оформити книги
• Не забувайте читацький квиток
• При першому відвідуванні потрібен паспорт для реєстрації

📞 Для уточнення інформації телефонуйте: (0532) 67-64-02

🔖 Забронюйте книгу через бот і забирайте без черги!
"""
    
    bot.send_message(message.chat.id, schedule_text, parse_mode="Markdown")

# Команда /help
@bot.message_handler(commands=['help'])
def help_command(message):
    help_text = """
🤖 *Довідка по боту*

*Основні команди:*
/start - Запустити бота
/help - Показати цю довідку

*Доступні функції:*

📚 *Каталог книг* - перегляд книг за категоріями
🔍 *Пошук книги* - знайти книгу за назвою або автором
⭐ *Рекомендації* - отримати рекомендації від бібліотекарів
📖 *Мої книги* - переглянути свої взяті та заброньовані книги
📰 *Новини та події* - актуальні події бібліотеки
ℹ️ *Інформація* - контакти та соціальні мережі
📅 *Режим роботи* - години роботи бібліотеки

🔖 *Бронювання:*
Натисніть на команду /bookX поруч з книгою для бронювання

💬 Якщо у вас є запитання, пишіть нам!
"""
    bot.send_message(message.chat.id, help_text, parse_mode="Markdown")

# Обробка всіх інших повідомлень
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.send_message(message.chat.id, 
                    "Вибачте, я не зрозумів це повідомлення. 🤔\n\nВикористовуйте меню нижче або команду /help, щоб дізнатися про мої можливості.",
                    reply_markup=main_menu())

# Запуск бота
print("🤖 Бот запущено! Очікування повідомлень...")
print("📚 Полтавська обласна бібліотека для юнацтва імені Олеся Гончара")
print("⏰ Бот працює цілодобово!")
print("")
print("✅ Функції бота:")
print("   🔖 Система бронювання книг")
print("   📩 Замовлення відсутніх книг")
print("   🔍 Розширений пошук")
print("   📰 Новини та події з нагадуваннями")
print("   📊 База даних: 22 книги у 4 категоріях")
print("")
bot.polling(none_stop=True)