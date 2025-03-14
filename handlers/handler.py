import asyncio
import os

from aiogram import Bot, Router, F, types
from aiogram.types import Message, CallbackQuery
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import CommandStart, Command
from dotenv import load_dotenv


base_router = Router()


class UserInfo(StatesGroup):
    school_lesson = State()
    school_class = State()
    type_lesson = State()
    lesson_level = State()
    extra_time = State()

@base_router.message(CommandStart())
async def start(message: types.Message):
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Вопросы и ответы", callback_data="faq")],
        [InlineKeyboardButton(text="Мои сценарии", callback_data="scenarios")],
        [InlineKeyboardButton(text="Топ пользователей", callback_data="top_users")]
    ])
    await message.answer("Привет! Я крутой бот. Введите команду /create чтобы начать или выберите опцию:", reply_markup=markup)

@base_router.callback_query(F.data == 'faq')
async def ask_and_ques(callback: CallbackQuery):
    faq_txt = f"""
    1. Как создать новый сценарий?
    Для создания сценария необходимо ввести команду /create и следовать указаниям бота. Необходимо будут ввести предмет, класс учеников, тему урока, уровень подготовки (базовый/профильный) и количество запасного времени.

    2. Что делать, если бот присылает сценарий по другой теме? Постарайтесь подробнее описать тему и урока и попробовать ещё раз :)
    """
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Назад', callback_data='back')]  
    ])
    await callback.message.edit_text(faq_txt, reply_markup=markup)
    await callback.answer()


@base_router.callback_query(F.data == 'scenarios')
async def my_scenes(callback: CallbackQuery):
    user_id = str(callback.from_user.id)
    scenes = {"label": "text", "text": "text"}
    if isinstance(scenes,list):
        scen_text = ''.join([f'{scen['label']}: {scen['text']}' for scen in scenes])
    else:
        scen_text = f'{scenes['label']}: {scenes['text']}'

    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Назад', callback_data='back')]  
    ])

    await callback.message.edit_text(scen_text, reply_markup=markup)
    await callback.answer()

@base_router.callback_query(F.data=="back")
async def start(callback: CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=None) 
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Вопросы и ответы", callback_data="faq")],
        [InlineKeyboardButton(text="Мои сценарии", callback_data="scenarios")],
        [InlineKeyboardButton(text="Топ пользователей", callback_data="top_users")]
    ])
    await callback.message.edit_text("Привет! Я крутой бот. Для начала работы напиши любое слово.\nВведите команду /create чтобы начать или выберите опцию:", reply_markup=markup) 
    await callback.answer()
