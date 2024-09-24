# GraBLEE
## Программное обеспечение для автоматизации работы с  приложением Cytoscape
Узнать о значимости и актуальности проекта, архитектурных решениях и использованных технологиях можно в документе summary.pdf(https://github.com/MilaMilaMilaMila/GraBLEE/blob/main/summary.pdf) и в презентации grablee.pptx(https://github.com/MilaMilaMilaMila/GraBLEE/blob/main/grablee.pptx, https://docs.google.com/presentation/d/10iQkoLkNGChkdPLSD9VeaC_pcBWTWPEG/edit?usp=sharing&ouid=113384589332914961135&rtpof=true&sd=true)

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

# Способы решения некоторых проблем

- При работе с большими графами приложению Cytoscape может быть недостаточно оператичной памяти и памяти в стеке. Эти параметры можно настроить в файле Cytoscape.vmoptions, который находится в директории исполняемого файла Cytoscape. https://manual.cytoscape.org/en/latest/Launching_Cytoscape.html#overall-memory-size-for-cytoscape - здесь можно подробнее узнать, как настроить размер оперативной памяти, https://www.baeldung.com/jvm-configure-stack-sizes#custom - здесь можно найти информацию по изменению размера стека
