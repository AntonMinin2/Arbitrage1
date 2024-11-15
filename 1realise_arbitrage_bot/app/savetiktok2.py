import pyktok as pyk
import os

def tiktok_save(url):
    try:
        print(os.getcwd())
        # Определяем директорию для сохранения видео
        save_dir = "./app/savedvideo_DO"

        # Переходим в папку для сохранения
        os.chdir(save_dir)

        pyk.specify_browser('chrome')

        # Скачиваем видео (в текущую директорию, т.е. в savedvideo)
        pyk.save_tiktok(url, True)

        # Текущая директория (например, savedvideo_DO)
        current_dir = os.getcwd()

        # Поднимаемся на один уровень вверх (в папку app)
        parent_dir = os.path.dirname(current_dir)
        os.chdir(parent_dir)
    except Exception as e:
        # Ловим все ошибки внутри и бросаем их дальше
        raise RuntimeError(f"Ошибка при скачивании видео: {e}")
