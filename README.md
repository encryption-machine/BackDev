<div align='center'>
  <br>

  <h1>Шифровальная машина</h1>

  <a href='http://shifmachine.acceleratorpracticum.ru'>http://shifmachine.acceleratorpracticum.ru</a>

  <a href="http://shifmachine.acceleratorpracticum.ru">
    <img src="https://img.shields.io/badge/-frontend-0D1117?style=for-the-badge" alt="http://shifmachine.acceleratorpracticum.ru"><img src='https://img.shields.io/website?down_color=red&down_message=offline&label=&style=for-the-badge&up_color=%23238636&up_message=online&url=http%3A%2F%2Fshifmachine.acceleratorpracticum.ru'/>
  </a>
    <a href="http://shifmachine.acceleratorpracticum.ru">
    <img src="https://img.shields.io/badge/-backend-0D1117?style=for-the-badge" alt="http://shifmachine.acceleratorpracticum.ru"><img src='https://img.shields.io/website?down_color=red&down_message=down&label=&style=for-the-badge&up_color=%23238636&up_message=up&url=http%3A%2F%2Fshifmachine.acceleratorpracticum.ru/api/v1'/>
  </a>
</div>

**Текущий репозиторий является backend частью проекта "[Шифровальная машина](https://github.com/encryption-machine)"**

### Шифровальная машина - это онлайн сервис шифрования текстовых сообщений. Разработан выпускниками [Яндекс.Практикума](https://practicum.yandex.ru), силами команд:
- Backend разработчиков
- Frontend разработчиков ([frontend часть проекта](https://github.com/encryption-machine/Front))
- UX/UI дизайнеров ([макет дизайна](https://www.figma.com/file/sXoX6dcw6Z1RoAZCmAe6BA/%D0%A8%D0%B8%D1%84%D1%80%D0%BE%D0%B2%D0%B0%D0%BB%D1%8C%D0%BD%D0%B0%D1%8F-%D0%BC%D0%B0%D1%88%D0%B8%D0%BD%D0%B0-(%D0%94%D0%B8%D0%B7%D0%B0%D0%B9%D0%BD)?type=design&node-id=7-5365&mode=design&t=7Oe5wcxCmfiithct-0))
- Project менеджеров
- QA инженеров

## Стэк:
- Python
- Django
- DRF
- Postgres
- Docker

## Фич-лист:
- Шифрование/дешифрование алгоритмами:
  - AES
  - Виженер
  - Цезарь
  - Морзе
  - QR (Только шифрование)
- Регистрация/вход пользователя
- Сброс пароля
- Личный кабинет с историей шифрования/дешифрования

## Контрибьюторы

<a href="https://github.com/encryption-machine/Back/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=encryption-machine/Back" />
</a>




# Для разработчиков:
## **pre-commit хуки
**
[Документация](https://pre-commit.com)
- Перед использованимем необходимо установить pre-commit глобально (не в виртуальном окружении):
    ```
    pip install pre-commit
    ```
- Необходимо установить pre-commit хуки в виртуальное окружение:
    ```
    pre-commit install
    ```
- При каждом коммите выполняются хуки перечисленные в **.pre-commit-config.yaml**.
Если при коммите возникает ошибка, можно запустить хуки вручную:
    ```
    pre-commit run --all-files
    ```

- Коммит без запуска хуков:
    ```
    git commit --no-verify -m 'your text'
    ```


## **Инструкция по развертыванию бэкенда в контейнере докер для тестирования фронтом:**

- Клонировать себе репозиторий Back, перейти в ветку develop

- Перейти в папку encryption_machine

```cd encryption_machine```

- Запустить docker-compose:

```docker-compose -f docker-compose.develop.yaml up```

- При необходимости выполнить миграции внутри контейнера докер
```
python manage.py makemigrations
python manage.py migrate
```

- Документация redoc и swagger будет доступна по следующим адресам:
```
http://127.0.0.1:8000/redoc/
http://127.0.0.1:8000/swagger/
```
