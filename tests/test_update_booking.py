""" Модуль с тестами put запросов - UpdateBooking """


from typing import Union, Dict, Any
import json
import pytest
import requests
import allure   # type: ignore
import conftest


@allure.feature("PUT - UpdateBooking")
@allure.story("Обновление всех параметров сущности")
@pytest.mark.all_tests
@pytest.mark.positive
def test_put_booking_update_all_fields(booker_api: conftest.ApiClient) -> None:
    """
    Тестовая функция для проверки вызова put запроса с передаваемым телом.
    Проверяется обновление всех значений.
    Обращение напрямую к определенному id в урле.

    :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient

    """
    data: Dict[str, Any] = {
        "firstname": "Spencer",
        "lastname": "Watson",
        "totalprice": 1,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2000-12-31",
            "checkout": "2020-06-01"
        },
        "additionalneeds": "Dinner"}

    with allure.step(f"Отправляем put запрос с телом - {data}"):
        response: requests.models.Response =\
            booker_api.put(path="/booking/7", data=json.dumps(data))

    with allure.step("Проверяем, что код ответа 200"):
        assert response.status_code == 200, f"Код ответа - {response.status_code}"

    with allure.step(f"Проверяем, что firstname - '{data['firstname']}'"):
        assert response.json()["firstname"] == "Spencer", \
            f"Имя - '{response.json()['firstname']}'"

    with allure.step(f"Проверяем, что lastname - '{data['lastname']}'"):
        assert response.json()["lastname"] == "Watson", \
            f"Фамилия - '{response.json()['lastname']}'"

    with allure.step(f"Проверяем, что totalprice - '{data['totalprice']}'"):
        assert response.json()["totalprice"] == 1, \
            f"Итоговая цена - '{response.json()['totalprice']}'"

    with allure.step(f"Проверяем, что depositpaid - '{data['depositpaid']}'"):
        assert response.json()["depositpaid"] is True, \
            f"Депозит - '{response.json()['depositpaid']}'"

    with allure.step(f"Проверяем, что checkin - '{data['bookingdates']['checkin']}'"):
        assert response.json()["bookingdates"]["checkin"] == "2000-12-31", \
            f"Дата заезда - '{response.json()['bookingdates']['checkin']}'"

    with allure.step(f"Проверяем, что checkout - '{data['bookingdates']['checkout']}'"):
        assert response.json()["bookingdates"]["checkout"] == "2020-06-01", \
            f"Дата выезда - '{response.json()['bookingdates']['checkout']}'"

    with allure.step(f"Проверяем, что additionalneeds - '{data['additionalneeds']}'"):
        assert response.json()["additionalneeds"] == "Dinner", \
            f"Депозит - '{response.json()['additionalneeds']}'"


@allure.feature("PUT - UpdateBooking")
@allure.story("Обновление части параметров сущности")
@pytest.mark.all_tests
@pytest.mark.negative
@pytest.mark.parametrize("data", [{"firstname": "John", "lastname": "Smith"}, {}])
def test_put_booking_update_not_all_fields(booker_api: conftest.ApiClient,
                                           data: Dict[str, str]) -> None:
    """
    Тестовая функция для проверки вызова put запроса с передаваемым телом.
    Негативная проверка передачи в теле части значений / пустого тела.
    Обращение напрямую к определенному id в урле.

    :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
    :param data: передаваемое тело запроса

    """
    with allure.step(f"Отправляем put запрос с телом - {data}"):
        response: requests.models.Response =\
            booker_api.put(path="/booking/5", data=json.dumps(data))

    with allure.step("Проверяем, что код ответа 400"):
        assert response.status_code == 400, f"Код ответа - {response.status_code}"


@allure.feature("PUT - UpdateBooking")
@allure.story("Обновление параметров несуществующей сущности")
@pytest.mark.all_tests
@pytest.mark.negative
@pytest.mark.parametrize("param", [321342, "&*&^(&"])
def test_put_booking_invalid_id(booker_api: conftest.ApiClient,
                                param: Union[str, int]) -> None:
    """
    Тестовая функция для проверки вызова put запроса с передаваемым телом.
    Негативная проверка обращение к несуществующему урлу.

    :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
    :param param: передаваемый в урле id

    """
    data: Dict[str, Any] = {
        "firstname": "Spencer",
        "lastname": "Watson",
        "totalprice": 1,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2000-12-31",
            "checkout": "2020-06-01"
        },
        "additionalneeds": "Dinner"}

    with allure.step(f"Отправляем put запрос с id {param}"):
        response: requests.models.Response =\
            booker_api.put(path=f"/booking/{param}", data=json.dumps(data))

    with allure.step("Проверяем, что код ответа 405"):
        assert response.status_code == 405, f"Код ответа - {response.status_code}"
