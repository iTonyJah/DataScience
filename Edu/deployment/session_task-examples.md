# 1. Рекомендуемая архитектура проекта
```text
credit-card-ml-deployment/
├── app/
│   ├── __init__.py
│   ├── api.py                  # Flask-приложение
│   └── model_handler.py        # Загрузка и использование модели
├── models/
│   ├── train_model.py          # Скрипт обучения модели
│   └── model_v1.pkl            # Сохраненная модель
├── tests/
│   └── test_api.py             # Тесты API
├── docker/
│   └── Dockerfile              # Конфигурация Docker
├── requirements.txt            # Зависимости Python
├── docker-compose.yml          # Опционально: для оркестрации
├── ab_test_plan.md             # Документация по A/B-тесту
└── README.md                   # Основная документация
```
# 2. Пример Flask-приложения (app/api.py)
```python
from flask import Flask, request, jsonify
import pickle
import numpy as np

app = Flask(__name__)

# Загрузка модели при старте
with open('models/model_v1.pkl', 'rb') as f:
    model = pickle.load(f)

@app.route('/predict', methods=['POST'])
def predict():
    """Эндпоинт для предсказания дефолта"""
    try:
        data = request.get_json()
        features = preprocess_input(data)
        prediction = model.predict(features)
        probability = model.predict_proba(features)[0][1]
        
        return jsonify({
            'prediction': int(prediction[0]),
            'probability': float(probability),
            'model_version': 'v1'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/health', methods=['GET'])
def health():
    """Проверка здоровья сервиса"""
    return jsonify({'status': 'healthy'}), 200

def preprocess_input(data):
    """Предобработка входных данных"""
    # Преобразование JSON в numpy array
    features = np.array([data[key] for key in sorted(data.keys())]).reshape(1, -1)
    return features

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
```
# 3. Пример Dockerfile
```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Копирование зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование кода и модели
COPY app/ ./app/
COPY models/ ./models/

# Открытие порта
EXPOSE 5000

# Запуск приложения
CMD ["python", "app/api.py"]
```