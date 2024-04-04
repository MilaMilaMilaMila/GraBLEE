# GraBLEE


# Как настроить виртуальное окружение

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

Активируем виртуальное окружение  
```sh
pipenv shell
```

