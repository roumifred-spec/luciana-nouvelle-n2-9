# -*- coding: utf-8 -*-
"""COMPRENDRE LA SITUATION AVANT DE CHERCHER -- piece 4 de la bibliotheque rangee (decidee avec Fred le 20/10/2026).

Avant chaque recherche, cette etape lit TOUTE la conversation (les 50 000 a 80 000 caracteres, comme elle et comme le
bibliothecaire : ca ne change pas) + le nouveau message, et dit, comme une personne qui ecoute :
  - QUI PARLE et DE QUI ON PARLE (etape b, 20/10/2026) : elle lit le registre des personnes (personnes.py) et deduit ;
    elle ne suppose personne. Le PROGRAMME tranche ensuite (personnes.attribuer) ;
  - DE QUOI il parle : une phrase de sens qui se comprend toute seule (« elle » devient « sa fille », « lui » devient
    « le docteur Martin ») -> c'est CETTE phrase qui est donnee au moteur Google, au lieu de coller ses deux messages
    d'avant a sa phrase (cause verifiee le 20/10 : bibliotheque + Satisfaire + trading melanges en une seule recherche) ;
  - QUAND : maintenant, le plus recent, un moment precis, ou toute l'histoire ; les dates (« hier », « le 2 octobre »)
    sont CALCULEES PAR LE PROGRAMME, jamais par l'IA ;
  - si ca touche au VITAL (alors le journal du quotidien de ces jours-la est lu par le programme) ;
  - si la question est vraiment trop FLOUE (alors UNE seule question courte, a poser seulement si elle ne trouve pas).

CE QU'ELLE NE FAIT JAMAIS : decider « pas besoin de chercher ». C'est exactement le bug de la V188 (l'etape « comprendre »
disait « rien ne manque » sans regarder, et Luciana avait oublie que WhatsApp etait installe). Ici elle PREPARE la
recherche ; la recherche a TOUJOURS lieu. En panne, on cherche avec le message tel quel (et on le dit).
"""
import datetime


def C():
    import coeur
    return coeur


QUANDS = ("maintenant", "recent", "moment", "histoire")


def comprendre(message, bloc, date_message=None):
    """Rend {"de_quoi", "quand", "du", "au", "dates_incertaines", "vital", "flou", "panne",
    "qui_parle", "de_qui", "question_qui"}. Ne leve jamais. Qui parle n'est ici qu'une DEDUCTION : c'est
    personnes.attribuer() qui tranche et l'ecrit."""
    co = C()
    import quotidien as Q
    import personnes as PE
    msg = str(message or "").strip()
    date_message = co._date_propre(date_message) or co.maintenant()
    rendu = {"de_quoi": msg, "quand": "maintenant", "du": "", "au": "", "dates_incertaines": [], "vital": False,
             "flou": "", "panne": "", "qui_parle": {"comment": "inconnu"}, "de_qui": [], "question_qui": ""}
    if not msg:
        return rendu
    registre, suite = PE.pour_comprendre(date_message)
    contenu = (
        (("LA CONVERSATION EN COURS, mot pour mot (la meme que l'assistante a sous les yeux) :\n----- DEBUT -----\n" +
          bloc + "\n----- FIN -----\n\n") if str(bloc or "").strip() else "") +
        "LE NOUVEAU MESSAGE (ecrit le %s) : %s\n\n" % (date_message, msg) +
        "LE REGISTRE DES PERSONNES CONNUES (tenu par le programme) :\n%s\n%s\n\n" % (registre, suite) +
        "TON TRAVAIL : tu ecoutes comme une personne attentive. Le programme NE SAIT PAS qui ecrit : ne suppose personne "
        "(ni le proprietaire, ni la personne d'avant, ni l'assistante). Tu dis QUI PARLE, DE QUI on parle, et CE QUE LA "
        "PERSONNE VEUT DIRE MAINTENANT, pour qu'on aille chercher dans la memoire ce qui repond a CETTE situation. Tu ne "
        "reponds pas au message ; tu ne decides pas s'il faut chercher (on cherche toujours).\n"
        "- \"qui_parle\" : {\"numero\": \"<le pN du registre si c'est cette personne, sinon vide>\", \"nouveau\": "
        "\"<si c'est quelqu'un qui n'est pas au registre et que le message nomme ou designe (« c'est Marie », « je suis "
        "l'infirmiere du matin ») : ce nom, tel qu'il est dit ; sinon vide>\", \"comment\": \"dit|deduit|suite|inconnu\", "
        "\"raison\": \"<en une phrase : ce qui le montre>\", \"distingue\": \"<SEULEMENT si plusieurs personnes du "
        "registre portent ce nom : ce qui, dans le message ou la conversation, montre que c'est celle-la et pas "
        "l'autre (ex. « elle dit : Marie, la voisine ») ; sinon vide. Le nom seul ne distingue rien.>\"}. dit = le message le dit lui-meme (un prenom, « c'est moi », "
        "« je suis... », une signature) ; deduit = tu le comprends par le sens sans que ce soit dit ; suite = rien ne "
        "montre un changement, c'est la meme personne qu'au message d'avant (seulement si le registre ci-dessus le "
        "permet) ; inconnu = rien ne permet de le savoir : NE DEVINE PAS. Au moindre signe de changement (un prenom, "
        "« je suis sa fille », une signature, une piece jointe, la personne d'avant dont on parle maintenant a la "
        "3e personne) : tu re-deduis, jamais « suite ». « dit » est une parole, pas une preuve.\n"
        "- \"de_qui\" : les PERSONNES dont parle le message (pas les choses), ou [] : [{\"numero\": \"<pN ou vide>\", "
        "\"nouveau\": \"<son nom si elle n'est pas au registre>\", \"appellation\": \"<le mot employe ici pour elle : "
        "maman, le docteur...>\", \"lien\": \"<son lien avec la personne qui parle, ex. mere ; sinon vide>\"}].\n"
        "- \"question_qui\" : vide, SAUF si on doit savoir qui parle et qu'on ne peut pas : deux personnes du registre "
        "collent, OU qui parle est inconnu ET (un geste vital est raconte OU la reponse change selon qui parle). Alors "
        "UNE question courte, dans la langue du message. Un simple bonjour d'un inconnu : PAS de question.\n"
        "- \"de_quoi\" : UNE phrase de sens qui se comprend TOUTE SEULE, sans la conversation : remplace « elle », "
        "« lui », « ca », « la-bas » par ce dont il s'agit vraiment (ex. « les cheveux de sa fille quand elle avait "
        "8 ans »). Dans la langue du message. Pour un simple bonjour : ce qui est dit, tel quel.\n"
        "- \"quand\" : maintenant (ce qui se passe, ou rien n'est dit), recent (le plus recent sur ce sujet), moment (un "
        "moment ou un jour precis), histoire (toute l'histoire, comment ca a evolue).\n"
        "- \"du\" / \"au\" : DES que le message nomme un jour ou une periode, meme dans une question, tu les remplis : "
        "TOUJOURS avec ces mots francais (aujourd'hui, hier, avant-hier) ou une date AAAA-MM-JJ, quelle que soit sa "
        "langue ; sinon vide. Si l'annee n'est pas dite, c'est l'annee du message ; si cette date tombe dans le futur, "
        "c'est l'annee d'avant. Exemple, pour un message ecrit le 2026-10-20 : « Qu'est-ce qu'on a fait le 14 juillet ? » "
        "-> du = au = 2026-07-14 ; « en septembre » -> du = 2026-09-01, au = 2026-09-30.\n"
        "- \"vital\" : true si ca touche a la sante, aux medicaments, aux soins, a la securite de quelqu'un (dans le "
        "doute : true).\n"
        "- \"flou\" : vide, SAUF si le message est vraiment trop flou pour savoir quoi chercher, meme avec la "
        "conversation : alors UNE seule question courte a poser.\n"
        "Reponds UNIQUEMENT en JSON strict : {\"qui_parle\": {\"numero\": \"\", \"nouveau\": \"\", \"comment\": "
        "\"inconnu\", \"raison\": \"\", \"distingue\": \"\"}, \"de_qui\": [], \"question_qui\": \"\", \"de_quoi\": \"...\", \"quand\": "
        "\"maintenant|recent|moment|histoire\", \"du\": \"\", \"au\": \"\", \"vital\": false, \"flou\": \"\"}")
    r = co.reglages()
    brut, panne = co.appel_simple(r["cerveau_bibliothecaire"], "Tu ecoutes et tu comprends la personne qui ecrit. JSON strict.",
                                  contenu, "comprendre", reflechir=False, max_tokens=1500,
                                  timeout=float(r["bibliothecaire_plafond_secondes"]))
    d = co.json_dans(brut)
    if not isinstance(d, dict):
        rendu["panne"] = panne or "reponse illisible : on cherche avec le message tel quel"
        return rendu
    if isinstance(d.get("qui_parle"), dict):
        rendu["qui_parle"] = d["qui_parle"]
    if isinstance(d.get("de_qui"), list):
        rendu["de_qui"] = d["de_qui"]
    rendu["question_qui"] = str(d.get("question_qui") or "").strip()[:300]
    de_quoi = str(d.get("de_quoi") or "").strip()
    if de_quoi:
        rendu["de_quoi"] = de_quoi[:600]
    q = co.sans_accents(d.get("quand") or "").strip()
    rendu["quand"] = q if q in QUANDS else "maintenant"
    for cle in ("du", "au"):
        brut_j = str(d.get(cle) or "").strip()
        if brut_j:
            jour, certain = Q._jour_et_certitude(brut_j, date_message)
            if certain:
                rendu[cle] = jour
            else:
                rendu["dates_incertaines"].append(brut_j[:40])
    if rendu["du"] and not rendu["au"]:
        rendu["au"] = rendu["du"]
    if rendu["au"] and not rendu["du"]:
        rendu["du"] = rendu["au"]
    if rendu["du"] and rendu["au"] and rendu["du"] > rendu["au"]:
        rendu["du"], rendu["au"] = rendu["au"], rendu["du"]
    v = d.get("vital")
    rendu["vital"] = (v is True) or (str(v).strip().lower() in ("true", "oui", "1", "yes"))
    rendu["flou"] = str(d.get("flou") or "").strip()[:300]
    return rendu


def jours_du_journal(compris, date_message=None):
    """Les jours du journal du quotidien a lire pour une question vitale : la periode dite, sinon aujourd'hui."""
    co = C()
    if compris.get("du"):
        try:
            a = datetime.date.fromisoformat(compris["du"])
            b = datetime.date.fromisoformat(compris.get("au") or compris["du"])
        except Exception:
            return []
        out = []
        while a <= b and len(out) < 31:
            out.append(a.isoformat())
            a += datetime.timedelta(days=1)
        return out
    return [(co._date_propre(date_message) or co.maintenant())[:10]]


def en_clair(compris):
    """Ce qui a ete compris, en une ligne, pour le bibliothecaire et pour la trace."""
    t = "Le message parle de : %s. Quand : %s" % (compris.get("de_quoi", ""), compris.get("quand", "maintenant"))
    if compris.get("du"):
        t += " (du %s au %s)" % (compris["du"], compris.get("au") or compris["du"])
    if compris.get("dates_incertaines"):
        t += " (dates pas comprises : %s)" % ", ".join(compris["dates_incertaines"])
    if compris.get("vital"):
        t += ". Ca touche au VITAL"
    if compris.get("flou"):
        t += ". Si rien ne repond, une question possible : « %s »" % compris["flou"]
    return t + "."
