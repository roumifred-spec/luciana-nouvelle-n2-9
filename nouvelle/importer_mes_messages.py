# -*- coding: utf-8 -*-
"""LA MEMOIRE DE DEPART DE LA NOUVELLE LUCIANA (decision du 19/10/2026) :
SEULEMENT CE QUE LE PROPRIETAIRE A DIT. Tous ses messages, en entier, jusqu'a aujourd'hui. RIEN de ce qu'elle a
ecrit (ses reponses, notes, souvenirs, consignes, recettes : « il y a des choses fausses dedans »).

1) D'abord un ESSAI : le programme lit ~/Luciana/luciana_memoire.json (sans y toucher), compte tes
   messages, en montre des exemples, et ecrit la liste COMPLETE dans un fichier que tu peux lire.
2) Seulement si tu tapes OUI : l'archiviste les range par le sens dans la bibliotheque (mot pour mot),
   et releve ce qu'ils lui apprennent (regles, faits, personnes...), tires de TES mots seulement.
   S'il s'arrete (panne, internet), il reprend ou il en etait au prochain lancement.
L'ancienne memoire n'est ni modifiee ni effacee.
"""
import os, sys, json, time

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
import luciana_neuve as N     # charge l'ancien programme (cles, cerveaux) et le coeur
C = N.coeur

SOURCE = os.path.join(os.path.expanduser("~"), "Luciana", "luciana_memoire.json")
F_LISTE = os.path.join(C.DOSSIER, "IMPORT - mes messages trouves.txt")
F_MARQUE = os.path.join(C.DOSSIER, "import_marque_page.json")


def mes_messages():
    """Les messages du proprietaire : role 'user', du texte, pas un message du programme (commence par '[').
    Le meme message repete MOT POUR MOT n'est garde qu'une fois (la premiere)."""
    brut = C.lire_json(SOURCE, [])
    vus, out, ignores = set(), [], {"programme": 0, "vides": 0, "doublons_exacts": 0, "pas_du_texte": 0}
    for m in brut if isinstance(brut, list) else []:
        if not isinstance(m, dict) or m.get("role") != "user":
            continue
        t = m.get("content")
        if not isinstance(t, str):
            ignores["pas_du_texte"] += 1
            continue
        t = t.strip()
        if not t:
            ignores["vides"] += 1
            continue
        if t.startswith("["):
            ignores["programme"] += 1
            continue
        if t in vus:
            ignores["doublons_exacts"] += 1
            continue
        vus.add(t)
        out.append({"n": len(out) + 1, "role": "user", "date": str(m.get("date") or ""), "texte": t})
    return out, ignores, len(brut) if isinstance(brut, list) else 0


def poser_le_proprietaire():
    """CES MESSAGES SONT CEUX D'UNE SEULE PERSONNE : celle a qui est cette memoire. L'import la fait entrer au
    registre des personnes (p1 sur une machine neuve), avec le role « proprietaire » et « dit (import) » :
    ses propres mots la nomment, et on dit d'ou ca vient. Rien n'est suppose : si le nom n'est pas encore
    ecrit dans le reglage, on le DEMANDE, puis on l'ecrit UNE FOIS (une mise a jour ne l'ecrasera jamais)."""
    nom = str(C.reglages().get("proprietaire") or "").strip()
    if not nom:
        print("\n  Le nom du proprietaire n'est pas encore ecrit dans nouvelle/reglages.json.")
        nom = input("  A qui est cette memoire ? (le prenom, tel qu'elle doit l'appeler) : ").strip()
        ecrit, nom = C.poser_le_proprietaire(nom)
        if ecrit:
            print("  Ecrit une fois dans nouvelle/reglages.json : « %s ». Une mise a jour ne l'ecrasera pas." % nom)
    if not nom:
        print("  Aucun nom donne : personne n'entre au registre. Tu pourras le faire plus tard.")
        return ""
    pid, ce_qui = C.personnes.poser_le_proprietaire(nom, "dit (import)", date=C.maintenant())
    print("  Registre des personnes : %s = « %s », role proprietaire (%s)." % (pid or "rien", nom, ce_qui))
    return pid


def main():
    print("\n  LA MEMOIRE DE DEPART DE LA NOUVELLE LUCIANA : seulement tes messages a toi.\n")
    if not os.path.exists(SOURCE):
        print("  Je ne trouve pas %s : rien a importer." % SOURCE)
        return
    msgs, ignores, total = mes_messages()
    car = sum(len(m["texte"]) for m in msgs)
    dates = sorted(m["date"] for m in msgs if m["date"])
    print("  Ancienne memoire lue (sans y toucher) : %d messages en tout (les tiens + les siens)." % total)
    print("  TES messages retenus : %d (%d caracteres), du %s au %s." % (len(msgs), car, (dates or ["?"])[0][:10],
                                                                        (dates or ["?"])[-1][:10]))
    print("  Laisses de cote : %d messages du programme, %d vides, %d repetes mot pour mot (gardes une fois), %d sans texte."
          % (ignores["programme"], ignores["vides"], ignores["doublons_exacts"], ignores["pas_du_texte"]))
    with open(F_LISTE, "w", encoding="utf-8") as f:
        for m in msgs:
            f.write("[%s] %s\n\n" % (m["date"], m["texte"]))
    print("  La liste COMPLETE est ici, tu peux la lire : %s\n" % F_LISTE)
    for m in msgs[:3] + msgs[len(msgs) // 2:len(msgs) // 2 + 2] + msgs[-3:]:
        print("   - [%s] %s" % (m["date"], m["texte"][:150].replace("\n", " ")))
    millions = car / 3.5 / 1e6          # ~3,5 caracteres par jeton ; le texte part UNE fois a l'archiviste
    print("\n  Cout estime (DeepSeek, archiviste) : environ %.2f $ (estimation), plus le calcul du sens chez Google."
          % (millions * (0.30 * 1.3 + 1.20 * 0.15)))
    if input("\n  Tape OUI (en majuscules) pour les ranger dans sa bibliotheque : ").strip() != "OUI":
        print("  Rien n'a ete fait.")
        return
    poser_le_proprietaire()
    deja = int(C.lire_json(F_MARQUE, {}).get("fait_jusqu_a", 0))
    reste = [m for m in msgs if m["n"] > deja]
    paquets = C.decouper(reste, 20000)
    print("\n  %d message(s) a ranger, en %d paquet(s)%s." % (len(reste), len(paquets),
                                                           (" (reprise apres le n%d)" % deja) if deja else ""))
    avant = [m for m in msgs if m["n"] <= deja][-2:]
    souvenirs = 0
    for i, p in enumerate(paquets, 1):
        ok, nb = C.ranger_un_paquet(p, avant, avec_lecons=True)
        if not ok:
            print("  PANNE de l'archiviste au paquet %d : je m'arrete. Relance plus tard, je reprendrai ici." % i)
            break
        souvenirs += nb
        C.ecrire_json(F_MARQUE, {"fait_jusqu_a": p[-1]["n"], "le": C.maintenant()})
        avant = p[-2:]
        print("  paquet %d/%d range (%d souvenir(s))" % (i, len(paquets), nb))
    lecons = len([f for f in C.fiches() if f.get("nature") != "souvenir"])
    print("\n  Calcul du sens des fiches chez Google (une seule fois)...")
    C.MOTEUR.indexer(C.fiches())
    C.ecrire_lisible()
    print("  FINI : %d souvenir(s) crees ; la bibliotheque compte %d fiche(s), dont %d lecon(s) tirees de tes mots."
          % (souvenirs, len(C.fiches()), lecons))
    print("  Moteur de sens : %s" % ("OK" if not C.MOTEUR.panne else "EN PANNE (%s) : relance plus tard" % C.MOTEUR.panne))
    print("  Tu peux tout lire ici : %s" % C.F_LISIBLE)


if __name__ == "__main__":
    main()
