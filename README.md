# Caspian Sea Level project

## Abstract

Project for visualize Caspian level sea from different posts. Code download fresh raw data from site, prepare them and save in sqlite database. 

Глобальной целью проекта является предсказание уровня Каспийского моря в ближайшие несколько месяцев (2). Проект скачивает свежие данные с сайта, подготавливает их, сохраняет в базу данных. Далее данные предобрабатываются (очищаются аутлаеры, заполняются пропуски, данные нормализуются), и отправляются в модель на предсказание следующих значений. Когда уже есть обученная модель, новые данные пропускаются сперва через нее, если качество падает ниже определенного порога, модель обучается заново.

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