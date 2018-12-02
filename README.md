# wargaming

Поправлен allure-плагин для nose, потому что он неправильно отображал тесты из генераторов. 

Установка:
$ pip install -r requirements.txt

$ cd allure-nose

$ pip install .


Запуск генерации:

$ python initialize_db.py

Запуск теста:
$ nosetests tests/test.py --with-allure --logdir=./results

Посмотреть отчет:
$ allure serve  ./results/
