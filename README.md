# Викторина на Django
![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![Visual Studio Code](https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white)


## Введение
Это приожение позволяет создавать собственные тесты. В тестах вы создаёте свои вопросы, а к каждому вопросу варианты ответа. Приложение включает в себя такие страницы как «Главная», «Контакты», «Список викторин (как своих так и от других пользователей)», «Просмотр статистики», кастомные страницы 403, 404 и 500.

## Содержание

* [Введение](#введение)
* [Установка](#установка)
* [Базовая страница шаблона](#базовая-страница-шаблона)
* [Используемые технологии](#основные-технологии)
* [Основные страницы](#основные-страницы)
* [Скриншоты сайта](#скриншоты-сайта)

## Установка

1. Клонируйте репозиторий
```
git clone https://github.com/4eLoBeK-001/Quiz.git

cd Quiz
```

2. Создайте и активируйте виртуальное окружение
```python
python -m venv venv

.\venv\Scripts\activate
```

3. Установите зависимости
```
pip install -r requirements.txt
```

4. Перейдите глубже в в проект
```
cd quiz
```

5. Выполните миграции
```
python manage.py migrate
```

6. Создайте администратора (опционально)
```
python manage.py createsuperuser
```

7. Запусите сервер
```
python manage.py runserver
```

## Готово!

Для корректной работы почты не забудьте заменить переменные `EMAIL_HOST_USER` и `EMAIL_HOST_PASSWORD`

```python
# Настройки для отправки почты
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # smtp.gmail.com для Gmail
EMAIL_PORT = 465
EMAIL_USE_SSL=True
EMAIL_HOST_USER = 'your_emailf@gmail.com'  # Не забудьте изменить
EMAIL_HOST_PASSWORD = 'your_password'  # Не забудьте изменить
```


## Базовая страница шаблона

![Base_template](https://github.com/user-attachments/assets/beb378bc-ab0d-4260-bd12-feef913c055a)


## Основные технологии

1. HTML
2. CSS
3. JavaScript
4. Python

## Основные библиотеки

1. Django==4.2.16
2. psycopg2==2.9.10


## Основные страницы

* `home` - Главная страница
* `contacts` - Основная информация для обратной связи, также возможность через форму отправить сообщение владельцу сайта
* `create_quiz` - Позволяет создать собственную викторину
* `view_quizzes` - Список собственных викторин
* `list_quizzes` - Список викторин от других пользователей (викторины можно проходить будучи неавторизованным)
* `global_statistics` - Статистика викторины: сколько раз прошли, за какое время и прочая информация


## Скриншоты сайта
**Контакты**
![contacts](https://github.com/user-attachments/assets/c5bf6720-86d9-4ba9-bba9-693eb53241f6)

**Список квизов**
![Quiz_list](https://github.com/user-attachments/assets/1c7df244-7f4f-43e2-8a23-353f93969449)

**Подробная статистика**
![statistics](https://github.com/user-attachments/assets/5d7fba66-1d25-4960-b0a9-f7639eb036f3)

**Профиль**
![profile](https://github.com/user-attachments/assets/89af4c01-178b-439d-bef2-9d1da845f318)
