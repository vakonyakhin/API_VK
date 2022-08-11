# Публикация комиксов
При каждом запуске программы происходит публикация поста в группе с фото и текстом полученными с xkcd.com. Выбор комикса осуществляется случайным образом из всех имеющихся в базе.

# Как установить
Python3 должен быть установлен. Для установки зависимостей используйте pip:
```
pip install -r requirements.txt
```

## Как запустить
Необходимо прописать переменные окружения:

GROUP_ID - идентификатор группы, в которой будет производиться публикация.

ACCESS_TOKEN - токен для создаваемого standalone приложения, полученный от API VK по процедуре Implicit Flow. Необходимые разрешения для токена - photos, groups.

Для запуска используйте команду:
```
python main.py
```

# Цель проекта
Код написан в образовательных целях.
