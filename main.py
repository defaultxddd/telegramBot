import httpx
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Создание бота и диспетчера
bot = Bot(token="6234842062:AAG-gshHugD6SuX2l0QZ9nYW1xYYUJgLFv0")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Функция для получения информации о фильме из API
async def get_movie_info(title):
    api_key = "9dd91112"
    url = f"http://www.omdbapi.com/?apikey={api_key}&t={title}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        data = response.json()
    return data

# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    await message.reply("Привет! Введи название фильма, чтобы получить информацию о нем.")

# Обработчик сообщений с названием фильма
@dp.message_handler()
async def movie_handler(message: types.Message):
    movie_title = message.text
    movie_info = await get_movie_info(movie_title)

    if movie_info.get("Response") == "True":
        title = movie_info["Title"]
        year = movie_info["Year"]
        plot = movie_info["Plot"]
        rating = movie_info["imdbRating"]
        imdb_id = movie_info["imdbID"]
        imdb_url = f"https://www.imdb.com/title/{imdb_id}/"

        response = f"Фильм: {title}\nГод: {year}\nРейтинг: {rating}\n\n{plot}\n\n{imdb_url}"

        keyboard = InlineKeyboardMarkup(row_width=1)
        button = InlineKeyboardButton(text="Подробнее", url=imdb_url)
        keyboard.add(button)

        await message.reply(response, reply_markup=keyboard)
    else:
        response = "Не удалось получить информацию о фильме."
        await message.reply(response)

# Запуск бота
if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp)
