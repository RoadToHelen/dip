Внести user_token, group_token,my_id в config.py

requirements.txt - версии библиотек, используемых в проекте
Документация:https://learn.microsoft.com/ru-ru/VisualStudio/python/managing-required-packages-with-requirements-txt?view=vs-2022

**Входные данные**

id пользователя в ВК, для которого мы ищем пару.

Информацию по пользователю получаем методом VK API users.get https://dev.vk.com/method/users.get
Информацию по подбираемым пользователям получаем методом VK API users.search https://dev.vk.com/method/users.search
Фотографии подбираем методом VK API photos.get https://dev.vk.com/method/photos.get

Все слышали про известное приложение для знакомств - Tinder. Приложение предоставляет простой интерфейс для выбора понравившегося человека. Сейчас в Google Play более 100 миллионов установок.

Используя данные из VK, нужно сделать сервис намного лучше, чем Tinder, а именно: чат-бота “VKinder”. Бот должен искать людей, подходящих под условия, на основании информации о пользователе из VK:

Возраст,
пол,
город,
семейное положение.
У тех людей, которые подошли по требованиям пользователю, получать топ-3 популярных фотографии профиля и отправлять их пользователю в чат вместе со ссылкой на найденного человека.
Популярность определяется по количеству лайков и комментариев.

Требования к сервису:

Код программы удовлетворяет PEP8.
Получать токен от пользователя с нужными правами.
Программа декомпозирована на функции/классы/модули/пакеты.
Результат программы записывать в БД.
Люди не должны повторяться при повторном поиске.
Не запрещается использовать внешние библиотеки для vk.
