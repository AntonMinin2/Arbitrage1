from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Парсер чатов'),
                                      KeyboardButton(text='Уникализация видео')]],
                           resize_keyboard=True,
                           input_field_placeholder='Выберите пункт меню...')



