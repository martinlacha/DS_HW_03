# Distribuováná cache
Cílem je navhnout a implementovat distribuovanou cache se stromovou strukturou. Bude se jednat o binární strom, kde maximální počet úrovní bude 3 nebo 4. Počet úrovní je volitelný pomocí konfiguračního parametru. Pokud bude zadána jiná hodnota bude nastavena na výchozí hodnotu 3. Dále je možné v konfiguraci identifikace (IP adresa nebo jméno) kořenového uzlu. Hierarchická struktura cache bude evidována jako odpovídající model v Apache Zookeeper.

Jednotlivé uzle spolu budou komunikovat pomocí následujícího API rozhraní:
* GET - Metoda vrátí hodnotu nalezenou v lokální cache daného uzlu. Pokud není hodnota nalezena uzel se pokusí získat hodnotu z rodičovského uzlu, který bude mít stejné chování a nejprve se podívá do lokální cache a při nenalezení hodnoty se zeptá rodičovského uzlu. Pokud se hodnota rekurzivně nenalezne ani v kořenovém uzlu vrátí hodnota None s příslušným návratovým kódem.
* PUT
* DELETE

```
code
```

<img src="images/01.png">

# Swagger Api
https://flask-restplus.readthedocs.io/en/stable/swagger.html