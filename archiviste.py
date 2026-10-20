# -*- coding: utf-8 -*-
# =====================================================================
#  L'ARCHIVISTE — il POSE DES ETIQUETTES sur les morceaux de la bibliotheque.
#  Chantier du 07/10/2026, demande de Fred. UN SEUL SUJET : les etiquettes.
#
#  CE QU'IL NE FAIT PAS, ET C'EST LE PLUS IMPORTANT :
#   - il ne reorganise RIEN, ne deplace RIEN, ne supprime RIEN, n'ajoute RIEN a la bibliotheque ;
#   - il OUVRE LA BIBLIOTHEQUE EN LECTURE SEULE. Pas un octet n'est ecrit dans bibliotheque\,
#     ni dans carnet.json, souvenirs.json, consignes.jsonl, plan_bibliotheque.json,
#     noms_propres.json, journal_tiroirs.jsonl ;
#   - il ne touche pas au moteur du sens (~\Luciana_sens) : il ne le lit meme pas ;
#   - il ne touche pas a luciana.py ;
#   - il ne fait AUCUN APPEL PAYE. Zero centime, 100 % Python sur le PC.
#
#  LES SEULS FICHIERS QU'IL ECRIT (et rien d'autre) :
#   1) ~\Luciana\etiquettes_essai.jsonl          <- les etiquettes, une par ligne
#   2) ~\Luciana\etiquettes_essai_rapport.json   <- les comptes + les empreintes avant/apres
#   3) ~\Luciana\sauvegardes_archiviste\<date>\  <- la copie datee des deux fichiers ci-dessus
#                                                  s'ils existaient deja (rien n'est jamais ecrase)
#   4) ~\Luciana\etiquettes_des_avis.jsonl       <- v136 : les etiquettes NEUVES des passages de
#                                                  conversation ranges dans un tiroir cree par les
#                                                  avis de Luciana (voir le pave v136 plus bas).
#                                                  Refabrique a chaque passe depuis le journal des
#                                                  avis : rien ne peut y etre perdu.
#  ~\Luciana\avis_de_luciana.jsonl est LU, jamais ecrit : c'est luciana.py qui l'ecrit.
#
#  L'ETIQUETTE A SIX CHAMPS (demande de Fred) :
#   1 date   2 tiroir   3 sujet   4 personnes   5 resume (une phrase)   6 STATUT
#  Le 6e est le neuf et c'est celui qui compte : sans lui, une decision MORTE et la decision
#  VIVANTE qui l'a remplacee se ressemblent a l'identique pour le moteur du sens.
#
#  LA REGLE DE L'ARCHIVISTE : IL NE DEVINE JAMAIS.
#  Une etiquette fausse est pire qu'une etiquette absente, parce qu'on filtre dessus. Donc :
#   - tout ce qui est MECANIQUE (lisible noir sur blanc dans les fichiers) est rempli ;
#   - partout ailleurs il ecrit "a trancher" et il s'arrete la ;
#   - quand il voit un INDICE de mort ("projet clos", "obsolete", une echeance passee), il le note
#     dans "indices_statut" avec la citation, MAIS IL NE CHANGE PAS LE STATUT. L'indice sert a
#     trancher vite a la main ; il ne decide pas tout seul.
#
#  D'OU VIENNENT LES REGLES COPIEES ICI (rien n'est reinvente) :
#   - _MOTS_EN_REPOS / _MOTS_ECHEANCE / _DATE_DANS_TEXTE : copies de luciana.py (~ligne 4098),
#     la liste deja validee par Fred pour reperer une consigne qui dort.
#   - consignes_actives() : la meme relecture ligne par ligne que luciana.py (~ligne 3066).
#   - _slug() : le meme calcul de nom de dossier que luciana.py (~ligne 17503).
#   - _noms_propres() / _noms_dans() : la meme regle d'etiquettes que luciana.py (~ligne 1533).
#   Elles sont RECOPIEES et pas importees : importer luciana.py demarrerait le serveur.
#
#  CHANTIER DU 07/10/2026 (v134) — CE QUI A CHANGE, ET RIEN D'AUTRE :
#   * LE RESUME EST REPARE. Il valait "a trancher" sur 290 etiquettes sur 300 ; il est maintenant
#     RECOPIE d'un endroit precis de chaque fichier (voir le pave "LE RESUME" plus bas).
#   * Les souvenirs recoivent enfin une date ("inconnue", qui est la verite), un tiroir
#     ("souvenirs") et un sujet (le debut du souvenir). Leur STATUT reste "a trancher" : rien
#     dans souvenirs.json ne dit qu'un souvenir en remplace un autre, et on ne devine pas.
#   * Les lignes VIDES de consignes.jsonl ne recoivent PLUS d'etiquette (c'etait du bruit pur).
#     Attention : une ligne de RETRAIT n'a pas de texte et n'est pas vide pour autant ; elle est
#     gardee, parce que c'est elle qui tue la consigne qu'elle retire.
#   * Le rapport donne les chiffres demandes par Fred : lus, poses, resume rempli, resume encore
#     a trancher, vides sautes, erreurs.
#   Ce chantier N'A PAS TOUCHE a luciana.py : le numero de version et le badge de Luciana ne
#   bougent donc pas. C'est normal, ce n'est pas un oubli.
#
#  COMMENT ON S'EN SERT (dans une fenetre de commande, dans le dossier du programme) :
#     python archiviste.py --combien 0          -> TOUS les morceaux (LA COMMANDE DE REFERENCE)
#     python archiviste.py                      -> echantillon de 300 morceaux
#     python archiviste.py --combien 300        -> pareil, dit en clair
#     python archiviste.py --lister             -> la liste des morceaux et leur identifiant
#     python archiviste.py --lister --contient domaine
#     python archiviste.py --voir <identifiant> -> montre UN morceau et son etiquette, sans rien ecrire
#     python archiviste.py --etiqueter <identifiant>    -> etiqueter UN morceau A LA MAIN
#     python archiviste.py --avis               -> v136 : les avis de Luciana et ce qu'ils FERAIENT,
#                                                  sans rien ecrire (le regard, pas la main)
#     python _verif_archiviste.py               -> le controle (comptes + la bibliotheque a-t-elle bouge)
#     python _verif_v136_avis.py                -> le controle du chantier des avis (v136)
#
#  CHANTIER DU 07/10/2026 (v136) — CE QUI A CHANGE, ET RIEN D'AUTRE :
#   * L'ARCHIVISTE LIT LES AVIS DE LUCIANA et, au bout de TROIS rejets du MEME passage, il cree un
#     nouveau tiroir et y range le passage. En dessous de trois : il NOTE, et rien ne bouge.
#     Tout est explique dans le pave "v136" plus bas, avec ce qui marche et ce qui ne marche pas
#     encore. Rien d'autre du travail de l'archiviste n'a ete touche.
# =====================================================================
import argparse
import hashlib
import io
import json
import os
import re
import shutil
import sys
import time
import unicodedata

# Les noms de tiroirs de Fred contiennent des accents et des tirets longs ("Luciana - comment elle
# marche" s'ecrit chez lui avec un tiret cadratin). Quand la sortie part dans un fichier ou dans un
# tuyau, Windows retombe sur son vieux jeu de caracteres et le programme PLANTE en plein affichage.
# On force donc l'affichage en UTF-8, et on remplace ce qui ne passe pas au lieu de s'arreter.
for _flux in (sys.stdout, sys.stderr):
    try:
        _flux.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# ---------- OU SONT LES CHOSES (exactement comme luciana.py) ----------
HOME = os.path.expanduser("~")
DOSSIER = os.path.join(HOME, "Luciana")

DOSSIER_BIBLIO = os.path.join(DOSSIER, "bibliotheque")
FICHIER_PLAN = os.path.join(DOSSIER, "plan_bibliotheque.json")
FICHIER_CARNET = os.path.join(DOSSIER, "carnet.json")
FICHIER_SOUVENIRS = os.path.join(DOSSIER, "souvenirs.json")
FICHIER_CONSIGNES = os.path.join(DOSSIER, "consignes.jsonl")
FICHIER_NOMS_PROPRES = os.path.join(DOSSIER, "noms_propres.json")

# LES SEULES SORTIES. Elles sont A PART : la bibliotheque n'est pas modifiee d'un octet.
FICHIER_ETIQUETTES = os.path.join(DOSSIER, "etiquettes_essai.jsonl")
FICHIER_RAPPORT = os.path.join(DOSSIER, "etiquettes_essai_rapport.json")
DOSSIER_SAUVEGARDES = os.path.join(DOSSIER, "sauvegardes_archiviste")

ECHANTILLON_PAR_DEFAUT = 300
A_TRANCHER = "a trancher"
STATUTS = ("vivant", "annule", "remplace", A_TRANCHER)

# Ce que l'archiviste note une fois pour toutes a cote du champ "personnes", pour que personne ne
# se trompe sur ce que ce champ contient VRAIMENT chez Fred aujourd'hui.
_D_OU_PERSONNES = ("noms reconnus par la MEME regle que luciana.py (_noms_propres : les mots en "
                   "Majuscule des noms de carnets + noms_propres.json). ATTENTION : chez Fred, "
                   "noms_propres.json est VIDE ('ajouter' et 'retirer' a zero), donc ce sont "
                   "surtout des noms de PROJETS, pas de personnes. Pour avoir les vraies "
                   "personnes (Daniela, Angelova, Kyosev...), il suffit de les ecrire dans "
                   "noms_propres.json > 'ajouter' : l'archiviste les prendra sans changer une "
                   "ligne de code.")


# =====================================================================
#  LES PETITS OUTILS RECOPIES DE luciana.py (meme calcul, meme resultat)
# =====================================================================
def _sans_accents(t):
    """Recopie de luciana.py (~ligne 2381)."""
    return "".join(c for c in unicodedata.normalize("NFD", str(t or "").lower())
                   if unicodedata.category(c) != "Mn")


def _slug(nom):
    """Recopie de luciana.py (~ligne 17503). C'est ce calcul qui a donne leurs noms aux dossiers
    de la bibliotheque : "Luciana - mon fonctionnement" -> "luciana-mon-fonctionnement"."""
    s = re.sub(r"[^a-z0-9]+", "-", _sans_accents(nom).strip()).strip("-")
    return s[:60] or "sans-nom"


# Recopie de luciana.py (~ligne 1259 et ~1526) : les mots qui ne sont jamais des noms propres.
_MOTS_VIDES = set("""alors aussi autre avant avec avoir bien bon bonne cela celle celui cest cette comme comment dans
depuis donc elle elles encore entre etait etre faire fait faut fois font hein ici juste leur leurs lui mais meme
merci mieux moins mon mes notre nous parce pas peut plus pour pourquoi quand quel quelle quelque quoi sais sans
sera ses sont sous suis sur tant tes tien tiens tjrs toi ton tous tout toute toutes tres trop une vais veux vos
votre vous voila voilà ouais oui non euh bah ben bref chose choses truc trucs faire dire dit peux pouvez pourrais
luciana fred aujourd demain hier matin soir maintenant jamais toujours""".split())
_MOTS_PAS_DES_NOMS = set("""projet projets site sites chantier chantiers dossier dossiers version versions client
clients mail mails compta facture factures audit plan page pages video videos formation formations fred
luciana bibliotheque memoire carnet carnets consigne consignes outil outils travail travaux suivi idee idees
liste note notes rendez vous agenda photo photos texte textes document documents fichier fichiers ancien
nouveau nouvelle grand grande petit petite general generale divers""".split()) - {"luciana"}

# Recopie de luciana.py (~ligne 4098) : les mots qui disent qu'une chose est FINIE, et ceux qui
# annoncent une echeance. Liste deja validee par Fred ; on ne la reinvente pas.
_MOTS_EN_REPOS = ("bug repare", "bug corrige", "c'est repare", "c'est corrige", "deja repare",
                  "chantier termine", "chantier fini", "projet clos", "projet termine",
                  "projet abandonne", "affaire classee", "plus la peine", "n'est plus d'actualite",
                  "plus d'actualite", "ca ne sert plus", "ne sert plus a rien", "obsolete")
_MOTS_ECHEANCE = ("jusqu'au", "jusqu'a", "avant le", "d'ici le", "pour le", "au plus tard le",
                  "le temps de", "cette semaine", "ce week-end")
_DATE_DANS_TEXTE = re.compile(r"(\d{4})-(\d{2})-(\d{2})|(\d{1,2})/(\d{1,2})/(\d{4})")
DATE_SANS_LIMITE = "2999-12-31"   # recopie de luciana.py (~ligne 2851)

# Des mots que Fred emploie quand il ANNULE ou REMPLACE quelque chose. Ils ne servent QU'A poser un
# indice ; ils ne changent JAMAIS le statut tout seuls (sinon on devinerait, et c'est interdit).
# Liste volontairement courte et sans doublons : "annule" attrape deja "annulee" et "annulation".
_MOTS_INDICE_MORT = ("annule", "abandonne", "laisse tomber", "on ne fait plus", "finalement non",
                     "remplace par", "remplacee par", "ce n'est plus la peine", "on arrete",
                     "on oublie", "erreur de ma part", "fausse piste", "plus besoin",
                     "on change d'avis", "contrordre")


def _dates_du_texte(texte):
    """Recopie de luciana.py (~ligne 4107). Les dates ecrites dans un texte, en AAAA-MM-JJ."""
    trouvees = []
    for m in _DATE_DANS_TEXTE.finditer(str(texte or "")):
        if m.group(1):
            trouvees.append("%s-%s-%s" % (m.group(1), m.group(2), m.group(3)))
        else:
            try:
                trouvees.append("%s-%02d-%02d" % (m.group(6), int(m.group(5)), int(m.group(4))))
            except Exception:
                pass
    return trouvees


def _lire_texte(chemin):
    """Lit un fichier en LECTURE SEULE. Ne leve jamais : un fichier illisible rend None, et
    l'appelant le compte comme une ERREUR. Un fichier illisible n'est jamais pris pour un
    fichier vide : on ne fabrique pas de morceau a partir de rien."""
    try:
        with io.open(chemin, "r", encoding="utf-8", errors="replace") as f:
            return f.read()
    except Exception:
        return None


def _charger_json(chemin, defaut):
    t = _lire_texte(chemin)
    if t is None:
        return defaut
    try:
        return json.loads(t)
    except Exception:
        return defaut


def _lignes_jsonl(chemin):
    """Rend (numero de ligne dans le fichier, dictionnaire). Une ligne illisible est rendue avec
    None a la place du dictionnaire : on la compte comme erreur, on ne l'invente pas."""
    t = _lire_texte(chemin)
    if t is None:
        return []
    sorties = []
    for n, ligne in enumerate(t.splitlines(), 1):
        ligne = ligne.strip()
        if not ligne:
            continue
        try:
            d = json.loads(ligne)
        except Exception:
            d = None
        sorties.append((n, d))
    return sorties


# =====================================================================
#  LES ETIQUETTES DE NOMS (meme regle que luciana.py, en LECTURE SEULE)
#  Difference voulue avec luciana.py : luciana.py CREE noms_propres.json s'il manque.
#  L'archiviste, lui, n'ecrit JAMAIS dans le dossier de Fred : s'il manque, il s'en passe.
# =====================================================================
def noms_propres():
    noms = {"luciana", "luminita"}
    carnet = _charger_json(FICHIER_CARNET, {})
    if isinstance(carnet, dict):
        for cle in carnet.keys():
            for mot in re.findall(r"[A-Za-zÀ-ÿ][A-Za-zÀ-ÿ'-]{2,}", str(cle)):
                if mot[0].isupper():
                    m = _sans_accents(mot.strip("'-"))
                    if len(m) >= 3 and m not in _MOTS_PAS_DES_NOMS and m not in _MOTS_VIDES:
                        noms.add(m)
    d = _charger_json(FICHIER_NOMS_PROPRES, None)
    if isinstance(d, dict):
        noms.update(_sans_accents(x) for x in (d.get("ajouter") or []) if str(x).strip())
        noms.difference_update(_sans_accents(x) for x in (d.get("retirer") or []))
    return sorted(n for n in noms if n)


def noms_dans(texte, noms):
    """Recopie de luciana.py (~ligne 1575) : les noms presents en MOTS ENTIERS (pas 'lumi' dans
    'lumiere'). On ne retire pas l'interpellation ici : on etiquette un morceau de bibliotheque,
    pas la phrase que Fred vient de taper."""
    t = _sans_accents(texte)
    return sorted(n for n in noms
                  if re.search(r"(?<![a-z0-9])%s(?![a-z0-9])" % re.escape(n), t))


# =====================================================================
#  LE PLAN : il donne, pour chaque tiroir, son titre et son etat (actif / dort / clos)
# =====================================================================
def charger_plan():
    """Rend deux dictionnaires : par slug de NOM de tiroir, et par slug de CATEGORIE (le rayon).
    Les dossiers de la bibliotheque portent tantot un nom de tiroir, tantot un nom de rayon :
    on regarde les deux, et on dit lequel a repondu."""
    plan = _charger_json(FICHIER_PLAN, {}) or {}
    tiroirs = plan.get("tiroirs") if isinstance(plan, dict) else None
    par_nom, par_categorie = {}, {}
    for t in (tiroirs or []):
        if not isinstance(t, dict):
            continue
        nom = str(t.get("nom") or "").strip()
        if nom:
            par_nom[_slug(nom)] = t
        cat = str(t.get("categorie") or "").strip()
        if cat and _slug(cat) not in par_categorie:
            par_categorie[_slug(cat)] = t
    return par_nom, par_categorie


# =====================================================================
#  L'INVENTAIRE : QUELS SONT LES "MORCEAUX" DE LA BIBLIOTHEQUE
#  Quatre sources, et c'est tout ce que Luciana sert comme memoire longue :
#   - bibliotheque\  : un morceau = UN FICHIER (.md / .txt). C'est ainsi qu'elle les sert.
#   - carnet.json    : un morceau = UN TIROIR (son etat courant).
#   - souvenirs.json : un morceau = UN SOUVENIR (une ligne de la liste).
#   - consignes.jsonl: un morceau = UNE LIGNE du fichier (un ajout, une correction, un retrait).
#  archive_outils.jsonl n'en fait PAS partie : ce sont des resultats d'outils, pas des decisions.
# =====================================================================
_NOM_JOURNEE = re.compile(r"journee[-_](\d{4}-\d{2}-\d{2})")
_NOM_DATE = re.compile(r"(\d{4}-\d{2}-\d{2})")


def _date_du_nom_de_fichier(nom):
    m = _NOM_JOURNEE.search(nom) or _NOM_DATE.search(nom)
    return m.group(1) if m else ""


def _ou_est_rangee_la_fiche(relatif, nom_fichier):
    """Rend (rangement technique, niveau 1, niveau 2) pour une fiche de la bibliotheque.
    Deux rangements techniques existent chez Fred, et ils cachent le vrai tiroir :
      - anciennes_versions\\<date>\\<tiroir>__<sous-tiroir>__<fiche>_HHhMMSS.md
        -> le tiroir est ECRIT DANS LE NOM DU FICHIER, avant le premier "__" ;
      - _doublons_<date>\\<tiroir>\\<sous-tiroir>\\<fiche>.md
        -> le tiroir est un cran plus bas.
    Dans les deux cas on va chercher le vrai tiroir au bon endroit : c'est de la lecture de
    chemin, pas une supposition."""
    bouts = relatif.split("/")
    bas = bouts[0].lower()
    if bas == "anciennes_versions":
        parts = nom_fichier.rsplit(".", 1)[0].split("__")
        if len(parts) >= 2:
            return "anciennes_versions", parts[0], parts[1]
        return "anciennes_versions", "", ""
    if bas.startswith("_doublons"):
        return ("_doublons",
                bouts[1] if len(bouts) > 2 else "",
                bouts[2] if len(bouts) > 3 else "")
    return ("",
            bouts[0] if len(bouts) > 1 else "",
            bouts[1] if len(bouts) > 2 else "")


def inventaire(erreurs):
    """La liste de TOUS les morceaux, en lecture seule. 'erreurs' se remplit tout seul : on dit
    ce qu'on n'a pas su lire, on ne le passe pas sous le tapis."""
    morceaux = []

    # ---- 1) le dossier bibliotheque ----
    if os.path.isdir(DOSSIER_BIBLIO):
        for racine, dossiers, fichiers in os.walk(DOSSIER_BIBLIO):
            dossiers.sort()
            for nom in sorted(fichiers):
                if not nom.lower().endswith((".md", ".txt")):
                    continue
                chemin = os.path.join(racine, nom)
                relatif = os.path.relpath(chemin, DOSSIER_BIBLIO).replace("\\", "/")
                texte = _lire_texte(chemin)
                if texte is None:
                    erreurs.append({"quoi": "fichier illisible", "ou": chemin})
                    continue
                technique, niveau1, niveau2 = _ou_est_rangee_la_fiche(relatif, nom)
                morceaux.append({
                    "id": "biblio:" + relatif,
                    "source": "bibliotheque",
                    "chemin": chemin,
                    "relatif": relatif,
                    "rangement_technique": technique,
                    "niveau1": niveau1,
                    "niveau2": niveau2,
                    "nom_fichier": nom,
                    "texte": texte,
                })

    # ---- 2) carnet.json ----
    carnet = _charger_json(FICHIER_CARNET, None)
    if carnet is None:
        erreurs.append({"quoi": "carnet.json illisible", "ou": FICHIER_CARNET})
    elif isinstance(carnet, dict):
        for nom in sorted(carnet.keys()):
            v = carnet.get(nom)
            etat = v.get("etat") if isinstance(v, dict) else v
            morceaux.append({
                "id": "carnet:" + str(nom),
                "source": "carnet",
                "chemin": FICHIER_CARNET,
                "nom_tiroir": str(nom),
                "maj": str(v.get("maj") or "") if isinstance(v, dict) else "",
                "texte": str(etat or ""),
            })

    # ---- 3) souvenirs.json ----
    souvenirs = _charger_json(FICHIER_SOUVENIRS, None)
    if souvenirs is None:
        erreurs.append({"quoi": "souvenirs.json illisible", "ou": FICHIER_SOUVENIRS})
    elif isinstance(souvenirs, list):
        for i, s in enumerate(souvenirs):
            morceaux.append({
                "id": "souvenir:%d" % i,
                "source": "souvenirs",
                "chemin": FICHIER_SOUVENIRS,
                "rang": i,
                "texte": str(s or ""),
            })

    # ---- 4) consignes.jsonl ----
    for n, d in _lignes_jsonl(FICHIER_CONSIGNES):
        if d is None:
            erreurs.append({"quoi": "ligne de consignes.jsonl illisible",
                            "ou": "%s ligne %d" % (FICHIER_CONSIGNES, n)})
            continue
        morceaux.append({
            "id": "consigne:L%d" % n,
            "source": "consignes",
            "chemin": FICHIER_CONSIGNES,
            "ligne": n,
            "numero": d.get("numero"),
            "action": str(d.get("action") or "ajouter"),
            "date_ecrite": str(d.get("date") or ""),
            "importance": str(d.get("importance") or ""),
            "texte": str(d.get("texte") or ""),
        })

    return morceaux


# =====================================================================
#  LE STATUT DES CONSIGNES : 100 % MECANIQUE, RIEN N'EST DEVINE
#  consignes.jsonl est un journal : il n'est jamais reecrit, on ne fait qu'y AJOUTER des lignes.
#  Donc le fichier DIT LUI-MEME ce qui est mort :
#   - une ligne dont le numero est ensuite "oublie" / "retire" / "supprime" -> ANNULE ;
#   - une ligne dont le numero recoit ensuite un nouveau texte             -> REMPLACE ;
#   - la derniere ligne qui porte le texte d'un numero encore vivant       -> VIVANT.
#  C'est exactement la relecture que fait consignes_actives() dans luciana.py (~ligne 3066).
# =====================================================================
def statuts_des_consignes(morceaux):
    par_numero = {}
    for m in morceaux:
        if m["source"] != "consignes":
            continue
        try:
            num = int(m.get("numero") or 0)
        except Exception:
            num = 0
        if not num:
            continue
        par_numero.setdefault(num, []).append(m)

    statuts = {}
    for num, lignes in par_numero.items():
        lignes.sort(key=lambda x: x["ligne"])
        # On rejoue le journal dans l'ordre, exactement comme luciana.py.
        porteuse = None        # la ligne qui porte, pour l'instant, le texte vivant du numero
        for m in lignes:
            action = _sans_accents(m.get("action")).strip()
            if action.startswith(("oubli", "retir", "suppr")):
                if porteuse is not None:
                    statuts[porteuse["id"]] = (
                        "annule",
                        "consignes.jsonl dit lui-meme que la consigne n%d a ete '%s' a la ligne %d"
                        " (%s)" % (num, m.get("action"), m["ligne"], m.get("date_ecrite") or "sans date"))
                    porteuse = None
                statuts[m["id"]] = (
                    "annule",
                    "cette ligne EST le retrait de la consigne n%d ('%s')" % (num, m.get("action")))
                continue
            if not str(m.get("texte") or "").strip():
                # Meme regle que luciana.py : une ligne sans texte ne change rien.
                statuts[m["id"]] = (A_TRANCHER,
                                    "a trancher : ligne sans texte, elle ne change rien au carnet")
                continue
            if porteuse is not None:
                statuts[porteuse["id"]] = (
                    "remplace",
                    "la consigne n%d a recu un nouveau texte a la ligne %d (%s)"
                    % (num, m["ligne"], m.get("date_ecrite") or "sans date"))
            porteuse = m
        if porteuse is not None:
            statuts[porteuse["id"]] = (
                "vivant",
                "derniere ligne qui porte le texte de la consigne n%d, et aucun retrait apres"
                % num)
    return statuts


# =====================================================================
#  LES INDICES DE MORT : on les NOTE, on ne tranche pas avec.
# =====================================================================
def indices_statut(texte, aujourd_hui):
    t = _sans_accents(texte)
    trouves = []
    for mot in _MOTS_EN_REPOS + _MOTS_INDICE_MORT:
        place = t.find(_sans_accents(mot))
        if place < 0:
            continue
        debut = max(0, place - 60)
        extrait = re.sub(r"\s+", " ", texte[debut:place + len(mot) + 90]).strip()
        trouves.append({"mot": mot, "extrait": extrait})
        if len(trouves) >= 6:
            break
    if any(_sans_accents(mot) in t for mot in _MOTS_ECHEANCE):
        dates = [d for d in _dates_du_texte(texte) if d < DATE_SANS_LIMITE]
        if dates and all(d < aujourd_hui for d in dates):
            trouves.append({"mot": "echeance passee",
                            "extrait": "toutes les dates du morceau sont passees (%s ; nous sommes "
                                       "le %s)" % (", ".join(sorted(set(dates))[:6]), aujourd_hui)})
    return trouves


# =====================================================================
#  LA PREMIERE PHRASE ET LE RESUME  —  LE COEUR, REPARE LE 07/10/2026
#
#  CE QUI N'ALLAIT PAS, ET C'EST MESURE, PAS SUPPOSE : apres l'essai de 300 etiquettes du
#  07/10/2026, le champ "resume" valait "a trancher" sur 290 etiquettes sur 300. Or c'est LE
#  champ qui doit faire gagner un petit carnet precis contre un gros bavard. Sans lui,
#  l'archiviste ne sert a rien : c'est le coeur qui manquait.
#  LA CAUSE : l'ancienne version ne remplissait le resume QUE si le morceau contenait une ligne
#  "BUT : ..." ecrite noir sur blanc. Presque aucun morceau n'en a une.
#
#  CE QU'ON FAIT MAINTENANT — ET CE N'EST TOUJOURS PAS DEVINER :
#  on ne FABRIQUE aucune phrase. On RECOPIE une phrase qui existe DEJA dans les fichiers, et on
#  dit d'ou elle sort, mot pour mot. Un resume recopie est un FAIT ; une phrase inventee serait
#  un avis, et "une etiquette fausse est pire qu'une etiquette absente".
#  Par source, dans cet ordre ; le premier qui repond gagne :
#
#   - carnet.json      (a) les champs "contient" et "quand" du tiroir dans plan_bibliotheque.json
#                          (ces deux champs-la ont ete ecrits EXPRES pour dire ce qu'il y a dedans
#                           et quand le tiroir sort : c'est la meilleure source possible) ;
#                      (b) sinon la ligne "BUT : ..." du contenu du carnet ;
#                      (c) sinon la premiere phrase non vide du contenu.
#   - souvenirs.json   les 300 premiers caracteres du souvenir. souvenirs.json est une simple
#                      liste de phrases : le souvenir EST sa propre phrase, il n'y a rien d'autre.
#   - consignes.jsonl  le texte de la consigne, coupe a 300.
#   - bibliotheque\    (a) la ligne "BUT : ..." si elle y est (c'est elle qui remplissait deja les
#                          20 resumes qui marchaient : on ne casse pas ce qui marche) ;
#                      (b) sinon le PREMIER PARAGRAPHE non vide du fichier, coupe a 300.
#
#  S'IL N'Y A VRAIMENT RIEN A RECOPIER (contenu vide, illisible), le resume reste "a trancher",
#  sa provenance dit "Rien a recopier", et le rapport les compte A PART
#  ("resume_a_trancher_faute_de_texte"). On ne bouche pas le trou avec une phrase inventee.
#
#  NOTE HONNETE SUR LA LIGNE "BUT :". Trois carnets de Fred ("Robot physique pour Luciana",
#  "La voix qui parle", "Business reprogrammation auto") commencent par "BUT : ..." et l'ancienne
#  version ne les a pas repris. Je N'AI PAS PU lire ces trois carnets d'ici (carnet.json est dans
#  C:\Users\Fred\Luciana, hors d'atteinte de ce chantier), donc je ne sais pas POURQUOI la ligne
#  n'a pas repondu. Deux causes probables : un tiret long ("BUT — ...") au lieu des deux-points,
#  ou une decoration markdown devant. La reconnaissance a donc ete ELARGIE aux tirets longs et a
#  la decoration de debut de ligne. ET SURTOUT : ces trois carnets auront de toute facon un resume
#  par le chemin (a) ou (c) ci-dessus. La question n'est plus bloquante.
#
#  "premiere_phrase" reste a cote, inchangee : c'est une AIDE citee mot pour mot, et ce n'est PAS
#  le resume. Les deux champs restent distincts pour qu'on ne les confonde pas.
# =====================================================================
# =====================================================================
#  v136 (chantier du 07/10/2026, demande de Fred) : L'ARCHIVISTE APPREND DES AVIS DE LUCIANA.
#
#  LA CORRECTION DE CIBLE, ET C'EST LE COEUR : le BIBLIOTHECAIRE ne fait que CHERCHER. Celui qui
#  RANGE et qui CREE les tiroirs, c'est L'ARCHIVISTE. C'est donc ICI que les avis arrivent.
#
#  CE QUE FRED A DIT, MOT POUR MOT (07/10/2026, ~16h45) :
#    "c'est pas a nous de creer des tiroirs, c'est au bibliothecaire et a l'archiviste"
#    "si on se projette dans le long terme, le fait que toi quand tu les recois tu les analyses et
#     tu lui dis non ca c'est pas coherent, ca va l'aider a ranger et a creer de nouveaux tiroirs"
#    "effacer c'est pas la solution, un jour ca peut nous servir"
#
#  LE CHEMIN COMPLET, EN QUATRE TEMPS :
#    1) luciana.py sert un passage et lui colle son identifiant stable "#conv-<n>-<k>" ;
#    2) a chaque tour concerne, le PROGRAMME lui reclame son avis ;
#    3) elle ecrit "[AVIS #conv-312-2 : hors sujet - ...]", le programme le range dans
#       ~\Luciana\avis_de_luciana.jsonl (un enregistrement par ligne) ;
#    4) L'ARCHIVISTE (ici) lit ce fichier, et AU BOUT DE TROIS REJETS DU MEME PASSAGE, il cree un
#       nouveau tiroir et y range le passage avec ses etiquettes.
#
#  LE GARDE-FOU, ET IL EST OBLIGATOIRE : TROIS REJETS, JAMAIS UN SEUL. En dessous de trois, l'avis
#  est NOTE dans le rapport et RIEN NE BOUGE. Un tiroir ne se cree JAMAIS pour un cas isole, sinon
#  on finit avec 400 tiroirs et on retombe dans le bazar qu'on vient de nettoyer.
#  DEUXIEME GARDE-FOU, pour la meme raison : les passages rejetes pour la MEME raison atterrissent
#  dans le MEME tiroir (le nom du tiroir est fabrique a partir des mots que Luciana repete dans ses
#  raisons), et le nombre de tiroirs crees en une passe est plafonne (MAXI_NOUVEAUX_TIROIRS).
#
#  "DEPLACER" VEUT DIRE CHANGER L'ETIQUETTE, ET RIEN D'AUTRE. Aucun fichier d'origine n'est
#  supprime, reecrit ni meme ouvert en ecriture. L'archiviste ne touche toujours qu'a SES propres
#  sorties (etiquettes_essai.jsonl, son rapport, ses sauvegardes datees). Le fichier des avis
#  lui-meme est ouvert EN LECTURE SEULE : c'est luciana.py qui l'ecrit, jamais l'archiviste.
#
#  CE QU'IL FAUT DIRE FRANCHEMENT, ET QUI EST LE POINT FAIBLE DU MONTAGE AUJOURD'HUI :
#  les passages servis par la bibliotheque sont des morceaux de CONVERSATION ("conv-<n>-<k>").
#  Ils ne sont PAS dans l'inventaire de l'archiviste, qui ne connait que des FICHIERS (les fiches
#  de bibliotheque\, carnet.json, souvenirs.json, consignes.jsonl). L'archiviste cree donc pour eux
#  une etiquette NEUVE, de source "conversation", avec leur nouveau tiroir, leur date, qui parlait
#  et l'extrait -- c'est bien un rangement, et il est complet. MAIS : aujourd'hui, luciana.py NE
#  LIT PAS ENCORE etiquettes_des_avis.jsonl ; il ne relit que les lignes de source "carnet" de
#  etiquettes_essai.jsonl (voir _lire_etiquettes_archiviste). Ces nouvelles lignes sont donc
#  ECRITES ET VERIFIABLES, mais le bibliothecaire ne s'en sert pas ENCORE. C'est la brique
#  suivante, et elle n'est pas dans ce chantier.
#  Quand un avis porte sur un identifiant qui EST dans l'inventaire (une fiche, un carnet, un
#  souvenir, une consigne), le deplacement est complet et immediat : son etiquette change de tiroir.
# =====================================================================
#  LE FICHIER DES AVIS EST OUVERT EN LECTURE SEULE (c'est luciana.py qui l'ecrit).
FICHIER_AVIS = os.path.join(DOSSIER, "avis_de_luciana.jsonl")
#  LA QUATRIEME SORTIE DE L'ARCHIVISTE (les trois autres sont en haut de ce fichier) : les
#  etiquettes NEUVES des passages de conversation ranges dans un tiroir cree par les avis.
#  A PART, EXPRES : etiquettes_essai.jsonl doit garder exactement une etiquette par morceau non
#  vide, c'est ce que _verif_archiviste.py verifie, et on ne casse pas ce qui marche.
FICHIER_ETIQUETTES_AVIS = os.path.join(DOSSIER, "etiquettes_des_avis.jsonl")

REJETS_POUR_UN_NOUVEAU_TIROIR = 3     # LE GARDE-FOU DE FRED. Trois. Jamais un seul.
MAXI_NOUVEAUX_TIROIRS = 20            # par passe : on ne fabrique pas 400 tiroirs d'un coup
PREFIXE_TIROIR_AVIS = "Ecarte par les avis"

# Les mots qui ne designent jamais un sujet dans une raison ("ce passage parle de la compta" ->
# seul "compta" compte). On reprend _MOTS_VIDES, deja en place, et on ajoute les mots de la
# tournure elle-meme : sans ca, tous les tiroirs s'appelleraient "passage" ou "parle".
_MOTS_DE_LA_RAISON = set("""passage passages parle parlent parlait sujet sujets hors rien voir
concerne concernant discussion conversation message messages moment maintenant ici cela celui
coherent coherente coherents incoherent trancher avis luciana fred""".split())


def lire_les_avis(chemin=None, erreurs=None):
    """LES AVIS DE LUCIANA, EN LECTURE SEULE. Rend la liste des enregistrements lisibles.
    Fichier absent = liste vide = l'archiviste travaille exactement comme en v134. C'est le filet :
    tant que Luciana n'a donne aucun avis, RIEN ne change dans son travail."""
    chemin = chemin or FICHIER_AVIS
    avis = []
    if not os.path.isfile(chemin):
        return avis
    for n, d in _lignes_jsonl(chemin):
        if d is None:
            if erreurs is not None:
                erreurs.append({"quoi": "ligne d'avis illisible", "ou": "%s ligne %d" % (chemin, n)})
            continue
        ident = str(d.get("identifiant") or "").strip()
        if not ident:
            continue
        avis.append({
            "ligne": n,
            "identifiant": ident,
            "verdict": str(d.get("verdict") or "").strip().lower(),
            "raison": str(d.get("raison") or "").strip(),
            "phrase_de_fred": str(d.get("phrase_de_fred") or "").strip(),
            "extrait": str(d.get("extrait") or "").strip(),
            "date": str(d.get("date") or "").strip(),
            "date_du_passage": str(d.get("date_du_passage") or "").strip(),
            "qui_parlait": str(d.get("qui_parlait") or "").strip(),
        })
    return avis


def rejets_par_identifiant(avis):
    """COMBIEN DE FOIS CHAQUE PASSAGE A ETE REJETE, et par quelles raisons.
    ON NE COMPTE QUE LES VRAIS REJETS : verdict "hors sujet". Un "coherent" ou un "a trancher" ne
    compte pas, et ne fait donc jamais monter vers le seuil de trois.
    ON NE COMPTE QU'UNE FOIS PAR TOUR : deux marques identiques ecrites dans la MEME reponse (meme
    date, meme phrase de Fred) ne font pas trois rejets a elles seules. C'est le garde-fou du
    garde-fou : il faut VRAIMENT que le passage revienne mal trois fois."""
    par_id = {}
    for a in avis:
        if a["verdict"] != "hors sujet":
            continue
        d = par_id.setdefault(a["identifiant"], {
            "rejets": 0, "raisons": [], "quand": [], "phrases": [], "vus": set(),
            "extrait": "", "date_du_passage": "", "qui_parlait": ""})
        empreinte_du_tour = (a["date"][:19], a["phrase_de_fred"][:80])
        if empreinte_du_tour in d["vus"]:
            continue
        d["vus"].add(empreinte_du_tour)
        d["rejets"] += 1
        if a["raison"]:
            d["raisons"].append(a["raison"])
        d["quand"].append(a["date"])
        if a["phrase_de_fred"]:
            d["phrases"].append(a["phrase_de_fred"])
        # On garde le dernier extrait vu : c'est la preuve de ce qui a ete juge, mot pour mot.
        d["extrait"] = a["extrait"] or d["extrait"]
        d["date_du_passage"] = a["date_du_passage"] or d["date_du_passage"]
        d["qui_parlait"] = a["qui_parlait"] or d["qui_parlait"]
    for d in par_id.values():
        d.pop("vus", None)
    return par_id


def _mots_utiles(textes):
    """Les mots qui portent vraiment un sujet, dans l'ordre ou ils apparaissent.
    ON N'UTILISE PAS _MOTS_PAS_DES_NOMS ICI, ET C'EST VOULU : cette liste sert a reconnaitre les
    mots qui ne sont jamais des NOMS PROPRES ("compta", "mail", "facture", "video"...). Or ce sont
    EXACTEMENT les mots qui nomment bien un tiroir. On ne garde donc que les mots de liaison
    (_MOTS_VIDES) et les mots de la tournure elle-meme (_MOTS_DE_LA_RAISON)."""
    mots = []
    for t in textes:
        for mot in re.findall(r"[a-z0-9]{4,}", _sans_accents(str(t or ""))):
            if mot in _MOTS_VIDES or mot in _MOTS_DE_LA_RAISON:
                continue
            mots.append(mot)
    return mots


def nom_du_tiroir_pour(info):
    """LE NOM DU NOUVEAU TIROIR, FABRIQUE MECANIQUEMENT, JAMAIS INVENTE.
    On prend les mots que Luciana REPETE dans ses raisons (au moins deux fois sur ses trois
    rejets) : c'est ce qu'elle dit, pas ce qu'on suppose. Deux passages rejetes pour la meme
    raison tombent donc dans le MEME tiroir -- c'est ce qui empeche d'en fabriquer 400.
    S'il n'y a aucun mot repete, on se rabat sur les premiers mots de l'extrait du passage.
    S'il n'y a vraiment rien, le tiroir s'appelle "... a trancher" et c'est la verite."""
    compte = {}
    for mot in _mots_utiles(info.get("raisons") or []):
        compte[mot] = compte.get(mot, 0) + 1
    repetes = [m for m, n in sorted(compte.items(), key=lambda x: (-x[1], x[0])) if n >= 2]
    choisis = repetes[:2]
    if not choisis:
        choisis = _mots_utiles([info.get("extrait") or ""])[:2]
    if not choisis:
        return "%s - %s" % (PREFIXE_TIROIR_AVIS, A_TRANCHER)
    return "%s - %s" % (PREFIXE_TIROIR_AVIS, " ".join(choisis))


def tiroirs_a_creer(par_id, seuil=REJETS_POUR_UN_NOUVEAU_TIROIR, maxi=MAXI_NOUVEAUX_TIROIRS):
    """QUI BOUGE, QUI NE BOUGE PAS. Rend (deplacements, en_attente).
      - deplacements : {identifiant: {"tiroir": nom, "rejets": n, ...}} -- seulement ceux qui ont
        atteint le seuil, et dans la limite de 'maxi' NOUVEAUX tiroirs par passe ;
      - en_attente   : ceux qui n'ont pas encore trois rejets, ou que le plafond a repousses. Ils
        ne sont PAS perdus : ils sont ecrits dans le rapport, et ils passeront la fois d'apres.
    On traite les plus rejetes d'abord : si le plafond coupe, il coupe les cas les moins nets."""
    deplacements, en_attente, tiroirs = {}, {}, set()
    ordre = sorted(par_id.items(), key=lambda x: (-x[1]["rejets"], x[0]))
    for ident, info in ordre:
        if info["rejets"] < seuil:
            en_attente[ident] = dict(info, pourquoi=(
                "%d rejet(s) sur les %d qu'il faut : l'archiviste NOTE et ne bouge rien"
                % (info["rejets"], seuil)))
            continue
        nom = nom_du_tiroir_pour(info)
        if nom not in tiroirs and len(tiroirs) >= maxi:
            en_attente[ident] = dict(info, pourquoi=(
                "le plafond de %d nouveaux tiroirs par passe est atteint : ce passage attend la "
                "passe suivante, rien n'est perdu" % maxi))
            continue
        tiroirs.add(nom)
        deplacements[ident] = dict(info, tiroir=nom)
    return deplacements, en_attente


def deplacer_selon_les_avis(e, deplacements):
    """LE DEPLACEMENT, ET IL TIENT EN UNE LIGNE : ON CHANGE L'ETIQUETTE.
    Aucun fichier d'origine n'est supprime, reecrit, ni meme ouvert en ecriture. L'ancien tiroir
    est GARDE dans l'etiquette ("tiroir_avant") : on peut toujours revenir en arriere, et on voit
    d'ou le morceau vient. Rend l'etiquette, modifiee ou non."""
    d = (deplacements or {}).get(str(e.get("id") or ""))
    if not d:
        return e
    e["tiroir_avant"] = e.get("tiroir")
    e["tiroir"] = d["tiroir"]
    e["deplace_par"] = "les avis de Luciana"
    e["rejets"] = d["rejets"]
    e["raisons_du_rejet"] = d["raisons"][:5]
    e["d_ou_ca_vient"]["tiroir"] = (
        "DEPLACE PAR LES AVIS DE LUCIANA : ce passage a ete juge hors sujet %d fois (le seuil est "
        "%d, jamais un seul). Son tiroir d'avant etait \"%s\". Raison(s) donnee(s) : %s"
        % (d["rejets"], REJETS_POUR_UN_NOUVEAU_TIROIR, e.get("tiroir_avant"),
           " | ".join(d["raisons"][:3]) or "(aucune raison ecrite)"))
    if "tiroir" in (e.get("a_trancher") or []):
        e["a_trancher"] = [c for c in e["a_trancher"] if c != "tiroir"]
    return e


def etiquette_pour_un_passage_de_conversation(ident, d):
    """L'ETIQUETTE NEUVE D'UN PASSAGE DE CONVERSATION (les identifiants "conv-<n>-<k>").
    Ces passages-la ne sont PAS des fichiers : ils ne sont donc pas dans l'inventaire, et aucune
    etiquette n'existait pour eux. On en fabrique une, avec ce que l'avis porte VRAIMENT (la date
    du passage, qui parlait, l'extrait mot pour mot) et son nouveau tiroir. Rien n'est devine :
    chaque champ dit d'ou il vient, et ce qu'on ne sait pas reste "a trancher"."""
    return {
        "id": ident,
        "source": "conversation",
        "chemin": FICHIER_AVIS,
        "longueur": len(d.get("extrait") or ""),
        "date": d.get("date_du_passage") or "inconnue",
        "tiroir": d["tiroir"],
        "tiroir_avant": "(aucun : un passage de conversation n'etait range nulle part)",
        "sujet": _couper(d.get("extrait"), SUJET_MAXI) or A_TRANCHER,
        "personnes": [],
        "resume": _couper(d.get("extrait"), RESUME_MAXI) or A_TRANCHER,
        "statut": A_TRANCHER,
        "premiere_phrase": _couper(d.get("extrait"), RESUME_MAXI),
        "indices_statut": [],
        "deplace_par": "les avis de Luciana",
        "rejets": d["rejets"],
        "raisons_du_rejet": d["raisons"][:5],
        "qui_parlait": d.get("qui_parlait") or A_TRANCHER,
        "d_ou_ca_vient": {
            "date": "le champ 'date_du_passage' de l'avis ecrit par luciana.py",
            "tiroir": ("TIROIR CREE PAR LES AVIS DE LUCIANA : ce passage a ete juge hors sujet %d "
                       "fois (le seuil est %d, jamais un seul). Raison(s) : %s"
                       % (d["rejets"], REJETS_POUR_UN_NOUVEAU_TIROIR,
                          " | ".join(d["raisons"][:3]) or "(aucune raison ecrite)")),
            "sujet": "les premiers caracteres de l'extrait, recopies",
            "personnes": _D_OU_PERSONNES,
            "resume": "l'extrait du passage, recopie mot pour mot depuis l'avis",
            "statut": ("a trancher : un passage de conversation n'a ni etat ni remplacant ecrit "
                       "nulle part. On ne le devine pas."),
        },
        "pose_par": "archiviste (avis de Luciana, mecanique, aucun appel paye)",
        "pose_le": time.strftime("%Y-%m-%d %H:%M"),
        "a_trancher": ["statut"],
        "note": ("ATTENTION, A DIRE FRANCHEMENT : cette etiquette est ECRITE et VERIFIABLE, mais "
                 "luciana.py NE LIT PAS ENCORE etiquettes_des_avis.jsonl. Aujourd'hui il ne relit "
                 "que les lignes de source 'carnet' de etiquettes_essai.jsonl (voir "
                 "_lire_etiquettes_archiviste). Le rangement est donc FAIT et consultable, mais le "
                 "bibliothecaire ne s'en sert pas encore : c'est la brique suivante."),
    }


RESUME_MAXI = 300
SUJET_MAXI = 80

# "BUT : ...", "**OBJECTIF** - ...", "# BUT — ..." : on accepte la decoration de debut de ligne
# et toute la famille des tirets (le tiret long est partout chez Fred). "BUT DU CHANTIER" est
# place AVANT "BUT" dans la liste, sinon "BUT" gagnerait et la ligne ne serait pas reconnue.
_LIGNE_BUT = re.compile(
    r"^[\s>*#+_-]*(BUT DU CHANTIER|OBJECTIF|BUT)[\s*_]*[:\u2013\u2014\u2015>-]+\s*(.+)$",
    re.IGNORECASE | re.MULTILINE)

# Un trait de separation ("-----", "=====") ne porte aucune information : il ne peut pas servir
# de resume. On le saute.
_TRAIT_DE_SEPARATION = re.compile(r"^\s*[-=_*~#]{3,}\s*$")
# Un titre markdown ("# Robot physique") dit DE QUOI on parle, mais pas CE QU'IL Y A DEDANS.
_TITRE_MARKDOWN = re.compile(r"^\s*#{1,6}\s+\S")


def _couper(texte, maxi=RESUME_MAXI):
    """Met le texte sur une seule ligne et le coupe a 'maxi' caracteres, sur un blanc quand c'est
    possible. Quand il a fallu couper, on ecrit " [...]" : une citation coupee doit SE VOIR,
    sinon on croirait lire la phrase entiere."""
    t = re.sub(r"\s+", " ", str(texte or "")).strip()
    if len(t) <= maxi:
        return t
    coupe = t[:maxi]
    blanc = coupe.rfind(" ")
    if blanc > maxi // 2:
        coupe = coupe[:blanc]
    return coupe.rstrip(" .,;:-") + " [...]"


def _sans_decor(ligne):
    """Enleve la DECORATION markdown de debut de ligne (#, *, +, >, "- ") et les etoiles de gras.
    On n'enleve que de la decoration : pas un seul MOT n'est retire. Le tiret n'est enleve que
    s'il est suivi d'un blanc, pour ne pas transformer "-5 degres" en "5 degres"."""
    l = re.sub(r"^\s*(?:#{1,6}\s+|[*+>]\s*|-\s+)+", "", str(ligne or ""))
    return l.replace("**", "").replace("__", "").strip()


def _premiere_phrase(texte, maxi=RESUME_MAXI):
    """La premiere phrase, CITEE MOT POUR MOT. Si elle est trop longue et qu'on doit la couper,
    on ecrit " [...]" a la fin : une citation coupee doit se voir."""
    t = re.sub(r"\s+", " ", str(texte or "")).strip()
    if not t:
        return ""
    m = re.search(r"[.!?](\s|$)", t[:maxi])
    if m:
        return t[:m.start() + 1].strip()
    return _couper(t, maxi)


def _paragraphes(texte):
    """Les paragraphes non vides d'un texte, dans l'ordre. Rend des couples
    (texte du paragraphe, est-ce un titre tout seul).
    Un paragraphe = un bloc separe des autres par une ligne blanche. Les traits de separation
    sont sautes. La decoration markdown de debut de ligne est enlevee."""
    sortis = []
    for bloc in re.split(r"\n\s*\n", str(texte or "")):
        lignes, commence_par_un_titre = [], False
        for ligne in bloc.splitlines():
            if not ligne.strip() or _TRAIT_DE_SEPARATION.match(ligne):
                continue
            if not lignes and _TITRE_MARKDOWN.match(ligne):
                commence_par_un_titre = True
            propre = _sans_decor(ligne)
            if propre:
                lignes.append(propre)
        if lignes:
            sortis.append((re.sub(r"\s+", " ", " ".join(lignes)).strip(),
                           commence_par_un_titre and len(lignes) == 1))
    return sortis


def _premier_paragraphe(texte):
    """Le premier paragraphe non vide du fichier. Quand ce premier paragraphe n'est QU'UN TITRE
    ("# Robot physique"), on lui colle le paragraphe suivant : un titre dit de quoi on parle,
    pas ce qu'il y a dedans. On AJOUTE, on n'enleve rien."""
    ps = _paragraphes(texte)
    if not ps:
        return ""
    if ps[0][1] and len(ps) > 1:
        return "%s - %s" % (ps[0][0], ps[1][0])
    return ps[0][0]


def _resume_de_la_ligne_but(texte):
    """Rend (resume, provenance) a partir d'une ligne "BUT : ..." ecrite dans le morceau,
    ou ("", "") s'il n'y en a pas."""
    m = _LIGNE_BUT.search(str(texte or ""))
    if not m:
        return "", ""
    phrase = _couper(_sans_decor(m.group(2)))
    if not phrase:
        return "", ""
    return phrase, ("la ligne \"%s :\" ecrite dans le morceau, citee mot pour mot"
                    % re.sub(r"\s+", " ", m.group(1)).upper())


def _resume_du_plan(tiroir_du_plan):
    """Rend (resume, provenance) a partir des champs "contient" et "quand" du tiroir, tels qu'ils
    sont ecrits dans plan_bibliotheque.json. Ces deux champs sont RECOPIES ; le seul mot ajoute
    est le raccord "Il sort", pour qu'on comprenne que la deuxieme partie est un declencheur."""
    if not isinstance(tiroir_du_plan, dict):
        return "", ""
    contient = str(tiroir_du_plan.get("contient") or "").strip()
    quand = str(tiroir_du_plan.get("quand") or "").strip()
    if contient and quand:
        return (_couper("%s. Il sort %s" % (contient.rstrip(". "), quand)),
                "les champs 'contient' et 'quand' du tiroir dans plan_bibliotheque.json, recopies")
    if contient:
        return (_couper(contient),
                "le champ 'contient' du tiroir dans plan_bibliotheque.json, recopie")
    if quand:
        return (_couper("Il sort %s" % quand),
                "le champ 'quand' du tiroir dans plan_bibliotheque.json, recopie")
    return "", ""


def resume_du_morceau(m, tiroir_du_plan=None):
    """LE COEUR. Rend (resume, d'ou il vient). Il RECOPIE une phrase qui existe deja ; il n'en
    fabrique aucune. Quand il n'y a vraiment rien a recopier, il rend "a trancher" et une
    provenance qui contient "Rien a recopier" : c'est ce bout de phrase que le rapport compte."""
    source = m.get("source")
    texte = str(m.get("texte") or "")

    if source == "carnet":
        du_plan, d_ou = _resume_du_plan(tiroir_du_plan)
        if du_plan:
            return du_plan, d_ou
        but, d_ou = _resume_de_la_ligne_but(texte)
        if but:
            return but, d_ou
        phrase = _premiere_phrase(texte)
        if phrase:
            return phrase, ("la premiere phrase du contenu du tiroir dans carnet.json, citee "
                            "mot pour mot")
        return A_TRANCHER, ("a trancher : ce tiroir n'a ni 'contient' ni 'quand' dans le plan, "
                            "aucune ligne 'BUT :', et son contenu est vide. Rien a recopier.")

    if source == "souvenirs":
        court = _couper(texte)
        if court:
            return court, ("le souvenir lui-meme, recopie et coupe a %d caracteres. "
                           "souvenirs.json est une liste de phrases : le souvenir EST sa propre "
                           "phrase, il n'y a rien d'autre a reprendre." % RESUME_MAXI)
        return A_TRANCHER, "a trancher : ce souvenir est vide. Rien a recopier."

    if source == "consignes":
        court = _couper(texte)
        if court:
            return court, ("le champ 'texte' de la ligne dans consignes.jsonl, recopie et coupe "
                           "a %d caracteres" % RESUME_MAXI)
        return A_TRANCHER, ("a trancher : cette ligne de consignes.jsonl ne porte aucun texte. "
                            "Rien a recopier.")

    # Les fiches de la bibliotheque. On garde d'abord la ligne "BUT :" (c'est elle qui remplissait
    # deja les resumes qui marchaient), puis le premier paragraphe du fichier.
    but, d_ou = _resume_de_la_ligne_but(texte)
    if but:
        return but, d_ou
    para = _premier_paragraphe(texte)
    if para:
        return _couper(para), ("le premier paragraphe non vide du fichier, recopie et coupe a %d "
                               "caracteres" % RESUME_MAXI)
    return A_TRANCHER, ("a trancher : ce fichier ne contient aucun paragraphe lisible (vide, ou "
                        "seulement des traits de separation). Rien a recopier.")


def resume_est_rempli(e):
    """La seule definition d'un resume REMPLI, pour que l'archiviste et le controle comptent
    exactement la meme chose."""
    return str(e.get("resume") or "").strip() not in ("", A_TRANCHER)


def _compter_provenances(etiquettes):
    """Combien de resumes viennent de chaque source d'information. C'est la preuve, chiffree, que
    rien n'est invente : chaque resume rempli est rattache a un endroit precis d'un fichier."""
    compte = {}
    for e in etiquettes:
        d = str((e.get("d_ou_ca_vient") or {}).get("resume") or "?")
        compte[d] = compte.get(d, 0) + 1
    return dict(sorted(compte.items(), key=lambda kv: (-kv[1], kv[0])))


# =====================================================================
#  LES MORCEAUX QU'ON NE DOIT PAS ETIQUETER DU TOUT
#  Mesure du 07/10 : 2 lignes de consignes.jsonl sont VIDES et portaient quand meme une
#  etiquette complete. C'est du bruit pur, et le bruit fait rater les filtres.
# =====================================================================
def morceau_a_sauter(m):
    """Rend "" si le morceau doit etre etiquete, sinon LA RAISON de le sauter.
    ATTENTION, c'est le piege : une ligne de consignes.jsonl qui est un RETRAIT ("oublier la
    consigne n5") n'a pas de texte, et elle n'est PAS vide pour autant : c'est ELLE qui tue la
    consigne n5. On la garde. On ne saute que les lignes qui n'apprennent RIEN a personne.
    Les autres sources gardent leur etiquette meme sans texte : un tiroir de carnet au contenu
    vide porte quand meme un nom, une date et une place dans le plan."""
    if str(m.get("texte") or "").strip():
        return ""
    if m.get("source") != "consignes":
        return ""
    action = _sans_accents(m.get("action")).strip()
    if action.startswith(("oubli", "retir", "suppr")):
        return ""
    return "ligne de consignes.jsonl sans aucun texte : elle ne change rien au carnet"


# =====================================================================
#  POSER L'ETIQUETTE SUR UN MORCEAU
# =====================================================================
def etiqueter(m, plan_par_nom, plan_par_cat, noms, statuts_consignes, aujourd_hui):
    texte = str(m.get("texte") or "")
    e = {
        "id": m["id"],
        "source": m["source"],
        "chemin": m["chemin"],
        "longueur": len(texte),
        "date": A_TRANCHER,
        "tiroir": A_TRANCHER,
        "sujet": A_TRANCHER,
        "personnes": [],
        "resume": A_TRANCHER,
        "statut": A_TRANCHER,
        "premiere_phrase": _premiere_phrase(texte),
        "indices_statut": indices_statut(texte, aujourd_hui),
        "d_ou_ca_vient": {"date": A_TRANCHER, "tiroir": A_TRANCHER, "sujet": A_TRANCHER,
                          "personnes": _D_OU_PERSONNES, "resume": A_TRANCHER, "statut": A_TRANCHER},
        "pose_par": "archiviste (mecanique, aucun appel paye)",
        "pose_le": time.strftime("%Y-%m-%d %H:%M"),
    }
    d_ou = e["d_ou_ca_vient"]

    # --- 4) les personnes / noms cites : la meme regle que luciana.py ---
    e["personnes"] = noms_dans(texte, noms)

    # Le resume n'est PAS calcule ici : il a besoin de savoir quel tiroir du plan on a retrouve.
    # Il est donc calcule TOUT A LA FIN, quand tiroir_du_plan est connu.
    tiroir_du_plan = None

    if m["source"] == "bibliotheque":
        # 1) LA DATE : seulement si elle est ECRITE dans le nom du fichier. La date de
        #    modification du fichier Windows n'est PAS la date du morceau : on la donne a part,
        #    clairement nommee, et on ne la fait pas passer pour la date du morceau.
        d = _date_du_nom_de_fichier(m["nom_fichier"]) or _date_du_nom_de_fichier(m["relatif"])
        if d:
            e["date"], d_ou["date"] = d, "la date ecrite dans le nom du fichier (%s)" % m["nom_fichier"]
        try:
            e["fichier_modifie_le"] = time.strftime("%Y-%m-%d %H:%M",
                                                    time.localtime(os.path.getmtime(m["chemin"])))
        except Exception:
            pass

        # 2) LE TIROIR : la ou le fichier EST range. C'est un fait, pas un avis. Pour les deux
        #    rangements techniques (anciennes_versions, _doublons), on va chercher le vrai tiroir
        #    la ou il est ecrit (voir _ou_est_rangee_la_fiche).
        niveau1 = m["niveau1"]
        technique = m.get("rangement_technique") or ""
        ou = ("le nom du fichier, avant le premier \"__\"" if technique == "anciennes_versions"
              else "le dossier sous \"%s\"" % m["relatif"].split("/")[0] if technique
              else "le dossier")
        if niveau1:
            tiroir_du_plan = plan_par_nom.get(niveau1) or plan_par_cat.get(niveau1)
            if tiroir_du_plan and plan_par_nom.get(niveau1):
                e["tiroir"] = str(tiroir_du_plan.get("nom") or niveau1)
                d_ou["tiroir"] = ("%s \"%s\", retrouve dans plan_bibliotheque.json comme NOM de "
                                  "tiroir" % (ou, niveau1))
            elif tiroir_du_plan:
                e["tiroir"] = str(tiroir_du_plan.get("categorie") or niveau1)
                d_ou["tiroir"] = ("%s \"%s\", retrouve dans plan_bibliotheque.json comme RAYON "
                                  "(categorie)" % (ou, niveau1))
            else:
                e["tiroir"] = niveau1
                d_ou["tiroir"] = ("%s \"%s\" (il n'est PAS dans plan_bibliotheque.json)"
                                  % (ou, niveau1))
            e["sous_tiroir"] = m["niveau2"] or ""

        # 3) LE SUJET : le titre du plan s'il existe, sinon le nom du sous-dossier. Deux faits.
        if tiroir_du_plan and str(tiroir_du_plan.get("titre") or "").strip():
            e["sujet"] = str(tiroir_du_plan["titre"]).strip()
            d_ou["sujet"] = "le champ 'titre' du tiroir dans plan_bibliotheque.json"
        elif m["niveau2"]:
            e["sujet"] = m["niveau2"].replace("-", " ")
            d_ou["sujet"] = "le nom du sous-dossier \"%s\"" % m["niveau2"]

        # 6) LE STATUT : seulement quand le RANGEMENT lui-meme le dit, noir sur blanc.
        if technique == "anciennes_versions":
            e["statut"] = "remplace"
            d_ou["statut"] = ("le fichier est range dans bibliotheque\\anciennes_versions : c'est "
                              "par construction une version gardee, pas la version courante")
        elif technique == "_doublons":
            e["statut"] = "remplace"
            d_ou["statut"] = ("le fichier est range dans un dossier \"%s\" : c'est un doublon mis "
                              "de cote" % m["relatif"].split("/")[0])
        elif tiroir_du_plan and str(tiroir_du_plan.get("etat") or "").strip():
            d_ou["statut"] = ("a trancher : le plan dit que le tiroir est \"%s\", mais l'etat du "
                              "TIROIR ne dit pas si CE fichier-la est encore la version vivante"
                              % tiroir_du_plan.get("etat"))

    elif m["source"] == "carnet":
        nom = m["nom_tiroir"]
        tiroir_du_plan = plan_par_nom.get(_slug(nom))
        # 1) LA DATE : le champ 'maj' du carnet. Ecrit noir sur blanc.
        if m.get("maj"):
            e["date"] = str(m["maj"])[:10]
            e["date_et_heure"] = m["maj"]
            d_ou["date"] = "le champ 'maj' du tiroir dans carnet.json (%s)" % m["maj"]
        # 2) LE TIROIR : c'est la cle du carnet. C'est litteralement le tiroir.
        e["tiroir"] = nom
        d_ou["tiroir"] = "le nom du tiroir, c'est-a-dire la cle dans carnet.json"
        # 3) LE SUJET
        if tiroir_du_plan and str(tiroir_du_plan.get("titre") or "").strip():
            e["sujet"] = str(tiroir_du_plan["titre"]).strip()
            d_ou["sujet"] = "le champ 'titre' du tiroir dans plan_bibliotheque.json"
        else:
            e["sujet"] = nom
            d_ou["sujet"] = "le nom du tiroir lui-meme (pas de 'titre' dans le plan)"
        # 6) LE STATUT
        etat_plan = str(tiroir_du_plan.get("etat") or "").strip() if tiroir_du_plan else ""
        if etat_plan == "actif":
            e["statut"] = "vivant"
            d_ou["statut"] = ("carnet.json ne garde QU'UN SEUL etat par tiroir, le plus recent "
                              "(maj %s), et plan_bibliotheque.json dit que ce tiroir est \"actif\""
                              % (m.get("maj") or "?"))
        elif etat_plan:
            d_ou["statut"] = ("a trancher : plan_bibliotheque.json dit que ce tiroir \"%s\". Ca ne "
                              "veut pas dire que la decision est annulee : c'est a Fred de le dire"
                              % etat_plan)
        else:
            d_ou["statut"] = ("a trancher : ce tiroir n'a pas ete retrouve dans "
                              "plan_bibliotheque.json")

    elif m["source"] == "souvenirs":
        e["rang"] = m["rang"]
        # souvenirs.json est une simple LISTE DE PHRASES : pas de date, pas de titre, pas de marque
        # de remplacement. Mesure du 07/10 : les 203 souvenirs avaient les QUATRE champs "a
        # trancher", donc 203 etiquettes qui ne servaient a rien. On remplit maintenant ce qui est
        # VRAI SANS DEVINER, et uniquement ca :
        # 1) LA DATE : elle est reellement inconnue. On ECRIT "inconnue" au lieu de "a trancher" :
        #    "a trancher" veut dire "il reste du travail a faire la-dessus", or il n'y a rien a
        #    trancher — le fichier ne porte aucune date et n'en portera jamais. C'est un fait.
        e["date"] = "inconnue"
        d_ou["date"] = ("souvenirs.json est une liste de phrases sans aucune date : la date est "
                        "REELLEMENT inconnue, ce n'est pas un travail en attente")
        # 2) LE TIROIR : le fichier lui-meme. C'est le seul rangement qui existe pour un souvenir.
        e["tiroir"] = "souvenirs"
        d_ou["tiroir"] = ("le fichier souvenirs.json lui-meme : c'est le seul rangement qui existe "
                          "pour un souvenir, il n'y a pas d'autre tiroir a chercher")
        # 3) LE SUJET : le debut du souvenir, recopie. Pas un titre invente : un debut de phrase.
        debut = _couper(m.get("texte"), SUJET_MAXI)
        if debut:
            e["sujet"] = debut
            d_ou["sujet"] = ("les %d premiers caracteres du souvenir, recopies (souvenirs.json ne "
                             "porte aucun titre)" % SUJET_MAXI)
        else:
            d_ou["sujet"] = "a trancher : ce souvenir est vide, il n'y a rien a recopier"
        # 6) LE STATUT : il reste "a trancher", et on NE LE DEVINE PAS. C'est le vrai trou.
        d_ou["statut"] = ("a trancher : souvenirs.json ne fait que s'allonger. Rien dans le fichier "
                          "ne dit qu'un souvenir en remplace un autre. C'EST EXACTEMENT LE TROU "
                          "QUE FRED DECRIT : la decision morte et la vivante s'y ressemblent.")

    elif m["source"] == "consignes":
        e["ligne"] = m["ligne"]
        e["numero_consigne"] = m.get("numero")
        e["action"] = m.get("action")
        e["importance"] = m.get("importance")
        # 1) LA DATE : le champ 'date' de la ligne.
        if m.get("date_ecrite"):
            e["date"] = str(m["date_ecrite"])[:10]
            e["date_et_heure"] = m["date_ecrite"]
            d_ou["date"] = "le champ 'date' de la ligne dans consignes.jsonl"
        # 2) LE TIROIR : consignes.jsonl ne range pas par tiroir. On ne l'invente pas.
        d_ou["tiroir"] = ("a trancher : consignes.jsonl ne porte aucun tiroir. Le rattachement "
                          "d'une regle a un projet n'est pas ecrit dans le fichier.")
        d_ou["sujet"] = ("a trancher : une consigne n'a pas de titre, juste son texte")
        # 6) LE STATUT : mecanique, le journal le dit lui-meme.
        if m["id"] in statuts_consignes:
            e["statut"], d_ou["statut"] = statuts_consignes[m["id"]]
        else:
            d_ou["statut"] = ("a trancher : cette ligne n'a pas de numero de consigne utilisable, "
                              "donc le journal ne dit rien de son sort")

    # --- 5) LE RESUME, LE COEUR. Il est calcule EN DERNIER parce qu'il a besoin, pour un tiroir
    #        de carnet, de savoir quel tiroir du plan a repondu. Voir resume_du_morceau().
    e["resume"], d_ou["resume"] = resume_du_morceau(m, tiroir_du_plan)

    e["a_trancher"] = [c for c in ("date", "tiroir", "sujet", "resume", "statut")
                       if e.get(c) == A_TRANCHER]
    if not e["personnes"]:
        e["a_trancher"].append("personnes")
    return e


# =====================================================================
#  L'EMPREINTE DE LA BIBLIOTHEQUE : la preuve qu'elle n'a pas bouge d'un octet
# =====================================================================
def fichiers_de_la_bibliotheque():
    """TOUS les fichiers que l'archiviste ouvre. C'est sur ceux-la qu'on prend l'empreinte."""
    liste = [FICHIER_PLAN, FICHIER_CARNET, FICHIER_SOUVENIRS, FICHIER_CONSIGNES,
             FICHIER_NOMS_PROPRES]
    if os.path.isdir(DOSSIER_BIBLIO):
        for racine, dossiers, fichiers in os.walk(DOSSIER_BIBLIO):
            dossiers.sort()
            for nom in sorted(fichiers):
                liste.append(os.path.join(racine, nom))
    return [c for c in liste if os.path.isfile(c)]


def empreinte(chemins):
    """Taille + empreinte sha256 + date de modification, pour chaque fichier. Lecture seule."""
    out = {}
    for c in chemins:
        try:
            h = hashlib.sha256()
            with io.open(c, "rb") as f:
                for bloc in iter(lambda: f.read(262144), b""):
                    h.update(bloc)
            out[c] = {"octets": os.path.getsize(c), "sha256": h.hexdigest(),
                      "modifie": round(os.path.getmtime(c), 3)}
        except Exception as ex:
            out[c] = {"erreur": repr(ex)}
    return out


# =====================================================================
#  ECRIRE : SAUVEGARDER AVANT, NE JAMAIS ECRASER
# =====================================================================
def sauvegarder_avant(chemins):
    """Copie datee de tout fichier qu'on est sur le point de toucher. Si le fichier n'existe pas
    encore, il n'y a rien a sauvegarder et on le dit. Rend (dossier de sauvegarde, liste copiee)."""
    a_copier = [c for c in chemins if os.path.isfile(c)]
    if not a_copier:
        return "", []
    base = os.path.join(DOSSIER_SAUVEGARDES, time.strftime("%Y-%m-%d_%Hh%Mm%S"))
    # Deux passages dans la MEME seconde ne doivent pas s'ecraser l'un l'autre.
    dossier, n = base, 1
    while os.path.exists(dossier):
        dossier, n = "%s_%d" % (base, n), n + 1
    os.makedirs(dossier)
    copies = []
    for c in a_copier:
        dest = os.path.join(dossier, os.path.basename(c))
        shutil.copy2(c, dest)
        copies.append(dest)
    return dossier, copies


def ecrire_remplace(chemin, texte):
    """Ecrit par fichier temporaire puis renommage : une coupure de courant ne laisse jamais un
    fichier a moitie ecrit. Meme facon de faire que luciana.py."""
    tmp = chemin + ".tmp"
    with io.open(tmp, "w", encoding="utf-8", newline="\n") as f:
        f.write(texte)
    os.replace(tmp, chemin)


def ajouter_une_ligne(chemin, ligne):
    with io.open(chemin, "a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(ligne, ensure_ascii=False) + "\n")


# =====================================================================
#  L'ECHANTILLON : 300 morceaux, repartis sur TOUT, et toujours les memes
#  On ne prend pas "les 300 premiers" (ce serait 300 fichiers du meme tiroir). On prend un
#  morceau tous les N, dans chaque source, pour que le vieux et le neuf soient tous les deux la.
#  Aucun hasard : relance deux fois, tu obtiens le meme echantillon.
# =====================================================================
ORDRE_SOURCES = ("carnet", "consignes", "souvenirs", "bibliotheque")


def echantillon(morceaux, combien):
    if combien <= 0 or combien >= len(morceaux):
        return list(morceaux)
    par_source = {}
    for m in morceaux:
        par_source.setdefault(m["source"], []).append(m)
    total = len(morceaux)
    # Chaque source recoit sa part, au prorata, avec au moins 1 morceau si elle existe.
    parts = {}
    for s in ORDRE_SOURCES:
        liste = par_source.get(s) or []
        if not liste:
            continue
        parts[s] = min(len(liste), max(1, int(round(combien * len(liste) / float(total)))))
    # On ajuste pour tomber PILE sur 'combien'. Chaque tour change une part, donc ca finit toujours.
    while parts and sum(parts.values()) > combien:
        candidats = [k for k in parts if parts[k] > 1]
        if not candidats:
            break
        parts[max(candidats, key=lambda k: parts[k])] -= 1
    while parts and sum(parts.values()) < combien:
        candidats = [k for k in parts if parts[k] < len(par_source[k])]
        if not candidats:
            break
        parts[max(candidats, key=lambda k: len(par_source[k]) - parts[k])] += 1
    choisis = []
    for s in ORDRE_SOURCES:
        liste = par_source.get(s) or []
        n = parts.get(s, 0)
        if not n:
            continue
        if n >= len(liste):
            choisis.extend(liste)
            continue
        pas = len(liste) / float(n)
        choisis.extend(liste[min(len(liste) - 1, int(i * pas))] for i in range(n))
    return choisis


# =====================================================================
#  LA PASSE COMPLETE
# =====================================================================
def passe(combien, sortie, rapport):
    aujourd_hui = time.strftime("%Y-%m-%d")
    if not os.path.isdir(DOSSIER):
        print("Le dossier %s n'existe pas. Rien n'a ete lu, rien n'a ete ecrit." % DOSSIER)
        return 2

    print("L'ARCHIVISTE : il pose des etiquettes, il ne deplace rien.")
    print("Bibliotheque lue (LECTURE SEULE) : %s" % DOSSIER)
    print("")

    fichiers = fichiers_de_la_bibliotheque()
    print("Empreinte AVANT de %d fichiers de la bibliotheque..." % len(fichiers))
    avant = empreinte(fichiers)

    erreurs = []
    tous = inventaire(erreurs)
    print("Morceaux trouves : %d" % len(tous))
    for s in ORDRE_SOURCES:
        n = sum(1 for m in tous if m["source"] == s)
        if n:
            print("   - %-14s %6d" % (s, n))

    plan_par_nom, plan_par_cat = charger_plan()
    if not plan_par_nom:
        erreurs.append({"quoi": "plan_bibliotheque.json vide ou illisible", "ou": FICHIER_PLAN})
    noms = noms_propres()
    # Le journal des consignes est rejoue sur TOUS les morceaux, y compris ceux qu'on va sauter :
    # une ligne de retrait sans texte doit continuer a tuer la consigne qu'elle retire.
    statuts_c = statuts_des_consignes(tous)

    # ---- v136 : LES AVIS DE LUCIANA, LUS UNE SEULE FOIS, EN LECTURE SEULE ----
    # Fichier absent ou vide = rien ne change, l'archiviste travaille exactement comme en v134.
    avis = lire_les_avis(erreurs=erreurs)
    par_id = rejets_par_identifiant(avis)
    deplacements, en_attente = tiroirs_a_creer(par_id)
    print("")
    print("AVIS DE LUCIANA lus (%s) : %d" % (FICHIER_AVIS, len(avis)))
    print("   passages rejetes au moins une fois  : %6d" % len(par_id))
    print("   passages a DEPLACER (%d rejets)      : %6d"
          % (REJETS_POUR_UN_NOUVEAU_TIROIR, len(deplacements)))
    print("   passages NOTES, rien ne bouge       : %6d" % len(en_attente))

    # ON SAUTE LES MORCEAUX VIDES. Une etiquette complete posee sur une ligne vide, c'est du bruit
    # pur, et le bruit fait rater les filtres. On dit lesquels et pourquoi, on ne les efface pas.
    sautes = [{"id": m["id"], "source": m["source"], "pourquoi": morceau_a_sauter(m)}
              for m in tous if morceau_a_sauter(m)]
    a_etiqueter = [m for m in tous if not morceau_a_sauter(m)]
    if sautes:
        print("")
        print("Morceaux VIDES sautes (aucune etiquette posee dessus) : %d" % len(sautes))
        for x in sautes[:10]:
            print("   - %s : %s" % (x["id"], x["pourquoi"]))

    pris = echantillon(a_etiqueter, combien)
    print("")
    print("Echantillon traite : %d morceaux%s" % (len(pris), " (TOUT)" if combien <= 0 else ""))

    etiquettes = []
    for m in pris:
        try:
            e = etiqueter(m, plan_par_nom, plan_par_cat, noms, statuts_c, aujourd_hui)
            # v136 : ET C'EST TOUT LE DEPLACEMENT -- on change l'etiquette, rien d'autre. Si ce
            # morceau n'a pas ses trois rejets, deplacer_selon_les_avis le rend tel quel.
            etiquettes.append(deplacer_selon_les_avis(e, deplacements))
        except Exception as ex:
            erreurs.append({"quoi": "etiquette impossible", "ou": m.get("id"), "erreur": repr(ex)})

    # v136 : LES PASSAGES DE CONVERSATION. Les identifiants "conv-<n>-<k>" ne sont PAS des fichiers
    # et ne sont donc dans AUCUN inventaire : aucune etiquette n'existait pour eux. On leur en
    # fabrique une, avec ce que l'avis porte vraiment, et avec leur nouveau tiroir. C'est la que le
    # tiroir est CREE : il n'existe que par son nom sur les etiquettes, et aucun fichier d'origine
    # n'est touche.
    # ELLES VONT DANS UN FICHIER A PART (etiquettes_des_avis.jsonl), ET C'EST VOULU :
    # etiquettes_essai.jsonl doit garder EXACTEMENT une etiquette par morceau non vide -- c'est ce
    # que son controle verifie depuis le 07/10, et on ne casse pas ce qui marche.
    ids_connus = {m["id"] for m in tous}
    deja_etiquetes = {e.get("id") for e in etiquettes}
    etiquettes_des_avis, hors_echantillon = [], []
    tiroirs_crees = set()
    for ident, d in sorted(deplacements.items()):
        tiroirs_crees.add(d["tiroir"])
        if ident in deja_etiquetes:
            continue            # deja deplace juste au-dessus, dans son etiquette normale
        if ident in ids_connus:
            # Il EST dans l'inventaire, mais l'echantillon ne l'a pas pris a cette passe. On le dit,
            # on ne fabrique pas une etiquette en double. Il sera deplace a la passe sur TOUT
            # (python archiviste.py --combien 0).
            hors_echantillon.append({"identifiant": ident, "tiroir": d["tiroir"],
                                     "pourquoi": "dans l'inventaire, mais hors de cet echantillon"})
            continue
        try:
            etiquettes_des_avis.append(etiquette_pour_un_passage_de_conversation(ident, d))
        except Exception as ex:
            erreurs.append({"quoi": "etiquette de passage impossible", "ou": ident,
                            "erreur": repr(ex)})

    # ---------- SAUVEGARDER AVANT, PUIS ECRIRE (a part, jamais dans la bibliotheque) ----------
    # v136, ET C'EST UN CHOIX, PAS UN OUBLI : etiquettes_des_avis.jsonl n'est PAS copie dans le
    # dossier de sauvegardes, pour deux raisons dites franchement.
    #  1) RIEN NE PEUT ETRE PERDU : ce fichier est entierement REFABRIQUE a chaque passe a partir de
    #     avis_de_luciana.jsonl, qui est un JOURNAL (on ne fait qu'y ajouter des lignes, jamais le
    #     reecrire). La vraie memoire des avis est la, et elle n'est jamais touchee.
    #  2) ON NE CASSE PAS CE QUI MARCHE : _verif_archiviste.py prend comme point de comparaison LE
    #     PLUS VIEUX fichier .jsonl du dossier de sauvegardes. Y deposer un fichier d'avis (quelques
    #     lignes) ferait croire a une chute du nombre d'etiquettes, et son controle dirait n'importe
    #     quoi. On le laisse donc en dehors.
    dossier_sauv, copies = sauvegarder_avant([sortie, rapport])
    if copies:
        print("")
        print("Sauvegarde datee des anciennes sorties : %s" % dossier_sauv)
    else:
        print("")
        print("Rien a sauvegarder : aucune sortie precedente (premier passage).")

    ecrire_remplace(sortie, "".join(json.dumps(e, ensure_ascii=False) + "\n" for e in etiquettes))
    # v136 : les etiquettes NEUVES des passages de conversation, dans LEUR fichier a part.
    # On l'ecrit meme vide : un fichier vide dit "aucun passage n'a atteint les trois rejets",
    # et c'est une information. Rien n'est jamais efface ailleurs.
    ecrire_remplace(FICHIER_ETIQUETTES_AVIS,
                    "".join(json.dumps(e, ensure_ascii=False) + "\n" for e in etiquettes_des_avis))

    apres = empreinte(fichiers)
    bouges = sorted(c for c in fichiers
                    if avant.get(c, {}).get("sha256") != apres.get(c, {}).get("sha256")
                    or avant.get(c, {}).get("octets") != apres.get(c, {}).get("octets"))

    # LES CHIFFRES DU RESUME : c'est LE point du chantier du 07/10. On compte separement les
    # resumes encore "a trancher" PARCE QU'IL N'Y AVAIT RIEN A RECOPIER (contenu vide) : ceux-la
    # sont normaux et ne se repareront jamais ; les autres sont de vrais manques.
    remplis = [e for e in etiquettes if resume_est_rempli(e)]
    vides_de_resume = [e for e in etiquettes if not resume_est_rempli(e)]
    faute_de_texte = [e for e in vides_de_resume
                      if "rien a recopier" in _sans_accents(e["d_ou_ca_vient"]["resume"])]

    comptes = {
        "morceaux_lus": len(tous),
        "morceaux_lus_par_source": {s: sum(1 for m in tous if m["source"] == s)
                                    for s in ORDRE_SOURCES},
        "morceaux_vides_sautes": len(sautes),
        "morceaux_vides_sautes_par_source": {s: sum(1 for x in sautes if x["source"] == s)
                                             for s in ORDRE_SOURCES},
        "etiquettes_posees": len(etiquettes),
        "resume_rempli": len(remplis),
        "resume_a_trancher": len(vides_de_resume),
        "resume_a_trancher_faute_de_texte": len(faute_de_texte),
        "resume_a_trancher_sans_raison_dite": len(vides_de_resume) - len(faute_de_texte),
        "resume_rempli_par_source": {s: sum(1 for e in remplis if e["source"] == s)
                                     for s in ORDRE_SOURCES},
        "resume_rempli_par_provenance": _compter_provenances(remplis),
        "erreurs": len(erreurs),
        "a_trancher_total": sum(1 for e in etiquettes if e["a_trancher"]),
        "a_trancher_par_champ": {c: sum(1 for e in etiquettes if c in e["a_trancher"])
                                 for c in ("date", "tiroir", "sujet", "personnes", "resume", "statut")},
        "statuts": {s: sum(1 for e in etiquettes if e["statut"] == s) for s in STATUTS},
        "morceaux_avec_indice_de_mort": sum(1 for e in etiquettes if e["indices_statut"]),
        "morceaux_a_trancher_mais_avec_indice": sum(
            1 for e in etiquettes if e["statut"] == A_TRANCHER and e["indices_statut"]),
        "appels_payes": 0,
        # ---- v136 : LES AVIS DE LUCIANA, CHIFFRE PAR CHIFFRE ----
        "avis_lus": len(avis),
        "avis_passages_rejetes": len(par_id),
        "avis_seuil": REJETS_POUR_UN_NOUVEAU_TIROIR,
        "avis_deplacements": len(deplacements),
        "avis_en_attente": len(en_attente),
        "avis_tiroirs_crees": sorted(tiroirs_crees),
        "avis_etiquettes_de_conversation": len(etiquettes_des_avis),
        "avis_hors_echantillon": len(hors_echantillon),
        "avis_etiquettes_de_l_inventaire_deplacees": sum(
            1 for e in etiquettes if e.get("deplace_par")),
    }

    ecrire_remplace(rapport, json.dumps({
        "quand": time.strftime("%Y-%m-%d %H:%M:%S"),
        "dossier_lu": DOSSIER,
        "combien_demande": combien,
        "sortie": sortie,
        "sauvegarde": dossier_sauv,
        "comptes": comptes,
        # v136 : LE DETAIL DES AVIS. "deplaces" = les trois rejets sont la, le tiroir est cree.
        # "en_attente" = NOTE, rien n'a bouge, et on dit pourquoi. C'est exactement le garde-fou
        # de Fred : un cas isole n'a jamais le droit de fabriquer un tiroir.
        "avis_fichier": FICHIER_AVIS,
        "avis_sortie": FICHIER_ETIQUETTES_AVIS,
        "avis_deplaces_detail": {i: {"tiroir": d["tiroir"], "rejets": d["rejets"],
                                     "raisons": d["raisons"][:5], "quand": d["quand"][:5]}
                                 for i, d in sorted(deplacements.items())},
        "avis_en_attente_detail": {i: {"rejets": d["rejets"], "pourquoi": d["pourquoi"],
                                       "raisons": d["raisons"][:5]}
                                   for i, d in sorted(en_attente.items())},
        "avis_hors_echantillon_detail": hors_echantillon[:200],
        "erreurs_detail": erreurs[:200],
        "morceaux_vides_sautes_detail": sautes[:200],
        "bibliotheque_fichiers": len(fichiers),
        "bibliotheque_octets_avant": sum(v.get("octets", 0) for v in avant.values()),
        "bibliotheque_octets_apres": sum(v.get("octets", 0) for v in apres.values()),
        "bibliotheque_fichiers_bouges": bouges,
        "empreinte_avant": avant,
        "empreinte_apres": apres,
    }, ensure_ascii=False, indent=1))

    print("")
    print("CHIFFRE PAR CHIFFRE")
    print("-" * 70)
    print("morceaux lus                        : %6d" % comptes["morceaux_lus"])
    print("morceaux VIDES sautes               : %6d" % comptes["morceaux_vides_sautes"])
    print("etiquettes posees                   : %6d" % comptes["etiquettes_posees"])
    print("   resume REMPLI                    : %6d%s" % (
        comptes["resume_rempli"],
        ("   (%d %%)" % round(100.0 * comptes["resume_rempli"] / len(etiquettes))
         if etiquettes else "")))
    print("   resume encore 'a trancher'       : %6d" % comptes["resume_a_trancher"])
    print("      dont : rien a recopier        : %6d   (contenu vide : c'est normal)"
          % comptes["resume_a_trancher_faute_de_texte"])
    print("      dont : sans raison dite       : %6d   (0 attendu)"
          % comptes["resume_a_trancher_sans_raison_dite"])
    print("erreurs                             : %6d" % comptes["erreurs"])
    print("-" * 70)
    print("D'ou viennent les resumes remplis (rien n'est invente) :")
    for d, n in list(comptes["resume_rempli_par_provenance"].items())[:12]:
        print("   %5d  <- %s" % (n, d[:95]))
    print("")
    print("Dont au moins un champ 'a trancher' : %d" % comptes["a_trancher_total"])
    for c, n in sorted(comptes["a_trancher_par_champ"].items()):
        print("   - %-10s a trancher : %4d" % (c, n))
    print("Statuts : " + ", ".join("%s=%d" % (s, comptes["statuts"][s]) for s in STATUTS))
    print("Morceaux 'a trancher' qui portent un INDICE de mort : %d (a relire a la main)"
          % comptes["morceaux_a_trancher_mais_avec_indice"])
    print("Erreurs : %d" % comptes["erreurs"])
    for x in erreurs[:10]:
        print("   ! %s : %s" % (x.get("quoi"), x.get("ou")))
    print("")
    print("Bibliotheque : %d fichiers, %d octets avant, %d octets apres, %d fichier(s) bouge(s)."
          % (len(fichiers), sum(v.get("octets", 0) for v in avant.values()),
             sum(v.get("octets", 0) for v in apres.values()), len(bouges)))
    print("")
    print("LES AVIS DE LUCIANA (v136) — ce qu'ils ont fait bouger")
    print("-" * 70)
    print("avis lus                            : %6d" % comptes["avis_lus"])
    print("passages rejetes au moins une fois  : %6d" % comptes["avis_passages_rejetes"])
    print("   -> DEPLACES (%d rejets atteints)  : %6d"
          % (REJETS_POUR_UN_NOUVEAU_TIROIR, comptes["avis_deplacements"]))
    print("   -> NOTES, rien ne bouge          : %6d   (moins de %d rejets, ou plafond atteint)"
          % (comptes["avis_en_attente"], REJETS_POUR_UN_NOUVEAU_TIROIR))
    print("tiroirs CREES par les avis          : %6d" % len(comptes["avis_tiroirs_crees"]))
    for nom in comptes["avis_tiroirs_crees"][:12]:
        print("      + %s" % nom)
    print("etiquettes de l'inventaire deplacees: %6d"
          % comptes["avis_etiquettes_de_l_inventaire_deplacees"])
    print("etiquettes NEUVES de conversation   : %6d   -> %s"
          % (comptes["avis_etiquettes_de_conversation"], FICHIER_ETIQUETTES_AVIS))
    if comptes["avis_hors_echantillon"]:
        print("a deplacer mais hors echantillon    : %6d   (relance avec --combien 0)"
              % comptes["avis_hors_echantillon"])
    print("RIEN N'A ETE EFFACE : 'deplacer' veut dire CHANGER L'ETIQUETTE, et rien d'autre.")
    print("")
    print("Ecrit : %s" % sortie)
    print("Ecrit : %s" % rapport)
    print("Ecrit : %s" % FICHIER_ETIQUETTES_AVIS)
    print("Appels payes : 0.")
    return 1 if (bouges or erreurs) else 0


# =====================================================================
#  LA PETITE INTERFACE EN LIGNE DE COMMANDE
# =====================================================================
def trouver(morceaux, bout):
    """Retrouve UN morceau a partir de son identifiant, ou d'un bout d'identifiant."""
    exact = [m for m in morceaux if m["id"] == bout]
    if exact:
        return exact, ""
    b = _sans_accents(bout)
    proches = [m for m in morceaux if b in _sans_accents(m["id"])]
    if len(proches) == 1:
        return proches, ""
    if not proches:
        return [], "Aucun morceau ne correspond a \"%s\"." % bout
    return proches, ("%d morceaux correspondent a \"%s\". Precise lequel :" % (len(proches), bout))


def montrer(e, m=None):
    print("")
    print("IDENTIFIANT : %s" % e["id"])
    print("source      : %s   (%s)" % (e["source"], e["chemin"]))
    print("longueur    : %d caracteres" % e["longueur"])
    print("1 date      : %s" % e["date"])
    print("              <- %s" % e["d_ou_ca_vient"]["date"])
    print("2 tiroir    : %s" % e["tiroir"])
    print("              <- %s" % e["d_ou_ca_vient"]["tiroir"])
    print("3 sujet     : %s" % e["sujet"])
    print("              <- %s" % e["d_ou_ca_vient"]["sujet"])
    print("4 personnes : %s" % (", ".join(e["personnes"]) or A_TRANCHER))
    print("5 resume    : %s" % e["resume"])
    print("              <- %s" % e["d_ou_ca_vient"]["resume"])
    print("6 STATUT    : %s" % e["statut"].upper())
    print("              <- %s" % e["d_ou_ca_vient"]["statut"])
    if e["indices_statut"]:
        print("   INDICES (ils ne decident rien, ils aident a trancher) :")
        for i in e["indices_statut"]:
            print("     * \"%s\" : %s" % (i["mot"], i["extrait"][:200]))
    print("premiere phrase (citation, PAS un resume) : %s" % e["premiere_phrase"][:300])
    if m is not None:
        print("")
        print("--- DEBUT DU MORCEAU (1 200 premiers caracteres) ---")
        print(str(m.get("texte") or "")[:1200])
        print("--- FIN ---")


def demander(question, defaut=""):
    try:
        r = input("%s%s : " % (question, (" [%s]" % defaut) if defaut else "")).strip()
    except (EOFError, KeyboardInterrupt):
        print("")
        return None
    return r or defaut


def etiqueter_a_la_main(bout, sortie, donne):
    """Ecrit UNE etiquette posee a la main, en AJOUT a la fin du fichier d'etiquettes.
    Rien n'est efface : comme consignes.jsonl, le fichier ne fait que grossir, et c'est la
    DERNIERE etiquette d'un identifiant qui compte."""
    erreurs = []
    tous = inventaire(erreurs)
    trouves, message = trouver(tous, bout)
    if message:
        print(message)
        for m in trouves[:30]:
            print("   %s" % m["id"])
        return 2
    m = trouves[0]
    plan_par_nom, plan_par_cat = charger_plan()
    e = etiqueter(m, plan_par_nom, plan_par_cat, noms_propres(),
                  statuts_des_consignes(tous), time.strftime("%Y-%m-%d"))
    montrer(e, m)

    champs = [("date", "1 date (AAAA-MM-JJ)"), ("tiroir", "2 tiroir"), ("sujet", "3 sujet"),
              ("resume", "5 resume en UNE phrase"), ("statut", "6 statut (%s)" % "/".join(STATUTS))]
    print("")
    print("Tape la bonne valeur, ou Entree pour garder ce qui est propose.")
    for cle, question in champs:
        if donne.get(cle):
            e[cle] = donne[cle]
            e["d_ou_ca_vient"][cle] = "donne a la main, en ligne de commande"
            continue
        r = demander(question, e.get(cle) or A_TRANCHER)
        if r is None:
            print("Abandon : rien n'a ete ecrit.")
            return 2
        if r != (e.get(cle) or A_TRANCHER):
            e[cle] = r
            e["d_ou_ca_vient"][cle] = "pose a la main par Fred"
    if donne.get("personnes"):
        e["personnes"] = [x.strip() for x in donne["personnes"].split(",") if x.strip()]
        e["d_ou_ca_vient"]["personnes"] = "donne a la main, en ligne de commande"

    # On remet le statut dans son ecriture officielle ("Vivant" tape a la main -> "vivant"),
    # sinon le filtre ne le reconnaitrait pas plus tard.
    officiel = {_sans_accents(s): s for s in STATUTS}
    if _sans_accents(e["statut"]) not in officiel:
        print("")
        print("REFUSE : le statut doit etre l'un de %s. Rien n'a ete ecrit." % ", ".join(STATUTS))
        return 2
    e["statut"] = officiel[_sans_accents(e["statut"])]

    e["a_trancher"] = [c for c in ("date", "tiroir", "sujet", "resume", "statut")
                       if e.get(c) == A_TRANCHER]
    if not e["personnes"]:
        e["a_trancher"].append("personnes")
    e["pose_par"] = "a la main"
    e["pose_le"] = time.strftime("%Y-%m-%d %H:%M")

    dossier_sauv, copies = sauvegarder_avant([sortie])
    ajouter_une_ligne(sortie, e)
    print("")
    if copies:
        print("Sauvegarde datee avant ecriture : %s" % dossier_sauv)
    print("Etiquette ajoutee a la fin de %s (rien n'a ete efface)." % sortie)
    return 0


def main(argv=None):
    p = argparse.ArgumentParser(
        description="L'archiviste : il pose des etiquettes sur la bibliotheque, en lecture seule.")
    p.add_argument("--combien", type=int, default=ECHANTILLON_PAR_DEFAUT,
                   help="combien de morceaux traiter (0 = tous). Par defaut %d."
                        % ECHANTILLON_PAR_DEFAUT)
    p.add_argument("--sortie", default=FICHIER_ETIQUETTES, help="le fichier d'etiquettes a ecrire")
    p.add_argument("--rapport", default=FICHIER_RAPPORT, help="le fichier de rapport a ecrire")
    p.add_argument("--lister", action="store_true", help="lister les morceaux et leurs identifiants")
    p.add_argument("--source", default="", help="avec --lister : une seule source")
    p.add_argument("--contient", default="", help="avec --lister : ne garder que ce qui contient ce mot")
    p.add_argument("--voir", default="", help="montrer UN morceau et son etiquette, sans rien ecrire")
    p.add_argument("--etiqueter", default="", help="etiqueter UN morceau a la main")
    p.add_argument("--statut", default="", help="avec --etiqueter : le statut, sans question posee")
    p.add_argument("--date", default="", help="avec --etiqueter : la date")
    p.add_argument("--tiroir", default="", help="avec --etiqueter : le tiroir")
    p.add_argument("--sujet", default="", help="avec --etiqueter : le sujet")
    p.add_argument("--resume", default="", help="avec --etiqueter : le resume en une phrase")
    p.add_argument("--personnes", default="", help="avec --etiqueter : les personnes, separees par des virgules")
    p.add_argument("--avis", action="store_true",
                   help="v136 : montrer les avis de Luciana et ce qu'ils feraient, SANS RIEN ECRIRE")
    a = p.parse_args(argv)

    if a.avis:
        # LE REGARD, SANS LA MAIN : on montre exactement ce qu'une passe ferait des avis, et on
        # n'ecrit pas une ligne. C'est ce qu'on lance quand on veut comprendre avant d'agir.
        erreurs = []
        avis = lire_les_avis(erreurs=erreurs)
        par_id = rejets_par_identifiant(avis)
        deplacements, en_attente = tiroirs_a_creer(par_id)
        print("LES AVIS DE LUCIANA — %s" % FICHIER_AVIS)
        print("Le seuil est de %d rejets du MEME passage. Jamais un seul."
              % REJETS_POUR_UN_NOUVEAU_TIROIR)
        print("")
        print("avis lus                           : %6d" % len(avis))
        print("passages rejetes au moins une fois : %6d" % len(par_id))
        print("")
        print("CE QUI SERAIT DEPLACE (%d) :" % len(deplacements))
        for ident, d in sorted(deplacements.items(), key=lambda x: -x[1]["rejets"]):
            print("   %-22s %d rejets  ->  %s" % (ident, d["rejets"], d["tiroir"]))
            for r in d["raisons"][:3]:
                print("        \"%s\"" % r[:100])
        print("")
        print("CE QUI EST NOTE, SANS RIEN BOUGER (%d) :" % len(en_attente))
        for ident, d in sorted(en_attente.items(), key=lambda x: -x[1]["rejets"])[:40]:
            print("   %-22s %s" % (ident, d["pourquoi"]))
        print("")
        print("Erreurs de lecture : %d" % len(erreurs))
        for x in erreurs[:10]:
            print("   ! %s : %s" % (x.get("quoi"), x.get("ou")))
        print("")
        print("(Rien n'a ete ecrit.)")
        return 0

    if a.lister:
        erreurs = []
        tous = inventaire(erreurs)
        b = _sans_accents(a.contient)
        n = 0
        for m in tous:
            if a.source and m["source"] != a.source:
                continue
            if b and b not in _sans_accents(m["id"]) and b not in _sans_accents(m.get("texte")):
                continue
            n += 1
            print("%-9s %-70s %7d car." % (m["source"], m["id"][:70], len(m.get("texte") or "")))
        print("")
        print("%d morceau(x). Erreurs de lecture : %d" % (n, len(erreurs)))
        return 0

    if a.voir:
        erreurs = []
        tous = inventaire(erreurs)
        trouves, message = trouver(tous, a.voir)
        if message:
            print(message)
            for m in trouves[:30]:
                print("   %s" % m["id"])
            return 2
        m = trouves[0]
        plan_par_nom, plan_par_cat = charger_plan()
        e = etiqueter(m, plan_par_nom, plan_par_cat, noms_propres(),
                      statuts_des_consignes(tous), time.strftime("%Y-%m-%d"))
        montrer(e, m)
        print("")
        print("(Rien n'a ete ecrit.)")
        return 0

    if a.etiqueter:
        return etiqueter_a_la_main(a.etiqueter, a.sortie, {
            "date": a.date, "tiroir": a.tiroir, "sujet": a.sujet, "resume": a.resume,
            "statut": a.statut, "personnes": a.personnes})

    return passe(a.combien, a.sortie, a.rapport)


if __name__ == "__main__":
    sys.exit(main())
