````markdown
# NSFW Moderation Service

Простой FastAPI‑сервис, который принимает изображение и проверяет его через Hugging Face модель `Falconsai/nsfw_image_detection`.

## Установка

```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
````

## Получение API‑ключа Hugging Face

1. Перейдите на [https://huggingface.co](https://huggingface.co) и зарегистрируйтесь (если ещё не зарегистрированы).
2. Войдите в личный кабинет и откройте [страницу Access Tokens](https://huggingface.co/settings/tokens).
3. Создайте новый токен с правами **Read** (чтение).
4. Скопируйте токен.
5. В терминале экспортируйте его в переменную окружения:

   ```bash
   export HF_API_TOKEN="your-huggingface-token"
   ```

## Запуск

```bash
uvicorn main:app --reload
```

Сервер будет доступен по адресу `http://127.0.0.1:8000`.

## Пример запроса

```bash
curl -X POST -F "file=@path/to/your_image.jpg" http://127.0.0.1:8000/moderate
```

> Вместо `path/to/your_image.jpg` укажите относительный или абсолютный путь к вашему файлу.

## Возможные ответы

```json
// если nsfw_score ≤ 0.7
{"status":"OK","score":0.123}

// если nsfw_score > 0.7
{"status":"REJECTED","reason":"NSFW content","score":0.89}
```

## Важно

* Убедитесь, что токен в переменной `HF_API_TOKEN` указан корректно и имеет доступ к Inference API.
* Модель `Falconsai/nsfw_image_detection` обрабатывает изображения и возвращает вероятности NSFW контента.
* Для корректной работы API отправляйте файлы с типами: `.jpg`, `.jpeg`, `.png`.
