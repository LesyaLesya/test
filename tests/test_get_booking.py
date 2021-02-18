""" Модуль с тестами get запросов - GetBooking """


from typing import Union
import pytest
import requests
import allure  # type: ignore
import conftest


@allure.feature("GET - GetBooking")
@allure.story("Получение существующей сущности по id")
@pytest.mark.positive
@pytest.mark.parametrize("param", [7, 5, 16])
def test_get_booking_by_id_positive(booker_api: conftest.ApiClient,
                                    param: int) -> None:
    """
    Тестовая функция для проверки вызова get запроса.
    Проверяются позитивные варианты для id через параметризацию.

    :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
    :param param: передаваемые в урле id сущностей

    """
    with allure.step(f"Отправляем get запрос с id {param}"):
        response: requests.models.Response = booker_api.get(path=f"/booking/{param}")

    with allure.step("Проверяем, что код ответа 200"):
        assert response.status_code == 200, f"Код ответа - {response.status_code}"

    with allure.step(f"Проверяем длину тела ответа сущности с id {param}"):
        assert len(response.json()) != 0, "Такой сущности не существует"


@allure.feature("GET - GetBooking")
@allure.story("Получение несуществующей сущности по id")
@pytest.mark.negative
@pytest.mark.parametrize("param", [10000, "hello", True, 0])
def test_get_booking_by_id_negative(booker_api: conftest.ApiClient,
                                    param: Union[int, str, bool]) -> None:
    """
    Тестовая функция для проверки вызова get запроса.
    Проверяются негативные варианты для id через параметризацию -
    несуществующий id, передача не числового типа данных.

    :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
    :param param: передаваемые в урле id сущностей

    """
    with allure.step(f"Отправляем get запрос с id {param}"):
        response: requests.models.Response = booker_api.get(path=f"/booking/{param}")

    with allure.step("Проверяем, что код ответа 404"):
        assert response.status_code == 404, f"Код ответа - {response.status_code}"

    with allure.step("Проверяем, что текст ответа - Not found"):
        assert response.text == "Not Found", f"Текст ответа  - '{response.text}'"
