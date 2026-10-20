# -*- coding: utf-8 -*-
# SIMULATION DU RE-TRI DE LA BIBLIOTHEQUE - 06/10/2026
# LECTURE SEULE : on ne deplace RIEN. On regarde seulement ce que le programme
# proposerait de faire, pour que Fred tranche avant qu'on touche a quoi que ce soit.
import os, sys, inspect, json, traceback

DOSSIER = r"C:\Users\Fred\Desktop\Anciennes_versions_Luciana\luciana_v75"
os.chdir(DOSSIER)
sys.path.insert(0, DOSSIER)

print("=== 1) OU EST LE CODE ===")
print("dossier de travail :", DOSSIER)
for nom in ("luciana.py", os.path.join("luciana_v74", "luciana.py")):
    p = os.path.join(DOSSIER, nom)
    if os.path.exists(p):
        print(nom, "->", os.path.getsize(p), "octets")
    else:
        print(nom, "-> ABSENT")

print("")
print("=== 2) IMPORT DU PROGRAMME ===")
L = None
try:
    import luciana as L
    print("import OK, fichier :", getattr(L, "__file__", "?"))
except Exception:
    print("L'IMPORT A ECHOUE :")
    traceback.print_exc()

if L is not None:
    print("")
    print("=== 3) LES FONCTIONS DU RE-TRI PRESENTES DANS LE FICHIER ===")
    for n in sorted(dir(L)):
        low = n.lower()
        if ("retri" in low) or ("biblio" in low) or n in ("_ou_ranger_ce_dossier", "_deplacer_un_dossier"):
            print(" -", n)

    print("")
    print("=== 4) LA FONCTION retrier_la_bibliotheque ===")
    f = getattr(L, "retrier_la_bibliotheque", None)
    if f is None:
        print("ABSENTE du fichier importe.")
    else:
        try:
            print("signature :", inspect.signature(f))
        except Exception as e:
            print("signature illisible :", e)
        try:
            src = inspect.getsource(f)
            lignes = src.splitlines()
            print("taille de la fonction :", len(lignes), "lignes")
            print("---- source (300 premieres lignes) ----")
            print("\n".join(lignes[:300]))
        except Exception as e:
            print("source illisible :", e)

    print("")
    print("=== 5) SIMULATION, LECTURE SEULE (rien ne doit bouger) ===")
    if f is not None:
        res = None
        for essai in ((False, False), (False,), ()):
            try:
                res = f(*essai)
                print("appel", essai, "-> OK")
                break
            except TypeError as e:
                print("appel", essai, "-> mauvais arguments :", e)
            except Exception as e:
                print("appel", essai, "-> ERREUR :", type(e).__name__, e)
                traceback.print_exc()
                break
        print("")
        print("--- RESULTAT ---")
        try:
            if isinstance(res, (dict, list)):
                t = json.dumps(res, ensure_ascii=False, indent=1, default=str)
                print(t[:20000])
                if len(t) > 20000:
                    print("...(tronque, ", len(t), "caracteres au total)")
            else:
                print(repr(res)[:20000])
        except Exception as e:
            print("resultat illisible :", e)

print("")
print("=== FIN ===")
