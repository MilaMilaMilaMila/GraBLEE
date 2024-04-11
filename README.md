# GraBLEE


# Как скачать необходимые зависимости

Установим pipenv (для Ubuntu)  
```sh
pip3 install pipenv
```

Создаем Pipfile.lock из Pipfile (файл с зависимостями)  
```sh
pipenv lock
```

Установим зависимости из файла Pipfile.lock  
```sh
pipenv install
```

# Запуск серверной части

```sh
cd ~/GraBLEE/server
python3 main.py
```

# Запуск клиентской части
