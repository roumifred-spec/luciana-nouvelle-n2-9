# -*- coding: utf-8 -*-
# CONSTAT SUR DU REEL. Ne modifie RIEN : il ne fait que LIRE et compter.
import io, json, os

DOSSIER = os.path.join(os.path.expanduser("~"), "Luciana")

d = json.load(io.open(os.path.join(DOSSIER, "luciana_memoire.json"), encoding="utf-8-sig"))
if isinstance(d, list):
    hist = d
else:
    print("cles racine :", list(d.keys())[:15])
    hist = d.get("messages") or d.get("historique") or d.get("conversation") or []

carnet = json.load(io.open(os.path.join(DOSSIER, "journee_rangee.json"), encoding="utf-8-sig"))
dernier = int(carnet.get("dernier", -1))
debut = dernier + 1

print("NB MESSAGES dans la memoire  len(hist) =", len(hist))
print("carnet 'dernier'                       =", dernier)
print("debut de fenetre (dernier+1)           =", debut)
print("MESSAGES ENCORE DANS LA FENETRE        =", len(hist) - debut)
print("dernier_rangement                      =", carnet.get("dernier_rangement"))

# la taille du fil non range, mesuree comme le programme la mesure (contenu brut seul ici)
def taille(m):
    c = m.get("content")
    return len(c if isinstance(c, str) else str(c))

if 0 <= debut <= len(hist):
    print("CARACTERES DU FIL NON RANGE (contenu)  =", sum(taille(m) for m in hist[debut:]))
else:
    print("!!! debut HORS BORNES : la fenetre est VIDE")
