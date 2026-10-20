# -*- coding: utf-8 -*-
"""PATCH DU MOTEUR DE SCORE (point 3) - UNE SEULE CORRECTION, MESUREE AVANT / APRES.

Pose par Luciana avec ses mains, le 11/10/2026, apres le diagnostic de Claude Code.

LA CAUSE TROUVEE (et verifiee dans le code) : poids_texte = 0.9 s'appliquait a TOUTES
les fiches, meme courtes, parce que la protection "etiquette vide" ne se declenchait
jamais (l'etiquette vaut toujours au moins "rayon - tiroir"). Donc la note d'une bonne
fiche valait 0,9 x l'ancienne : -10 % garantis. C'est mecanique, ce n'est pas un reglage.

LA CORRECTION, EN UNE PHRASE : le poids allege ne frappe plus que les textes VRAIMENT
bavards (plusieurs passages de 700 caracteres). Un souvenir qui tient en UN SEUL passage
est court : il compte a plein. Sans etiquette utilisable : plein aussi.

CE QUI EST GARANTI PAR CONSTRUCTION : la nouvelle note est TOUJOURS superieure ou egale a
l'ancienne. Plus aucune fiche ne peut perdre des points en etant mieux rangee.

RIEN D'AUTRE N'EST TOUCHE : ni le curseur (0,35), ni la prime des facettes, ni un seul
autre fichier. Ce script seul, et il refuse d'ecrire si une ancre manque ou est en double.
"""
import io, os, shutil, sys, time

CIBLE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "biblio2_bibliothecaire.py")

if not os.path.isfile(CIBLE):
    print("FICHIER INTROUVABLE : rien n'est ecrit.")
    sys.exit(1)

raw = io.open(CIBLE, encoding="utf-8", newline="").read()
crlf = "\r\n" in raw
S = raw.replace("\r\n", "\n")

paires = []

# --- 1) on RETIENT combien de passages fait le texte (bavard ou pas) -------------
old1 = '''            bouts = _morceaux(brut, maxi, combien)
            debut_etiq = len(a_mesurer)
            if etiq:
                a_mesurer.append(etiq)
            debut_txt = len(a_mesurer)
            a_mesurer.extend(bouts or ([brut] if brut else []))
            plages.append((debut_etiq if etiq else None, debut_txt, len(a_mesurer)))'''
new1 = '''            bouts = _morceaux(brut, maxi, combien)
            bouts_txt = bouts or ([brut] if brut else [])
            debut_etiq = len(a_mesurer)
            if etiq:
                a_mesurer.append(etiq)
            debut_txt = len(a_mesurer)
            a_mesurer.extend(bouts_txt)
            # on retient AUSSI combien de passages fait le texte : c'est ce qui dit
            # s'il est bavard (plusieurs passages) ou court (un seul).
            plages.append((debut_etiq if etiq else None, debut_txt, len(a_mesurer),
                           len(bouts_txt)))'''
paires.append(("bloc 1 / compter les passages", old1, new1))

# --- 2) la boucle de notation lit ce 4e element ---------------------------------
old2 = '''        for (i_etiq, d_txt, f_txt), (cat, sous, fi) in zip(plages, fiches):'''
new2 = '''        for (i_etiq, d_txt, f_txt, n_txt), (cat, sous, fi) in zip(plages, fiches):'''
paires.append(("bloc 2 / la boucle de notation", old2, new2))

# --- 3) LE COEUR : on ne taxe plus les souvenirs COURTS --------------------------
old3 = '''            if s_txt is not None:
                poids = float(r["poids_texte"]) if s_etiq is not None else 1.0
                bouts_notes.append(poids * s_txt)'''
new3 = '''            if s_txt is not None:
                # LE POIDS ALLEGE NE FRAPPE PLUS TOUT LE MONDE. Il etait la pour empecher
                # un long souvenir bavard de gagner parce qu'il est long. Or un souvenir
                # qui tient en UN SEUL passage est court : il n'a rien de bavard, et il
                # payait quand meme la taxe. Mesure de Fred : le meilleur candidat tombait
                # a 0,492 au lieu de passer la barre.
                # Maintenant : un seul passage = plein pot ; plusieurs passages = allege ;
                # et sans etiquette utilisable = plein pot. Donc plus jamais de perte.
                if s_etiq is None or n_txt <= 1:
                    poids = 1.0
                else:
                    poids = float(r["poids_texte"])
                bouts_notes.append(poids * s_txt)'''
paires.append(("bloc 3 / le coeur du calcul", old3, new3))

# --- controle des ancres AVANT d'ecrire quoi que ce soit ------------------------
tout_bon = True
for nom, o, _n in paires:
    c = S.count(o)
    print("%-34s : %d occurrence(s)" % (nom, c))
    if c != 1:
        tout_bon = False
if not tout_bon:
    print("")
    print("ANCRE INTROUVABLE OU EN DOUBLE : RIEN N'A ETE ECRIT. Le fichier est intact.")
    sys.exit(1)

# --- sauvegarde datée, puis UNE seule ecriture ----------------------------------
quand = time.strftime("%Y-%m-%d_%Hh%M")
sauv = CIBLE + ".AVANT_patch_score_" + quand + ".py"
shutil.copy2(CIBLE, sauv)
print("")
print("sauvegarde datee : %s" % os.path.basename(sauv))

for _nom, o, n in paires:
    S = S.replace(o, n, 1)

sortie = S.replace("\n", "\r\n") if crlf else S
io.open(CIBLE, "w", encoding="utf-8", newline="").write(sortie)
print("ECRIT : les 3 blocs du moteur de score sont poses.")
print("RIEN D'AUTRE N'A ETE TOUCHE.")
