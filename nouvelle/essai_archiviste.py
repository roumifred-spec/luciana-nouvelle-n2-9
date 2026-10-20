# -*- coding: utf-8 -*-
"""ESSAI DE L'ARCHIVISTE AVEC UN VRAI CERVEAU, SUR DE FAUX SOUVENIRS (piece 2, 20/10/2026).

Pourquoi : sur ce PC seulement on a les vraies cles (DeepSeek, Google). L'archiviste range ici une VIE ENTIERE de
faux souvenirs (une fille de 8 a 18 ans, un chien, un carrossier qui change de methode puis y revient, un
traitement qui change...), dans un dossier A PART : ~/Luciana_neuve_essai_archiviste.
SA VRAIE BIBLIOTHEQUE N'EST PAS TOUCHEE (ni lue, ni ecrite).

A la fin : le plan qu'il a construit (MON PLAN (catalogue).txt dans ce dossier) et les controles du programme.
"""
import os, sys, shutil

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
import luciana_neuve as N
C = N.coeur
K = C.classement
P = C.plan

DOSSIER_ESSAI = os.path.join(os.path.expanduser("~"), "Luciana_neuve_essai_archiviste")

FILLE = [
    "premiere rentree en CE2, elle avait peur de ne pas avoir de copines", "elle s'est fait une amie, Ines, a la cantine",
    "elle a eu 18/20 en dictee et elle etait fiere", "dispute avec la maitresse a cause d'un exercice de maths",
    "elle porte les cheveux longs jusqu'au milieu du dos, elle refuse qu'on les coupe",
    "spectacle de fin d'annee : elle chantait au premier rang", "elle a eu la varicelle, une semaine a la maison",
    "vacances a la mer chez sa grand-mere, elle a appris a nager", "elle veut devenir veterinaire",
    "entree au college, elle prend le bus toute seule", "premiere mauvaise note en anglais, elle a pleure",
    "elle a coupe ses cheveux tres courts, elle se trouve plus libre", "elle est tombee amoureuse d'un garcon de sa classe",
    "conseil de classe : felicitations", "elle a du mal avec une fille qui se moque d'elle au college",
    "elle passe le brevet, mention bien", "elle fait du handball le mercredi", "elle a eu son premier telephone",
    "elle vit chez sa maman la semaine et chez moi un week-end sur deux", "anniversaire de ses 15 ans, on est alles au restaurant",
    "elle prepare le bac de francais", "elle a eu son bac avec mention, elle part a la fac de biologie",
    "elle a perdu sa premiere dent, la petite souris est passee", "elle a lu tout Harry Potter en un mois",
    "elle a fait une crise de colere parce qu'elle voulait un chat", "reunion parents-professeurs : elle bavarde trop",
    "elle a eu une otite, antibiotiques pendant 7 jours", "on a fait un gateau au chocolat ensemble",
    "elle a peur du noir, elle dort avec la lumiere du couloir", "classe verte a la montagne, premiere nuit loin de nous",
    "elle a gagne un concours de dessin a l'ecole", "elle s'est fait une frange elle-meme avec des ciseaux, catastrophe",
    "elle a des lunettes maintenant, elle les a choisies violettes", "premiere boum chez une copine",
    "elle s'est cassee le poignet au handball, platre pendant 5 semaines", "elle a decouvert le piano",
    "elle a teint ses cheveux en bleu pour la fete de fin d'annee", "stage de 3e chez un veterinaire",
    "elle s'est disputee avec Ines, elles ne se parlent plus", "elle s'est reconciliee avec Ines",
    "elle a eu son code de la route du premier coup", "elle veut faire un voyage en Angleterre avec sa classe",
    "elle a passe sa premiere nuit chez son amoureux, j'etais inquiet", "elle a appris a conduire avec moi le dimanche",
    "elle a eu son permis", "elle a pleure en quittant la maison pour la fac",
    "on s'est parle longtemps de son avenir, elle hesite entre veto et biologie", "elle a des maux de tete, rendez-vous chez l'ophtalmo",
    "elle a fait du baby-sitting pour gagner de l'argent", "elle a garde les cheveux courts depuis ses 14 ans",
    "elle m'a appele pour me dire qu'elle avait reussi son premier partiel", "elle est rentree pour Noel, on a decore le sapin",
]
CHIEN = ["on a adopte Rex, un berger de 3 mois", "Rex a mange une chaussure", "Rex chez le veterinaire pour ses vaccins",
         "promenade en foret avec Rex, il a couru apres un chevreuil", "Rex a appris a donner la patte"]
CARROSSIER = [
    ("savoir_faire", "Ma methode de peinture : base eau, 3 couches fines, sechage 20 minutes entre chaque couche"),
    ("souvenir", "J'ai peint une Clio rouge avec la base eau, le client etait content"),
    ("savoir_faire", "Nouvelle methode de peinture : je passe au solvant, 2 couches epaisses, c'est plus rapide"),
    ("souvenir", "Avec le solvant, j'ai eu des coulures sur une Golf, j'ai du reprendre"),
    ("savoir_faire", "Je reviens a l'ancienne methode a la base eau : finalement elle etait meilleure"),
]
TRAITEMENT = [
    ("fait", "Mon traitement : 2 cachets de Levothyrox par jour, le matin a jeun"),
    ("souvenir", "Rendez-vous chez le docteur Martin, prise de sang a faire"),
    ("fait", "Le docteur a change mon traitement : maintenant 3 cachets par jour, matin, midi et soir"),
    ("souvenir", "J'ai oublie mon cachet de midi, j'ai eu des vertiges"),
]
TRAVAIL = ["devis pour un client, reparation d'une portiere", "commande de peinture chez le fournisseur",
           "facture impayee d'un client, relance par mail", "nouvel apprenti a l'atelier, il s'appelle Kevin"]


def faux_souvenirs():
    out = []
    for i, t in enumerate(FILLE):
        an = 2026 + (i * 10) // len(FILLE)
        out.append(("souvenir", "Ma fille (%d ans) : %s" % (8 + an - 2026, t), t, "%d-%02d-12 18:30" % (an, i % 12 + 1)))
    for i, t in enumerate(CHIEN):
        out.append(("souvenir", "Mon chien : " + t, t, "2027-%02d-03 09:15" % (i + 2)))
    for i, (nat, t) in enumerate(CARROSSIER):
        out.append((nat, t[:90], t, "%d-03-10 14:00" % (2026 + i)))
    for i, (nat, t) in enumerate(TRAITEMENT):
        out.append((nat, t[:90], t, "2026-%02d-05 08:00" % (i * 3 + 1)))
    for i, t in enumerate(TRAVAIL):
        out.append(("souvenir", "Atelier : " + t, t, "2026-%02d-20 11:00" % (i + 4)))
    return out


def main():
    print("\n  ESSAI DE L'ARCHIVISTE (vrai cerveau, FAUX souvenirs, dossier a part).")
    print("  Ta vraie bibliotheque n'est pas touchee. Dossier de l'essai : %s\n" % DOSSIER_ESSAI)
    shutil.rmtree(DOSSIER_ESSAI, ignore_errors=True)
    C.poser_le_dossier(DOSSIER_ESSAI)
    for nat, sujet, texte, date in faux_souvenirs():
        C.ecrire_fiche(nat, sujet, texte, date=date, source="essai")
    print("  %d faux souvenirs ecrits. L'archiviste range (quelques minutes, quelques centimes)...\n" % len(C.fiches()))
    while True:
        st = K.ranger_le_neuf(tout=True, lots_max=0, dire=lambda t: print("   ", t))
        for p in st["pannes"]:
            print("  PANNE : %s" % p)
        if not st["reste"] or not st["rangees"]:
            break
    toutes = C.fiches(toutes=True)
    par = {f["sujet"]: f for f in toutes}
    print("\n  CONTROLES DU PROGRAMME :")
    print("   - fiches pas rangees : %d" % len(P.non_rangees(C.fiches())))
    c = P.comptes(toutes)
    print("   - tiroirs : %d ; le plus plein a %d fiche(s) rangee(s) directement dedans"
          % (len(c), max([x["direct"] for x in c.values()] or [0])))
    for cle in ("Le docteur a change mon traitement", "Nouvelle methode de peinture", "Je reviens a l'ancienne methode"):
        f = [x for s, x in par.items() if s.startswith(cle)]
        if f:
            print("   - « %s » : %s ; liens %s ; vital : %s" % (cle, " > ".join(P.chemin_de_la_fiche(f[0]["n"])),
                                                           P.liens_de(f[0]["n"]) or "aucun", P.vital_de(f[0]["n"]) or "?"))
    print("   - grandes categories : %s" % " | ".join(P.charger()["tiroirs"][t]["nom"] for t in P.enfants(None)))
    metier = [x for s, x in par.items() if s.startswith("Atelier :")]
    fille = [x for s, x in par.items() if s.startswith("Ma fille")]
    if metier and fille:
        m0 = (P.chemin_de_la_fiche(metier[0]["n"]) or ["?"])[0]
        f0 = (P.chemin_de_la_fiche(fille[0]["n"]) or ["?"])[0]
        print("   - le metier et la fille dans la meme grande categorie : %s (%s / %s)"
              % ("OUI -> PAS BON" if m0 == f0 else "NON -> JUSTE", m0, f0))
    rev = [x for s, x in par.items() if s.startswith("Je reviens a l'ancienne methode")]
    prem = [x for s, x in par.items() if s.startswith("Ma methode de peinture : base eau")]
    if rev and prem:
        k = P.liens_de(rev[0]["n"]).get("reprend")
        cible = [x for x in toutes if int(x["n"]) == int(k or 0)]
        print("   - le retour a l'ancienne methode REPREND : %s -> %s" % (
            ("n%s « %s »" % (k, cible[0]["sujet"])) if cible else "rien",
            "JUSTE (la premiere methode, base eau)" if (k and int(k) == int(prem[0]["n"])) else "PAS LA BONNE FICHE"))
    anc = [x for s, x in par.items() if s.startswith("Mon traitement : 2 cachets")]
    if anc:
        print("   - l'ancien traitement (2 cachets) : %s" % ("REMPLACE (archive, pas efface)" if anc[0]["etat"] == "remplacee" else "toujours actif"))
    print("\n  LE PLAN QU'IL A CONSTRUIT :\n")
    print(open(P.F_PLAN_LISIBLE, encoding="utf-8").read())
    print("  Envoie-moi le fichier : %s" % P.F_PLAN_LISIBLE)


if __name__ == "__main__":
    main()
