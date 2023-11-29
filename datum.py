import csv
from datetime import date, datetime
from datetime import timedelta
import os

def saveDatum( datum = date.today().isoformat() ):
    # --------------------------------------------------------------
    # schrijft de datum weg naar een txt bestand
    # als geen datum gegeven is, dan huidige gebruiken
    # --------------------------------------------------------------

    datumFile = "werkdatum.txt"
    datumFile = os.getcwd() + "\\" + datumFile
    with open( datumFile,"w", newline='') as txtfile:
        regel=csv.writer( txtfile )
        txtfile.write( datum )

def readDatum():
    # --------------------------------------------------------------
    # leest de datum uit de txt file
    # indien leeg of niet gevonden, dan huidige datum gebruiken
    # --------------------------------------------------------------

    datumFile = "werkdatum.txt"
    datumFile = os.getcwd() + "\\" + datumFile
    datum = ""
    # print( f"   * Werk directory: {os.getcwd()}")
    # print( f"   * Bestand: {datumFile}")

    if os.path.isfile( datumFile ):
        with open( datumFile ) as csv_file:
            csv_reader = csv.reader(csv_file)
            for regel in csv_reader:
                datum = regel[0]
    else:
        print( f"Bestand {datumFile} niet gevonden")
    if datum == "":
        datum = date.today().isoformat() 
    
    return datum

def setDatum( args ):
    # --------------------------------------------------------------
    # past de werkdatum aan door deze te verschuiven tov huidige
    # --------------------------------------------------------------
    werkDatum = readDatum()
    dateFormat= "%Y-%m-%d"

    # print( f"   Werk directory: {os.getcwd()}")
    # print( f"   Huidige werkdatum: {werkDatum}")
    if int( args.aanpassendatum ) == 0:
        werkDatum = date.today().isoformat() 
    else:
        print( f"   Aanpassen met {args.aanpassendatum} dagen")
        werkDatum = (datetime.strptime( werkDatum, dateFormat) + timedelta( days= int( args.aanpassendatum ))).strftime(dateFormat)
    print( f"   Nieuwe datum: {werkDatum}" )

    saveDatum( werkDatum )

# --------------------------------------------------------------
# Testen
# --------------------------------------------------------------

#cwd = os.getcwd()
#print(cwd)

#print( "Schrijf datum" )
#saveDatum(  )
#print( f"Leesdatum {readDatum()}" )
