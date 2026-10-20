# -*- coding: utf-8 -*-
"""ETAPE 0 DU CHANTIER "PERSONNAGE ANIME" : REMETTRE LA BONNE BASE DE TRAVAIL.

POURQUOI. Le luciana.py du depot est la version WHISPER (dictee locale), que Fred a DECIDE
D'ABANDONNER : trop lente sur son PC. Le fichier qui TOURNE chez lui est revenu en v100, la
version JUSTE AVANT Whisper. Si on partait du fichier du depot, on ramenerait Whisper chez
Fred. C'est interdit.

CE QUE FAIT CE SCRIPT, ET RIEN D'AUTRE :
  1. il copie la v100 qui tourne chez Fred
         C:\\Users\\Fred\\Desktop\\luciana_v96\\luciana_v96\\luciana_v100_avant_whisper_2026-10-04.py
     a la racine du chantier, sous le nom de sauvegarde
         SAUVEGARDE_luciana_v100_avant_personnage_2026-10-04.py
     (regle de Fred : une copie nommee et datee AVANT de toucher au fichier) ;
  2. il copie cette meme v100 par-dessus luciana.py : c'est la base du chantier ;
  3. il CONTROLE le resultat : octet pour octet identique a la v100, le badge dit bien v100,
     aucune trace de la dictee Whisper (faster_whisper, menu Dictee, ligne d'etat), et le
     fichier compile.

Il n'ecrase pas la sauvegarde si elle existe deja. Il ne touche a rien d'autre.

POUR LE LANCER (dans ce dossier) :  python _poser_la_base_v100.py
"""
import hashlib
import os
import py_compile
import shutil
import sys

ICI = os.path.dirname(os.path.abspath(__file__))

# Le fichier qui TOURNE chez Fred (sa copie nommee, identique a son luciana.py : c'est son
# propre script retour_v100.bat qui l'a remise en place, voir resultat_retour_v100.txt).
SOURCE_V100 = os.path.join("C:\\", "Users", "Fred", "Desktop", "luciana_v96", "luciana_v96",
                           "luciana_v100_avant_whisper_2026-10-04.py")
EN_SERVICE = os.path.join("C:\\", "Users", "Fred", "Desktop", "luciana_v96", "luciana_v96",
                          "luciana.py")

SAUVEGARDE = os.path.join(ICI, "SAUVEGARDE_luciana_v100_avant_personnage_2026-10-04.py")
CIBLE = os.path.join(ICI, "luciana.py")


def sha(chemin):
    h = hashlib.sha256()
    with open(chemin, "rb") as f:
        for bloc in iter(lambda: f.read(1 << 20), b""):
            h.update(bloc)
    return h.hexdigest()


def main():
    print("=== 1) LA SOURCE ===")
    # D'abord la v100 qui tourne chez Fred. Si on n'est pas sur son PC (ou si le dossier a
    # bouge), on se rabat sur la sauvegarde deja deposee ici : apres le premier passage, ce
    # script marche donc n'importe ou, sans aucun chemin a retaper.
    if os.path.isfile(SOURCE_V100):
        source = SOURCE_V100
    elif os.path.isfile(SAUVEGARDE):
        source = SAUVEGARDE
        print("    (la v100 du PC de Fred n'est pas accessible d'ici : je prends la sauvegarde")
        print("     deja deposee a la racine, qui en est la copie exacte)")
    else:
        print("ECHEC : je ne trouve la v100 ni ici ni la :")
        print("    %s" % SOURCE_V100)
        print("    %s" % SAUVEGARDE)
        print("Rien n'a ete touche.")
        return 1

    print("    %s" % source)
    print("    %d octets, sha256 %s" % (os.path.getsize(source), sha(source)[:16]))
    if os.path.isfile(EN_SERVICE):
        meme = sha(EN_SERVICE) == sha(source)
        print("    le luciana.py EN SERVICE chez Fred est %s a cette v100"
              % ("IDENTIQUE" if meme else "DIFFERENT (!)"))
        if not meme:
            print("    ARRET : je ne pars pas d'une base dont je ne suis pas sur.")
            return 1

    print("\n=== 2) LA SAUVEGARDE (copie nommee et datee) ===")
    if os.path.exists(SAUVEGARDE):
        print("    elle existe deja, je n'y touche pas : %s" % os.path.basename(SAUVEGARDE))
    else:
        shutil.copyfile(source, SAUVEGARDE)
        print("    ecrite : %s (%d octets)" % (os.path.basename(SAUVEGARDE),
                                               os.path.getsize(SAUVEGARDE)))

    print("\n=== 3) LA BASE DE TRAVAIL ===")
    if os.path.isfile(CIBLE):
        print("    l'ancien luciana.py du depot (version Whisper) faisait %d octets ;"
              % os.path.getsize(CIBLE))
        print("    il reste dans l'historique git, c'est voulu.")
    shutil.copyfile(source, CIBLE)
    print("    luciana.py <- la v100 (%d octets)" % os.path.getsize(CIBLE))

    print("\n=== 4) CONTROLES ===")
    ok = True

    if sha(CIBLE) == sha(source):
        print("    [OK] luciana.py est octet pour octet la v100")
    else:
        print("    [RATE] luciana.py n'est pas identique a la v100"); ok = False

    texte = open(CIBLE, "r", encoding="utf-8", errors="replace").read()

    # La dictee Whisper (v101 a v104) ne doit PAS etre revenue.
    # RESERVE HONNETE : on ne cherche PAS "faster_whisper" ni "WhisperModel". Ces deux-la
    # existent AUSSI, et depuis bien avant la v101, dans la TRANSCRIPTION DE VIDEOS, qui est
    # une fonction a part et qui marche. Ce qu'on traque ici, c'est la DICTEE locale.
    interdits = ["etatDictee", "moteurDictee", "dicteeLocale", "wBasculerSurChrome",
                 '<option value="whisper">', '<option value="whisper_auto">']
    revenus = [m for m in interdits if m in texte]
    if revenus:
        print("    [RATE] traces de la dictee Whisper : %s" % ", ".join(revenus)); ok = False
    else:
        print("    [OK] aucune trace de la dictee locale Whisper (v101-v104)")

    nb_whisper = texte.lower().count("whisper")
    print("    (information : le mot 'whisper' apparait %d fois, uniquement dans la"
          % nb_whisper)
    print("     TRANSCRIPTION DE VIDEOS, qui existait bien avant et qui marche)")

    if "&middot; v100" in texte:
        print("    [OK] le badge de la page dit bien v100")
    else:
        print("    [RATE] le badge ne dit pas v100"); ok = False

    try:
        py_compile.compile(CIBLE, doraise=True)
        print("    [OK] le fichier compile")
    except Exception as ex:
        print("    [RATE] il ne compile pas : %s" % str(ex)[:300]); ok = False

    print("\n%s" % ("TOUT EST BON : la base est la v100." if ok else "IL Y A UN PROBLEME."))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
