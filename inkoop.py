import csv
from datetime import date, datetime
from datetime import timedelta
import os

def ink( args ):
    # --------------------------------------------------------------
    # Controleer de invoer en schrijf de data dan naar een CSV file
    # --------------------------------------------------------------
    #print("* In func Inkoop")
    #print( "Args: ", args )   
    print( f"Ingekocht: {args.aantal} keer {args.productnaam} voor € {args.inkoopprijs}")

    inkFile = "inkoop.txt"
    inkFile = os.getcwd() + "\\" + inkFile

    # haal aant regels op voor ID:
    lastID = telRegels( inkFile )

    with open(inkFile,"a", newline='') as csvfile:
        #veldnamen=['ID', 'omschr', 'inkoopprijs', 'aantal', 'inkoopdatum', 'expdatum']
        regel=csv.writer(csvfile, delimiter=';' )
        #regel.writerow( veldnamen )

        lijst = [lastID +1,
                args.productnaam,
                args.inkoopprijs,
                args.aantal,
                args.expdatum,
                args.inkdatum ]
                
        regel.writerow( lijst )

def telRegels(filename):
    # --------------------------------------------------------------
    # tel aant regels in CSV bestand, nodig voor ID
    # --------------------------------------------------------------
    with open(filename) as f:
        return sum(1 for line in f)
    

# --------------------------------------------------------------
#print(telRegels( os.getcwd() + "\\superpy\\inkoop.txt") )