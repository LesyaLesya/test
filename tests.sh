#!/bin/bash

# Собираем image с тегом tests
docker build -t tests .


# Запускаем контейнер под именем my_container из image tests
docker run --name my_container tests --login=admin --passw=password123 -n 2

# Копируем из контейнера созданный allure-report
docker cp my_container:/app/allure-report .

# Запускаем хост для отчёта аллюр (утилита лежит локально)
# Хост отчёта нужно будет остановить руками
/Users/lesya/Desktop/selenoid/allure/bin/allure serve allure-report

# Удаляем из системы созданный контейнер
docker system prune -f
docker image rm tests
