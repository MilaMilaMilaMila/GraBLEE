# GraBLEE


# Как настроить виртуальное окружение

Установим pipenv (для Ubuntu)  
`
pip3 install pipenv
`

Создаем Pipfile.lock из Pipfile (файл с зависимостями)  
`
pipenv lock
`

Установим зависимости из файла Pipfile.lock  
`
pipenv install
`

Активируем виртуальное окружение  
`
pipenv shell
`

