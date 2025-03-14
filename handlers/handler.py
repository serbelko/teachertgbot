import asyncio
import os

from aiogram import Bot, Dispatcher, F, types
from aiogram.types import Message, CallbackQuery
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import CommandStart, Command
from dotenv import load_dotenv
from database.using import get_text, get_top_users

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

class UserInfo(StatesGroup):
    school_lesson = State()
    school_class = State()
    type_lesson = State()
    lesson_level = State()
    extra_time = State()

@dp.message(CommandStart())
async def start(message: types.Message, state: FSMContext):
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Вопросы и ответы", callback_data="faq"),
         InlineKeyboardButton(text="Мои сценарии", callback_data="scenarios"),
         InlineKeyboardButton(text="Топ пользователей", callback_data="top_users")]
    ])
    await message.answer("Привет! Я крутой бот. Для начала работы напиши любое слово.\nВведите команду /create чтобы начать или выберите опцию:", reply_markup=markup) 

@dp.callback_query(F.data == 'faq')
async def ask_and_ques(callback: CallbackQuery):
    faq_txt = f'1. aaaa ответ: bbbbbbbbb'
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Назад', callback_data='back')]  
    ])
    await callback.message.edit_text(faq_txt, reply_markup=markup)
    await callback.answer()


@dp.callback_query(F.data == 'scenarios')
async def my_scenes(callback: CallbackQuery):
    user_id = str(callback.from_user.id)
    scenes = get_text(user_id)
    if isinstance(scenes,list):
        scen_text = ''.join([f'{scen['label']}: {scen['text']}' for scen in scenes])
    else:
        scen_text = f'{scenes['label']}: {scenes['text']}'

    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Назад', callback_data='back')]  
    ])

    await callback.message.edit_text(scen_text, reply_markup=markup)
    await callback.answer()

@dp.callback_query(F.data=="back")
async def start(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup(reply_markup=None) 
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Вопросы и ответы", callback_data="faq"),
         InlineKeyboardButton(text="Мои сценарии", callback_data="scenarios"),
         InlineKeyboardButton(text="Топ пользователей", callback_data="top_users")]
    ])
    await callback.message.answer("Привет! Я крутой бот. Для начала работы напиши любое слово.\nВведите команду /create чтобы начать или выберите опцию:", reply_markup=markup) 


@dp.message(Command('create'))
async def sh_lesson(message: types.Message, state: FSMContext):
    markup = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Math", callback_data="lesson_math"),InlineKeyboardButton(text="Russian", callback_data="lesson_russ")]])
    await message.answer("Выберите предмет:", reply_markup=markup)
    await state.set_state(UserInfo.school_lesson)

@dp.callback_query(F.data.startswith("lesson_"))
async def sc_class(callback: CallbackQuery, state: FSMContext):
    await state.update_data(school_lesson=callback.data)
    await callback.message.edit_reply_markup(reply_markup=None) 
    
    markup = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=str(i), callback_data=f"class_{i}") for i in range(1, 12)]
    ])
    await callback.message.answer("Выберите класс:", reply_markup=markup)
    await state.set_state(UserInfo.school_class)

@dp.callback_query(F.data.startswith("class_"))
async def theme(callback: CallbackQuery, state: FSMContext):
    await state.update_data(school_class=callback.data)
    await callback.message.edit_reply_markup(reply_markup=None)  
    
    await callback.message.answer("Введите тему урока:")
    await state.set_state(UserInfo.type_lesson)

@dp.message(UserInfo.type_lesson)
async def level(message: Message, state: FSMContext):
    # await state.update_data(type_lesson=message.text)
    
    markup = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Базовый", callback_data="level_base"),
     InlineKeyboardButton(text="Профильный", callback_data="level_profiled")]
    ])
    await message.answer("Выберите уровень подготовки:", reply_markup=markup)
    await state.set_state(UserInfo.lesson_level)

@dp.callback_query(F.data.startswith("level_"))
async def extime(callback: CallbackQuery, state: FSMContext):
    await state.update_data(lesson_level=callback.data)
    await callback.message.edit_reply_markup(reply_markup=None)  
    
    await callback.message.answer("Введите количество запасного времени в минутах (число):")
    await state.set_state(UserInfo.extra_time)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())