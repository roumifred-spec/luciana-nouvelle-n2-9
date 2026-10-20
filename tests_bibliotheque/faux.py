# -*- coding: utf-8 -*-
"""LE BANC D'ESSAI : un FAUX cerveau, un FAUX Google, un FAUX ancien programme.

Rien ici ne sort de la machine, rien ne touche la vraie memoire. Chaque essai travaille dans un dossier
jetable (tests_bibliotheque/home_<nom>) : ni ~/Luciana, ni ~/Luciana_neuve, ni le port 8002.

Ce que le faux cerveau rend est decide par l'essai, etape par etape (REPONSES["bibliothecaire"] = ...).
Un essai ne prouve donc JAMAIS que le SENS est bon : il prouve que le PROGRAMME tient ses regles.
"""
import os, sys, json, shutil

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(ICI)
NOUVELLE = os.path.join(RACINE, "nouvelle")
if NOUVELLE not in sys.path:
    sys.path.insert(0, NOUVELLE)

# Ce que le faux cerveau doit repondre, par etape ("bibliothecaire", "comprendre", "archiviste"...).
# Une valeur peut etre un dict/texte, ou une LISTE (une reponse par appel, dans l'ordre).
REPONSES = {}
APPELS = []          # la trace de tous les appels : (etape, systeme, contenu)


class _Bloc:
    def __init__(self, texte):
        self.type, self.text = "text", texte


class _Outil:
    def __init__(self, nom, entree):
        self.type, self.name, self.input, self.id = "tool_use", nom, entree, "u1"


class _Reponse:
    def __init__(self, blocs):
        self.content = blocs
        self.usage = None
        self.stop_reason = "end_turn"


def _a_rendre(etape):
    r = REPONSES.get(etape, {})
    if isinstance(r, list):
        r = r.pop(0) if r else {}
    return r


class ArretDemandeParFred(Exception):
    """Le nom vient de l'ancien programme (luciana.py) : on le garde tel quel, il n'est jamais montre."""


class FauxAncien:
    """L'ancien programme, juste ce dont le coeur se sert. Aucun appel reseau, aucune cle."""
    ArretDemandeParFred = ArretDemandeParFred
    DOSSIER = ""

    # --- les cerveaux
    def client_de(self, cerveau):
        return self

    def with_options(self, **k):
        return self

    def modele_api(self, cerveau):
        return "faux-cerveau"

    def fournisseur_de(self, cerveau):
        return "deepseek"

    def lire_cerveau(self):
        return "deepseek-flash"

    def lire_cle_gemini(self):
        return ""            # pas de cle : le moteur de sens tombe sur les mots en commun, et le dit

    def _options_reflexion(self, cerveau):
        return {}

    def _options_rangement_sans_reflexion(self, cerveau):
        return {}

    def compter_depense(self, cerveau, usage, quoi=""):
        return 0.0

    def _appel_cerveau(self, cli, cerveau, requete, max_tokens=8000):
        systeme = ""
        for b in requete.get("system") or []:
            systeme += b.get("text", "") if isinstance(b, dict) else str(b)
        contenu = json.dumps(requete.get("messages") or [], ensure_ascii=False)
        etape = _etape_de(systeme, contenu)
        APPELS.append((etape, systeme, contenu))
        r = _a_rendre(etape)
        if isinstance(r, dict) and r.get("outil"):
            return _Reponse([_Outil(r["outil"], r.get("entree") or {})])
        texte = r if isinstance(r, str) else json.dumps(r, ensure_ascii=False)
        return _Reponse([_Bloc(texte)])

    # --- l'ecran, les listes, les arrets : rien a faire ici
    def _tour_commence(self):
        pass

    def _tour_termine(self):
        pass

    def _arret_oublier(self):
        pass

    def _arret_si_fred_a_dit_stop(self, *a, **k):
        return None

    def _v180_ecrit(self, *a, **k):
        pass

    def _horodatage(self):
        return "[Repere temporel ecrit par le programme.]"

    def rappel_de_la_mission(self, m):
        return ""

    def texte_travaux_en_cours(self):
        return ""

    def rappel_des_choses_en_cours(self, m):
        return ""

    def _demande_photo_ecran(self, m):
        return False

    def outils_pour(self, cerveau):
        return []

    def _executer_outil(self, nom, entree):
        return "(faux outil %s)" % nom

    def enregistrer_le_pas_de_la_mission(self, *a):
        pass

    def _v180_appel_flux(self, cli, cerveau, requete, max_tokens=8000):
        return self._appel_cerveau(cli, cerveau, requete, max_tokens=max_tokens)

    def _retirer_appels_en_texte(self, texte):
        return texte, []

    def _info_cerveau(self, cerveau):
        return {"libelle": cerveau}

    _DERNIER_TOUR = {}

    def ajouter_evenement(self, *a, **k):
        pass


def _etape_de(systeme, contenu):
    """Quel travail on demande au cerveau : reconnu au MORCEAU DE CONSIGNE propre a chaque etape
    (pas au nom du cerveau : plusieurs etapes partagent la meme phrase de systeme)."""
    s = (systeme + " " + contenu).lower()
    for mot, etape in (("tu ecoutes et tu comprends", "comprendre"),
                       ("gestes vitaux deja faits", "journal_du_quotidien"),
                       ("un tiroir est devenu trop gros", "archiviste_division"),
                       ("tu ranges des fiches neuves dans son plan", "archiviste_rangement"),
                       ("ne respectent pas", "relecture"),
                       ("tu es son bibliothecaire", "bibliothecaire"),
                       ("tu decoupes ces messages en souvenirs", "archiviste"),
                       ("ce que ce moment apprend", "apprentissage")):
        if mot in s:
            return etape
    return "conversation"


# ------------------------------------------------------------------------------ montage / demontage
REGLAGES_LIVRES = os.path.join(NOUVELLE, "reglages.json")


def monter(nom, proprietaire=None, rangee=True):
    """Monte le coeur sur un dossier jetable, avec SON PROPRE fichier de reglages : le reglages.json
    livre dans nouvelle/ n'est jamais lu ni ecrit par les essais. proprietaire : None = pas de nom."""
    import coeur, json as _j
    dossier = os.path.join(ICI, "home_" + nom)
    assert os.path.basename(dossier).startswith("home_"), "un essai n'ecrit que dans tests_bibliotheque/home_*"
    shutil.rmtree(dossier, ignore_errors=True)
    os.makedirs(dossier, exist_ok=True)
    coeur.L = FauxAncien()
    coeur.CROCHETS.update({k: None for k in coeur.CROCHETS})
    coeur.poser_le_dossier(dossier)
    coeur.F_REGLAGES = os.path.join(dossier, "reglages.json")
    with open(coeur.F_REGLAGES, "w", encoding="utf-8") as f:
        _j.dump({"proprietaire": proprietaire or "", "bibliotheque_rangee": bool(rangee),
                 "diviser_a_partir_de": 4}, f, ensure_ascii=False)
    coeur.MOTEUR.panne = ""
    coeur.MOTEUR.cache = None
    coeur.MOTEUR.index_n, coeur.MOTEUR.index_v, coeur.MOTEUR.index_fait = [], [], set()
    REPONSES.clear()
    del APPELS[:]
    return coeur, dossier


def reglage_proprietaire_livre():
    """Ce que le fichier LIVRE (nouvelle/reglages.json) porte vraiment comme nom de proprietaire."""
    import coeur
    d = coeur.lire_json(REGLAGES_LIVRES, {})
    return str((d or {}).get("proprietaire") or "")


def appels_de(etape):
    return [(s, c) for e, s, c in APPELS if e == etape]


def tout_ce_qui_est_parti():
    """Tout ce qui a ete envoye au cerveau depuis le montage, en un seul texte."""
    return "\n".join(s + "\n" + c for _e, s, c in APPELS)


# ------------------------------------------------------------------------------ compter les essais
class Compte:
    def __init__(self, titre):
        self.titre, self.justes, self.rates = titre, 0, []
        print("\n=== %s ===" % titre)

    def oui(self, quoi, condition, detail=""):
        if condition:
            self.justes += 1
            print("  JUSTE  %s" % quoi)
        else:
            self.rates.append(quoi + ((" -- " + str(detail)) if detail else ""))
            print("  RATE   %s%s" % (quoi, ("  [" + str(detail) + "]") if detail else ""))
        return bool(condition)

    def fin(self):
        total = self.justes + len(self.rates)
        print("  -> %s : %d juste(s) sur %d." % (self.titre, self.justes, total))
        for r in self.rates:
            print("     RATE : %s" % r)
        return self.justes, total
