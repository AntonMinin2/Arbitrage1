from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

# Настройка параметров Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")  # Без графического интерфейса
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--remote-debugging-port=9222")  # Порт для отладки
chrome_options.add_argument("user-data-dir=/home/youruser/tiktok-profile")  # Путь к новому профилю
chrome_options.add_argument("profile-directory=Default")  # Профиль по умолчанию

# Создание драйвера Selenium
driver = webdriver.Chrome(options=chrome_options)

# Переход на сайт TikTok
driver.get("https://www.tiktok.com")
time.sleep(5)  # Ждём, пока загрузятся cookies

# Извлекаем cookies
cookies = driver.get_cookies()

# Выводим cookies для отладки
for cookie in cookies:
    print(f"{cookie['name']} = {cookie['value']}")

# Закрытие браузера
driver.quit()
