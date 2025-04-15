## Установка
```bash
git clone https://github.com/Mililitr/customer_complaints_test.git
cd customer_complaints_test
```

## Установка зависимостей
```bash
pip install -r requirements.txt
```

## Настройка переменных окружения
Создайте файл .env в корневой директории проекта со следующим содержимым:
```bash
API_KEY=ваш_api_ключ_для_sentiment_analysis_by_apilayer
```

## Запуск приложения
```bash
uvicorn app.main:app --reload
```
