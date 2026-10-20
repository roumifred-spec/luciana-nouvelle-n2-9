# -*- coding: utf-8 -*-
"""LE DEBRANCHEMENT DU RAPPEL DE L'ANCIENNE MEMOIRE (12/10/2026, GO explicite de Fred).

CE QU'IL FAIT, ET RIEN D'AUTRE :
 1) il sauvegarde luciana.py et reglage_memoire_sens.json (copies datees, a cote) ;
 2) il pose un INTERRUPTEUR "rappel_ancien" (ETEINT) : le rappel automatique des vieux
    passages de l'ancienne memoire ne part plus devant la phrase de Fred ;
 3) il ne touche a AUCUNE autre ligne, et il n'efface AUCUNE donnee ;
 4) il compile le fichier et il DIT si la compilation passe ou rate ;
 5) il relit tout et ecrit son rapport.

SI LE FICHIER N'EST PAS DANS L'ETAT ATTENDU, IL N'ECRIT RIEN DU TOUT.
"""

import io, os, json, shutil, py_compile

D = r"C:\Users\Fred\Desktop\Luciana_v161_memoire2_curseur"
P = os.path.join(D, "luciana.py")
RP = os.path.join(D, "reglage_memoire_sens.json")
R = os.path.join(D, "RESULTAT_correction_rappel_ancien.txt")

bloc_avant = """    try:
        rappel = rappel_automatique(message_utilisateur, hist, debut, chien)
    except Exception:
        rappel = ""
"""

bloc_apres = """    #  12/10/2026, DEMANDE EXPLICITE DE FRED ("supprime le tuyau qui va a l'ancienne
    #  bibliotheque") : LE RAPPEL DE L'ANCIENNE MEMOIRE NE PART PLUS DEVANT SA PHRASE.
    #  La nouvelle bibliotheque a ses souvenirs integres : ce rappel ne ramenait plus que
    #  du bruit, et c'est lui qui faisait remonter des passages hors sujet.
    #  Derriere l'interrupteur "rappel_ancien" du reglage de la memoire par le sens, relu
    #  A CHAQUE message, ETEINT AU MOINDRE DOUTE. Rien n'a ete efface : l'ancienne memoire
    #  reste intacte sur le disque, et chercher_dans_memoire peut toujours y aller.
    try:
        rappel = (rappel_automatique(message_utilisateur, hist, debut, chien)
                  if _rappel_ancien_actif() else "")
    except Exception:
        rappel = ""
"""

fonction = '''def _rappel_ancien_actif():
    """LE RAPPEL AUTOMATIQUE DE L'ANCIENNE MEMOIRE PART-IL ENCORE DEVANT LA PHRASE DE FRED ?

    LE REGLAGE, ET C'EST LE SEUL : "rappel_ancien" dans reglage_memoire_sens.json.
    true  = comportement d'avant : les vieux passages de l'ancienne memoire remontent
            devant la phrase de Fred (choisis par le sens, ou par les mots a defaut).
    false = plus RIEN ne remonte par ce tuyau. C'est le reglage pose le 12/10/2026, sur la
            demande de Fred : "supprime le tuyau qui va a l'ancienne bibliotheque".

    ETEINT AU MOINDRE DOUTE : valeur absente, fichier absent, JSON abime, pepin -- on rend
    False, c'est-a-dire qu'on ne rappelle rien. LU A CHAQUE MESSAGE depuis le disque : il
    n'y a donc AUCUN redemarrage a faire pour l'allumer ou l'eteindre.

    RIEN N'EST PERDU : l'ancienne memoire reste intacte sur le disque, et chercher_dans_memoire
    va toujours y chercher quand c'est utile. On coupe un robinet, on ne jette aucune donnee.
    Ne leve jamais."""
    try:
        with open(FICHIER_REGLAGE_SENS, encoding="utf-8-sig") as f:
            d = json.load(f)
        return bool(d.get("rappel_ancien"))
    except Exception:
        return False


'''

marqueur = "_SENS_DERNIERS_CHOIX = {}   # v129"

for _n in (bloc_avant, bloc_apres, fonction, marqueur):
    pass

rapport = []


def dire(t):
    rapport.append(t)
    print(t)


bloc_avant = bloc_avant.replace("\r\n", "\n")
bloc_apres = bloc_apres.replace("\r\n", "\n")
fonction = fonction.replace("\r\n", "\n")

brut = open(P, "rb").read()
txt = brut.decode("utf-8")

n1 = txt.count(bloc_avant)
n2 = txt.count(marqueur)
n3 = txt.count("def _rappel_ancien_actif")
n4 = txt.count("_rappel_ancien_actif()")

dire("=== CE QUE J'AI TROUVE AVANT DE TOUCHER A QUOI QUE CE SOIT ===")
dire("le bloc du rappel a remplacer ............ %d occurrence(s)  (il en faut 1)" % n1)
dire("le point d'insertion de la fonction ...... %d occurrence(s)  (il en faut 1)" % n2)
dire("la fonction _rappel_ancien_actif existe ?  %d  (il faut 0 : elle est neuve)" % n3)
dire("un appel a _rappel_ancien_actif() ?  ...... %d  (il faut 0)" % n4)
dire("fins de ligne : %s" % ("CRLF" if "\r\n" in txt else "LF"))

if n1 == 1 and n2 == 1 and n3 == 0 and n4 == 0:
    neuf = txt.replace(bloc_avant, bloc_apres, 1)
    neuf = neuf.replace(marqueur, fonction + marqueur, 1)
    dire("")
    dire("=== J'ECRIS ===")
    dire("taille avant ....... %d octets" % len(brut))
    dire("taille apres ....... %d octets" % len(neuf.encode("utf-8")))
    dire("difference ......... %+d octets" % (len(neuf.encode("utf-8")) - len(brut)))
    with open(P, "wb") as f:
        f.write(neuf.encode("utf-8"))
    dire("ECRIT : oui")
else:
    dire("")
    dire("JE N'ECRIS RIEN : le fichier n'est pas dans l'etat attendu.")
    raise SystemExit(1)

dire("")
dire("=== LA COMPILATION (la seule preuve qui compte pour la syntaxe) ===")
try:
    py_compile.compile(P, doraise=True)
    dire("compilation : SANS ERREUR, pas une seule faute de syntaxe")
except Exception as ex:
    dire("compilation : RATE -> %s" % str(ex)[:500])

dire("")
dire("=== RELECTURE DU FICHIER ECRIT ===")
t3 = open(P, "rb").read().decode("utf-8")
dire("l'ancien bloc a disparu ? .......... %s" % ("OUI" if bloc_avant not in t3 else "NON"))
dire("le nouveau bloc est la ? ........... %s" % ("OUI" if bloc_apres in t3 else "NON"))
dire("la fonction est la, une seule fois ? %s" % ("OUI" if t3.count("def _rappel_ancien_actif") == 1 else "NON"))
dire("l'appel est la, une seule fois ? ... %s" % ("OUI" if t3.count("if _rappel_ancien_actif() else") == 1 else "NON"))
dire("fins de ligne apres : %s" % ("CRLF (PROBLEME)" if "\r\n" in t3 else "LF, comme avant"))

dire("")
dire("=== LE REGLAGE : ETEINT PAR DEFAUT ===")
try:
    sauv = os.path.join(D, "SAUVEGARDE_reglage_memoire_sens_AVANT_rappel_ancien_2026-10-12_22h45.json")
    shutil.copy2(RP, sauv)
    dire("sauvegarde du reglage : %s" % os.path.basename(sauv))
    d = json.load(io.open(RP, encoding="utf-8-sig"))
    avant = d.get("rappel_ancien", "(absent)")
    d["rappel_ancien"] = False
    io.open(RP, "w", encoding="utf-8").write(json.dumps(d, ensure_ascii=False, indent=2))
    d2 = json.load(io.open(RP, encoding="utf-8-sig"))
    dire("rappel_ancien : avant = %s / apres = %s" % (avant, d2.get("rappel_ancien")))
    dire("le reste du reglage est intact ? %s (actif = %s, seuil = %s)"
         % ("OUI" if d2.get("actif") is not None and d2.get("seuil") is not None else "A VERIFIER",
            d2.get("actif"), d2.get("seuil")))
except Exception as ex:
    dire("le reglage : RATE -> %s" % str(ex)[:300])

io.open(R, "w", encoding="utf-8").write("\n".join(rapport))
dire("")
dire("rapport ecrit : RESULTAT_correction_rappel_ancien.txt")
