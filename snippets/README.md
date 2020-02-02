# Ki Snippets


## downloader.py
Das `downloader.py` snippet kann nur benutzt werden, wenn vorher mit [wfs-downloader](https://github.com/codeforberlin/wfs-downloader) und der im hier abgelegten `config.yaml` das dataset als xml Datei heruntergeladen wurde. Das `downloader.py` Snippet wandelt die xml Datei in json um und transformiert die Koordinaten von [EPSG:25833]() zu [EPSG:25833]().

Danach wird die Ausführung der im Hauptverzeichnis beigelegten `parser.py` zum Laden des Datensatzes in die Datenbank (default `app.db`(sqlite) oder in enviroment spezifiziert).
