# -*- coding: utf-8 -*-
"""
V196 (18/10/2026, decide avec Fred) : LE MOTEUR DE SENS DU BIBLIOTHECAIRE, CELUI DE GOOGLE.

CE QU'IL REMPLACE, ET RIEN D'AUTRE : le petit moteur (MiniLM) qui sortait de l'armoire les fiches
que le bibliothecaire lit ensuite en entier. Ce petit moteur ne savait pas assez bien juger le sens.
Le bibliothecaire, l'archiviste, la bibliotheque et le plan ne changent pas. Les autres recherches de
Luciana (conversations, carnets) gardent leur moteur : on n'y touche pas.

LE MOTEUR : gemini-embedding-001 de Google (le nom est dans reglage_biblio2.json, cle "v180").
Il transforme un texte en une "empreinte de sens" ; deux textes qui veulent dire la meme chose avec
d'autres mots ont des empreintes proches. Les fiches sont envoyees comme "documents", la phrase de
Fred comme "question" (c'est l'usage prevu par Google pour retrouver un document).

LA CLE : la meme que le cerveau Gemini (~/Luciana/cle_gemini.txt ou le panneau Cles).

CE QUI EST GARDE SUR LE DISQUE : les empreintes deja calculees, dans
~/Luciana/bibliotheque2/sens_google/ . Une fiche n'est envoyee a Google qu'UNE fois ; ensuite, a
chaque message, seule la phrase de Fred part. Chaque programme (Luciana, ou le calcul lance par
« CALCULER LE SENS DE MA BIBLIOTHEQUE.bat ») ecrit dans SES fichiers, et chacun relit ceux des
autres : les deux peuvent tourner en meme temps sans s'abimer.

EN PANNE (pas de cle, pas d'internet, Google refuse) : le moteur le dit (derniere_erreur) et rend
une erreur ; le bibliothecaire passe alors par son secours deja existant (il choisit lui-meme les
tiroirs dans le plan). Rien n'est invente, rien n'est cache : la raison est ecrite dans la trace.

LANCE A LA MAIN (python biblio2_moteur_google.py --tout) : calcule les empreintes de TOUTES les
fiches de la bibliotheque en service, une fois. On peut fermer la fenetre et relancer : il reprend
ou il en etait (ce qui est calcule est ecrit a chaque lot).
"""

import hashlib, json, os, sys, threading, time, urllib.error, urllib.request

URL = "https://generativelanguage.googleapis.com/v1beta/models/%s:batchEmbedContents"
PAR_APPEL = 100            # Google accepte 100 textes par appel (batchEmbedContents)
TEXTE_MAXI = 8000          # en caracteres ; les bouts de fiche font au plus 4000 : jamais coupe en pratique


def _cle_cache(modele, dimension, tache, texte):
    return hashlib.sha1(("%s|%s|%s|%s" % (modele, dimension, tache, texte))
                        .encode("utf-8", "replace")).hexdigest()


class PanneMoteur(Exception):
    pass


class Moteur:
    def __init__(self, lire_cle, modele, dimension, dossier, qui="luciana"):
        self.lire_cle = lire_cle          # une fonction : la cle est relue a chaque appel
        self.modele = str(modele or "gemini-embedding-001").strip()
        self.dimension = int(dimension or 768)
        self.dossier = dossier
        self.qui = "".join(c for c in str(qui) if c.isalnum()) or "luciana"
        self.cache = {}
        self.lus = {}                     # fichier -> (lignes deja lues, octets de vecteurs deja lus)
        self.verrou = threading.RLock()
        self.derniere_erreur = ""
        self.caracteres_envoyes = 0
        self._relire()

    # ---------------------------------------------------------------- le cache sur le disque
    def _fichiers(self):
        try:
            noms = os.listdir(self.dossier)
        except Exception:
            return []
        out = []
        for n in sorted(noms):
            if n.startswith("cles_") and n.endswith(".txt"):
                qui = n[5:-4]
                out.append((os.path.join(self.dossier, n),
                            os.path.join(self.dossier, "vecteurs_%s.f16" % qui)))
        return out

    def _relire(self):
        """Lit ce qui a ete ajoute depuis la derniere fois, dans tous les fichiers (les siens et
        ceux de l'autre programme). Ne leve jamais."""
        import numpy as np
        dim = self.dimension
        for f_cles, f_vect in self._fichiers():
            try:
                deja_lignes = self.lus.get(f_cles, 0)
                with open(f_cles, encoding="utf-8") as f:
                    cles = [l.strip() for l in f if l.strip()]
                taille = os.path.getsize(f_vect) if os.path.exists(f_vect) else 0
                lignes = min(len(cles), taille // (2 * dim))
                if lignes <= deja_lignes:
                    continue
                with open(f_vect, "rb") as f:
                    f.seek(deja_lignes * dim * 2)
                    brut = f.read((lignes - deja_lignes) * dim * 2)
                vect = np.frombuffer(brut, dtype="float16").reshape(-1, dim).astype("float32")
                for i, v in enumerate(vect):
                    k = cles[deja_lignes + i]
                    if k:
                        self.cache[k] = v
                self.lus[f_cles] = lignes
            except Exception:
                continue

    def _ecrire(self, couples):
        """Ajoute au bout de SES fichiers (jamais ceux de l'autre programme). Vecteurs d'abord,
        cles ensuite : une cle n'existe jamais sans son vecteur."""
        import numpy as np
        if not couples:
            return
        os.makedirs(self.dossier, exist_ok=True)
        f_cles = os.path.join(self.dossier, "cles_%s.txt" % self.qui)
        f_vect = os.path.join(self.dossier, "vecteurs_%s.f16" % self.qui)
        par_ligne = self.dimension * 2
        try:
            # Si une ecriture precedente a ete coupee (fenetre fermee), on remet les deux
            # fichiers d'accord en gardant ce qui est complet des deux cotes.
            lignes = []
            if os.path.exists(f_cles):
                with open(f_cles, encoding="utf-8") as f:
                    lignes = [l.strip() for l in f if l.strip()]
            taille = os.path.getsize(f_vect) if os.path.exists(f_vect) else 0
            complet = min(len(lignes), taille // par_ligne)
            if complet != len(lignes) or taille != complet * par_ligne:
                with open(f_vect, "r+b" if taille else "wb") as f:
                    f.truncate(complet * par_ligne)
                with open(f_cles, "w", encoding="utf-8") as f:
                    f.write("".join(k + "\n" for k in lignes[:complet]))
            with open(f_vect, "ab") as f:
                f.write(np.asarray([v for _k, v in couples], dtype="float32").astype("float16").tobytes())
            with open(f_cles, "a", encoding="utf-8") as f:
                f.write("".join(k + "\n" for k, _v in couples))
            self.lus[f_cles] = complet + len(couples)
        except Exception as ex:
            self.derniere_erreur = "empreintes calculees mais pas ecrites sur le disque : %s" % str(ex)[:200]

    # ---------------------------------------------------------------- l'appel a Google
    def _appeler(self, textes, tache, timeout):
        cle = self.lire_cle() if callable(self.lire_cle) else self.lire_cle
        if not cle:
            raise PanneMoteur("il manque la cle Gemini (panneau Cles, nom 'gemini')")
        corps = {"requests": [{"model": "models/" + self.modele,
                               "content": {"parts": [{"text": t}]},
                               "taskType": tache,
                               "outputDimensionality": self.dimension} for t in textes]}
        req = urllib.request.Request(URL % self.modele, data=json.dumps(corps).encode("utf-8"),
                                     headers={"Content-Type": "application/json",
                                              "x-goog-api-key": cle}, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                d = json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            try:
                detail = e.read().decode("utf-8", "replace")[:300]
            except Exception:
                detail = ""
            raise PanneMoteur("Google a repondu %s : %s" % (e.code, detail), ) from None
        except Exception as e:
            raise PanneMoteur("pas de reponse de Google : %s" % str(e)[:200]) from None
        emb = d.get("embeddings") or []
        if len(emb) != len(textes):
            raise PanneMoteur("Google a rendu %d empreintes pour %d textes" % (len(emb), len(textes)))
        self.caracteres_envoyes += sum(len(t) for t in textes)
        return [e.get("values") or [] for e in emb]

    def vecteurs(self, textes, tache="RETRIEVAL_DOCUMENT", timeout=60, reessais=0, dire=None):
        """Les empreintes (longueur 1) des textes, dans l'ordre. Ce qui est deja calcule vient du
        disque ; le reste part chez Google, par lots de 100, et est ecrit tout de suite.
        'reessais' : combien de fois attendre et reessayer quand Google dit « trop de demandes »
        ou est en panne passagere (0 pendant un message de Fred ; le calcul complet en met).
        Leve PanneMoteur si ca ne marche pas (la raison est dans derniere_erreur)."""
        import numpy as np
        textes = [str(t or " ")[:TEXTE_MAXI] or " " for t in textes]
        with self.verrou:
            cles = [_cle_cache(self.modele, self.dimension, tache, t) for t in textes]
            manquants = [(k, t) for k, t in zip(cles, textes) if k not in self.cache]
            if manquants:
                self._relire()            # l'autre programme les a peut-etre deja faits
                manquants = [(k, t) for k, t in dict(manquants).items() if k not in self.cache]
            for i in range(0, len(manquants), PAR_APPEL):
                lot = manquants[i:i + PAR_APPEL]
                essai = 0
                while True:
                    try:
                        vals = self._appeler([t for _k, t in lot], tache, timeout)
                        break
                    except PanneMoteur as ex:
                        self.derniere_erreur = str(ex)
                        passager = any(c in str(ex) for c in (" 429 ", " 500 ", " 502 ", " 503 ",
                                                               " 504 ", "pas de reponse"))
                        if not passager or essai >= reessais:
                            raise
                        attente = (20, 60, 180)[min(essai, 2)]
                        if dire:
                            dire("  Google : %s -- j'attends %d s et je reessaie." % (str(ex)[:120], attente))
                        time.sleep(attente)
                        essai += 1
                couples = []
                for (k, _t), v in zip(lot, vals):
                    v = np.asarray(v, dtype="float32")
                    if v.shape[0] != self.dimension:
                        self.derniere_erreur = ("Google a rendu une empreinte de %d au lieu de %d"
                                                % (v.shape[0], self.dimension))
                        raise PanneMoteur(self.derniere_erreur)
                    n = float(np.linalg.norm(v)) or 1.0
                    couples.append((k, v / n))
                for k, v in couples:
                    self.cache[k] = v
                self._ecrire(couples)
            self.derniere_erreur = ""
            return np.asarray([self.cache[k] for k in cles], dtype="float32")

    def deja_calcule(self, textes, tache="RETRIEVAL_DOCUMENT"):
        with self.verrou:
            return sum(1 for t in textes
                       if _cle_cache(self.modele, self.dimension, tache, str(t or " ")[:TEXTE_MAXI] or " ")
                       in self.cache)


# ==================================================================== le calcul complet, a la main
def _calcul_complet():
    """Lance par « CALCULER LE SENS DE MA BIBLIOTHEQUE.bat ». Prend les fiches de la bibliotheque
    en service, les coupe EXACTEMENT comme Luciana les coupe (c'est son propre code qui le fait),
    et calcule ce qui manque. Rien n'est modifie dans la bibliotheque."""
    print("CALCUL DU SENS DE TA BIBLIOTHEQUE (moteur de Google), une seule fois.")
    print("Tu peux fermer cette fenetre et relancer : il reprend ou il en etait.\n")
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import luciana as L
    reg = L._v180_reglages_biblio()
    if str(reg.get("moteur_de_sens") or "").lower() != "google":
        print("Le reglage dit que le moteur du bibliothecaire n'est PAS celui de Google "
              "(reglage_biblio2.json, \"moteur_de_sens\"). Rien a faire.")
        return 1
    mg = L._biblio2_moteur_google(qui="calcul")
    if mg is None:
        print("Impossible de demarrer le moteur : %s" % (L._V196_MOTEUR.get("erreur") or "?"))
        return 1
    arbre = L._biblio2_arbre()
    if not arbre:
        print("La bibliotheque en service est introuvable ou vide : %s" % L._BIBLIO2_ARBRE)
        return 1
    textes, vus = [], set()
    fiches = L._biblio2_toutes_les_fiches(arbre)
    for cat, sous, fi in fiches:
        tous, _e, _m = L._biblio2_bouts_de_fiche(cat, sous, fi)
        for b in tous:
            if b not in vus:
                vus.add(b)
                textes.append(b)
    deja = mg.deja_calcule(textes)
    reste = [t for t in textes if _cle_cache(mg.modele, mg.dimension, "RETRIEVAL_DOCUMENT",
                                             str(t or " ")[:TEXTE_MAXI] or " ") not in mg.cache]
    print("Fiches : %d. Passages a mesurer : %d. Deja faits (on les saute) : %d. A faire : %d.\n"
          % (len(fiches), len(textes), deja, len(reste)))
    t0 = time.time()
    fait = 0
    for i in range(0, len(reste), PAR_APPEL):
        lot = reste[i:i + PAR_APPEL]
        try:
            mg.vecteurs(lot, "RETRIEVAL_DOCUMENT", timeout=120, reessais=3, dire=print)
        except PanneMoteur as ex:
            print("\nARRET : %s" % ex)
            print("Ce qui etait fait est garde (%d passages). Relance le meme fichier pour reprendre." % fait)
            return 1
        fait += len(lot)
        print("  %d/%d  (%d s)" % (fait, len(reste), int(time.time() - t0)), flush=True)
    print("\nFINI : %d passages mesures en %d s. Caracteres envoyes a Google : %d."
          % (fait, int(time.time() - t0), mg.caracteres_envoyes))
    print("Le bibliothecaire s'en sert tout de suite, meme si Luciana est deja ouverte.")
    return 0


if __name__ == "__main__":
    if "--tout" in sys.argv:
        sys.exit(_calcul_complet())
    print("Usage : python biblio2_moteur_google.py --tout")
