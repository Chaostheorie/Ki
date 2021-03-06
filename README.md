# Ki

Ki ist als Projekt aufbauend auf einem beim [Utopia 2020 Hackathon](https://www.naturfreundejugend.de/termine/-/-/show/4517/coding_utopia_der_umwelt_hackathon/) entstehenden Protoypen zum [roofseed Projekt](https://github.com/MauriceHeinze/roofseed) entstanden und wird zurzeit von [Cobalt](https://sinclair.gq) unabhängig entwickelt. Jeder Inhalt verbunden mit Ki, welcher nicht von Cobalt erstellt wurde, wie Bilder, ist Eigentum seiner respektiven Eigentümer. Der Code ist unter der [LGPL v3.0 Lizenz](https://github.com/Chaostheorie/Ki/blob/master/LICENSE) verfügbar. Einen großen dank an Burkhard für seine Hilfe mit der Karte.

## Developer notes

Die Daten werden aus der [Open Code street tree API](https://github.com/codeforberlin/trees-api) bezogen und mit `app.models.Trees.parse` als Objekte in die Datenbank geladen und dann später wieder herausgezogen. Das eingrenzen des Bereiches basiert auf dem Kernpunkt der Postleitzahlen (in Berlin). Spätere Implementierung wird den Standort eines Handys durch den Browser unterstützen.

Es läuft ein heroku environment unter [dev-ki.heroku.com](https://dev-ki.heroku.com), welches nach jedem commit neu geladen wird.

### Toolkit

Das Toolkit (`toolkit.py`) vereint alle ehemaligen snippets.

Alle Befehle können mit `python3 toolkit.py --help` eingesehen werden.
