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

# Configs
Значения host и port в config.ini у client и server должны быть одинаковыми.
Если вы хотите использовать Cytoscape на локальной машине, можно взять значения для host = 127.0.0.1, а port можно выбрать любой свободный.

Так же можно использовать значения из файла values.ini из секции REMOTE, чтобы использовать Cytoscape, развернутый на удаленном сервере.

# Запуск серверной части
Перед работой с серверной частью необходимо запустить приложение Cytoscape
Если вам доступен графический интерфес сервера, можно запустить приложение через ярлык.
На случай, если графической оболочки нет, нужно перейти в папку,  куда был установлен Cytoscape и запустить файл cytoscape.sh (для Linux)
Пример запуска на Linux:
```sh
cd /opt/Cytoscape_v3.10.1/

 ./cytoscape.sh
```
нужно запустить main.py из папки GraBLEE/server скачанного репозитория
Если репозиторий скачан в корневой каталог, запуск может выглядеть так:
```sh
cd ~/GraBLEE/server
python3 main.py
```
Если вы работаете локально, можно запустить программу так же из командной строки или прям из IDE

# Запуск клиентской части

Чтобы начать использовать функцию получения Cytoscape session нужно инициализировтаь клиент в вашей программе. Для этого напишите следующее:
```py
# path to client can be differ
from client.main import init_cytoscape_extension

# your code

# add cytoscape extension to networkx.Graph
init_cytoscape_extension()

# your code
```
В папке example есть файл example.py, в котором приведен пример использования функции получения сессии.
