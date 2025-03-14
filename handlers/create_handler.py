import asyncio
import os

from aiogram import Bot, Dispatcher, F, types, Router
from aiogram.types import Message, CallbackQuery
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import CommandStart, Command
from dotenv import load_dotenv
from .gpt import get_get_gpt_info

load_dotenv()

router = Router()

class UserInfo(StatesGroup):
    school_lesson = State()
    school_class = State()
    description = State()
    type_lesson = State()
    lesson_level = State()
    extra_time = State()
    text = State()


@router.message(Command('create'))
async def sh_lesson(message: types.Message, state: FSMContext):
    
    await message.answer("Выберите предмет:")
    await state.set_state(UserInfo.school_lesson)



@router.message(UserInfo.school_lesson)
async def sc_class(message: Message, state: FSMContext):
    """Получние данных класса"""
    await state.update_data(school_lesson=message.text)
    
    markup = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=str(i), callback_data=f"class_{i}") for i in range(1, 7)],
    [InlineKeyboardButton(text=str(i), callback_data=f"class_{i}") for i in range(7, 12)],
    ])
    await message.answer(f"Выберите класс:", reply_markup=markup)
    await state.set_state(UserInfo.school_class)


@router.callback_query(F.data.startswith("class_"))
async def theme(callback: CallbackQuery, state: FSMContext):
    await state.update_data(school_class=callback.data)
    await callback.message.edit_reply_markup(reply_markup=None)  
    
    await callback.message.answer("Введите тему урока:")
    await state.set_state(UserInfo.type_lesson)


@router.message(UserInfo.type_lesson)
async def level(message: Message, state: FSMContext):
    await state.update_data(type_lesson=message.text)
    markup = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Базовый", callback_data="level_base"),
     InlineKeyboardButton(text="Профильный", callback_data="level_profiled")]
    ])
    await message.answer("Выберите уровень подготовки:", reply_markup=markup)
    await state.set_state(UserInfo.lesson_level)


@router.callback_query(F.data.startswith("level_"))
async def extime(callback: CallbackQuery, state: FSMContext):
    await state.update_data(lesson_level=callback.data)
    await callback.message.edit_reply_markup(reply_markup=None)  
    
    await callback.message.answer("Введите количество времени на урок:")
    await state.set_state(UserInfo.extra_time)


@router.message(UserInfo.extra_time)
async def generation(message: Message, state: FSMContext):
    data = await state.update_data(extra_time=message.text)
    await message.answer("Введите описание вашего урока")
    await state.set_state(UserInfo.description)


@router.message(UserInfo.description)
async def description(message: Message, state: FSMContext):
    data = await state.update_data(description=message.text)
    await message.answer("Загрука")

    text = get_get_gpt_info(subject=data["school_lesson"], 
                        class_int=data["school_class"], 
                        description=data["description"],
                        theme=data["type_lesson"], 
                        hard=data["lesson_level"], 
                        time_lesson=data["extra_time"], 
                        tests=False, homework=False)

    await message.answer(text)
    await state.clear()
    

