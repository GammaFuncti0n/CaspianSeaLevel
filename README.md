# Caspian Sea Level project

## Quick starts

For docker build run:
```bash
bash docker_build.sh
```

For run container run:
```bash
bash docker_run.sh
```

Now open window from container in browser or in vscode

First launch for download data and process it:
```bash
python main.py
```

## Ключевые шаги

1. Запрос на сайт, для скачивания данных. Подготовка данных, сохранение в базу данных.

2. Чтобы загрузить данные, запустить main.py

Затем создание графиков в sea_level.ipynb

Конвертация в CMYK через cmyk_converter.sh 

Проверка файла: gs -o - -sDEVICE=inkcov figure.pdf