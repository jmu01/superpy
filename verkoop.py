import csv
from datetime import date, datetime
from datetime import timedelta
import os
from inkoop import telRegels
from datum import readDatum

def verk( args ):
    # ------------------------------------------------------------------
    # Invoer van de verkopen. Eerst wordt gecontroleerd of een artikel
    # aanwezig is in de inkoop tabel en dan wordt ook de datum en 
    # het aantal gecontroleerd
    # Let op: gebruik systeem datum indien verkoopdatum niet gegeven
    # ------------------------------------------------------------------

    print("* In func Verkoop")
    #print( "Args: ", args )   
    print( f"Verkocht: {args.aantal} van {args.productnaam} voor € {args.verkoopprijs}")

    # sysDatum = readDatum()
    sysDatum = args.verkdatum
    print( f"* Systeemdatum: {sysDatum}")

    inkList = getInkVoorr( args.productnaam, sysDatum)
    aantVoorr = inkList[0]
    aantVerkocht = getAantVerkocht(args.productnaam, sysDatum)

    print( f"Actuele voorr: {aantVoorr} minus al verkocht: {aantVerkocht} ")

    # met naam zoeken naar ID in inkoop:
    inkFile = "inkoop.txt"
    inkFile = os.getcwd() + "\\" + inkFile

    if (aantVoorr - aantVerkocht) >= int(args.aantal):
        # er is voldoende voorraad, dus boeken
        newID = writeToVerk( args, inkList[1], sysDatum )
        print( f"Verkoopregel geschreven. Last ID: {newID}")
    else:
        # er is ONvoldoende voorraad, melden
        print("* Let op: voorraad niet voldoende voor deze transactie")


def getInkVoorr( prod, sysDatum ):
    # ------------------------------------------------------------------
    # Bepaal voorr op basis van records in inkoop tabel
    # Let op: gebruik systeem datum en exp datum
    # ------------------------------------------------------------------
    
    inkFile = "inkoop.txt"
    # inkFile = os.getcwd() + "\\superpy\\" + inkFile
    inkFile = os.getcwd() + "\\" + inkFile
    totVoorr = 0

    with open(inkFile) as csvfile:
        csvRegels=csv.reader(csvfile, delimiter=';' )
        filtered = filter( lambda p: prod in p[1] and p[4] >= sysDatum and p[5] <= sysDatum, csvRegels )
        for row in filtered:
            totVoorr = totVoorr + int(row[3])
            lastID = row[0]
            lastPrice = row[2]
            lastExpDate = row[4]
            # print(row)
    
    return [totVoorr, lastID, lastPrice, lastExpDate]
    
def getAantVerkocht( prod, sysDatum ):
    # ------------------------------------------------------------------
    # Bepaal aantal verkochte items op basis van records in verkoop tabel
    # Let op: gebruik systeem datum
    # ------------------------------------------------------------------
    
    inkFile = "verkoop.txt"
    # inkFile = os.getcwd() + "\\superpy\\" + inkFile
    inkFile = os.getcwd() + "\\" + inkFile
    aantVerkocht = 0

    with open(inkFile) as csvfile:
        csvRegels=csv.reader(csvfile, delimiter=';' )
        filtered = filter( lambda p: prod in p[2] and p[5] <= sysDatum, csvRegels )
        for row in filtered:
            aantVerkocht = aantVerkocht + int(row[4])
    
    return aantVerkocht
    
def writeToVerk( args, IDinkoop, sysDatum):
    # ------------------------------------------------------------------
    # Verwerk de verkoopregels. Let op: gebruik de systeemdatum 
    # ------------------------------------------------------------------

    verkFile = "verkoop.txt"
    verkFile = os.getcwd() + "\\" + verkFile

    # haal aant regels op voor ID:
    lastID = telRegels( verkFile )
    print( f"Last ID = {lastID}")
    #lastID=0

    with open(verkFile,"a", newline='') as csvfile:
        # veldnamen=['ID', 'IDinkoop', 'omschr', 'verkoopprijs', 'aantal', 'verkoopdatum']
        regel=csv.writer(csvfile, delimiter=';' )
        #regel.writerow( veldnamen )

        lijst = [lastID +1,
                IDinkoop, 
                args.productnaam,
                args.verkoopprijs,
                args.aantal,
                args.verkdatum ]
                
        regel.writerow( lijst )

    return lastID +1
