# superPY
## _Project voor cursus Programming with Python_


Doel van het project is creëren van een command-line tool in Python voor het bijhouden van de voorraad van een supermarkt.
## Eisen aan project:
- Gebruik CSV bestanden voor opslag van data
- Gebruik argParse om de command-line tool vorm te geven
- Gebruik de standaard datum format
 
## Eisen aan de code:
- Gestructureerd, duidelijke namen voor variabelen, duidelijke comments in de source
- Meerdere modules
- Externe bestanden voor de opslag van data
- Zelfverklarende command-line interface

## Features
- Instellen systeem datum
- Invoeren van Inkopen
- Invoeren van Verkopen
- Verschillende rapporten
 
## Systeem datum
De datum die wordt gebruikt tijdens de verschillende commando's is gebaseerd op de *systeemdatum* van de applicatie. Door deze in te stellen kan er worden gewerkt met een andere datum dan de huidige.
Commando:
```sh
superPY date [-h] [--aanpassendatum AANPASSENDATUM]
options:
  -h, --help                            show this help message and exit
  --aanpassendatum AANPASSENDATUM, -ad AANPASSENDATUM
                                        Datum n dagen vooruit of achteruit zetten
```

## Inkopen
Nieuwe voorraad kan aan het systeem worden toegevoegd met het volgende commando:
```sh
usage: superPY ink [-h] --productnaam PRODUCTNAAM --inkoopprijs INKOOPPRIJS --aantal AANTAL --expdatum EXPDATUM [--inkdatum INKDATUM]

options:
  -h, --help            show this help message and exit
  --productnaam PRODUCTNAAM, -pn PRODUCTNAAM
                        naam van het artikel
  --inkoopprijs INKOOPPRIJS, -ip INKOOPPRIJS
                        inkoopprijs van het artikel
  --aantal AANTAL, -ai AANTAL
                        aantal van het artikel
  --expdatum EXPDATUM, -ed EXPDATUM
                        houdbaarheidsdatum van het artikel
  --inkdatum INKDATUM, -id INKDATUM
                        inkoopdatum (standaard: systeemdatum)
```
Nieuwe regels worden toegevoegd aan de tabel met inkopen, genaamd `inkoop.txt`. Indien de inkoopdatum niet gegeven is, wordt de systeemdatum gebruikt.
Vooraf aan het uitvoeren van het commando wordt getoond wat de systeemdatum is.

## Verkopen
Een verkoop kan worden ingevoerd met het volgende commando:
```sh
usage: superPY verk [-h] --productnaam PRODUCTNAAM --verkoopprijs VERKOOPPRIJS --aantal AANTAL [--verkdatum VERKDATUM]

options:
  -h, --help            show this help message and exit
  --productnaam PRODUCTNAAM, -pn PRODUCTNAAM
                        naam van het artikel
  --verkoopprijs VERKOOPPRIJS, -vp VERKOOPPRIJS
                        verkoopprijs van het artikel
  --aantal AANTAL, -av AANTAL
                        aantal van het artikel
  --verkdatum VERKDATUM, -vd VERKDATUM
                        verkoopdatum (standaard: systeemdatum)
```
Nieuwe regels worden toegevoegd aan de tabel met verkopen, genaamd `verkoop.txt`. Indien de verkoopdatum niet gegeven is, wordt de systeemdatum gebruikt.
Vooraf aan het uitvoeren van het commando wordt getoond wat de systeemdatum is.
Tevens wordt een check uitgevoerd op de aanwezige voorraad; dit is het aantal ingekochte items minus het aantal reeds verkochte items en minus het aantal artikelen waarvan de houdbaarheidsdatum is verstreken, rekening houdend met de systeemdatum.

## Rapporten
Voor goede bedrijfsvoering zijn overzichten erg belangrijk. SuperPY beschikt over een aantal nuttige rapporten:
- inkopen
- verkopen en omzet
- bruto winst
- voorraden

Commando:
```sh
usage: superPY report [-h] [--gisteren] [--vandaag] [--csvbestand CSVBESTAND] [--periode {week,maand,jaar}] {inkoop,verkoop,voorraad}

positional arguments:
  {inkoop,verkoop,voorraad}
                        Mogelijke rapporten

options:
  -h, --help            show this help message and exit
  --gisteren
  --vandaag
  --csvbestand CSVBESTAND, -csv CSVBESTAND
  --periode {week,maand,jaar}
                        Kies de lengte van de periode, standaard=jaar
```
Op basis van de opties kan een periode worden bepaald waarvoor het rapport wordt opgesteld. Ook hier geldt weer de systeemdatum als uitgangspunt. Met de optie **--gisteren** worden de gegevens van de dag voorafgaande aan de systeemdatum getoond. Met de optie **--periode** kan worden aangegeven dat het overzicht over een week, of een maand voorafgaande aan de systeemdatum moet worden getoond, of de periode vanaf 1 januari van het jaar van de systeemdatum tot aan de systeemdatum.

De rapporten kunnen i.p.v. naar het scherm ook naar een CSV bestand worden uitgevoerd.

## Tech
Alle bestanden zijn opgeslagen in de map **<werkmap>\superpy**
Het uitvoeren van een commando gaat met de opdracht in deze map:
```sh
python super.py <opties>
```

Alle CSV bestanden gebruiken de punt-komma als scheidingsteken. Op de eerste regel staan de veldnamen. Per regel bestaat het eerste veld uit een ID.
Datumvelden hebben het formaat JJJJ-MM-DD. De systeemdatum wordt opgeslagen in het bestand **werkdatum.txt**.

