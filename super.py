# Imports
import argparse
import sys
import csv
from datetime import date
from verkoop import verk 
from inkoop import ink 
from report import report 
from datum import *

# Do not change these lines.
__winc_id__ = "a2bc36ea784242e4989deb157d527ba0"
__human_name__ = "superpy"


# Your code below this line.
def main():
    ''' 
    --------------------------------------------------------
        Tuig de parser op. Er zijn een aantal verschillende 
        commando's mogelijk. Die worden door subparsers afgehandeld.
        Iedere subparser heeft zijn eigen set parameters.
        Mogelijk: inkoop, verkoop, report en <leeg>
        Na de invoer van de opdracht wordt de juiste functie 
        aangeroepen, daar wordt alles afgehandeld.
    --------------------------------------------------------
    '''

    # begin met werkdatum op te halen:
    werkDatum = readDatum()
    print( "-------------------------------------------" )
    print( f'*** Let op: {werkDatum} wordt gebruikt ***')
    print( "-------------------------------------------" )

    # --------------------------------------------------------------
    parser = argparse.ArgumentParser( prog="superPY", 
        description='Supermarkt PYthon voorraadbeheer. Je kan verschillende opties gebruiken.')
        # help = 'Mogelijke acties: VERK, INK, REPORT')
    #parser.add_argument( '--aanpassendatum', '-ad', required=True, 
    #                    help = 'Datum n dagen vooruit of achteruit zetten')
    #parser.set_defaults( func = setDatum)

    # --------------------------------------------------------------
    subParsers = parser.add_subparsers( title="acties", help="mogelijke acties")

    # --------------------------------------------------------------
    dateParser = subParsers.add_parser( "date", help="Datum aanpassen.")
    dateParser.add_argument( '--aanpassendatum', '-ad',
                        help = 'Datum n dagen vooruit of achteruit zetten')
    dateParser.set_defaults( func = setDatum)

    # --------------------------------------------------------------
    verkParser = subParsers.add_parser( "verk", help="Voeg verkoop toe aan lijst verkopen.")
    verkParser.add_argument('--productnaam',  '-pn', help = "naam van het artikel", required=True)
    verkParser.add_argument('--verkoopprijs', '-vp', help = "verkoopprijs van het artikel", required=True)
    verkParser.add_argument('--aantal',       '-av', help = "aantal van het artikel", required=True)
    verkParser.add_argument('--verkdatum',    "-vd", help = "verkoopdatum (standaard: " + werkDatum + ")", default=werkDatum)
    verkParser.set_defaults( func = verk)

    # --------------------------------------------------------------
    inkParser = subParsers.add_parser( "ink", help="Voeg inkoop toe aan lijst verkopen.")
    inkParser.add_argument('--productnaam',  '-pn', help = "naam van het artikel", required=True)
    inkParser.add_argument('--inkoopprijs',  '-ip', help = "inkoopprijs van het artikel", required=True)
    inkParser.add_argument('--aantal',       '-ai', help = "aantal van het artikel", required=True)
    inkParser.add_argument('--expdatum',     "-ed", help = "houdbaarheidsdatum van het artikel", required=True)
    inkParser.add_argument('--inkdatum',     "-id", help = "inkoopdatum (standaard: " + werkDatum + ")", default=werkDatum)
    inkParser.set_defaults( func = ink)

    # --------------------------------------------------------------
    rapParser = subParsers.add_parser( "report", help="Report lijst artikelen.")
    rapParser.add_argument('opdracht', choices=["inkoop", "verkoop", "voorraad"], help = "Mogelijke rapporten")
    rapParser.add_argument('--gisteren',action="store_true")
    rapParser.add_argument('--vandaag', action="store_true")
    rapParser.add_argument('--csvbestand', '-csv', default = "")
    rapParser.add_argument('--periode', choices=["week", "maand", "jaar"], help = "Kies de lengte van de periode, standaard=jaar", default='jaar')
                           
    rapParser.set_defaults( func = report)

    # --------------------------------------------------------------
    args = parser.parse_args()
    # print( args.productnaam, args.verkoopprijs, args.expdatum)
    if len(sys.argv) <= 1:
        sys.argv.append('-h')

    # print( args )
    args.func( args )



if __name__ == "__main__":
    main()
