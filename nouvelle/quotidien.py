# -*- coding: utf-8 -*-
"""LE JOURNAL DU QUOTIDIEN : LE VITAL, NOTE PAR LE PROGRAMME A L'HEURE EXACTE -- piece 3 de la bibliotheque rangee
(decidee le 20/10/2026).

  - Apres chaque echange, l'archiviste repere si le message recu raconte un GESTE VITAL DEJA FAIT (« j'ai pris mon
    cachet », « je sors de chez le docteur »). C'est lui qui juge ce qui est vital (dans le doute : vital), jamais une
    liste de mots. Un geste OUBLIE, dit clairement (« hier soir j'ai oublie mon cachet »), est note aussi, comme
    PAS FAIT (« l'oubli affirme »). Un geste seulement PREVU ou une question : rien.
  - LE PROGRAMME l'ecrit dans le journal, avec l'heure exacte du message. Si le message donne une autre heure (« je l'ai
    pris a 8h », dit a 10h), le journal note 8h, ET qu'il l'a dit a 10h. Le mot de la personne est garde tel quel.
  - Elle lit ce journal pour repondre en disant D'OU ELLE LE SAIT (« tu m'as dit a 8h12 que... », « c'est moi qui l'ai fait »). Pas de trace -> « je n'ai pas de trace », jamais « oui ».
  - Lisible au Bloc-notes, jour par jour : « MON JOURNAL DU QUOTIDIEN.txt ».
Rien n'est jamais efface.
"""
import os, json, time, datetime, re


def C():
    import coeur
    return coeur


# CE QUI EST ECRIT DANS LE JOURNAL quand l'heure a ete DITE par la personne. Le mot a change (c'est un
# produit a vendre : plus aucun prenom), mais L'ANCIEN MOT EST TOUJOURS RELU : les journaux deja ecrits
# gardent « dite par Fred » et se lisent exactement comme avant. Rien n'est reecrit, rien n'est perdu.
HEURE_DITE = "heure dite par la personne"
HEURE_DITE_ANCIENNES = ("dite par Fred",)
HEURE_DITE_TOUTES = (HEURE_DITE,) + HEURE_DITE_ANCIENNES


def _f_journal():
    return os.path.join(C().DOSSIER, "journal_du_quotidien.jsonl")


def _f_lisible():
    return os.path.join(C().DOSSIER, "MON JOURNAL DU QUOTIDIEN.txt")


def entrees():
    return C().lire_lignes(_f_journal())


def _jour_et_certitude(jour_dit, date_message):
    """« aujourd'hui », « hier », « avant-hier » ou une date AAAA-MM-JJ : le PROGRAMME calcule le jour, a partir du
    message. Rend (jour, certain). Une reponse qu'il ne comprend pas (ex. « ieri ») n'est JAMAIS devinee : certain=False."""
    base = datetime.datetime.strptime(date_message[:10], "%Y-%m-%d").date()
    j = C().sans_accents(jour_dit or "").strip()
    if not j or j.startswith("aujourd") or j in ("ce matin", "ce soir", "cet apres-midi", "ce midi"):
        return base.isoformat(), True
    if j.startswith("avant-hier") or j.startswith("avant hier"):
        return (base - datetime.timedelta(days=2)).isoformat(), True
    if j.startswith("hier"):
        return (base - datetime.timedelta(days=1)).isoformat(), True
    m = re.match(r"^(\d{4})-(\d{2})-(\d{2})$", j)
    if m:
        try:
            return datetime.date(int(m.group(1)), int(m.group(2)), int(m.group(3))).isoformat(), True
        except Exception:
            pass
    return base.isoformat(), False


def _jour_calcule(jour_dit, date_message):
    return _jour_et_certitude(jour_dit, date_message)[0]


def _heure_propre(h):
    """« 8h », « 08:30 », « 8.30 », « 8 pm » -> « HH:MM » sur 24 h ; ce qui n'est pas compris -> « »."""
    t = str(h or "").strip().lower()
    pm = re.search(r"\bp\.?m\.?$", t)
    am = re.search(r"\ba\.?m\.?$", t)
    t = re.sub(r"\s*[ap]\.?m\.?$", "", t)
    m = re.match(r"^\s*(\d{1,2})\s*(?:[h:.]\s*(\d{0,2}))?\s*$", t)
    if not m:
        return ""
    hh, mm = int(m.group(1)), int(m.group(2) or 0)
    if pm and hh < 12:
        hh += 12
    if am and hh == 12:
        hh = 0
    return "%02d:%02d" % (hh, mm) if (0 <= hh <= 23 and 0 <= mm <= 59) else ""


def noter_le_vital(message, date_message=None):
    """Apres un echange : l'archiviste juge s'il y a un geste vital FAIT (ou dit PAS FAIT) ; le programme l'ecrit. Rend les entrees ecrites."""
    co = C()
    msg = str(message or "").strip()
    if not msg or msg.startswith("["):
        return []
    date_message = co._date_propre(date_message) or co.maintenant()
    contenu = (
        "LE MESSAGE RECU (ecrit le %s) :\n%s\n\n"
        "TON TRAVAIL : dis si ce message raconte un ou plusieurs GESTES VITAUX DEJA FAITS par la personne qui ecrit, "
        "ou DITS CLAIREMENT "
        "PAS FAITS (oublies, pas pris) : prendre un "
        "medicament ou un traitement, un soin, un rendez-vous medical fait, une mesure de sante (tension, sucre...), "
        "manger ou boire quand c'est un enjeu de sante, une chose de securite (gaz ferme, porte fermee)... C'est TOI "
        "qui juges ce qui est vital, par le sens ; dans le doute, c'est vital. Un geste dit clairement PAS FAIT (« j'ai "
        "oublie mon cachet », « je ne l'ai pas pris ») se note avec \"fait\": false. Un geste seulement PREVU (« je vais "
        "le prendre ») ou une question (« est-ce que j'ai pris... ? ») ne se note PAS. Ne devine jamais une heure : "
        "donne-la seulement si le message la dit.\n"
        "Si ce n'est pas celui qui ecrit qui a fait le geste, ou si c'est une AUTRE PERSONNE qui parle (« c'est sa fille, "
        "ma mere m'a "
        "dit qu'elle a pris son cachet »), dis-le dans \"qui\" (ex. « Madame Dupont, d'apres sa fille ») ; sinon vide.\n"
        "Quelle que soit la langue du message, \"jour\" s'ecrit TOUJOURS avec ces mots francais (aujourd'hui, hier, "
        "avant-hier) ou une date AAAA-MM-JJ, et \"heure\" TOUJOURS sur 24 heures (HH:MM, ex. 20:00). \"quoi\" reste "
        "dans la langue du message.\n"
        "Reponds UNIQUEMENT en JSON strict : {\"gestes\": [{\"quoi\": \"<le geste, court, avec les mots du message>\", \"fait\": true, \"qui\": \"\", "
        "\"jour\": \"aujourd'hui|hier|avant-hier|AAAA-MM-JJ\", \"heure\": \"<HH:MM si le message la dit, sinon vide>\"}]} "
        "ou {\"gestes\": []}" % (date_message, msg))
    brut, panne = co.appel_simple(co.reglages()["cerveau_archiviste"], "Tu es l'archiviste de cette memoire. JSON strict.",
                                  contenu, "journal_du_quotidien", reflechir=False, max_tokens=1500)
    d = co.json_dans(brut)
    if not isinstance(d, dict):
        co.ajouter_ligne(co.F_TRACE, {"date": co.maintenant(), "panne": "journal du quotidien",
                                      "detail": panne or "reponse illisible"})
        return []
    ecrites = []
    for g in d.get("gestes") or []:
        if not isinstance(g, dict) or not str(g.get("quoi") or "").strip():
            continue
        heure_dite = _heure_propre(g.get("heure"))
        heure_brute = str(g.get("heure") or "").strip()
        jour, certain = _jour_et_certitude(g.get("jour"), date_message)
        meme_jour = (jour == date_message[:10])
        f = g.get("fait", True)
        pas_fait = (f is False) or (str(f).strip().lower() in ("false", "non", "0", "no"))
        # L'heure du message ne vaut QUE pour un geste du jour meme : « hier soir j'ai ferme le gaz » (sans heure),
        # dit a 16h10, n'a PAS ete fait a 16h10 (essai reel du 20/10). Jamais d'heure inventee.
        if heure_dite:
            heure, heure_de = heure_dite, HEURE_DITE
        elif heure_brute:
            heure = date_message[11:16] if (meme_jour and not pas_fait) else ""
            heure_de = "heure pas comprise : « %s »" % heure_brute[:40]
        elif meme_jour and not pas_fait:
            # Un oubli n'a pas d'heure : l'heure du message, c'est quand il l'a DIT (gardee dans dit_le).
            heure, heure_de = date_message[11:16], "heure du message"
        else:
            heure, heure_de = "", "heure pas dite"
        e = {"jour": jour,
             "heure": heure,
             "heure_de": heure_de,
             "quoi": str(g["quoi"]).strip()[:300],
             "dit_le": date_message, "message": msg[:2000], "note_le": co.maintenant()}
        if pas_fait:
            e["etat"] = "pas fait"
        if str(g.get("qui") or "").strip():
            e["qui"] = str(g["qui"]).strip()[:120]
        if not certain:
            e["jour_incertain"] = str(g.get("jour") or "")[:40]
        co.ajouter_ligne(_f_journal(), e)
        ecrites.append(e)
    if ecrites:
        ecrire_lisible()
        co.compter("gestes_vitaux_notes", len(ecrites))
    return ecrites


def _fr(jour):
    """« 2026-10-20 » -> « 20/10/2026 » (et « 2026-10-20 10:00 » -> « 20/10/2026 a 10:00 »)."""
    j = str(jour or "")
    if len(j) >= 10 and j[4] == "-" and j[7] == "-":
        return "%s/%s/%s%s" % (j[8:10], j[5:7], j[0:4], (" a " + j[11:16]) if len(j) >= 16 else "")
    return j


def _ligne(e):
    t = "%s  %s%s" % (e["heure"] or "--:--", "PAS FAIT : " if e.get("etat") == "pas fait" else "", e["quoi"])
    if e.get("qui"):
        t += "   (qui : %s)" % e["qui"]
    if e.get("heure_de") in HEURE_DITE_TOUTES and e.get("dit_le", "")[:16] != "%s %s" % (e["jour"], e["heure"]):
        t += ("   (heure dite par cette personne ; on me l'a dit le %s)" if e.get("qui")
              else "   (heure dite par {proprietaire} ; il l'a dit le %s)") % _fr(e["dit_le"])
    elif e.get("heure_de") == "heure du message":
        t += "   (heure de son message)"
    elif e.get("heure_de") == "heure pas dite":
        t += "   (heure pas dite ; %s le %s)" % ("on me l'a dit" if e.get("qui") else "il l'a dit", _fr(e.get("dit_le", "")))
    elif str(e.get("heure_de", "")).startswith("heure pas comprise"):
        t += "   (ATTENTION : %s%s)" % (e["heure_de"], " ; c'est l'heure de son message qui est notee" if e["heure"] else "")
    if e.get("jour_incertain"):
        t += "   (ATTENTION : jour incertain, « %s » ; c'est le jour de son message qui est note)" % e["jour_incertain"]
    return t


OUTILS_DE_MEMOIRE = {"journal_du_quotidien", "chercher_dans_ma_bibliotheque", "ouvrir_fiches", "trouver_un_outil",
                     "rappels", "retenir", "choses_en_cours", "carnet_de_mission"}


def ce_que_j_ai_fait(jour, dit_avant=None):
    """Ce qu'ELLE a fait ce jour-la avec ses mains (mails, fichiers, ecran...), note par le programme au moment meme
    (journal/<jour>.jsonl, ecrit par coeur.journal). Rien d'invente : l'outil, l'heure, le resultat tel qu'il est revenu."""
    co = C()
    out = []
    for e in co.lire_lignes(os.path.join(co.D_JOURNAL, jour + ".jsonl")):
        if e.get("outil") in OUTILS_DE_MEMOIRE:
            continue
        if dit_avant and "%s %s" % (jour, str(e.get("heure", ""))[:5]) > dit_avant[:16]:
            continue
        res = " ".join(str(e.get("resultat") or "").split())[:200]
        out.append("- %s  outil %s -> %s" % (str(e.get("heure", ""))[:5], e.get("outil"), res))
    return out


def lire(jour_demande="aujourd'hui", quoi="", avec_mes_gestes=True, dit_avant=None):
    """Ce que le journal contient pour ce jour (« aujourd'hui », « hier », une date). Jamais de supposition.
    avec_mes_gestes=False : quand la question porte sur la PERSONNE (son cachet), elle ne
    recoit que ce que la personne a dit avoir fait ou pas fait, sans ses mails a elle. L'outil, lui, montre tout.
    dit_avant (pour les essais seulement) : le journal tel qu'il etait a ce moment-la (« AAAA-MM-JJ HH:MM »)."""
    co = C()
    jour, certain = _jour_et_certitude(jour_demande, co.maintenant())
    if not certain:
        return ("Je n'ai pas compris le jour « %s ». Redonne-le en AAAA-MM-JJ, ou avec aujourd'hui / hier / avant-hier."
                % jour_demande)
    du_jour = sorted([e for e in entrees() if e.get("jour") == jour
                      and not (dit_avant and str(e.get("dit_le", ""))[:16] > dit_avant[:16])],
                     key=lambda e: e.get("heure", ""))
    mes_gestes = ce_que_j_ai_fait(jour, dit_avant) if avec_mes_gestes else []
    q = co.sans_accents(quoi or "")
    if not du_jour and not mes_gestes:
        return ("Le journal du quotidien n'a AUCUNE trace le %s (%s). Ne suppose rien : dis « je n'ai pas de trace, on ne m'en a pas parle », et propose de verifier "
                "ensemble (ou de demander a une personne de confiance). Jamais « oui, c'est fait » sans trace."
                % (_fr(jour), "ni ce qu'on m'a dit avoir fait, ni ce que j'ai fait moi-meme" if avec_mes_gestes
                   else "rien de ce qu'on m'a dit avoir fait ou pas fait"))
    t = ("LE JOURNAL DU QUOTIDIEN, le %s (note par le programme, a l'heure exacte). TU DIS TOUJOURS D'OU TU LE SAIS, "
         "sans jouer au gendarme : « c'est moi qui l'ai fait a ... » (tes gestes), « tu m'as dit a ... que c'etait fait » "
         "(ce qu'on t'a dit : c'est une parole, pas une preuve), « tu m'as dit a ... que tu l'avais oublie » (PAS FAIT), ou « je n'ai pas de trace ». Quand il y a un doute "
         "(ex. « le pilulier est plein »), pose une question plutot qu'affirmer : « tu es sur ? on verifie ensemble ? ». "
         "Si c'est une autre personne qui te parle, dis-lui qui a dit quoi.\n" % _fr(jour))
    if du_jour:
        t += "CE QU'ON M'A DIT AVOIR FAIT (OU PAS FAIT) :\n" + "\n".join("- " + _ligne(e) for e in du_jour)
    if mes_gestes:
        t += ("\n" if du_jour else "") + "CE QUE J'AI FAIT MOI-MEME (mes outils) :\n" + "\n".join(mes_gestes)
    if q:
        t += ("\n(Tu cherchais : « %s ». Si rien ci-dessus ne correspond, c'est qu'il n'y a pas de trace de ce geste ce "
              "jour-la : dis-le, ne suppose rien.)" % quoi)
    return t


def ecrire_lisible():
    try:
        par_jour = {}
        for e in entrees():
            par_jour.setdefault(e.get("jour", "?"), []).append(e)
        lignes = ["MON JOURNAL DU QUOTIDIEN (ecrit par le programme, a l'heure exacte ; rien n'est jamais efface).", ""]
        for jour in sorted(par_jour, reverse=True):
            lignes.append(_fr(jour))
            for e in sorted(par_jour[jour], key=lambda e: e.get("heure", "")):
                lignes.append("   " + _ligne(e))
            lignes.append("")
        with open(_f_lisible(), "w", encoding="utf-8") as f:
            f.write(C().avec_le_nom("\n".join(lignes)))      # le jeton {proprietaire} remplace pour la lecture
    except Exception:
        pass


OUTIL = {"name": "journal_du_quotidien",
         "description": "Le journal du quotidien, tenu par le PROGRAMME a l'heure exacte : les gestes vitaux que {proprietaire} (ou une "
                        "autre personne) a DIT avoir faits, ou oublies (medicaments, soins, rendez-vous...), c'est une parole, pas une "
                        "preuve ; ET ce que TU as fait toi-meme avec tes outils ce jour-la (mails envoyes, fichiers...). "
                        "Pour « est-ce que j'ai envoye la facture ? » ou « est-ce que j'ai pris mon cachet ? ». Pour repondre a « est-ce que j'ai pris mon "
                        "cachet ce matin ? », lis-le : jour = aujourd'hui, hier, avant-hier ou AAAA-MM-JJ. Pas de trace = "
                        "tu dis « je n'ai pas de trace », jamais « oui ».",
         "input_schema": {"type": "object", "properties": {"jour": {"type": "string"}, "quoi": {"type": "string"}},
                          "required": ["jour"]}}
