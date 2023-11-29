import csv
from datetime import date, datetime
from datetime import timedelta
import os
from inkoop import telRegels
from datum import readDatum
from verkoop import getInkVoorr, getAantVerkocht
import locale

def report( args ):
    # --------------------------------------------------------------
    # Afh van opdracht wordt hier een bepaald rapport getoond
    # --------------------------------------------------------------
    # print("* In func Report")
    #print( "Args: ", args )   
    print( f"* Rapport over {args.opdracht} ")

    # basisdaum bepalen:
    datum = readDatum()
    # datum = args.datum
    dateFormat= "%Y-%m-%d"
    if (args.gisteren and args.vandaag):
        print( "* Fout: niet zowel Gisteren als Vandaag geven. Huidige systeem datum wordt gebruikt" )
    elif args.gisteren:
        # neem datum minus 1
        datum = (datetime.strptime( datum, dateFormat) + timedelta( days=-1)).strftime(dateFormat)
    elif args.vandaag:
        # neem datum van vandaag, dus niets doen
        datum = datum

    if not (args.gisteren or args.vandaag):
        match args.periode:
            case "week":
                startDatum = (datetime.strptime( datum, dateFormat) - timedelta( weeks = 1)).strftime(dateFormat)
            case "maand":
                startDatum = (datetime.strptime( datum, dateFormat) - timedelta( days = 30)).strftime(dateFormat)
            case "jaar":
                startDatum = datetime( int(datum[0:4]), 1, 1).strftime(dateFormat)
    else:
        startDatum = datum

    print( f"* Gebruikte periode: {startDatum} t/m {datum}" )        

    match args.opdracht:
        case "inkoop":
            # toon een lijst met alle inkopen
            inkReport( datum, startDatum )
        case "verkoop":
            # toon een lijst met alle verkopen
            verkReport( datum, startDatum )
        case "voorraad":
            # toon een lijst de voorraad
            voorraadReport( datum, startDatum, args.csvbestand )
        case _:
            print("Niet de juiste opdracht ingevoerd")
    
def inkReport( werkDatum, startDatum ):
    # --------------------------------------------------------------
    # Maak een overzicht van alle inkoop regels 
    # --------------------------------------------------------------   
    inkFile = "inkoop.txt"
    inkFile = os.getcwd() + "\\" + inkFile

    with open(inkFile) as csvfile:
        csvRegels=csv.reader(csvfile, delimiter=';' )
        filtered = filter( lambda p: p[5] <= werkDatum, csvRegels )
        regelNr = 0
        row=['ID',      'omschr',     'inkprijs'   , 'aantal'   , 'expdatum'  , 'inkdatum']
        print( "-" * 80 )
        print( f"|{row[0]: <6}|{row[1]: <25}|{row[2]: >12}|{row[3]: <6}|{row[4]: <12}|{row[5]: <12}|")
        print( "-" * 80 )
        for row in filtered:
            print( f"|{row[0]: <6}|{row[1]: <25}|{row[2]: >12}|{row[3]: <6}|{row[4]: <12}|{row[5]: <12}|")
            regelNr += 1
        print( "-" * 80 )
        print( f"* Aantal regels: {regelNr}")


def verkReport( werkDatum, startDatum ):
    # --------------------------------------------------------------
    # Maak een overzicht van alle verkoop regels 
    # -------------------------------------------------------------- 
    verkFile = "verkoop.txt"
    verkFile = os.getcwd() + "\\" + verkFile
    locale.setlocale(locale.LC_ALL, 'nl_NL.UTF-8')

    with open(verkFile) as csvfile:
        csvRegels=csv.reader(csvfile, delimiter=';' )
        filtered = filter( lambda p: p[5] <= werkDatum and p[5] >= startDatum, csvRegels )
        regelNr = 0
        omzet = 0
        row=['ID',  '', 'omschr', 'verkprijs', 'aantal', 'omzet', 'verkdatum']
        #      0             2            3        4        5         6
        print( "-" * 80 )
        print( f"|{row[0]: <6}|{row[2]: <25}|{row[3]: >12}|{row[4]: <6}|{row[5]: >12}|{row[6]: <12}|")
        print( "-" * 80 )

        for row in filtered:
            regel = regelVerkoop( row, filtered )
            omzet += regel[4]
            regel[2] = locale.currency( regel[2], grouping = True)
            regel[4] = locale.currency( regel[4], grouping = True)
            print( f"|{regel[0]: <6}|{regel[1]: <25}|{regel[2]: >12}|{regel[3]: >6}|{regel[4]: >12}|{regel[5]: <12}|")
            regelNr += 1
        print( "-" * 80 )
        omzet = locale.currency( omzet, grouping = True)
        print( f"* Omzet over deze periode: {omzet}" )
        print( f"* Aantal regels: {regelNr}")

def regelVerkoop( row, allRow):
    # --------------------------------------------------------------
    # Maakt een list met de verkoop items
    # --------------------------------------------------------------
    regel = [row[0],
             row[2],
             float(row[3]),
             row[4],
             float(row[3]) * int(row[4]),
             row[5] ]
    return regel
    
def voorraadReport( sysDatum, startDatum, csvNaam ):
    # --------------------------------------------------------------
    # Maak een overzicht van de actuele voorraad
    # Voeg toe: schrijf data naar csv bestand
    # --------------------------------------------------------------

    # maak eerst een dict met alle ingekochte artikelen
    allArtikel = getAllArtikel()
    
    # sysDatum = readDatum()
    print( f"* Systeemdatum: {sysDatum}")
    row=['ID',  'Naam',     'inkprijs', 'aantal'   , 'exp datum']
    regelNr = 0
    
    # indien CSV bestand opgegeven geen print, maar export
    if csvNaam != "":
        # init settings voor export
        exportFile = os.getcwd() + "\\" + csvNaam
        print( f"* Export data naar CSV bestand: {exportFile}" )
        with open( exportFile, "w", newline='') as csvfile:
            csvRegels = csv.writer( csvfile, delimiter=';' )
            # schrijf header:
            csvRegels.writerow( row )

            # doorloop de artikelen:
            for artikel in allArtikel:
        
                # maak een lijst aan:
                row = regelVoorraad( artikel, allArtikel, sysDatum)
                csvRegels.writerow( row )
    else:
        # print header:
        print( "-" * 74 )
        print( f"|{row[0]: <6}|{row[1]: <25}|{row[2]: >12}|{row[3]: >12}|{row[4]: <12}|")
        print( "-" * 74 )    

        # doorloop de artikelen:
        for artikel in allArtikel:
            
            # maak een lijst aan:
            row = regelList( artikel, allArtikel, sysDatum)

            print( f"|{row[0]: <6}|{row[1]: <25}|{row[2]: >12}|{row[3]: >12}|{row[4]: >12}|" )
            regelNr += 1

        print( f"* Aantal regels: {regelNr}")


def regelVoorraad( artikel, allArtikel, sysDatum):
    # --------------------------------------------------------------
    # Opbouwen van een list met de afzonderlijke velden.
    # Hiermee kan een print en een csv gemaakt worden
    # --------------------------------------------------------------

    # haal de inkopen per werkdatum op:
    inkData = getInkVoorr( allArtikel[ artikel ]['naam'], sysDatum )
    allArtikel[ artikel ]['aantInk'] = inkData[0]
    allArtikel[ artikel ]['inkPrijs'] = inkData[2]
    allArtikel[ artikel ]['expDatum'] = inkData[3]

    # haal de verkopen op:
    allArtikel[ artikel ]['aantVerk'] = getAantVerkocht( allArtikel[ artikel ]['naam'], sysDatum )
    
    # print(  allArtikel[ artikel ]['naam'] , allArtikel[ artikel ]['aantInk'], allArtikel[ artikel ]['aantVerk']  )
    voorraad = inkData[0] - allArtikel[ artikel ]['aantVerk']

    # zet alles in een list:
    row = [ inkData[1], 
            allArtikel[ artikel ]['naam'], 
            allArtikel[ artikel ]['inkPrijs'], 
            voorraad,
            allArtikel[ artikel ]['expDatum'] ]    
    return row

def getAllArtikel():
    # --------------------------------------------------------------
    # Retourneert een dictionairy met alle arikelen in inkoop.txt
    # --------------------------------------------------------------
    inkFile = "inkoop.txt"
    #inkFile = os.getcwd() + "\\superpy\\" + inkFile
    inkFile = os.getcwd() + "\\" + inkFile
    allArtikel = {}


    with open(inkFile) as csvfile:
        csvRegels=csv.reader(csvfile, delimiter=';' )
        for row in csvRegels:
            if row[0] != 'ID':
                # print( row[0], row[1])
                allArtikel[ row[1]] = {'naam': row[1], 'aantInk': 0, 'aantVerk': 0, 'inkPrijs' :0, 'expDatum': None}
    
    return allArtikel

# allArt = getAllArtikel()
# print( allArt )
# voorraadReport()