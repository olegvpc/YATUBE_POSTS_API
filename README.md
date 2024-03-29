# YATUBE_POSTS_API
Социальная сеть - одна из многих, но единственная написанная мною :-)

## Возможности:

* Создавать посты 
* Комментировать посты
* Делать подписки на автора поста
* Авторизация по токену 'rest_framework.authentication.TokenAuthentication'

### Как запустить проект:
работа с github доступна только по Токен или по ssh ключу
https://htmlacademy.ru/blog/boost/frontend/git-console

```
git clone git@github.com:olegvpc/hw05_final.git
```
Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```
```
source venv/bin/activate
```

```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
pip install https://github.com/creimers/graphene-graphiql-explorer/archive/master.zip
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```
## ДЕТАЛИ ПРОЕКТА
###Проект размещен на яндекс web-hosting:
https://olegvpc.ru

#### Вход на виртульную машину

ssh olegvpc123@51.250.93.138

Проект работает не в контейнере

#### Копирование файлов на сервер
scp movie-project.png ssh olegvpc123@51.250.93.138:

###поднят wsgi-сервер: gunicorn - сервер внутренней обработки
```shell
sudo pip install gunicorn
```
gunicorn --bind 0.0.0.0:8000 yatube.wsgi
###Демон systemd - начальный запуск / перезапуск
```
sudo nano /etc/systemd/system/gunicorn.service 
```
```
sudo systemctl

sudo systemctl daemon-reload
sudo systemctl stop gunicorn
sudo systemctl start gunicorn
sudo systemctl restart gunicorn
sudo systemctl status gunicorn
```
###Поднят серер nginx

sudo apt install nginx -y
и файрвол
sudo ufw allow 'Nginx Full'
sudo ufw allow OpenSSH 

sudo systemctl start nginx

sudo systemctl start nginx 

sudo nano /etc/nginx/sites-enabled/default

sudo nginx -t

sudo nginx -s reload

###  REST API:

Документирование и структура API описана на drf-yasg (Swagger generator)
и доступна на end-point
http://olegvpc.ru/api/v1/swagger/

###  Пример работы с API:
#### Авторризация
Требуется авторизация по Токен (доступно только для зарегистрированных пользователей сайта)
http://olegvpc.ru/api/v1/api-token-auth/

```json
{
  "username": "string",
  "password": "string"
}
```
Получение Token
```json
{
  "token": "9fcdce20c2dbbafardse38b8c68b50a6dbeb39c6"
}
```

#### Запрос для чтения всех постов

http://olegvpc.ru/api/v1/posts/
Ответ от API
```json
  [
  {
    "id": 125,
    "author": "pitt",
    "text": "Уи́льям Брэ́дли Питт (англ. William Bradley Pitt; род. 18 декабря 1963, Шони, Оклахома, США) — американский актёр и кинопродюсер. Лауреат двух премий «Золотой глобус». Обладатель премии «Оскар» как один из продюсеров фильма «12 лет рабства» — победителя в категории «Лучший фильм» на церемонии 2014 года — и за лучшую мужскую роль второго плана в картине «Однажды в Голливуде» (2020)[1]. До этого пять раз номинировался на премию «Оскар» (трижды — как актёр и два раза — как продюсер).",
    "pub_date": "2021-07-17T18:57:05.085102Z",
    "image": "http://olegvpc1.pythonanywhere.com/media/posts/pitt-2.jpg",
    "group": 1
  }
  ]
```
Пример кода на Python для выполнения записи поста через API
```python
import requests

url = 'http://olegvpc.ru/api/v1/posts/'
data = {
  'text': 'Тут Ваш текст'
}
TOKEN = 'тут Ваш Token авторизации'
headers = {
    'Authorization': f'Token {TOKEN}'
}
requests.post(url=url, headers=headers, data=data)
```

### Тестирование кода приложения posts и admin с детализацией
```
python3 manage.py test -v 2
```
или одного выбранного теста
```
python3 manage.py test -v 2 posts.tests.test_views.PostsViewsTests.test_post_page_shows_correct_context
```