from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from pyexpat.errors import messages

api = ''
bot = Bot(token = api)
dp = Dispatcher(bot, storage = MemoryStorage())

kb = ReplyKeyboardMarkup()
button1 = KeyboardButton(text = 'Рассчитать')
button2 = KeyboardButton(text = 'Информация')
kb.add(button1)
kb.add(button2)
kb.resize_keyboard = True

inline_kb = InlineKeyboardMarkup()
button3 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
button4 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
inline_kb.add(button3)
inline_kb.add(button4)
inline_kb.resize_keyboard = True

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.message_handler(text = 'Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup = inline_kb)

@dp.callback_query_handler(text = 'formulas')
async def get_formulas(call):
    await call.message.answer('10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5')
    await call.answer()

@dp.callback_query_handler(text = 'calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()

@dp.message_handler(state = UserState.age)
async def set_growth(message, state):
    await state.update_data(first = message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()

@dp.message_handler(state = UserState.growth)
async def set_weight(message, state):
    await state.update_data(second = message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()

@dp.message_handler(state = UserState.weight)
async def send_calories(message, state):
    await state.update_data(third = message.text)
    data = await state.get_data()
    calories = 10 * int(data['first']) + 6.25 * int(data['second']) - 5 * int(data['third']) + 5
    await message.answer(f'Ваша норма калорий - {calories}')

    await state.finish()

@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет! Я бот, помогающий твоему здоровью.', reply_markup = kb)

@dp.message_handler()
async def all_massages(message):
    await message.answer('Введите команду /start, чтобы начать общение.')



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)