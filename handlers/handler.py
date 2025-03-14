import asyncio
import os

from aiogram import Bot, Dispatcher, F, types
from aiogram.types import Message, CallbackQuery
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import CommandStart

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
    await message.answer("Привет! Я крутой бот. Для начала работы напиши любое слово.") 

@dp.message(F.text)
async def sh_lesson(message: types.Message, state: FSMContext):
    
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("Math", callback_data="lesson_math"),
        InlineKeyboardButton("Russian", callback_data="lesson_russ")
    )

    await message.answer("Выберите предмет:")
    await state.set_state(UserInfo.school_lesson)

@dp.callback_query(F.data.startswith("lesson_"))
async def sc_class(callback: CallbackQuery, state: FSMContext):
    await state.update_data(school_lesson=callback.data)
    await callback.message.edit_reply_markup(reply_markup=None) 
    
    markup = InlineKeyboardMarkup(row_width=2).add(
        *[InlineKeyboardButton(str(i), callback_data=f"class_{i}") for i in range(1, 12)]
    )
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
    await state.update_data(type_lesson=message.text)
    
    markup = InlineKeyboardMarkup(row_width=2).add(
        InlineKeyboardButton("Базовый", callback_data="level_base"),
        InlineKeyboardButton("Профильный", callback_data="level_profiled")
    )
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