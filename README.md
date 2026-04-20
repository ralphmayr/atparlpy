[![](https://img.shields.io/pypi/v/atparlpy)](https://pypi.org/project/atparlpy)

# atparlpy

This project provides a Python wrapper for the [Austrian Parliament](https://parlament.gv.at)'s [Open Data REST APIs](https://www.parlament.gv.at/recherchieren/open-data/). The API responses are available both as [dataclasses](https://docs.python.org/3/library/dataclasses.html) and as [Pandas Dataframes](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html).

## Installation

atparlpy is [availalbe on PyPI](https://pypi.org/project/atparlpy/) and can be installed via pip:

```
$ pip install atparlpy
```

## Usage

The `atparlpy` module exposes each [dataset](#supported-datasets) as a separate class. Import and instantiate the class for your desired dataset. For example, to get all `Inquiries` ("Parlamentarische Anfragen") in the 28. legislative period:

```python
>>> from atparlpy import Inquiries
>>> inquiries = Inquiries(gp=28, nrbr="NR").AsList()
>>> print(len(inquiries))
>>> print(inquiries[0].betreff)
```

To get the result as a Pandas DataFrame instead, use the `AsDataFrame()` method:

```python
>>> from atparlpy import Inquiries
>>> df = Inquiries(gp=28, nrbr="NR").AsDataFrame()
>>> print(df['status'].value_counts())
>>> df.to_csv('inquiries.csv', index=False)
```

All filters can be set either via the constructor or via the fluent setters. For example:

```python
>>> from atparlpy import Inquiries
>>> inquiries = Inquiries().gp(28).nrbr("NR").AsList()
```

For API responses which link to a details or history page, the wrapper classes expose a `GetDetails()` method, which fetches the json representation of the respective details or history page. The `references` and `names` of the details / history page are wrapped explicitly for easy access. The `meta` and `content` properties are available as raw dictionaries. For example:

```python
>>> reports = CommitteeReports(nrbr="NR", gp_code="XXV").AsList()
>>> details = reports[0].GetDetails()
>>> description = details.content['description']
>>> initiators = list(filter(lambda n: n.funktext == 'Eingebracht von', details.names))
```

---

See [examples.py](examples/examples.py) for more examples.

## Convenience features

* Wherever the REST API only accepts the legislative period as a Roman numeral (`"GP_CODE": ["XXVIII"]`), the wrapper also accepts the corresponding integer value. The Roman numeral can be set via `gp_code` and the integer value via `gp`. If both are provided, `gp_code` takes precedence.
* The wrapper accepts either a list of strings or a single string value wherever the REST API only accepts a list of string values (e.g., `"THEMEN": ["Arbeit"]` can be set as `.themen("Arbeit")` or `.themen(["Arbeit"])`).

## Supported datasets

### Anträge (Motions)

* [API Documentation](https://www.parlament.gv.at/recherchieren/open-data/daten-und-lizenz/antraege/index.html)

```python
# Beispiel: Abfrage nach allen Anträgen im Nationalrat während der XXVII. GP zum Thema Arbeit
motions = Motions(gp_code="XXVII").nrbr("NR").themen(["Arbeit"]).AsList()
```

### Ausschussberichte (CommitteeReports)

* [API Documentation](https://www.parlament.gv.at/recherchieren/open-data/daten-und-lizenz/ausschussberichte/index.html)

```python
# Beispiel: Alle Ausschussberichte im Nationalrat in der XXV. Gesetzgebungsperiode zum Thema Arbeit
reports = CommitteeReports(nrbr="NR", gp_code="XXV", themen="Arbeit").AsList()
```

### Beschlüsse (Resolutions)

* [API Documentation](https://www.parlament.gv.at/recherchieren/open-data/daten-und-lizenz/beschluesse/index.html)

```python
# Beispiel: Alle Beschlüsse im Nationalrat während der 25. GP zum Thema Kultur
resolutions = Resolutions().nrbr("NR").gp_code("XXV").themen("Kultur").AsList()
```

### Parlamentarische Anfragen (Inquiries)

* [API Documentation "Anfragen Bundesrat"](https://www.parlament.gv.at/recherchieren/open-data/daten-und-lizenz/datensatz-schriftliche-anfragen-br/index.html)
* [API Documentation "Anfragen Nationalrat"](https://www.parlament.gv.at/recherchieren/open-data/daten-und-lizenz/datensatz-schriftliche-anfragen-nr/index.html)

```python
# Beispiel: Alle parlamentarischen Anfragen im Nationalrat während der XXVIII. GP zum Thema Arbeit oder Bildung
inquiries = Inquiries(gp_code="XXVIII", nrbr="NR").themen(["Arbeit", "Bildung"]).AsList()
# Beispiel: Alle parlamentarischen Anfragen im Bundesrat während der 27. GP
inquiries = Inquiries(gp=27, nrbr="BR").AsList()
```

### Aktuelle Abgeordnete zum Nationalrat und Mitglieder des Bundesrats (Parliamentarians)

* [API Documentation Nationalrat](https://www.parlament.gv.at/recherchieren/open-data/daten-und-lizenz/aktuelle-abgeordnete-nr-/)
* [API Documentation Bundesrat](https://www.parlament.gv.at/recherchieren/open-data/daten-und-lizenz/aktuelle-mitglieder-br-/)

```python
# Beispiel: Alle aktuellen Abgeordneten zum Nationalrat
members_of_parliament = Parliamentarians(nrbr="NR").AsList()

# Beispiel: Fraktionen im Nationalrat plus Anzahl der Abgeordneten
df = Parliamentarians(nrbr="NR").AsDataFrame()
print(df['sort_wp'].value_counts())

# Beispiel: Aktuelle/r Präsident/in des Nationalrats
president = Parliamentarians(nrbr="NR").funk("1PNR").AsList()[0]
print(f"Präsident des NR: {president.name}")

# Beispiel: Alle aktuellen Mitglieder des Bundesrats
members_of_the_national_council = Parliamentarians(nrbr="BR").AsList()
```

The `GetDetails()` method of a `MemberOfParliament` or `MemberOfTheNationalCouncil` object fetch the details of the respective person, and return `Person` object. For example:

```python
person = Parliamentarians(nrbr="NR").funk("1PNR").AsList()[0].GetDetails()
print(f"Link zum Foto: {person.image}")
print(f"Sitzplatz: {person.sitzplatz}")
```

### Plenarsitzungen (PlenarySessions)

* [API Documentation](https://www.parlament.gv.at/recherchieren/open-data/daten-und-lizenz/plenarsitzungen/index.html)

```python
# Beispiel: Alle Plenarsitzungen des Nationalrats in der 28. GP
sessions = PlenarySessions(nrbr="NR",gp=28).AsList()
print(f"{len(sessions)} Sitzungen des Nationalrats gefunden")
```
