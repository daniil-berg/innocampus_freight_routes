# innoCampus Freight Routes (Aufgabe vom 24. Februar 2020)

## Installation
Benötigt Python 3.5 oder höher sowie das Python Modul `pipenv` global (für Python 3) installiert. 
Letzteres wird andernfalls automatisch nachinstalliert.

`pip3` sollte sich entsprechend im PATH befinden.

Die Dateien für die virtuelle Umgebung werden bei der Installation im Projektverzeichnis gespeichert.

Zum Starten der virtuellen Umgebung:

```$ pipenv shell```

Zum Starten des dev. Servers innerhalb der virtuellen Umgebung:

```$ python manage.py runserver``` 
(**Wichtig:** NICHT `python3`)

Der Server läuft dann hinter dem Port 8000.


## Externe Bibliotheken/Frameworks

Für das Backend wurde lediglich das [**Django REST Framework**](https://www.django-rest-framework.org/) (inkl. Django) für Python 3 gebraucht.

Für das Frontend wurde [**jQuery**](https://jquery.com/) als JavaScript Bibliothek nur für die AJAX calls an die REST API verwendet.

Zum Entwicklung einer angenehmen visuellen Darstellung der Graphen wurde [**Cytoscape.js**](https://js.cytoscape.org/) verwendet.


## Funktionsweise/Demonstration

Zwar bietet natürlich Cytoscape.js bereits die gängigsten Algorithmen zur Graphendurchmusterung,
jedoch habe ich mich natürlich dazu entschieden einen solchen selbst (in Python, also im Backend) zu implementieren.

Ebenfalls zu Demonstrationszwecken wird hier eine SQLite Datenbank verwendet.
Die Graphenstruktur wird damit über das Django-eigene ORM in die Datenbank ge-mapped.

Sämtliche Veränderungen des Graphen im Browser rufen asynchrone Serverabfragen, 
welche die Änderungen in der Datenbank speichern.

Somit läuft auch der Kürzeste-Wege-Algorithmus auf dem Server.
Bei größeren Strukturen bietet der Server in der Regel größere Rechenkapazitäten.
Der u.U. dadurch gewonnene Geschwindigkeitsvorteil kann dann ggf. die
kurzen Verzögerungen bei den AJAX calls ausgleichen.
In diesem Arbeitsbeispiel wird dies aber wohl kaum der Fall sein.
Dennoch habe ich mich zur Demonstration für diese Aufteilung entschieden.
