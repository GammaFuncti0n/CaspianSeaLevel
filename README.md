# Caspian Sea Level project

## Quick starts

For docker build run:
```bash
docker build -t caspian-sea-level .
```

For run container run:
```bash
docker run -it -d --name "caspian-sea-level-container" -p 8888:8888 -v $(pwd):/workspace caspian-sea-level
```

Now open window from container in browser or in vscode

First launch for download data and process it:
```bash
python main.py
```