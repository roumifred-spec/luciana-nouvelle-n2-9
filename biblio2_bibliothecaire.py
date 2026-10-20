# -*- coding: utf-8 -*-
"""
BRIQUE 2 — LE BIBLIOTHECAIRE.  Voie a part : il n'archive RIEN, il ne range RIEN.

CE QUE FAIT LE BIBLIOTHECAIRE, ET RIEN D'AUTRE : il RECOIT un besoin (la demande), il
LIT LE PLAN, il VA CHERCHER PAR LE SENS dans l'arbre range par l'archiviste, et il DONNE
a Luciana le strict necessaire -- sous un plafond. Luciana, elle, ne cherche pas.

LE PARTAGE DU TRAVAIL (le meme que l'archiviste) :
  - LA PETITE IA lit la demande et dit SUR QUELLES FACETTES filtrer (c'est du sens).
  - LE PYTHON descend l'arbre, filtre, note et tranche, deterministe.

LA LOGIQUE MARKETPLACE : plus la demande precise de facettes, plus on retrecit, moins on
envoie. "il y a 10 ans" = large. "la voiture rouge il y a 10 ans" = minuscule.


=====================================================================================
 CHANTIER DU 11/10/2026 — POINT 3 : LE MOTEUR DE SCORE. LE DIAGNOSTIC, PUIS LA REPARATION
=====================================================================================

 LA MESURE DE FRED (l'etat d'avant) : sur un de ses messages, 30 candidats dans la
 bibliotheque, MEILLEURE PERTINENCE 0,492 sur 1 -- donc aucune fiche servie, parce que
 le curseur etait a 0,60. Fred a baisse le curseur a 0,35 pour debloquer la sortie, et
 il a raison de dire que ca ne regle pas le fond : LA BONNE FICHE NE DEVRAIT PAS
 PLAFONNER A 0,49 QUAND C'EST VRAIMENT LA BONNE.

 CE QUE J'AI TROUVE EN LISANT LE CALCUL (luciana.py, _biblio2_pertinences) :

   1) ON COMPARAIT LA QUESTION AU TEXTE BRUT DU SOUVENIR. Pour chaque fiche, le calcul
      prenait « resume + texte », le coupait en morceaux de 700 caracteres, et gardait le
      meilleur morceau. Or le moteur de sens de Luciana est le modele
      « paraphrase-multilingual-MiniLM » : il est fait pour comparer DEUX PHRASES COURTES
      entre elles. Quand on lui donne un long passage bavard, le sens se dilue dans la
      moyenne et TOUS les scores s'ecrasent dans la meme bande, autour de 0,45-0,50. Le
      0,492 de Fred n'est pas le signe d'une fiche mediocre : c'est le plafond mecanique
      de ce qu'on peut obtenir en comparant une question a un long texte avec ce modele.

   2) TOUT LE TRAVAIL DE L'ARCHIVISTE ETAIT JETE AU MOMENT DE CHERCHER. L'archiviste avait
      pourtant deja decide, pour chaque fiche, son rayon, son tiroir, son type, son objet,
      les personnes, le lieu, et un resume d'une phrase. Le score n'en utilisait AUCUN,
      sauf le resume noye dans le texte. On rangeait par sens, et on cherchait sans.

   3) L'ACCORD DES ETIQUETTES NE COMPTAIT PAS. Quand les facettes du bibliothecaire
      tombaient juste (meme date, meme personne, meme objet), cette information servait
      seulement a trier l'ordre -- jamais a franchir la barre du curseur.

 CE QUI EST REMARQUABLE : luciana.py avait DEJA tire cette lecon pour ses carnets. En
 v134 il est ecrit noir sur blanc : « IL COMPARE AUX ETIQUETTES, PAS AU TEXTE ENTIER [...]
 Deux phrases courtes et precises battent un carnet de 20 000 caracteres : c'est tout le
 principe. » La memoire 2, plus recente, ne l'avait simplement pas encore appliquee.

 LA REPARATION (fonction noter(), plus bas) :
   a) ON COMPARE D'ABORD A L'ETIQUETTE DE LA FICHE : une phrase courte et dense faite du
      rayon, du tiroir, du filtre, du sous-filtre, du resume, de l'objet, des personnes et
      du lieu. Court contre court : c'est le regime dans lequel le modele est bon.
   b) ON GARDE LE TEXTE BRUT COMME DEUXIEME CHANCE, avec un poids un peu plus faible :
      une fiche peut gagner par son texte, mais un long texte bavard ne gagne plus juste
      parce qu'il est long. (Et si une fiche n'a pas d'etiquette utilisable, son texte
      compte a plein : aucune fiche ne perd de points a cause d'une etiquette vide.)
   c) ON AJOUTE UNE PETITE PRIME quand les facettes tombent juste. Volontairement petite
      et plafonnee (0,04 par facette, 0,12 au maximum) : elle fait passer la barre a un
      bon candidat, elle ne peut pas fabriquer un faux.

 TOUS CES NOMBRES SONT DANS reglage_biblio2.json (point 2), relus a chaque lancement.
 LA MESURE AVANT / APRES est faite par verifier_memoire2.py, qui joue les deux calculs
 cote a cote sur la meme bibliotheque et DIT les deux chiffres.

NOTE IA : tout est ecrit en POSITIF (regle de Fred).
"""

import json, os, re

try:
    import biblio2_reglages as reglages
except Exception:
    reglages = None
try:
    import biblio2_archiviste as arch
except Exception:
    arch = None
try:
    import biblio2_plan as plan_biblio
except Exception:
    plan_biblio = None

PLAFOND_DEFAUT = 40000   # ne sert que si le fichier de reglage manque


def plafond():
    """Le maximum envoye a Luciana, lu au reglage (point 2). Bien trie, on est tres en dessous."""
    try:
        return reglages.plafond()
    except Exception:
        return PLAFOND_DEFAUT


# conserve pour les appelants qui l'importaient tel quel
PLAFOND = PLAFOND_DEFAUT


def _reglages_score():
    try:
        return reglages.reglages_score()
    except Exception:
        return {"poids_etiquette": 1.0, "poids_texte": 0.9, "prime_par_facette": 0.04,
                "prime_facette_maxi": 0.12, "morceau_maxi": 700, "morceaux_par_fiche_maxi": 40}


def _colle(fiche, besoin):
    """Rend un SCORE (nb de facettes qui collent) si la fiche passe tous les filtres
    DONNES, ou None si une facette donnee ne colle pas (elle est alors ecartee : c'est
    le retrecissement). Une facette vide dans le besoin ne filtre pas.

    (luciana.py appelle cette fonction telle quelle : sa signature ne change pas.)"""
    f = fiche.get("filtres") or {}
    score = 0
    for champ in ("date", "ou", "objet", "type"):
        v = str(besoin.get(champ) or "").strip().lower()
        if not v:
            continue
        cible = str(f.get(champ) or "").strip().lower()
        if v and cible and (v in cible or cible in v or v[:4] == cible[:4]):
            score += 1
        else:
            return None                      # une facette precise qui ne colle pas -> ecarte
    vq = [str(x).strip().lower() for x in (besoin.get("qui") or []) if str(x).strip()]
    if vq:
        cq = " ".join(str(x).lower() for x in (f.get("qui") or []))
        if any(a in cq for a in vq):
            score += 1
        else:
            return None
    for m in (besoin.get("mots") or []):
        if str(m).lower() in (str(fiche.get("texte") or "") + str(fiche.get("resume") or "")).lower():
            score += 1
    return score


# =====================================================================
#  POINT 3 — LE MOTEUR DE SCORE REPARE.
# =====================================================================

def etiquette(cat, sous, fiche):
    """L'etiquette de sens de la fiche. On passe par l'archiviste, pour que les deux roles
    parlent EXACTEMENT de la meme chose (regle « tout le monde au courant de tout ») ;
    s'il manque, on sait fabriquer un repli ici."""
    if arch is not None:
        try:
            return arch.etiquette_de(cat, sous, fiche)
        except Exception:
            pass
    fi = fiche if isinstance(fiche, dict) else {}
    f = fi.get("filtres") if isinstance(fi.get("filtres"), dict) else {}
    qui = f.get("qui") if isinstance(f.get("qui"), (list, tuple)) else []
    bouts = [cat, sous, fi.get("filtre"), fi.get("sous_filtre"), fi.get("resume"),
             f.get("objet"), ", ".join(str(x) for x in qui), f.get("ou"), f.get("type")]
    vus, propres = set(), []
    for b in bouts:
        b = re.sub(r"\s+", " ", str(b or "")).strip(" .,;:-")
        if b and b.lower() not in vus:
            vus.add(b.lower())
            propres.append(b)
    return " — ".join(propres)[:600]


def _morceaux(texte, maxi, combien_maxi):
    """Coupe un texte en passages d'au plus 'maxi' caracteres, sur un blanc. Rien n'est
    perdu : les passages mis bout a bout redonnent tout le texte. (Meme decoupage que
    celui de luciana.py, pour que les deux donnent le meme resultat.)"""
    texte = str(texte or "").strip()
    morceaux = []
    while len(texte) > maxi:
        coupe = texte[:maxi]
        blanc = max(coupe.rfind("\n"), coupe.rfind(" "))
        if blanc < maxi // 2:
            blanc = maxi
        morceaux.append(texte[:blanc].strip())
        texte = texte[blanc:].strip()
    if texte:
        morceaux.append(texte)
    return morceaux[:combien_maxi]


def _produit(u, v):
    """La ressemblance entre deux empreintes DEJA normalisees : un simple produit scalaire.
    Marche avec des listes Python comme avec des vecteurs numpy. Ne leve jamais."""
    try:
        return float(sum(a * b for a, b in zip(u, v)))
    except Exception:
        return 0.0


def noter(message, fiches, vecteurs_de, besoin=None, reglage=None):
    """LA PERTINENCE DE CHAQUE FICHE, DE 0 A 1 -- le calcul repare (point 3).

    'fiches'      = [(categorie, sous_categorie, fiche), ...]
    'vecteurs_de' = une fonction vecteurs_de(liste_de_textes) -> liste d'empreintes
                    NORMALISEES (longueur 1). Luciana donne son moteur de sens ; le
                    script de controle donne un moteur de remplacement. Le calcul est
                    donc LE MEME partout, et il se mesure sans rien installer.
    'besoin'      = les facettes choisies par la petite IA (pour la petite prime).

    Rend la liste des scores, alignee sur 'fiches'. Ne leve JAMAIS : au moindre souci on
    rend None, et l'appelant sert alors le resultat des facettes tel quel.

    LE CALCUL, EN UNE PHRASE : on prend le MEILLEUR de (l'etiquette courte) et (le texte
    brut, un peu allege), et on ajoute une petite prime si les facettes tombent juste."""
    r = dict(_reglages_score())
    if isinstance(reglage, dict):
        r.update(reglage)
    fiches = list(fiches or [])
    if not fiches:
        return []
    besoin = besoin if isinstance(besoin, dict) else {}
    try:
        maxi = int(r["morceau_maxi"])
        combien = int(r["morceaux_par_fiche_maxi"])

        # on rassemble TOUS les textes a mesurer en UN SEUL appel au moteur : c'est ce qui
        # garde le calcul rapide meme avec beaucoup de fiches.
        a_mesurer = [str(message or " ")]
        plages = []
        for cat, sous, fi in fiches:
            etiq = etiquette(cat, sous, fi)
            brut = ((fi.get("resume") or "") + " " + (fi.get("texte") or "")).strip()
            bouts = _morceaux(brut, maxi, combien)
            bouts_txt = bouts or ([brut] if brut else [])
            debut_etiq = len(a_mesurer)
            if etiq:
                a_mesurer.append(etiq)
            debut_txt = len(a_mesurer)
            a_mesurer.extend(bouts_txt)
            # on retient AUSSI combien de passages fait le texte : c'est ce qui dit
            # s'il est bavard (plusieurs passages) ou court (un seul).
            plages.append((debut_etiq if etiq else None, debut_txt, len(a_mesurer),
                           len(bouts_txt)))

        vect = list(vecteurs_de(a_mesurer))
        if len(vect) != len(a_mesurer):
            return None
        q = vect[0]

        scores = []
        for (i_etiq, d_txt, f_txt, n_txt), (cat, sous, fi) in zip(plages, fiches):
            s_etiq = _produit(vect[i_etiq], q) if i_etiq is not None else None
            s_txt = max((_produit(vect[i], q) for i in range(d_txt, f_txt)), default=None)

            # (a) l'etiquette courte, (b) le texte brut un peu allege -> on garde le meilleur.
            # Quand il n'y a PAS d'etiquette utilisable, le texte compte a plein : une
            # etiquette vide ne doit jamais couter de points a une fiche.
            bouts_notes = []
            if s_etiq is not None:
                bouts_notes.append(float(r["poids_etiquette"]) * s_etiq)
            if s_txt is not None:
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
                bouts_notes.append(poids * s_txt)
            base = max(bouts_notes) if bouts_notes else 0.0

            # (c) la petite prime d'accord des facettes, plafonnee.
            prime = 0.0
            if besoin:
                try:
                    n = _colle(fi, besoin)
                except Exception:
                    n = None
                if n:
                    prime = min(float(r["prime_facette_maxi"]),
                                float(r["prime_par_facette"]) * int(n))
            scores.append(max(0.0, min(1.0, base + prime)))
        return scores
    except Exception:
        return None


def noter_a_l_ancienne(message, fiches, vecteurs_de, reglage=None):
    """LE CALCUL D'AVANT LA REPARATION, garde EXPRES et seulement pour la MESURE.
    C'est mot pour mot ce que faisait luciana.py : « resume + texte », coupe en morceaux,
    on garde le meilleur morceau. verifier_memoire2.py joue les deux cote a cote pour
    pouvoir DIRE l'avant et l'apres sur la meme bibliotheque."""
    r = dict(_reglages_score())
    if isinstance(reglage, dict):
        r.update(reglage)
    fiches = list(fiches or [])
    if not fiches:
        return []
    try:
        maxi, combien = int(r["morceau_maxi"]), int(r["morceaux_par_fiche_maxi"])
        a_mesurer, plages = [str(message or " ")], []
        for _cat, _sous, fi in fiches:
            brut = ((fi.get("resume") or "") + " " + (fi.get("texte") or "")).strip()
            bouts = _morceaux(brut, maxi, combien) or [brut or " "]
            debut = len(a_mesurer)
            a_mesurer.extend(bouts)
            plages.append((debut, len(a_mesurer)))
        vect = list(vecteurs_de(a_mesurer))
        if len(vect) != len(a_mesurer):
            return None
        q = vect[0]
        return [max(_produit(vect[i], q) for i in range(d, f)) for d, f in plages]
    except Exception:
        return None


# ---------------------------------------------------------------------
#  LE RANGEMENT DE LA REPONSE : mettre bout a bout, sous le plafond.
# ---------------------------------------------------------------------

def _bloc(cat, sous, fiche):
    """Le bloc texte d'UNE fiche, tel qu'il part a Luciana. Positif, borne.
    On DIT si la fiche est en suspens : Luciana saura qu'un doute reste a trancher,
    au lieu de la servir comme une certitude."""
    txt = str(fiche.get("texte") or fiche.get("resume") or "")
    doute = " (en suspens : un doute a trancher)" if fiche.get("en_suspens") else ""
    filtre = fiche.get("filtre") or ""
    sous_filtre = fiche.get("sous_filtre") or ""
    if filtre and sous_filtre:
        return "[%s / %s / %s / %s]%s %s" % (cat, sous, filtre, sous_filtre, doute, txt)
    return "[%s / %s]%s %s" % (cat, sous, doute, txt)


def construire_texte(fiches, budget=None):
    """Met bout a bout des fiches DEJA CHOISIES, DANS L'ORDRE, sous le plafond. Rend
    (texte, nb_donnes). 'fiches' = [(cat, sous, fiche), ...]. Le premier passe toujours,
    meme s'il depasse a lui seul le plafond (sinon on ne servirait rien). Ne leve jamais."""
    if budget is None:
        budget = plafond()
    donnes, taille = [], 0
    for cat, sous, fi in (fiches or []):
        bloc = _bloc(cat, sous, fi)
        if donnes and taille + len(bloc) + 1 > budget:
            break
        donnes.append(bloc)
        taille += len(bloc) + 1
    return "\n".join(donnes), len(donnes)


def chercher(arbre, besoin, budget=None):
    """LE PYTHON descend l'arbre et rend (texte_pour_luciana, rapport). Positif, borne,
    jamais de plantage. 'besoin' = ce que l'IA a lu de la demande :
    {categorie, sous_categorie, date, qui, ou, objet, type, mots}.
    Le rapport porte AUSSI 'fiches' = la liste [(cat, sous, fiche), ...] retenue par les
    facettes, dans l'ordre : c'est elle que le moteur de score va noter au retour."""
    if budget is None:
        budget = plafond()
    candidats = []
    for cat, sous_cats in (arbre or {}).items():
        if not isinstance(sous_cats, dict):
            continue
        if besoin.get("categorie") and str(besoin["categorie"]).lower() not in str(cat).lower():
            continue
        for sous, fiches in sous_cats.items():
            if not isinstance(fiches, list):
                continue
            if besoin.get("sous_categorie") and str(besoin["sous_categorie"]).lower() not in str(sous).lower():
                continue
            # POINT 4 : les niveaux 3 et 4 filtrent aussi, quand la demande les precise
            for fi in fiches:
                if not isinstance(fi, dict):
                    continue
                if besoin.get("filtre") and str(besoin["filtre"]).lower() not in str(fi.get("filtre") or "").lower():
                    continue
                if besoin.get("sous_filtre") and str(besoin["sous_filtre"]).lower() not in str(fi.get("sous_filtre") or "").lower():
                    continue
                candidats.append((cat, sous, fi))

    gardes = []
    for cat, sous, fi in candidats:
        sc = _colle(fi, besoin)
        if sc is not None:
            gardes.append((sc, cat, sous, fi))
    # le plus de facettes qui collent d'abord ; a egalite, la date la plus recente
    gardes.sort(key=lambda x: str(x[3].get("filtres", {}).get("date") or ""), reverse=True)
    gardes.sort(key=lambda x: -x[0])

    fiches_ordre = [(cat, sous, fi) for _sc, cat, sous, fi in gardes]
    texte, nb = construire_texte(fiches_ordre, budget)
    rapport = {"candidats_dans_l_arbre": len(candidats), "retenus_apres_filtres": len(gardes),
               "donnes_a_luciana": nb, "caracteres": len(texte), "plafond": budget,
               "fiches": fiches_ordre}
    return texte, rapport


def servir_avec_curseur(fiches, scores, curseur=None, budget=None):
    """LE RAG, AU RETOUR. On a les fiches retenues par les facettes ET leur PERTINENCE
    (le sens, 0 a 1), calculee par noter(). 'scores' est aligne sur 'fiches'.
    On garde ce qui ATTEINT le curseur, du plus proche au moins proche, sous le plafond.
    Rend (fiches_gardees, texte, rapport). Si rien n'atteint le curseur, texte = "" et
    fiches_gardees = [] : l'appelant sert alors la petite note (le silence), JAMAIS l'ancien
    tri. Deterministe, ne leve jamais : c'est le Python qui decide, le moteur n'a donne
    qu'un nombre."""
    if curseur is None:
        try:
            curseur = reglages.curseur_sortie()
        except Exception:
            curseur = 0.35
    if budget is None:
        budget = plafond()
    paires = sorted(zip(list(scores or []), list(fiches or [])), key=lambda x: -x[0]) \
        if fiches else []
    meilleur = paires[0][0] if paires else None
    gardes = [f for sc, f in paires if sc >= curseur]
    texte, nb = construire_texte(gardes, budget)
    rapport = {"meilleure_pertinence": round(meilleur, 3) if meilleur is not None else None,
               "curseur": curseur, "retenus_apres_curseur": len(gardes),
               "donnes_a_luciana": nb, "caracteres": len(texte),
               "pertinences": [round(sc, 3) for sc, _ in paires[:8]]}
    return gardes, texte, rapport


# =====================================================================
#  POINT 4 ET POINT 5 — LE BIBLIOTHECAIRE LIT LE PLAN, ET IL EST PREVENU.
# =====================================================================

def prendre_connaissance(chemin_plan=None, chemin_signal=None):
    """CE QUE LE BIBLIOTHECAIRE FAIT AVANT DE CHERCHER : il lit le PLAN (les quatre
    niveaux, point 4) et il lit le SIGNAL de l'archiviste (ce qui est neuf, point 5).
    Rend {plan, signal, carte, au_courant_depuis, nouveautes}. Ne leve jamais : sans plan,
    il cherche quand meme (la carte est alors vide, et le sens fait tout le travail)."""
    try:
        chemin_plan = chemin_plan or reglages.FICHIER_PLAN
        chemin_signal = chemin_signal or reglages.FICHIER_SIGNAL
    except Exception:
        pass
    plan, signal = {}, {}
    if plan_biblio is not None:
        try:
            plan = plan_biblio.charger(chemin_plan) if chemin_plan else {}
        except Exception:
            plan = {}
        try:
            signal = plan_biblio.lire_signal(chemin_signal) if chemin_signal else {}
        except Exception:
            signal = {}
    carte = ""
    if plan_biblio is not None and plan.get("rayons"):
        try:
            carte = plan_biblio.texte_pour_le_bibliothecaire(plan)
        except Exception:
            carte = ""
    return {"plan": plan, "signal": signal, "carte": carte,
            "version_du_plan": plan.get("version", 0),
            "au_courant_depuis": signal.get("quand") or plan.get("quand") or "",
            "nouveautes": signal.get("nouveautes") or [],
            "le_plan_a_change": bool(signal.get("le_plan_a_change"))}


def construire_demande(question, carte=""):
    """Le message POSITIF a l'IA : 'lis la demande, dis ou chercher'. On lui met la CARTE
    DU PLAN sous les yeux (point 4) pour qu'elle choisisse un etage QUI EXISTE."""
    return (
        "Tu es le bibliothecaire. Lis la demande de Fred et dis ou chercher dans sa memoire.\n"
        "Sa memoire est une marketplace a quatre etages : categorie > sous-categorie > filtre "
        "> sous-filtre > la fiche.\n"
        "Voici LE PLAN de ce qui existe vraiment. Choisis les etages DANS ce plan quand ils "
        "conviennent ; si aucun ne va, laisse-les vides et c'est le sens qui cherchera :\n%s\n\n"
        "Facettes libres en plus (remplis seulement ce qui aide) : date, qui (liste de noms), "
        "ou, objet, type, mots (liste).\n\n"
        "LA DEMANDE : %s\n\n"
        "Reponds UNIQUEMENT en JSON strict, avec les champs : categorie, sous_categorie, "
        "filtre, sous_filtre, date, qui, ou, objet, type, mots."
        % (carte or "(la bibliotheque est encore vide)", str(question or "")[:2000])
    )


def lire_le_besoin(question, categories, appel_ia):
    """L'IA lit la demande et dit SUR QUELLES FACETTES chercher. 'appel_ia(prompt) -> texte'
    est injecte : Luciana donne son DeepSeek, le test donne une fausse IA. Ne leve jamais :
    si l'IA rate, on rend {} (le bibliothecaire cherchera large, et le sens triera).

    (luciana.py appelle cette fonction telle quelle : sa signature ne change pas. Elle
    accepte maintenant une CARTE complete a la place d'une simple liste de categories --
    une liste de categories continue de marcher exactement comme avant.)"""
    if isinstance(categories, str):
        carte = categories
    else:
        carte = ", ".join(str(c) for c in (categories or [])) or "(aucune encore)"
    prompt = construire_demande(question, carte)
    try:
        brut = appel_ia(prompt) or ""
        m = re.search(r"\{.*\}", brut, re.S)
        b = json.loads(m.group(0)) if m else {}
        return b if isinstance(b, dict) else {}
    except Exception:
        return {}


def servir(arbre, question, appel_ia, vecteurs_de=None, curseur=None, budget=None):
    """LE BIBLIOTHECAIRE COMPLET, du debut a la fin. Ne leve jamais.

      1) il PREND CONNAISSANCE du plan et du signal de l'archiviste (points 4 et 5) ;
      2) la petite IA lit la demande et dit ou chercher ;
      3) les facettes retrecissent (deterministe) ;
      4) le moteur de score repare note chaque fiche par le SENS (point 3) ;
      5) le curseur de sortie tranche : au-dessus on sert, rien au-dessus = le silence.

    LE FILET : si les etiquettes ne gardent RIEN, on laisse le sens regarder TOUT l'arbre
    au lieu de partir en silence. Les etiquettes aident a viser ; c'est la pertinence qui
    decide."""
    if budget is None:
        budget = plafond()
    vu = prendre_connaissance()
    besoin = lire_le_besoin(question, vu["carte"] or list((arbre or {}).keys()), appel_ia)
    _texte, rapport = chercher(arbre, besoin, budget=budget)
    candidats = rapport["fiches"]
    elargi = False
    if not candidats and arch is not None:
        try:
            candidats = arch.toutes_les_fiches(arbre)
            elargi = True
        except Exception:
            candidats = []

    rapport["besoin"] = {k: v for k, v in (besoin or {}).items() if v}
    rapport["elargi_au_sens"] = elargi
    rapport["version_du_plan"] = vu["version_du_plan"]
    rapport["au_courant_depuis"] = vu["au_courant_depuis"]

    if vecteurs_de is None:
        # pas de moteur de sens : on sert le resultat des facettes, borne par le plafond,
        # et on le DIT. Jamais un retour silencieux a l'ancien tri.
        texte, nb = construire_texte(candidats, budget)
        rapport.update(sens="pas de moteur de sens", donnes_a_luciana=nb, caracteres=len(texte))
        return texte, rapport

    scores = noter(question, candidats, vecteurs_de, besoin=besoin)
    if scores is None:
        texte, nb = construire_texte(candidats, budget)
        rapport.update(sens="le moteur de sens n'a pas repondu", donnes_a_luciana=nb,
                       caracteres=len(texte))
        return texte, rapport

    gardes, texte, r2 = servir_avec_curseur(candidats, scores, curseur, budget)
    rapport.update(r2)
    return texte, rapport


if __name__ == "__main__":
    import math
    rate = []

    def controle(nom, condition):
        if condition:
            print("  OK   %s" % nom)
        else:
            print("  RATE %s" % nom)
            rate.append(nom)

    if arch is None:
        print("biblio2_archiviste.py est introuvable : ce test a besoin de lui.")
        raise SystemExit(1)

    # =================================================================
    #  UN MOTEUR DE SENS DE REMPLACEMENT, pour mesurer ICI sans rien installer.
    #  Il compte les suites de trois lettres communes entre deux textes, et il
    #  normalise : il a donc le MEME defaut que le vrai modele -- plus un texte est
    #  long, plus son empreinte se dilue. C'est exactement ce qu'il faut pour montrer
    #  l'avant / apres du point 3. (Sur le PC de Fred, c'est le vrai moteur qui sert.)
    # =================================================================
    import hashlib
    LARGEUR = 512          # un vrai espace de vecteurs, comme celui du modele de Fred

    def moteur_de_remplacement(textes):
        """Rend des empreintes NORMALISEES (longueur 1), de taille fixe, comme le vrai
        moteur. Le produit scalaire de deux empreintes est donc bien une ressemblance
        entre 0 et 1, et _produit() marche sans rien changer."""
        out = []
        for t in textes:
            t = re.sub(r"[^a-z0-9 ]+", " ", str(t or " ").lower())
            t = re.sub(r"\s+", " ", t).strip() or " "
            v = [0.0] * LARGEUR
            for i in range(max(1, len(t) - 2)):
                g = t[i:i + 3].encode("utf-8", "replace")
                v[int(hashlib.md5(g).hexdigest()[:8], 16) % LARGEUR] += 1.0
            n = math.sqrt(sum(x * x for x in v)) or 1.0
            out.append([x / n for x in v])
        return out

    # --- on batit une bibliotheque de demo avec l'archiviste -----------------------
    def faux_archiviste(s):
        t = s["texte"].lower()
        if "voiture rouge" in t:
            return {"categorie": "Vehicules", "sous_categorie": "Voitures",
                    "filtres": {"date": "2016", "objet": "voiture rouge", "type": "achat"},
                    "resume": "Clio rouge achetee en 2016.", "confiance": 0.9}
        if "voiture bleue" in t:
            return {"categorie": "Vehicules", "sous_categorie": "Voitures",
                    "filtres": {"date": "2020", "objet": "voiture bleue", "type": "achat"},
                    "resume": "Voiture bleue achetee en 2020.", "confiance": 0.9}
        if "anniversaire" in t:
            return {"categorie": "Famille", "sous_categorie": "Evenements",
                    "filtres": {"date": "2016", "qui": ["ma fille"], "ou": "maison",
                                "type": "evenement"}, "resume": "Anniversaire de ma fille.",
                    "confiance": 0.85}
        if "noel" in t:
            return {"categorie": "Famille", "sous_categorie": "Evenements",
                    "filtres": {"date": "2016", "qui": ["famille"], "ou": "maison",
                                "type": "evenement"}, "resume": "Noel en famille.", "confiance": 0.85}
        if "docteur" in t:
            return {"categorie": "Sante", "sous_categorie": "Rendez-vous",
                    "filtres": {"date": "2024", "qui": ["Dr Martin"], "ou": "Lyon",
                                "type": "medical"}, "resume": "RDV chez le Dr Martin.",
                    "confiance": 0.8}
        return {"categorie": "Divers", "sous_categorie": "A trier", "filtres": {},
                "resume": "", "confiance": 0.2}

    bavardage = ("Alors ce matin je me suis leve tot, il faisait gris, j'ai pris un cafe et "
                 "j'ai regarde par la fenetre, les voisins refaisaient leur toiture, ca tapait "
                 "fort, apres j'ai range le garage un peu, enfin pas tout, il reste des cartons, "
                 "et je me demandais s'il fallait repeindre le portail un de ces jours, ") * 6
    memoires = [
        {"texte": "J'ai achete une voiture rouge, une Clio, en 2016.", "source": "essai"},
        {"texte": "On a fete l'anniversaire de ma fille a la maison en 2016.", "source": "essai"},
        {"texte": "Noel en famille a la maison, 2016.", "source": "essai"},
        {"texte": "J'ai pris une voiture bleue en 2020.", "source": "essai"},
        {"texte": "Rendez-vous chez le docteur Martin a Lyon en 2024.", "source": "essai"},
        {"texte": bavardage, "source": "essai"},
    ]
    arbre = {}
    for s in memoires:
        s["repere"] = arch.repere_de("essai", s["texte"])
        arch.ranger(arbre, s, arch.valider_jugement(faux_archiviste(s)))
    print("=== La bibliotheque de demo : %d rayons, %d fiches ==="
          % (arch.compter(arbre)["rayons"], arch.compter(arbre)["fiches"]))

    def faux_besoin(question):
        q = question.lower()
        b = {}
        if "10 ans" in q or "2016" in q:
            b["date"] = "2016"
        if "voiture rouge" in q:
            b["objet"] = "voiture rouge"
        return b

    print("\n=== LE RETRECISSEMENT (la logique marketplace) ===")
    txt, rap = chercher(arbre, faux_besoin("qu'est-ce que je faisais il y a 10 ans"))
    txt2, rap2 = chercher(arbre, faux_besoin("la voiture rouge il y a 10 ans"))
    controle("la demande large ramene plusieurs souvenirs de 2016", rap["donnes_a_luciana"] >= 3)
    controle("la demande ciblee ramene UN seul souvenir", rap2["donnes_a_luciana"] == 1)
    controle("plus c'est cible, moins on envoie", rap2["caracteres"] < rap["caracteres"])
    controle("la demande ciblee ramene bien la voiture rouge", "Clio" in txt2)
    print("  large = %d car. / cible = %d car." % (rap["caracteres"], rap2["caracteres"]))

    # =================================================================
    #  POINT 3 : LA MESURE AVANT / APRES, sur la MEME bibliotheque et la MEME question.
    # =================================================================
    question = "c'etait quoi la voiture que j'avais achetee en 2016 ?"
    toutes = arch.toutes_les_fiches(arbre)
    avant = noter_a_l_ancienne(question, toutes, moteur_de_remplacement)
    apres = noter(question, toutes, moteur_de_remplacement, besoin={"objet": "voiture rouge"})

    def meilleure(scores):
        return max(scores) if scores else 0.0

    def la_bonne(scores):
        """le score de la fiche qui est VRAIMENT la bonne reponse (la Clio rouge)"""
        for (c, s, fi), sc in zip(toutes, scores):
            if "rouge" in (fi.get("resume") or "").lower():
                return sc
        return 0.0

    print("\n=== POINT 3 : LE MOTEUR DE SCORE, AVANT / APRES ===")
    print("  question : « %s »" % question)
    print("  candidats notes : %d" % len(toutes))
    print("  AVANT (on comparait au texte brut)   : la bonne fiche = %.3f / meilleure = %.3f"
          % (la_bonne(avant), meilleure(avant)))
    print("  APRES (on compare a l'etiquette)     : la bonne fiche = %.3f / meilleure = %.3f"
          % (la_bonne(apres), meilleure(apres)))
    try:
        curseur = reglages.curseur_sortie()
    except Exception:
        curseur = 0.35
    print("  curseur de sortie en service : %.2f" % curseur)
    controle("point 3 : la bonne fiche monte apres reparation",
             la_bonne(apres) > la_bonne(avant))
    controle("point 3 : la bonne fiche passe le curseur apres reparation",
             la_bonne(apres) >= curseur)
    controle("point 3 : la bonne fiche est la MIEUX notee apres reparation",
             abs(la_bonne(apres) - meilleure(apres)) < 1e-9)
    controle("point 3 : le long bavardage ne gagne pas",
             max(sc for (c, s, fi), sc in zip(toutes, apres)
                 if len(fi.get("texte") or "") > 500) < la_bonne(apres))
    controle("point 3 : les scores restent entre 0 et 1",
             all(0.0 <= sc <= 1.0 for sc in apres))
    controle("point 3 : une etiquette vide ne coute pas de points (le texte compte a plein)",
             (noter("voiture", [("X", "Y", {"texte": "une voiture rouge"})],
                    moteur_de_remplacement) or [0])[0] > 0)

    print("\n=== LE CURSEUR DE SORTIE (le silence quand rien n'est assez proche) ===")
    g_bas, t_bas, r_bas = servir_avec_curseur(toutes, apres, 0.05)
    g_haut, t_haut, r_haut = servir_avec_curseur(toutes, apres, 0.99)
    controle("plus le curseur monte, moins on sert", len(g_bas) >= len(g_haut))
    controle("curseur a 0,99 : rien ne passe -> le silence", g_haut == [] and t_haut == "")
    controle("aucune fiche -> aucun garde, aucun plantage",
             servir_avec_curseur([], [], 0.6)[0] == [])
    controle("noter() ne plante pas sur une bibliotheque vide",
             noter("x", [], moteur_de_remplacement) == [])

    print("\n=== POINT 4 ET 5 : le bibliothecaire lit le plan et le signal ===")
    import tempfile, biblio2_plan as pl
    d = tempfile.mkdtemp(prefix="essai_bib_")
    f_plan, f_signal = os.path.join(d, "plan.json"), os.path.join(d, "signal_plan.json")
    plan, signal = pl.rafraichir(arbre, f_plan, f_signal)
    vu = prendre_connaissance(f_plan, f_signal)
    controle("point 4 : le bibliothecaire LIT la carte aux 4 niveaux",
             "Vehicules" in vu["carte"] and "Voiture rouge" in vu["carte"])
    controle("point 5 : le bibliothecaire est PREVENU, avec une date",
             len(vu["au_courant_depuis"]) >= 10 and vu["le_plan_a_change"] is True)
    controle("point 4 : la carte part bien dans la demande a l'IA",
             "Voiture rouge" in construire_demande("ma voiture ?", vu["carte"]))
    controle("point 4 : les niveaux 3 et 4 filtrent aussi",
             chercher(arbre, {"filtre": "Achat", "sous_filtre": "Voiture rouge"})[1]["candidats_dans_l_arbre"] == 1)

    print("\n%s" % ("TOUT EST PASSE." if not rate else
                    "TESTS QUI RATENT (%d) :\n  - %s" % (len(rate), "\n  - ".join(rate))))
