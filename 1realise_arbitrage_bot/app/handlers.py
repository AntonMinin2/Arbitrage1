import os
import subprocess

from aiogram.types import FSInputFile
from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from telethon import TelegramClient
import re

from app.savetiktok import tiktok_save
import app.keyboards as kb

router = Router()


# Путь к директориям
SCRIPT_DIR = '../app'
SAVED_VIDEO_DO_DIR = os.path.join(SCRIPT_DIR, 'savedvideo_DO')
SAVED_VIDEO_PAST_DIR = os.path.join(SCRIPT_DIR, 'savedvideo_PAST')

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Привет! Для арбитража и для инвайтинга/realise1", reply_markup=kb.main)

@router.message(F.text == 'В главное меню')
async def nice(message: Message):
    await message.answer('Вы вернулись к главноему меню',  reply_markup=kb.main)

waiting_for_link = False
@router.message(F.text == 'Уникализация видео')
async def cmd_unique(message: Message):
    global waiting_for_link
    waiting_for_link = True
    await message.answer("Пожалуйста, введите ссылку на видео для уникализации.")

@router.message(lambda message: waiting_for_link and 'http' in message.text)
async def handle_tiktok_link(message: Message):
    await message.answer("Видео находится в обработке подождите немного")
    global waiting_for_link
    url = message.text

    try:
        initial_dir = os.getcwd()

        # 1. Скачиваем видео через tiktok_save (сохраняется в savedvideo_DO)
        tiktok_save(url)

        # 2. Получаем последний скачанный файл из папки savedvideo_DO
        downloaded_files = sorted(os.listdir(SAVED_VIDEO_DO_DIR),
                                  key=lambda x: os.path.getctime(os.path.join(SAVED_VIDEO_DO_DIR, x)))

        video_path = os.path.join(SAVED_VIDEO_DO_DIR, downloaded_files[-1])

        # 3. Выполняем скрипт consert.sh для обработки видео
        script_path = os.path.join(SCRIPT_DIR, 'consert.sh')
        subprocess.run(['bash', script_path], check=True)

        processed_video_filename = f"{os.path.splitext(os.path.basename(video_path))[0]}_processed.mp4"
        processed_video_path = os.path.join(SAVED_VIDEO_PAST_DIR, processed_video_filename)

        #удаление видео в папке
        os.remove(video_path)

        #делаем абсолютный путь к сохраненному файлу
        os.chdir('savedvideo_PAST')
        current_video_save = os.path.join(os.getcwd(), processed_video_filename)

        # 5. Отправляем обработанное видео пользователю
        await message.answer("Вот твое обработанное видео:")

        video = FSInputFile(current_video_save)
        await message.answer_video(video)

        # удаление файла
        os.remove(current_video_save)

        waiting_for_link = False

    except Exception as e:
        # Обрабатываем ошибки
        await message.answer(f"Произошла ошибка: {e}")
        await message.answer("Напишите в поддержку")
        waiting_for_link = False
    finally:
        # Возвращаемся в начальную рабочую директорию, даже если произошла ошибка
        os.chdir(initial_dir)

api_id = '29003141'
api_hash = '1155dcd7e08bbffbb369684e5d6bd9ed'
client = TelegramClient('session_name', api_id, api_hash)

waiting_for_parser = False
@router.message(F.text == 'Парсер чатов')
async def chat_parser_start(message: Message):
    global waiting_for_parser
    waiting_for_parser = True

    await message.answer('Введите ссылку на открытый чат:')

@router.message(lambda message: waiting_for_parser and 't.me/' in message.text)
async def handle_chat_link(message: Message):
    chat_link = message.text
    await message.answer("Парсинг участников чата, пожалуйста, подождите...")

    async with client:
        await fetch_chat_members(chat_link, message)

async def fetch_chat_members(chat_link, message: Message):
    try:
        # Проверяем, что ссылка ведет на правильный чат (публичный)
        match = re.search(r't\.me\/([\w_]+)', chat_link)

        chat_username = match.group(1)

        await client.start()  # Начинаем сессию клиента

        # Получаем сущность чата
        chat = await client.get_entity(chat_username)

        # Получаем список участников
        participants = await client.get_participants(chat)

        k = 0
        usernames = []
        # Выводим только username в список
        for user in participants:
            if user.username:
                k += 1
                usernames.append(f"@{user.username}")  # Добавляем username в список

        await message.answer(f"Всего пользователей: {k}")
        await message.answer("\n".join(usernames))  # Отправляем список пользователей обратно в чат

        global waiting_for_parser
        waiting_for_parser = False

    except Exception as e:
        # Обрабатываем ошибки
        await message.answer(f"Произошла ошибка: {e}")
        await message.answer("Напишите в поддержку")
        waiting_for_parser = False


