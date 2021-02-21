#!/bin/bash

# Собираем image с тегом tests
docker build -t tests .


# Запускаем контейнер под именем my_container из image tests
docker run --name my_container tests --login=admin --passw=password123 -n 2 -m all_tests

# Копируем из контейнера созданный allure-report
docker cp my_container:/app/allure-results .

# Запускаем хост для отчёта аллюр (утилита лежит локально)
# Хост отчёта нужно будет остановить руками
/Applications/allure/bin/allure serve allure-results

# Удаляем из системы созданный контейнер
docker system prune -f
docker image rm tests
