import requests

def test_spam_detection() -> None:
    """
    Клиент для отправки запросов к сервису
    """

    base_url = "http://localhost:8000/predict"

    test_cases = [
        "ВЫ ВЫИГРАЛИ 213070247 долларов!!! Перейдите по ссылке для получения приза!!!",
        "Привет, как дела? Что нового за сегодня?",
        "Ваша карта заблокирована! Срочно подтвердите данные здесь: http://obmana.net/scam"
    ]

    for i, sms_text in enumerate(test_cases, 1):
        print(f"Входящее СМС: {sms_text}")
        try:
            response = requests.post(base_url, json={"sms_text": sms_text})
            response.raise_for_status()
            result = response.json()
            print(f"Результат: is_spam={result['is_spam']}, reason={result['reason']}")
        except requests.exceptions.RequestException as e:
            print(f"Ошибка запроса: {e}")

if __name__ == "__main__":
    test_spam_detection()