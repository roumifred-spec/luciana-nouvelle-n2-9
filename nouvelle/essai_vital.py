# -*- coding: utf-8 -*-
"""ESSAI DU JOURNAL DU QUOTIDIEN AVEC UN VRAI CERVEAU, SUR DE FAUX MESSAGES (piece 3, 20/10/2026).

Treize faux messages d'une journee (dont roumain et anglais), dont des pieges : un geste PREVU, une QUESTION, une chose
pas vitale. Un geste OUBLIE (« j'ai oublie mon cachet ») est note « PAS FAIT », sans heure inventee (decision de Fred, 20/10).
L'archiviste juge ; le programme ecrit l'heure exacte. A la fin : SA VRAIE PHRASE (« la recette, pas le plat » : on voit
ce qu'elle dirait vraiment, avec sa personnalite). Tout se passe dans un
dossier A PART (~/Luciana_neuve_essai_vital) : SA VRAIE BIBLIOTHEQUE ET SON VRAI JOURNAL NE SONT PAS TOUCHES.
"""
import os, sys, shutil, re

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
import luciana_neuve as N
C = N.coeur
Q = C.quotidien

DOSSIER_ESSAI = os.path.join(os.path.expanduser("~"), "Luciana_neuve_essai_vital")

# (message, ecrit le, ce qu'on attend : "note HH:MM le AAAA-MM-JJ" ou "rien")
MESSAGES = [
    ("Bonjour Luciana, j'ai pris mon Levothyrox ce matin", "2026-10-20 08:12", ("2026-10-20", "08:12")),
    ("Je vais prendre mon cachet de midi apres manger", "2026-10-20 11:50", None),
    ("Mince, hier soir j'ai oublie mon cachet", "2026-10-20 12:00", ("2026-10-19", "", "pas fait")),
    ("Je sors de chez le docteur Martin, la prise de sang est faite", "2026-10-20 15:30", ("2026-10-20", "15:30")),
    ("Ma fille a eu 18 en dictee !", "2026-10-20 16:00", None),
    ("Hier soir j'ai bien ferme le gaz avant de partir, j'ai verifie a 22h", "2026-10-20 16:10", ("2026-10-19", "22:00")),
    ("Tension prise a l'instant : 13/8", "2026-10-20 18:00", ("2026-10-20", "18:00")),
    ("Est-ce que j'ai pris mon cachet ce matin ?", "2026-10-20 18:05", None),
    ("J'ai pris mon cachet du soir vers 20h", "2026-10-20 21:15", ("2026-10-20", "20:00")),
    # D'AUTRES LANGUES (Luminita, les clientes) : roumain, anglais.
    ("Ieri seara am luat pastila la ora 22", "2026-10-20 21:25", ("2026-10-19", "22:00")),
    ("Am uitat sa iau pastila de dimineata", "2026-10-20 21:30", ("2026-10-20", "", "pas fait")),
    ("I took my blood pressure pill at 7 am", "2026-10-20 21:35", ("2026-10-20", "07:00")),
    # UNE AUTRE PERSONNE parle a Luciana : le journal doit noter QUI a dit quoi.
    ("Bonjour, c'est la fille de Madame Dupont : ma mere m'a dit qu'elle a pris son cachet a 8h", "2026-10-20 21:40",
     ("2026-10-20", "08:00", "qui")),
]


def main():
    print("\n  ESSAI DU JOURNAL DU QUOTIDIEN (vrai cerveau, FAUX messages, dossier a part).")
    print("  Sa vraie bibliotheque et son vrai journal ne sont pas touches. Dossier : %s\n" % DOSSIER_ESSAI)
    shutil.rmtree(DOSSIER_ESSAI, ignore_errors=True)
    C.poser_le_dossier(DOSSIER_ESSAI)
    justes = 0
    for msg, quand, attendu in MESSAGES:
        notes = Q.noter_le_vital(msg, quand)
        if attendu is None:
            ok = not notes
            vu = "rien" if not notes else "NOTE : " + " ; ".join("%s %s %s" % (e["jour"], e["heure"] or "(heure pas dite)", e["quoi"]) for e in notes)
        else:
            ok = any(e["jour"] == attendu[0] and e["heure"] == attendu[1] and ("qui" not in attendu or e.get("qui"))
                     and ((e.get("etat") == "pas fait") == ("pas fait" in attendu)) for e in notes)
            vu = ("NOTE : " + " ; ".join("%s %s %s%s%s" % (e["jour"], e["heure"] or "(heure pas dite)",
                                                       "PAS FAIT : " if e.get("etat") == "pas fait" else "", e["quoi"],
                                                       (" (qui : %s)" % e["qui"]) if e.get("qui") else "") for e in notes)) if notes else "rien"
        inventee = [e for e in notes if e["jour"] != quand[:10] and e["heure"] == quand[11:16]]
        if inventee:
            ok = False          # l'heure du message collee sur un autre jour = une heure inventee
        justes += 1 if ok else 0
        print("  [%s] « %s »" % (quand[11:16], msg))
        print("        -> %s   %s" % (vu, "JUSTE" if ok else ("PAS BON (heure inventee)" if inventee else
                                                    "PAS BON (attendu : %s)" % ("rien" if attendu is None else
                                                    "%s %s%s" % (attendu[0], attendu[1] or "(heure pas dite)",
                                                                 "".join(" + " + x for x in attendu[2:]))))))
    print("\n  RESULTAT : %d juste(s) sur %d.\n" % (justes, len(MESSAGES)))
    # Un geste fait par Luciana ELLE-MEME (ici ecrit pour l'essai, dans le dossier de l'essai : marque ESSAI).
    os.makedirs(C.D_JOURNAL, exist_ok=True)
    C.ajouter_ligne(os.path.join(C.D_JOURNAL, "2026-10-20.jsonl"),
                    {"heure": "14:02:00", "outil": "envoyer_mail", "entree": {"a": "henri@exemple.fr"},
                     "resultat": "Mail envoye a henri@exemple.fr : facture n 12 (ESSAI)"})
    print("  CE QU'ELLE LIRAIT pour « est-ce que j'ai pris mon cachet ce matin ? » (le 20/10/2026) :\n")
    print(Q.lire("2026-10-20", "cachet ce matin"))
    print("\n  ET POUR UN JOUR SANS RIEN (le 21/10/2026) :\n")
    print(Q.lire("2026-10-21", "cachet"))
    print("\n  Le journal lisible : %s" % Q._f_lisible())
    sa_vraie_phrase()


# « LA RECETTE, PAS LE PLAT » (decision de Fred, 20/10) : ce qu'elle DIT vraiment, avec sa personnalite, son vrai cerveau,
# et exactement ce que le programme lui donne (pour une question sur la personne : seulement ce que la personne a dit
# avoir fait ou pas fait ; pour une question sur ses gestes a elle : son outil, qui montre tout).
QUESTIONS = [
    ("Fred", "2026-10-20 18:05", "Est-ce que j'ai pris mon cachet ce matin ?", "personne"),
    ("la fille de Madame Dupont", "2026-10-20 21:45",
     "Bonsoir, c'est la fille de Madame Dupont. Est-ce que maman a bien pris son cachet aujourd'hui ?", "personne"),
    ("Fred", "2026-10-20 21:50", "Est-ce que tu as envoye la facture a Monsieur Henri ?", "ses gestes"),
]


def sa_vraie_phrase():
    print("\n  SA VRAIE PHRASE (vrai cerveau, sa personnalite, ce que le programme lui donne vraiment) :")
    cerveau = C.L.lire_cerveau()
    systeme = C.personnalite() + "\n\n" + C.MEMOIRE_EN_CLAIR
    for qui, quand, question, sorte in QUESTIONS:
        if sorte == "personne":
            donne = Q.lire(quand[:10], avec_mes_gestes=False, dit_avant=quand)
        else:
            donne = "[Resultat de ton outil journal_du_quotidien]\n" + Q.lire(quand[:10], "facture Henri", dit_avant=quand)
        contenu = ("[Repere temporel, ecrit par le programme : nous sommes le %s, il est %s.]\n\n%s\n\n%s [%s] : %s"
                   % (Q._fr(quand[:10]), quand[11:16], donne, "Fred" if qui == "Fred" else "Message (" + qui + ")",
                      quand[11:16], question))
        texte, panne = C.appel_simple(cerveau, systeme, contenu, "essai_sa_vraie_phrase", reflechir=True,
                                      max_tokens=4000, timeout=180)
        t = (texte or "").strip()
        if "invoke name=" in t or "DSML" in t:
            # Dans cet essai, ses outils ne sont pas branches : elle a ecrit son geste en texte. On le dit, et on lui
            # redemande de repondre avec ce qu'elle a.
            m = re.search(r'invoke name="([^"]+)"', t)
            print("\n  « %s »  (%s, %s)" % (question, qui, quand[11:16]))
            print("     (elle a d'abord voulu utiliser son outil %s ; dans l'essai ses outils ne sont pas branches)"
                  % (m.group(1) if m else "?"))
            texte, panne = C.appel_simple(cerveau, systeme, contenu + "\n\n[Le programme : dans cet essai tes outils "
                                          "ne sont pas branches ; reponds avec ce que tu as ci-dessus.]",
                                          "essai_sa_vraie_phrase", reflechir=True, max_tokens=4000, timeout=180)
            print("     ELLE : %s" % ((texte or "").strip() or ("(PANNE : %s)" % panne)))
            continue
        print("\n  « %s »  (%s, %s)" % (question, qui, quand[11:16]))
        print("     ELLE : %s" % ((texte or "").strip() or ("(PANNE : %s)" % panne)))


if __name__ == "__main__":
    main()
