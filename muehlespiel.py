import math
import numpy as np

def farbe2name(farbe):
    conversions = {1:"Weiss", 2:"Schwarz", 0:"Unbesetzt"}
    return conversions[farbe]

class feld():
    def __init__(self):
        self.besetzung = 0
        self.unzerstoerbar = False

def routine():
    for ring_pos in range(len(spielfeld)):
        for stelle_pos in range(len(spielfeld[ring_pos])):
            spielfeld[ring_pos][stelle_pos].unzerstoerbar = False

def checkmuehle():
    for ring_pos in range(len(spielfeld)):
        for stelle_pos in range(len(spielfeld[ring_pos])):
            if stelle_pos%2 != 0 and spielfeld[ring_pos][stelle_pos].besetzung != 0:
                print("Found Spielstein at Ring {} Stelle {}".format(ring_pos, stelle_pos))
                if spielfeld[ring_pos][stelle_pos+1].besetzung == spielfeld[ring_pos][stelle_pos].besetzung and spielfeld[ring_pos][stelle_pos-1].besetzung == spielfeld[ring_pos][stelle_pos].besetzung:
                    spielfeld[ring_pos][stelle_pos].unzerstoerbar = True
                    spielfeld[ring_pos][stelle_pos+1].unzerstoerbar = True
                    spielfeld[ring_pos][stelle_pos-1].unzerstoerbar = True
                    print("{} hat eine Mühle!".format(farbe2name(spielfeld[ring_pos][stelle_pos].besetzung)))
                    print("Welchen Stein willst du entfernen?")
                    ring_wahl = int(input("Ring"))
                    stelle_wahl = int(input("Stelle"))
                    if spielfeld[ring_wahl][stelle_wahl].unzerstoerbar == False:
                        spielfeld[ring_wahl][stelle_wahl].besetzung.remove()
                if ring_pos == 1 and spielfeld[ring_pos][stelle_pos].besetzung == spielfeld[ring_pos+1][stelle_pos].besetzung and spielfeld[ring_pos][stelle_pos].besetzung == spielfeld[ring_pos-1][stelle_pos].besetzung:
                    spielfeld[ring_pos][stelle_pos].unzerstoerbar = True
                    spielfeld[ring_pos+1][stelle_pos].unzerstoerbar = True
                    spielfeld[ring_pos-1][stelle_pos].unzerstoerbar = True
                    print("{} hat eine Mühle!".format(farbe2name(spielfeld[ring_pos][stelle_pos].besetzung)))
                    print("Welchen Stein willst du entfernen?")
                    ring_wahl = int(input("Ring"))
                    stelle_wahl = int(input("Stelle"))
                    if spielfeld[ring_wahl][stelle_wahl].unzerstoerbar == False:
                        spielfeld[ring_wahl][stelle_wahl].besetzung.remove()
                        if farbe2name(spielfeld[ring_pos][stelle_pos].besetzung) == "Weiss":
                            figuren_schwarz -= 1
                        elif farbe2name(spielfeld[ring_pos][stelle_pos].besetzung) == "Schwarz":
                            figuren_schwarz -= 1

spielfeld = [[feld() for j in range(8)] for i in range(3)]

figuren_weiss = 10
figuren_weiss_übrig = 10
figuren_schwarz = 10
figuren_schwarz_übrig = 10
zug = 1

for i in range(20):
    if zug == 1:
        print("Weisst setzt noch {}".format(figuren_weiss_übrig))
        figuren_weiss_übrig -= 1
        setze_ring = int(input("Setze an Ring: "))
        setze_stelle = int(input("Setze an Stelle: "))
        spielfeld[setze_ring][setze_stelle].besetzung = 1
        zug = 2
    else:
        print("Schwarz setzt noch {}".format(figuren_schwarz_übrig))
        figuren_schwarz_übrig -= 1
        setze_ring = int(input("Setze an Ring: "))
        setze_stelle = int(input("Setze an Stelle: "))
        spielfeld[setze_ring][setze_stelle].besetzung = 2
        zug = 1

    checkmuehle()
