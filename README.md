# Ohjelmistoteknikka harjoitustyö

**korttipeli** *"kurkku"*

[Changelog](https://github.com/OGesko/Ohjelmistotekniikka/blob/main/kurkkupeli/dokumentaatio/Changelog.md)

[vaatimusmäärittely](https://github.com/OGesko/Ohjelmistotekniikka/blob/main/kurkkupeli/dokumentaatio/vaatimusmaarittely.md)

[tuntikirjanpito](https://github.com/OGesko/Ohjelmistotekniikka/blob/main/kurkkupeli/dokumentaatio/Tuntikirjanpito_kurkkupeli.md)

[Arkkitehtuuri](https://github.com/OGesko/Ohjelmistotekniikka/blob/main/kurkkupeli/dokumentaatio/arkkitehtuuri.md)

- moninpelattava (2-6)

## Asennus
```
git clone https://github.com/OGesko/Ohjelmistotekniikka/tree/main/kurkkupeli.git
```
```
cd Ohjelmistotekniikka/kurkkupeli
```
```
poetry install
```

## Käynnistys
```
poetry run invoke start
```

## Testaus
```
poetry run invoke test
```
```
poetry run invoke coverage-report
```
```
poetry run invoke lint
```
