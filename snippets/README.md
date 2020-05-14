# Ki Snippets


## downloader.py
Das `downloader.py` snippet kann nur benutzt werden, wenn vorher mit [wfs-downloader](https://github.com/codeforberlin/wfs-downloader) und der im hier abgelegten `config.yaml` das dataset als xml Datei heruntergeladen wurde. Das `downloader.py` Snippet wandelt die xml Datei in json um und transformiert die Koordinaten von [EPSG:25833]() zu [EPSG:25833]().

Danach wird die Ausführung der im Hauptverzeichnis beigelegten `parser.py` zum Laden des Datensatzes in die Datenbank (postgresql erforderlich!).

Erwartete Größe:
  - `strassenbaeume.xml` ~289M (04.02.2020)
  - `output.json` ~227M (04.02.2020)

Testdateien:
  - [strassenbaeume.xml](https://anonfiles.com/X6ebP3V8n8/strassenbaeume_xml) (859eb78098bb9a09e0fd9f63ec19899c310c715afbbacc5f7ef72174596a07e9 sha256sum)

Da das umwandeln der Koordinaten die Genauigkeit sinkt tauchen manche Bäume nun an gleichen Stellen auf. Um dies zu umgehen gibt es die beigelegt `purify.py`, welche basierend auf den Koordinaten Dopplungen entfernt.
