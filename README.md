# innoCampus Freight Routes (Aufgabe vom 24. Februar 2020)

## Aufgabe

Ein Logistik-Unternehmen betreibt Güterzüge auf einem Teil des Bahnnetzes
eines (kleinen) Landes. Alle Knoten des Netzes liegen auf Städten. Zwischen
je zwei Städten gibt es höchstens eine in beiden Richtungen befahrbare
Bahnstrecke ohne Zwischenhalt. Sollen nun Güter von einer Stadt A zu einer
anderen Stadt B gefahren werden, ist der kürzeste Weg auf dem Streckennetz
von A nach B gesucht.

Schreiben Sie dazu ein Programm mit einer einfachen Web-Oberfläche in
Python oder PHP.

1. Die aktuelle Definition des Streckennetzes wird in einer einfachen Form
angezeigt.
2. Es ist möglich, Städte und Verbindungen zwischen Städten mit einer
Längenangabe hinzuzufügen.
3. Der Nutzer kann zwei Städte auswählen und per Knopf-Klicken einen
optimalen (d.h. kürzesten) Weg zwischen diesen Städten anzeigen lassen.
4. Kümmern Sie sich auch um die Behandlung von Fehlern, die dabei
auftreten können.

Für die Umsetzung der Web-Oberfläche dürfen Sie Frameworks/Libraries
einsetzen. Bitte verwenden Sie insgesamt jedoch möglichst wenig externe Abhängigkeiten.

## Installation

Da bei der Installation eine Umgebungsvariable gesetzt wird, 
sollte das Skript mit dem `source`-Befehl aufgerufen werden, 
also `source install_freight_routes.sh`. (getestet mit Debian/Ubuntu)

Benötigt **Python 3.5 oder höher** sowie das Python Modul `pipenv` global (für Python 3) installiert. 
Letzteres wird andernfalls automatisch nachinstalliert.

`pip3` sollte sich dazu entsprechend im PATH befinden.

Die Dateien für die virtuelle Umgebung werden bei der Installation im Projektverzeichnis gespeichert.

Zum Starten der virtuellen Umgebung:

```$ pipenv shell```

Zum Starten des dev. Servers innerhalb der virtuellen Umgebung:

```$ python manage.py runserver``` 
(**Wichtig:** NICHT `python3`)

Der Server läuft dann hinter dem Port 8000.

Der Server kann normal mit `Ctrl+C` ausgeschaltet werden.


## Externe Bibliotheken/Frameworks

Für das Backend wurde lediglich das [**Django REST Framework**](https://www.django-rest-framework.org/) (inkl. Django) für Python 3 gebraucht.

Für das Frontend wurde [**jQuery**](https://jquery.com/) als JavaScript Bibliothek nur für die AJAX calls an die REST API verwendet.

Zum Entwicklung einer angenehmen visuellen Darstellung der Graphen wurde [**Cytoscape.js**](https://js.cytoscape.org/) verwendet.


## Funktionsweise/Demonstration

### Algorithmen
Zwar bietet natürlich Cytoscape.js bereits die gängigsten Algorithmen zur Graphendurchmusterung,
jedoch habe ich mich natürlich dazu entschieden einen solchen selbst (in Python, also im Backend) zu implementieren.

### Wieso Datenbank?
Ebenfalls zu Demonstrationszwecken wird hier eine SQLite Datenbank verwendet.
Die Graphenstruktur wird damit über das Django-eigene ORM in die Datenbank ge-mapped.
Sämtliche Veränderungen des Graphen im Browser rufen asynchrone Serverabfragen, 
welche die Änderungen in der Datenbank speichern.
Bei erneutem Aufruf der Seite, wird der letzte Stand geladen.

### Server- vs. Client-seitig
Somit läuft auch der Kürzeste-Wege-Algorithmus auf dem Server.
Bei größeren Strukturen bietet der Server in der Regel größere Rechenkapazitäten.
Der u.U. dadurch gewonnene Geschwindigkeitsvorteil kann dann ggf. die
kurzen Verzögerungen bei den AJAX calls ausgleichen.
In diesem Arbeitsbeispiel wird dies aber wohl kaum der Fall sein.
Dennoch habe ich mich zur Demonstration für diese Aufteilung entschieden.

### Wieso ohne Apache?
Ich habe mich bewusst dagegen entschieden, 
ein Zusammenspiel mit Apache zu unternehmen.
Der Development Server von Django reicht für diese Arbeit vollkommen aus.
Zudem hat mir meine eigene Erfahrung gezeigt, 
dass das Deployen einer Django App mit Apache über `mod_wsgi` alles andere als trivial ist,
sehr viele Systemconfigurationen erfordert 
und im Rahmen dieser Aufgabe entsprechend viel zu aufwändig wäre.
