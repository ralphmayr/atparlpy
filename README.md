# atparlpy

This project provides a Python wrapper for the [Austrian Parliament](https://parlament.gv.at)'s [Open Data REST APIs](https://www.parlament.gv.at/recherchieren/open-data/).

## Convenience features

* The API responses are available both as [dataclasses](https://docs.python.org/3/library/dataclasses.html) and as [Pandas Dataframes](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html).
* Wherever the REST API only accepts the legislative period ("GP_CODE") as a Roman numeral (e.g., "XXVIII" for 28), the wrapper also accepts the integer value.
* The wrapper accepts either a list of strings or a single string value wherever the REST API only accepts a list of string values (e.g., "THEMEN" or "SW").

## Supported datasets

### Anträge (Motions)

* [API Documentation](https://www.parlament.gv.at/recherchieren/open-data/daten-und-lizenz/antraege/index.html)

#### Example

```
# Beispiel: Abfrage nach allen Anträgen im Nationalrat während der XXVII. GP zum Thema Arbeit
motions = Motions(gp_code="XXVII").nrbr("NR").themen(["Arbeit"]).AsList()
```

### Ausschussberichte (CommitteeReports)

* [API Documentation](https://www.parlament.gv.at/recherchieren/open-data/daten-und-lizenz/ausschussberichte/index.html)

#### Example

```
# Beispiel: Abfrage nach allen parlamentarischen Anfragen im Bundesrat während der XXVIII. GP
inquiries = Inquiries(gp=28, nrbr="BR").AsList()
```

### Beschlüsse (Resolutions)

* [API Documentation](https://www.parlament.gv.at/recherchieren/open-data/daten-und-lizenz/beschluesse/index.html)

#### Example

```
# Beispiel: Abfrage nach allen Beschlüssen im Nationalrat während der 25. GP zum Thema Kultur
resolutions = Resolutions().nrbr("NR").gp_code("XXV").themen("Kultur").AsList()
```

### Anfragen (Inquiries)

* [API Documentation Anfragen BR](https://www.parlament.gv.at/recherchieren/open-data/daten-und-lizenz/datensatz-schriftliche-anfragen-br/index.html)
* [API Documentation Anfragen NR](https://www.parlament.gv.at/recherchieren/open-data/daten-und-lizenz/datensatz-schriftliche-anfragen-nr/index.html)

#### Example

```
# Beispiel: Abfrage nach allen parlamentarischen Anfragen im Nationalrat während der XXVIII. GP zum Thema Arbeit oder Bildung
inquiries = Inquiries(gp=28, nrbr="NR").themen(["Arbeit", "Bildung"]).AsList()
```

### Aktuelle Abgeordnete zum Nationalrat und Mitglieder des Bundesrats (Parliamentarians)

* [API Documentation Nationalrat](https://www.parlament.gv.at/recherchieren/open-data/daten-und-lizenz/aktuelle-abgeordnete-nr-/)
* [API Documentation Bundesrat](https://www.parlament.gv.at/recherchieren/open-data/daten-und-lizenz/aktuelle-mitglieder-br-/)

#### Example

```
# Beispiel: Abfrage nach allen aktuellen Abgeordneten zum Nationalrat
members_of_parliament = Parliamentarians(nrbr="NR").AsList()

# Beispiel: Fraktionen im Nationalrat plus Anzahl der Abgeordneten
df = Parliamentarians(nrbr="NR").AsDataFrame()
print(df['sort_wp'].value_counts())

# Beispiel: Abfrage nach dem aktuellen Präsidenten des Nationalrats
president = Parliamentarians(nrbr="NR").funk("1PNR").AsList()[0]

# Beispiel: Abfrage nach allen aktuellen Mitgliedern des Bundesrats
members_of_the_national_council = Parliamentarians(nrbr="BR").AsList()
```
