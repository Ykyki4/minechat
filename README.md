# minechat
 
Утилита для взаимодействия с minechat.
 
## Установка и настройка
Для начала, скачайте репозиторий в .zip или клонируйте его, изолируйте проект с помощью venv и установите зависимости командой:

```
pip install -r requirements.txt
```


В репозитории есть два скрипта

* ```reader.py``` - Бесконечно читает сообщения из полученого хоста и порта, отправляя их в терминал и записывая в файл.

* ```sender.py``` - Позволяет вам зарегистрироваться или авторизироваться в чате и отправить сообщение.

**Для корректного использования скриптов вам необходимо пользоваться cli-коммандами, или устанавливать переменные окружения в файле .env, в формате ПЕРЕМЕННАЯ=значение.**

Запуск скрипта:

```
python script.py
```

Чтобы просмотреть доступные настройки:

```
python script.py -h
```

**Все переменные окружения имеют идентичное название с полным названием аргумента.**
