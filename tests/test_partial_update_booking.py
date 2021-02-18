""" Модуль с тестами patch запросов - PartialUpdateBooking """


from typing import Union, Dict, Any
import json
import pytest
import requests
import allure   # type: ignore
import conftest


@allure.feature("PATCH - PartialUpdateBooking")
@allure.story("Обновление части параметров сущности")
@pytest.mark.positive
@pytest.mark.parametrize("first, last", [("Peter", "Jackson"), ("Emma", "Star")])
def test_patch_booking_update_part_fields(booker_api: conftest.ApiClient,
                                          first: str, last: str) -> None:
    """
    Тестовая функция для проверки вызова patch запроса с передаваемым телом.
    Проверяются позитивные варианты через параметризацию -
    обновление значений "firstname", "lastname".
    Обращение напрямую к определенному id в урле.

    :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
    :param first: передаваемый в теле запроса firstname
    :param last: передаваемый в теле запроса lastname

    """
    get_data: requests.models.Response = booker_api.get(path="/booking/7")
    data: Dict[str, str] = {"firstname": first, "lastname": last}

    with allure.step(f"Отправляем patch запрос с data - {data}"):
        response: requests.models.Response =\
            booker_api.patch(path="/booking/7", data=json.dumps(data))

    with allure.step("Проверяем, что код ответа 200"):
        assert response.status_code == 200, f"Код ответа - {response.status_code}"

    with allure.step(f"Проверяем, что firstname - '{first}'"):
        assert response.json()["firstname"] == first, \
            f"Фамилия - '{response.json()['firstname']}'"

    with allure.step(f"Проверяем, что lastname - '{last}'"):
        assert response.json()["lastname"] == last, \
            f"Фамилия - '{response.json()['lastname']}'"

    with allure.step(f"Проверяем, что totalprice - '{get_data.json()['totalprice']}'"):
        assert response.json()["totalprice"] == \
            get_data.json()["totalprice"], \
            f"Итоговая цена - '{response.json()['totalprice']}'"

    with allure.step(f"Проверяем, что depositpaid - '{get_data.json()['depositpaid']}'"):
        assert response.json()["depositpaid"] == \
            get_data.json()["depositpaid"], \
            f"Депозит - '{response.json()['depositpaid']}'"

    with allure.step(f"Проверяем, что checkin - '{get_data.json()['bookingdates']['checkin']}'"):
        assert response.json()["bookingdates"]["checkin"] == \
            get_data.json()["bookingdates"]["checkin"], \
            f"Дата заезда - '{response.json()['bookingdates']['checkin']}'"

    with allure.step(f"Проверяем, что checkout - '{get_data.json()['bookingdates']['checkout']}'"):
        assert response.json()["bookingdates"]["checkout"] == \
            get_data.json()["bookingdates"]["checkout"], \
            f"Дата выезда - '{response.json()['bookingdates']['checkout']}'"


@allure.feature("PATCH - PartialUpdateBooking")
@allure.story("Обновление всех параметров сущности")
@pytest.mark.positive
def test_patch_booking_update_all_fields(booker_api: conftest.ApiClient) -> None:
    """
    Тестовая функция для проверки вызова patch запроса с передаваемым телом.
    Проверяется обновление всех полей сущности.
    Обращение напрямую к определенному id в урле.

    :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient

    """
    data: Dict[str, Any] = {
        "firstname": "Leena",
        "lastname": "White",
        "totalprice": 1000,
        "depositpaid": False,
        "bookingdates": {
            "checkin": "2021-01-01",
            "checkout": "2023-12-01"
        },
        "additionalneeds": "Nothing"}

    with allure.step(f"Отправляем patch запрос с data - {data}"):
        response: requests.models.Response = \
            booker_api.patch(path="/booking/20", data=json.dumps(data))

    with allure.step("Проверяем, что код ответа 200"):
        assert response.status_code == 200, f"Код ответа - {response.status_code}"

    with allure.step(f"Проверяем, что firstname - '{data['firstname']}'"):
        assert response.json()["firstname"] == "Leena", \
            f"Имя - '{response.json()['firstname']}'"

    with allure.step(f"Проверяем, что lastname - '{data['lastname']}'"):
        assert response.json()["lastname"] == "White", \
            f"Фамилия - '{response.json()['lastname']}'"

    with allure.step(f"Проверяем, что totalprice - '{data['totalprice']}'"):
        assert response.json()["totalprice"] == 1000, \
            f"Итоговая цена - '{response.json()['totalprice']}'"

    with allure.step(f"Проверяем, что depositpaid - '{data['depositpaid']}'"):
        assert response.json()["depositpaid"] is False, \
            f"Депозит - '{response.json()['depositpaid']}'"

    with allure.step(f"Проверяем, что checkin - '{data['bookingdates']['checkin']}'"):
        assert response.json()["bookingdates"]["checkin"] == "2021-01-01", \
            f"Дата заезда - '{response.json()['bookingdates']['checkin']}'"

    with allure.step(f"Проверяем, что checkout - '{data['bookingdates']['checkout']}'"):
        assert response.json()["bookingdates"]["checkout"] == "2023-12-01", \
            f"Дата выезда - '{response.json()['bookingdates']['checkout']}'"

    with allure.step(f"Проверяем, что additionalneeds - '{data['additionalneeds']}'"):
        assert response.json()["additionalneeds"] == "Nothing", \
            f"Пожелания - '{response.json()['additionalneeds']}'"


@allure.feature("PATCH - PartialUpdateBooking")
@allure.story("Обновление сущности передачей пустого тела")
@pytest.mark.positive
def test_patch_booking_empty_body(booker_api: conftest.ApiClient) -> None:
    """
    Тестовая функция для проверки вызова patch запроса с передаваемым телом.
    Проверяется передача пустого тела.
    Обращение напрямую к определенному id в урле.

    :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient

    """
    get_data: requests.models.Response = booker_api.get(path="/booking/5")

    with allure.step("Отправляем patch запрос с пустым телом"):
        response: requests.models.Response = booker_api.patch(path="/booking/5", data={})

    with allure.step("Проверяем, что код ответа 200"):
        assert response.status_code == 200, f"Код ответа - {response.status_code}"

    with allure.step(f"Проверяем, что firstname - '{get_data.json()['firstname']}'"):
        assert response.json()["firstname"] == get_data.json()["firstname"], \
            f"Имя - '{response.json()['firstname']}'"

    with allure.step(f"Проверяем, что lastname - '{get_data.json()['lastname']}'"):
        assert response.json()["lastname"] == get_data.json()["lastname"], \
            f"Фамилия - '{response.json()['lastname']}'"

    with allure.step(f"Проверяем, что totalprice - '{get_data.json()['totalprice']}'"):
        assert response.json()["totalprice"] == \
            get_data.json()["totalprice"], \
            f"Итоговая цена - '{response.json()['totalprice']}'"

    with allure.step(f"Проверяем, что depositpaid - '{get_data.json()['depositpaid']}'"):
        assert response.json()["depositpaid"] == \
            get_data.json()["depositpaid"], \
            f"Депозит - '{response.json()['depositpaid']}'"

    with allure.step(f"Проверяем, что checkin - '{get_data.json()['bookingdates']['checkin']}'"):
        assert response.json()["bookingdates"]["checkin"] == \
            get_data.json()["bookingdates"]["checkin"], \
            f"Дата заезда - '{response.json()['bookingdates']['checkin']}'"

    with allure.step(f"Проверяем, что checkout - '{get_data.json()['bookingdates']['checkout']}'"):
        assert response.json()["bookingdates"]["checkout"] == \
            get_data.json()["bookingdates"]["checkout"], \
            f"Дата выезда - '{response.json()['bookingdates']['checkout']}'"


@allure.feature("PATCH - PartialUpdateBooking")
@allure.story("Обновление параметров несуществующей сущности")
@pytest.mark.negative
@pytest.mark.parametrize("param", [213123, "tests"])
def test_patch_booking_invalid_id(booker_api: conftest.ApiClient,
                                  param: Union[str, int]) -> None:
    """
    Тестовая функция для проверки вызова patch запроса с передаваемым телом.
    Проверяются негативные варианты через параметризацию -
    обращение к несуществующему id в урле.

    :param booker_api: фикстура, создающая и возвращающая экземпляр класса ApiClient
    :param param: передеваемый в урле id

    """
    data: Dict[str, str] = {"firstname": "Test", "lastname": "Test"}

    with allure.step(f"Отправляем patch запрос с id {param}"):
        response: requests.models.Response =\
            booker_api.patch(path=f"/booking/{param}", data=json.dumps(data))

    with allure.step("Проверяем, что код ответа 405"):
        assert response.status_code == 405, f"Код ответа - {response.status_code}"
