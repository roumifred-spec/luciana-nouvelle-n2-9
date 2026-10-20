# -*- coding: utf-8 -*-
"""ESSAI DE « COMPRENDRE LA SITUATION » AVEC UN VRAI CERVEAU (piece 4, 20/10/2026).

Onze situations (une petite conversation + la phrase de Fred), avec ce qu'on attend : de quoi il parle (la phrase de sens
doit contenir certains mots), quand, les dates (calculees par le programme), le vital, et si c'est trop flou.
Rien n'est ecrit nulle part : sa vraie bibliotheque n'est ni lue ni touchee. Quelques appels courts : presque rien.
"""
import os, sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
import luciana_neuve as N
C = N.coeur
K = C.comprendre

QUAND = "2026-10-20 18:00"
# (conversation, phrase de Fred, attendu)
#   attendu : mots = tous dans « de quoi » (sans accents), quand = un des choix, du/au, vital, flou (True = une question attendue)
CAS = [
    ("Fred : quand ma fille avait 8 ans, elle avait les cheveux tres longs.\nLuciana : Oui, tu me l'avais raconte.",
     "Et maintenant, elle les a comment ?", {"mots": ["fille", "cheveux"], "quand": ["maintenant", "recent"], "vital": False, "flou": False}),
    ("", "Est-ce que j'ai pris mon cachet ce matin ?",
     {"mots": ["cachet"], "quand": ["moment", "maintenant"], "du": "2026-10-20", "vital": True, "flou": False}),
    ("", "Qu'est-ce qu'on a fait hier sur le trading ?",
     {"mots": ["trading"], "quand": ["moment"], "du": "2026-10-19", "vital": False, "flou": False}),
    ("Fred : hier tu as pris huit positions sur TradingView.\nLuciana : Oui, sur le compte demo.",
     "Elles en sont ou, les positions ?", {"mots": ["position"], "quand": ["maintenant", "recent"], "vital": False, "flou": False}),
    ("", "Raconte-moi toute la vie de ma fille", {"mots": ["fille"], "quand": ["histoire"], "vital": False}),
    ("Fred : je sors de chez le docteur Martin, il m'a change mon traitement.\nLuciana : D'accord, je le note.",
     "Et lui, il pense que c'est grave ?", {"mots_un_de": ["martin", "docteur", "medecin"], "vital": True, "flou": False}),
    ("", "Le 2 octobre, on avait parle de quoi ?", {"quand": ["moment"], "du": "2026-10-02", "flou": False}),
    ("", "Et ca ?", {"flou": True}),
    ("", "Ce am facut ieri cu Luminita?", {"mots": ["luminita"], "du": "2026-10-19", "vital": False}),
    ("", "Bonjour Luciana !", {"quand": ["maintenant"], "vital": False, "flou": False}),
    ("", "Comment ca a evolue avec Satisfaire depuis septembre ?", {"mots": ["satisfaire"], "quand": ["histoire"], "du_commence": "2026-09"}),
]


def verifier(r, a):
    pb = []
    dq = C.sans_accents(r["de_quoi"])
    for m in a.get("mots", []):
        if m not in dq:
            pb.append("« de quoi » sans « %s »" % m)
    if a.get("mots_un_de") and not any(m in dq for m in a["mots_un_de"]):
        pb.append("« de quoi » sans %s" % " / ".join(a["mots_un_de"]))
    if "quand" in a and r["quand"] not in a["quand"]:
        pb.append("quand = %s (attendu %s)" % (r["quand"], " ou ".join(a["quand"])))
    if "du" in a and r["du"] != a["du"]:
        pb.append("du = %s (attendu %s)" % (r["du"] or "rien", a["du"]))
    if "du_commence" in a and not r["du"].startswith(a["du_commence"]):
        pb.append("du = %s (attendu en %s)" % (r["du"] or "rien", a["du_commence"]))
    if "vital" in a and bool(r["vital"]) != a["vital"]:
        pb.append("vital = %s (attendu %s)" % (r["vital"], a["vital"]))
    if "flou" in a and bool(r["flou"]) != a["flou"]:
        pb.append("flou = %s (attendu %s)" % ("question" if r["flou"] else "non", "question" if a["flou"] else "non"))
    if r.get("panne"):
        pb.append("PANNE : %s" % r["panne"])
    return pb


def main():
    print("\n  ESSAI DE « COMPRENDRE LA SITUATION » (vrai cerveau ; rien n'est ecrit, sa bibliotheque n'est pas touchee).\n")
    justes = 0
    for conv, msg, a in CAS:
        r = K.comprendre(msg, conv, QUAND)
        pb = verifier(r, a)
        justes += 0 if pb else 1
        print("  « %s »" % msg)
        print("     compris : %s" % K.en_clair(r))
        print("     -> %s" % ("JUSTE" if not pb else "PAS BON : " + " ; ".join(pb)))
    print("\n  RESULTAT : %d juste(s) sur %d." % (justes, len(CAS)))


if __name__ == "__main__":
    main()
