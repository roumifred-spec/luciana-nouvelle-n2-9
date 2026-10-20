# -*- coding: utf-8 -*-
# Montre, dans le VRAI luciana.py, ou le chien de garde a ete branche.
# LECTURE SEULE : ce script ne modifie rien.
import re

s = open('luciana.py', encoding='utf-8').read()
lignes = s.split('\n')

print("=" * 78)
print("1) LES LIGNES AJOUTEES QUI PARLENT DU CHIEN DE GARDE")
print("=" * 78)
mots = ('rangement_auto', 'chien_de_garde', 'chien de garde', 'rapports_rangement', 'verif_rangement_auto')
for i, l in enumerate(lignes, 1):
    bas = l.lower()
    if any(m.lower() in bas for m in mots):
        print("%6d | %s" % (i, l[:220]))
        print("-" * 78)

print()
print("=" * 78)
print("2) EST-CE QUE CA VA DANS LA PAGE (HTML/JS) OU DANS LA FENETRE NOIRE (print) ?")
print("=" * 78)
# On regarde uniquement les lignes autour des appels au chien de garde :
# si c'est un print(...) -> fenetre noire. Si c'est du HTML/JS -> page de Fred.
for i, l in enumerate(lignes, 1):
    if 'rangement_auto' in l.lower() or 'chien_de_garde' in l.lower():
        avant = lignes[max(0, i - 4):i]
        contexte = "\n".join("     %s" % x[:180] for x in avant)
        print("--- autour de la ligne %d ---" % i)
        print(contexte)
        print("  >>> %s" % l[:200])
        print()

print()
print("=" * 78)
print("3) COMPTE DES SIGNES : print (fenetre noire) contre balises HTML")
print("=" * 78)
zone = []
for i, l in enumerate(lignes, 1):
    if 'rangement_auto' in l.lower() or 'chien_de_garde' in l.lower():
        zone.extend(lignes[max(0, i - 6):i + 7])
texte = "\n".join(zone)
print("lignes regardees :", len(zone))
print("print( :", texte.count('print('))
print("<div  :", texte.count('<div'))
print("innerHTML :", texte.count('innerHTML'))
print("document. :", texte.count('document.'))
