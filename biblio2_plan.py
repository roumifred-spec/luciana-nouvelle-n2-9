# -*- coding: utf-8 -*-
"""
BRIQUE 4 — LE PLAN DE LA BIBLIOTHEQUE.  Le document que TOUT LE MONDE lit.

C'est la piece qui manquait. L'archiviste rangeait, le bibliothecaire cherchait, et
les deux ne se parlaient pas : quand l'archiviste creait un rayon neuf, le
bibliothecaire ne l'apprenait jamais. Ce fichier-la est leur point de rendez-vous.

CE QU'IL CONTIENT, ET RIEN D'AUTRE : les NOMS des etages, aux quatre niveaux voulus
par Fred, et le nombre de fiches a chaque etage.

    categorie  >  sous-categorie  >  filtre  >  sous-filtre  >  la fiche

CE QU'IL NE CONTIENT PAS : le texte des souvenirs. Le plan est une CARTE, pas la
bibliotheque. C'est ce qui le garde petit meme avec 60 ans de souvenirs : sa taille
depend du nombre de TIROIRS, jamais du nombre de SOUVENIRS.

LES TROIS REGLES DU CHANTIER DU 11/10/2026 :

  (point 4) LE PLAN EST VIVANT ET PARTAGE. On le refabrique a partir de l'arbre, et
      le bibliothecaire le LIT pour chercher -- il ne devine plus les tiroirs, il les
      lit. texte_pour_le_bibliothecaire() est exactement ce qu'il met sous les yeux
      de sa petite IA.

  (point 5) LA REMONTEE ARCHIVISTE -> BIBLIOTHECAIRE. Des que l'archiviste cree une
      categorie, une sous-categorie, un filtre ou un sous-filtre, on ECRIT un signal
      DATE (signal_plan.json) qui dit en clair ce qui est neuf. Le bibliothecaire le
      lit au lancement : il est AU COURANT, toujours. Plus de « lui il pouvait pas,
      il etait pas au courant ».

  (point 6) LE NOUVEAU PLAN REMPLACE L'ANCIEN. On reecrit le fichier en entier, d'un
      seul coup (ecriture a cote, puis remplacement). Pas d'empilement, pas de journal
      qui gonfle, pas deux versions du plan en meme temps. ET le plan ne remonte a
      Luciana QUE QUAND IL A CHANGE : on compare son EMPREINTE a celle que Luciana a
      deja vue. Jamais a chaque message.

      L'EMPREINTE PORTE LES NOMS DES ETAGES, PAS LES COMPTEURS. C'est voulu : si le
      compte des fiches entrait dans l'empreinte, le moindre souvenir range ferait
      « changer » le plan, et il remonterait a presque chaque message -- exactement ce
      que Fred refuse. Le plan change quand la FORME de la bibliotheque change.

NOTE IA : tout est ecrit en POSITIF (regle de Fred).
"""

import hashlib, json, os, time

try:
    import biblio2_archiviste as arch
except Exception:
    arch = None


def _fiches(arbre):
    """Toutes les fiches de l'arbre. On passe par l'archiviste (le seul qui sait comment
    l'arbre est pose sur le disque) ; s'il manque, on sait le faire ici aussi."""
    if arch is not None:
        try:
            return arch.toutes_les_fiches(arbre)
        except Exception:
            pass
    out = []
    for cat, sous_cats in (arbre or {}).items():
        if not isinstance(sous_cats, dict):
            continue
        for sous, fiches in sous_cats.items():
            if not isinstance(fiches, list):
                continue
            for fi in fiches:
                if isinstance(fi, dict):
                    out.append((cat, sous, fi))
    return out


# =====================================================================
#  POINT 4 — CONSTRUIRE LE PLAN, AUX QUATRE NIVEAUX.
# =====================================================================

def construire(arbre, version_avant=0, empreinte_avant=""):
    """Rend le PLAN COMPLET a quatre niveaux, a partir de l'arbre. Deterministe (les
    etages sont ranges par ordre alphabetique : deux arbres identiques donnent le meme
    plan, donc la meme empreinte). Ne leve jamais.

    'version' ne monte que si la FORME a change -- voir l'explication en tete de fichier."""
    rayons = {}
    for cat, sous, fi in _fiches(arbre):
        cat = str(cat or "(sans rayon)")
        sous = str(sous or "(sans tiroir)")
        filtre = str(fi.get("filtre") or "")
        sous_filtre = str(fi.get("sous_filtre") or "")
        if not filtre or not sous_filtre:
            # une fiche d'avant le chantier : on deduit ses niveaux 3 et 4 a la lecture,
            # pour que le plan soit complet sans avoir a tout reecrire.
            if arch is not None:
                try:
                    filtre, sous_filtre = arch.niveaux_3_et_4(fi.get("filtres"))
                except Exception:
                    filtre, sous_filtre = filtre or "Fait", sous_filtre or "General"
            else:
                filtre, sous_filtre = filtre or "Fait", sous_filtre or "General"

        R = rayons.setdefault(cat, {"fiches": 0, "en_suspens": 0, "sous_categories": {}})
        S = R["sous_categories"].setdefault(sous, {"fiches": 0, "filtres": {}})
        F = S["filtres"].setdefault(filtre, {"fiches": 0, "sous_filtres": {}})
        R["fiches"] += 1
        S["fiches"] += 1
        F["fiches"] += 1
        F["sous_filtres"][sous_filtre] = F["sous_filtres"].get(sous_filtre, 0) + 1
        if fi.get("en_suspens"):
            R["en_suspens"] += 1

    # on range tout par ordre alphabetique : le plan est alors toujours le meme pour le
    # meme contenu, et son empreinte est fiable.
    rayons = {c: {"fiches": R["fiches"], "en_suspens": R["en_suspens"],
                  "sous_categories": {s: {"fiches": S["fiches"],
                                          "filtres": {f: {"fiches": F["fiches"],
                                                          "sous_filtres": dict(sorted(F["sous_filtres"].items()))}
                                                      for f, F in sorted(S["filtres"].items())}}
                                      for s, S in sorted(R["sous_categories"].items())}}
              for c, R in sorted(rayons.items())}

    emp = empreinte(rayons)
    plan = {
        "_a_quoi_ca_sert": ("LE PLAN DE LA BIBLIOTHEQUE, a quatre niveaux : categorie > "
                            "sous-categorie > filtre > sous-filtre > la fiche. C'est la CARTE que "
                            "le bibliothecaire lit pour aller chercher par le sens. Cette version "
                            "REMPLACE l'ancienne : il n'y a jamais deux plans en meme temps."),
        "quand": time.strftime("%Y-%m-%d %H:%M:%S"),
        "empreinte": emp,
        "version": (int(version_avant or 0) if emp == (empreinte_avant or "")
                    else int(version_avant or 0) + 1),
        "chiffres": chiffres(rayons),
        "rayons": rayons,
    }
    return plan


def empreinte(rayons):
    """L'EMPREINTE DE LA FORME : les NOMS des quatre niveaux, sans les compteurs.
    Deux bibliotheques de meme forme ont la meme empreinte, meme si l'une a plus de
    fiches que l'autre. C'est ce qui evite de remonter le plan a chaque message."""
    lignes = []
    for cat, R in sorted((rayons or {}).items()):
        for sous, S in sorted((R.get("sous_categories") or {}).items()):
            for filtre, F in sorted((S.get("filtres") or {}).items()):
                for sf in sorted((F.get("sous_filtres") or {}).keys()):
                    lignes.append("%s|%s|%s|%s" % (cat, sous, filtre, sf))
    return hashlib.sha1("\n".join(lignes).encode("utf-8", "replace")).hexdigest()[:16]


def chiffres(rayons):
    """LES CHIFFRES DU PLAN, pour pouvoir DIRE l'avant / apres a Fred."""
    n_sous = n_filtres = n_sf = n_fiches = n_suspens = 0
    for _c, R in (rayons or {}).items():
        n_fiches += int(R.get("fiches") or 0)
        n_suspens += int(R.get("en_suspens") or 0)
        for _s, S in (R.get("sous_categories") or {}).items():
            n_sous += 1
            for _f, F in (S.get("filtres") or {}).items():
                n_filtres += 1
                n_sf += len(F.get("sous_filtres") or {})
    return {"rayons": len(rayons or {}), "sous_categories": n_sous, "filtres": n_filtres,
            "sous_filtres": n_sf, "fiches": n_fiches, "en_suspens": n_suspens}


# =====================================================================
#  POINT 6 — ECRIRE LE PLAN : LA NOUVELLE VERSION REMPLACE L'ANCIENNE.
# =====================================================================

def charger(chemin):
    """Le plan deja sur le disque, ou un plan vide. Ne leve jamais."""
    try:
        with open(chemin, encoding="utf-8-sig") as f:
            d = json.load(f)
        if isinstance(d, dict):
            d.setdefault("rayons", {})
            d.setdefault("version", 0)
            d.setdefault("empreinte", "")
            return d
    except Exception:
        pass
    return {"rayons": {}, "version": 0, "empreinte": "", "chiffres": chiffres({})}


def sauver(chemin, plan):
    """ECRITURE DE REMPLACEMENT, point 6 : on ecrit le plan ENTIER a cote, puis on
    remplace l'ancien d'un seul coup. Jamais d'empilement, jamais deux plans a la fois,
    et jamais un plan a moitie ecrit meme si le courant tombe."""
    dossier = os.path.dirname(os.path.abspath(chemin))
    if dossier:
        os.makedirs(dossier, exist_ok=True)
    tmp = chemin + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(plan, f, ensure_ascii=False, indent=2)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, chemin)
    return chemin


def a_change(plan, empreinte_deja_vue):
    """VRAI seulement si la FORME de la bibliotheque a change depuis la derniere fois.
    C'est la regle de Fred : le plan ne remonte a Luciana QUE quand il a change."""
    return str((plan or {}).get("empreinte") or "") != str(empreinte_deja_vue or "")


# =====================================================================
#  POINT 5 — LA REMONTEE ARCHIVISTE -> BIBLIOTHECAIRE : un signal ECRIT et DATE.
# =====================================================================

def nouveautes(plan_avant, plan_apres):
    """CE QUI EST NEUF entre deux plans, dit en clair, aux quatre niveaux. On compare les
    deux plans plutot que de faire confiance a un compte-rendu : meme si un rangement
    s'est passe ailleurs, ou si le programme s'est arrete en route, la comparaison voit
    tout. Ne leve jamais."""
    def etages(plan):
        r, sc, fl, sf = set(), set(), set(), set()
        for cat, R in ((plan or {}).get("rayons") or {}).items():
            r.add(cat)
            for sous, S in (R.get("sous_categories") or {}).items():
                sc.add((cat, sous))
                for filtre, F in (S.get("filtres") or {}).items():
                    fl.add((cat, sous, filtre))
                    for x in (F.get("sous_filtres") or {}):
                        sf.add((cat, sous, filtre, x))
        return r, sc, fl, sf

    r0, sc0, fl0, sf0 = etages(plan_avant)
    r1, sc1, fl1, sf1 = etages(plan_apres)
    neuf = []
    for c in sorted(r1 - r0):
        neuf.append({"niveau": 1, "quoi": "categorie", "chemin": c,
                     "dire": "nouvelle categorie « %s »" % c})
    for c, s in sorted(sc1 - sc0):
        neuf.append({"niveau": 2, "quoi": "sous_categorie", "chemin": "%s / %s" % (c, s),
                     "dire": "nouvelle sous-categorie « %s » dans « %s »" % (s, c)})
    for c, s, f in sorted(fl1 - fl0):
        neuf.append({"niveau": 3, "quoi": "filtre", "chemin": "%s / %s / %s" % (c, s, f),
                     "dire": "nouveau filtre « %s » dans « %s / %s »" % (f, c, s)})
    for c, s, f, x in sorted(sf1 - sf0):
        neuf.append({"niveau": 4, "quoi": "sous_filtre",
                     "chemin": "%s / %s / %s / %s" % (c, s, f, x),
                     "dire": "nouveau sous-filtre « %s » dans « %s / %s / %s »" % (x, c, s, f)})
    return neuf


SIGNAL_NOUVEAUTES_MAXI = 300    # point 6 : le signal reste petit, il ne gonfle pas


def signaler(chemin_signal, plan_avant, plan_apres):
    """ECRIT LE SIGNAL pour le bibliothecaire : date, version du plan, empreinte, et la
    liste en clair de ce qui vient d'etre cree. REMPLACE le signal precedent (point 6) :
    le bibliothecaire lit l'etat du jour, pas un journal qui s'allonge.

    Rend le signal ecrit. Ne leve jamais : si l'ecriture rate, on rend quand meme le
    signal en memoire, pour que l'appelant puisse le DIRE a Fred."""
    neuf = nouveautes(plan_avant, plan_apres)
    trop = max(0, len(neuf) - SIGNAL_NOUVEAUTES_MAXI)
    signal = {
        "_a_quoi_ca_sert": ("LA REMONTEE DE L'ARCHIVISTE AU BIBLIOTHECAIRE. Des que l'archiviste "
                            "cree un etage (categorie, sous-categorie, filtre ou sous-filtre), il "
                            "l'ecrit ici, date. Le bibliothecaire lit ce fichier : il est au "
                            "courant de tout. Ce fichier est REMPLACE a chaque fois, jamais empile."),
        "quand": time.strftime("%Y-%m-%d %H:%M:%S"),
        "version_du_plan": (plan_apres or {}).get("version", 0),
        "empreinte_du_plan": (plan_apres or {}).get("empreinte", ""),
        "le_plan_a_change": a_change(plan_apres, (plan_avant or {}).get("empreinte", "")),
        "combien_de_nouveautes": len(neuf),
        "nouveautes": neuf[:SIGNAL_NOUVEAUTES_MAXI],
        "nouveautes_non_listees": trop,
        "chiffres_avant": (plan_avant or {}).get("chiffres") or chiffres({}),
        "chiffres_apres": (plan_apres or {}).get("chiffres") or chiffres({}),
    }
    signal["pour_le_bibliothecaire"] = (
        "Le plan de la bibliotheque a change le %s (version %s) : %d etage(s) neuf(s). "
        "Relis plan.json avant de chercher." % (signal["quand"], signal["version_du_plan"], len(neuf))
    ) if signal["le_plan_a_change"] else (
        "Le plan de la bibliotheque est le meme qu'avant (version %s) : le bibliothecaire "
        "peut garder la carte qu'il connait." % signal["version_du_plan"])
    try:
        dossier = os.path.dirname(os.path.abspath(chemin_signal))
        if dossier:
            os.makedirs(dossier, exist_ok=True)
        tmp = chemin_signal + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(signal, f, ensure_ascii=False, indent=2)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, chemin_signal)
        signal["_ecrit_dans"] = chemin_signal
    except Exception as ex:
        signal["_ecriture_ratee"] = str(ex)[:160]
    return signal


def lire_signal(chemin_signal):
    """CE QUE LE BIBLIOTHECAIRE LIT AU LANCEMENT. Rend {} si le signal n'est pas encore
    la (la toute premiere fois) : ce n'est pas une panne, c'est juste un debut."""
    try:
        with open(chemin_signal, encoding="utf-8-sig") as f:
            d = json.load(f)
        return d if isinstance(d, dict) else {}
    except Exception:
        return {}


# =====================================================================
#  LE PLAN, DIT EN CLAIR : ce que le bibliothecaire met sous les yeux de sa petite IA,
#  et ce que Luciana recoit quand -- et seulement quand -- le plan a change.
# =====================================================================

def texte_pour_le_bibliothecaire(plan, maxi=None):
    """LA CARTE, aux quatre niveaux, en texte compact. C'est ce que le bibliothecaire LIT
    pour chercher (point 4) : il choisit un etage qui EXISTE, au lieu d'inventer un tiroir
    que le filtre ne trouverait jamais. 17/10/2026, DEMANDE DE FRED : LE PLAN EST TOUJOURS
    ENTIER, jamais coupe ('maxi' n'existe plus que pour un essai qui le demanderait). Ne leve jamais."""
    lignes = []
    for cat, R in ((plan or {}).get("rayons") or {}).items():
        lignes.append("- %s (%d)" % (cat, R.get("fiches") or 0))
        for sous, S in (R.get("sous_categories") or {}).items():
            lignes.append("   - %s (%d)" % (sous, S.get("fiches") or 0))
            for filtre, F in (S.get("filtres") or {}).items():
                sfs = ", ".join("%s (%d)" % (k, v) for k, v in (F.get("sous_filtres") or {}).items())
                lignes.append("      - %s : %s" % (filtre, sfs or "(aucun sous-filtre)"))
    texte = "\n".join(lignes) or "(la bibliotheque est encore vide)"
    if maxi and len(texte) > maxi:   # 17/10/2026 (Fred) : par defaut, le plan n'est JAMAIS coupe
        # on garde les premiers etages ENTIERS et on dit franchement ce qui est coupe
        coupe = texte[:maxi].rsplit("\n", 1)[0]
        restant = texte.count("\n") - coupe.count("\n")
        texte = coupe + "\n   ... et %d autre(s) ligne(s) de plan." % restant
    return texte


def texte_pour_luciana(plan):
    """LA PHRASE QUI REMONTE A LUCIANA -- et elle ne remonte QUE quand le plan a change
    (point 6). Courte par construction : elle donne la forme, pas le contenu."""
    c = (plan or {}).get("chiffres") or chiffres({})
    return ("LE PLAN DE TA MEMOIRE A CHANGE (version %s, le %s) : %d rayon(s), "
            "%d sous-categorie(s), %d filtre(s), %d sous-filtre(s), %d fiche(s) rangee(s)"
            "%s.\n%s"
            % ((plan or {}).get("version", 0), (plan or {}).get("quand", ""),
               c["rayons"], c["sous_categories"], c["filtres"], c["sous_filtres"], c["fiches"],
               (", dont %d en suspens (un doute a trancher)" % c["en_suspens"]) if c["en_suspens"] else "",
               texte_pour_le_bibliothecaire(plan)))


def rafraichir(arbre, chemin_plan, chemin_signal):
    """LE GESTE COMPLET, celui que l'archiviste appelle quand il a fini de ranger :
      1) on relit le plan d'avant (pour savoir ce qui est neuf et quelle version on en est) ;
      2) on refabrique le plan a partir de l'arbre ;
      3) on REMPLACE le plan sur le disque (point 6) ;
      4) on ECRIT le signal date pour le bibliothecaire (point 5).
    Rend (plan, signal). Ne leve jamais."""
    avant = charger(chemin_plan)
    apres = construire(arbre, version_avant=avant.get("version", 0),
                       empreinte_avant=avant.get("empreinte", ""))
    try:
        sauver(chemin_plan, apres)
    except Exception as ex:
        apres["_ecriture_ratee"] = str(ex)[:160]
    signal = signaler(chemin_signal, avant, apres)
    return apres, signal


if __name__ == "__main__":
    import tempfile
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

    def juge(s, _rayons):
        t = s["texte"].lower()
        if "voiture" in t:
            return {"categorie": "Vehicules", "sous_categorie": "Voitures",
                    "filtres": {"date": "2016-05-10", "objet": "voiture rouge", "type": "achat"},
                    "resume": "Clio rouge achetee en 2016.", "confiance": 0.9}
        if "docteur" in t:
            return {"categorie": "Sante", "sous_categorie": "Rendez-vous",
                    "filtres": {"date": "2024-03-02", "qui": ["Dr Martin"], "ou": "Lyon",
                                "type": "medical"}, "resume": "RDV chez le Dr Martin.",
                    "confiance": 0.85}
        return {"categorie": "Divers", "sous_categorie": "A trier", "filtres": {},
                "resume": "", "confiance": 0.2}

    souvenirs = [
        {"texte": "J'ai achete une voiture rouge en 2016.", "source": "essai"},
        {"texte": "Rendez-vous chez le docteur Martin a Lyon.", "source": "essai"},
    ]
    arbre = {}
    for s in souvenirs:
        s["repere"] = arch.repere_de("essai", s["texte"])
        arch.ranger(arbre, s, arch.valider_jugement(juge(s, arbre)))

    dossier = tempfile.mkdtemp(prefix="essai_plan_")
    f_plan = os.path.join(dossier, "plan.json")
    f_signal = os.path.join(dossier, "signal_plan.json")

    print("=== LE PLAN, AUX QUATRE NIVEAUX ===")
    plan, signal = rafraichir(arbre, f_plan, f_signal)
    print(texte_pour_le_bibliothecaire(plan))
    print("\nchiffres :", plan["chiffres"])

    print("\n=== CONTROLES ===")
    controle("point 4 : les quatre niveaux sont dans le plan",
             "Vehicules" in plan["rayons"]
             and "Voitures" in plan["rayons"]["Vehicules"]["sous_categories"]
             and "Achat" in plan["rayons"]["Vehicules"]["sous_categories"]["Voitures"]["filtres"]
             and "Voiture rouge" in (plan["rayons"]["Vehicules"]["sous_categories"]["Voitures"]
                                     ["filtres"]["Achat"]["sous_filtres"]))
    controle("point 4 : le plan compte bien les fiches", plan["chiffres"]["fiches"] == 2)
    controle("point 4 : le plan est ECRIT sur le disque", os.path.exists(f_plan))
    controle("point 5 : le signal est ECRIT et DATE",
             os.path.exists(f_signal) and len(lire_signal(f_signal).get("quand") or "") >= 10)
    controle("point 5 : le signal NOMME les nouveautes aux 4 niveaux",
             {n["niveau"] for n in signal["nouveautes"]} == {1, 2, 3, 4})
    controle("point 5 : le signal dit que le plan a change", signal["le_plan_a_change"] is True)
    controle("point 6 : premiere ecriture -> version 1", plan["version"] == 1)

    # on refait le plan SANS rien changer : la version ne doit PAS bouger, et le plan ne
    # doit PAS etre signale comme change (sinon il remonterait a Luciana pour rien).
    taille_avant = os.path.getsize(f_plan)
    plan2, signal2 = rafraichir(arbre, f_plan, f_signal)
    controle("point 6 : rien n'a change -> la version reste la meme", plan2["version"] == 1)
    controle("point 6 : rien n'a change -> le plan ne remonte PAS a Luciana",
             signal2["le_plan_a_change"] is False and not a_change(plan2, plan["empreinte"]))
    controle("point 6 : le plan REMPLACE l'ancien (le fichier ne gonfle pas)",
             os.path.getsize(f_plan) == taille_avant)

    # on ajoute un souvenir dans un rayon NEUF : le plan doit changer, et le signal le dire
    s3 = {"texte": "J'ai achete une voiture bleue en 2020.", "source": "essai"}
    s3["repere"] = arch.repere_de("essai", s3["texte"])
    arch.ranger(arbre, s3, arch.valider_jugement(
        {"categorie": "Vehicules", "sous_categorie": "Voitures",
         "filtres": {"date": "2020-01-01", "objet": "voiture bleue", "type": "achat"},
         "resume": "Voiture bleue, 2020.", "confiance": 0.9}))
    plan3, signal3 = rafraichir(arbre, f_plan, f_signal)
    controle("point 5 : un sous-filtre neuf est remonte au bibliothecaire",
             any("Voiture bleue" in n["chemin"] for n in signal3["nouveautes"]))
    controle("point 6 : la forme a change -> la version monte a 2", plan3["version"] == 2)
    controle("point 6 : le signal garde SEULEMENT les dernieres nouveautes (il ne s'empile pas)",
             signal3["combien_de_nouveautes"] == 1)
    controle("le bibliothecaire peut LIRE la carte des 4 niveaux",
             "Voiture bleue" in texte_pour_le_bibliothecaire(plan3))

    print("\n=== LE SIGNAL TEL QUE LE BIBLIOTHECAIRE LE LIT ===")
    print(lire_signal(f_signal)["pour_le_bibliothecaire"])

    print("\n%s" % ("TOUT EST PASSE." if not rate else
                    "TESTS QUI RATENT (%d) :\n  - %s" % (len(rate), "\n  - ".join(rate))))
