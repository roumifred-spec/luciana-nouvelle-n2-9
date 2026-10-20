# CHANTIER « LA PLOMBERIE QUI MANGE MES REPONSES » — v164 (12/10/2026)

Un seul sujet : la plomberie. Rien sur le bloc de questions, la chaine des questions,
Luminita, ni sur la bibliotheque elle-meme.

---

## 0. CE QUE JE N'AI PAS PU FAIRE, DIT FRANCHEMENT

**L'atelier refuse d'executer Python.** `python --version` passe, mais toute execution de
code (`python -c`, `python mon_script.py`, `python -m py_compile`) est refusee par le
bac a sable. Consequences, sans enjoliver :

* je n'ai **pas** pu faire tourner le controle sur les chiffres d'APRES ;
* je n'ai **pas** pu faire passer le verificateur de syntaxe sur `luciana.py`. Les
  modifications ont ete relues ligne a ligne, mais **ce n'est pas la meme chose qu'un
  test qui passe**. Premiere chose a faire chez toi :

  ```
  python -m py_compile luciana.py
  ```

  (Pas de sortie = le fichier est bon.)

**La copie de sauvegarde datee a ete refusee elle aussi** (`Copy-Item` bloque, comme le
12/10). Le fichier d'origine n'est pas perdu pour autant : il est intact dans le depot.
Pour recuperer le `luciana.py` **d'avant ce chantier**, en entier :

```
git show HEAD:luciana.py > SAUVEGARDE_luciana_AVANT_v164_plomberie_2026-10-12.py
```

Et pour tout annuler d'un coup si ca ne te plait pas :

```
git checkout -- luciana.py
```

La liste exacte des morceaux touches est au point 4, et le detail complet se lit avec
`git diff luciana.py`.

---

## 1. LE DIAGNOSTIC (sur les mesures, pas sur des suppositions)

### 1.1 Ce que disent les chiffres du 12/10

32 mises a jour du grand tiroir relevees dans `~/Luciana/controle_memoire_sens.jsonl` :

| passages ajoutes | secondes |
|---|---|
| 3 | 115,2 |
| 4 | 78,3 |
| 8 | **0,9** |
| 121 | **1 461,7** |
| 230 | 138,1 |

**La duree ne suit pas le nombre de passages.** 3 passages coutent 115 s, 8 passages
coutent 0,9 s, 230 passages coutent 138 s. Un travail qui coute 115 s pour 3 passages et
0,9 s pour 8 n'est pas un travail : **c'est une attente.**

### 1.2 Les quatre causes trouvees, dans l'ordre

**CAUSE N°1 — le petit cache d'empreintes etait vide a chaque redemarrage, et vide en
entier des qu'il etait plein.** C'est la grosse.

`_SENS_PETIT_CACHE` garde l'empreinte de sens de chaque morceau de fiche. Il y a
5 879 fiches dans la bibliotheque 2 ; decoupees en morceaux de 700 caracteres, ca fait
**de l'ordre de 30 000 empreintes a calculer**.

* `sens_installer_moteur()` faisait `_SENS_PETIT_CACHE.clear()`. Donc **apres chaque
  redemarrage, le PREMIER message devait recalculer les ~30 000 empreintes d'un coup,
  dans ton tour.** C'est exactement ton symptome : « j'attends 10 a 30 minutes depuis le
  redemarrage ». Redemarrage a 14:18:56, premiere mise a jour a 14:44:18 : **24 min 22 s.**
* Et passe 50 000 entrees, le code faisait un `clear()` **total** puis recalculait
  **tout** dans le meme message. Pas un ralentissement : une falaise.

Verifiable dans le carnet : entre ton message de 14:55:15 et la trace `biblio2` du
message suivant a 15:02:14, il s'est passe **6 min 59 s**, et cette trace est ecrite a la
toute fin du travail de la bibliotheque 2.

**CAUSE N°2 — le fil de fond prenait le verrou de la conversation.**
`sens_indexer()` faisait `with _verrou_tour: charger_memoire()`. Or `repondre()` garde ce
verrou **pendant tout le tour**. Le fil de fond attendait donc la fin de ton tour, et la
duree ecrite dans le carnet **melangeait l'attente et le travail**. C'est pour ca que les
chiffres etaient illisibles.

**CAUSE N°3 — le travail etait monolithique.** Le fil de fond indexait tout ce qui
restait, d'une traite, sans limite de temps.

**CAUSE N°4 — `np.vstack` recopiait tout l'index a chaque paquet.** 73 693 x 384 nombres
= **113 Mo recopies pour ajouter 256 lignes**, et ca a chaque paquet.

Deux couts plus petits mais reels, trouves au passage : `arbre.json` (5 879 fiches) etait
**relu et re-analyse a chaque message** meme sans avoir bouge ; et `_colle` etait appele
**deux fois par fiche et par message** pour le meme resultat.

---

## 2. CE QUI A ETE REPARE

| # | Avant | Apres |
|---|---|---|
| 1 | Cache d'empreintes vide a chaque redemarrage, et vide en entier a 50 000 | Cache **ecrit sur le disque** et relu au demarrage ; quand il est plein on jette **la moitie la plus ancienne**, jamais tout ; un fil de fond le **pre-chauffe par tranches** pendant les temps morts |
| 2 | Le fil de fond prenait `_verrou_tour` | Il ne le prend plus (la memoire est ecrite par remplacement d'un coup : la lire est deja sur). Il regarde un **temoin de tour** et ne travaille que dans le calme |
| 3 | Mise a jour monolithique, sans limite | **Tranche de 20 s maximum**, arret propre a une frontiere de paquet, le reste repart a la tranche suivante. **Rien n'est abandonne** : le marque-page dit toujours ou on en est |
| 4 | `np.vstack` a chaque paquet (113 Mo recopies) | Place **reservee d'avance** (8 192 passages de marge) : une recopie tous les 8 192 passages au lieu d'une toutes les 256 |
| 5 | `arbre.json` relu a chaque message | Relu **seulement s'il a bouge** (taille + date) |
| 6 | `_colle` calcule deux fois par fiche | Calcule **une fois**, garde le temps du message |
| 7 | Decoupage des 5 879 fiches refait a chaque message | Fait **une fois**, garde tant que l'arbre ne bouge pas |
| 8 | Injection de 29 358 a 39 872 caracteres | Cible **~13 000**, doublons retires, extraits plus courts, **jamais une source en moins** |

### Ce qui n'a PAS bouge

Recherche par le sens, bibliotheque, souvenirs, consignes, carnets, chaine des questions,
bibliothecaire, archiviste, et **tous les fichiers de donnees**. Aucune faculte retiree :
ce sont des **attentes** qui ont ete retirees, pas des capacites.

Deux garde-fous ecrits expres pour ca :

* le nombre de sources servies **ne peut pas baisser** : on calcule d'abord combien
  l'ancienne regle en aurait servies, et on en sert au moins autant ;
* les raccourcis (cache d'arbre, memo de `_colle`, decoupage garde) gardent **la fiche
  elle-meme** a cote du resultat et verifient que c'est bien la meme : impossible de
  servir le resultat d'une fiche pour une autre.

---

## 3. LES CHIFFRES

### 3.1 AVANT — mesure reelle, lue dans le carnet

| | 10/10 (64 000 passages) | 12/10 (73 693 passages) |
|---|---|---|
| mises a jour relevees | 14 | 32 |
| passages indexes | 684 | 1 558 |
| temps total | 891,8 s | 5 923,8 s |
| **cout par passage** | **1,30 s** | **3,80 s** |
| duree mediane d'une tranche | ~30 s | **130,9 s** |
| **pire tranche** | 173,8 s | **1 461,7 s** (24 min) |
| petits lots (<= 15 passages) | 21,8 s en moyenne | **92,3 s en moyenne** |

Le detail qui tranche : **les petits lots.** Pour a peu pres le meme travail reel
(~5 a 10 passages), on est passe de 21,8 s a 92,3 s. Ce n'est pas le volume qui a
augmente, c'est **le cout fixe** — et un cout fixe de 92 s pour 9 passages, c'est de
l'attente, pas du calcul.

Choix du tour : 12,07 s et 12,75 s en debut d'apres-midi, **64,33 s** au message de
15:02:18, 33,67 s a 15:08:37.

Injection BIBLIO2 : **29 358**, **32 520** et **39 872** caracteres pour 10 a 12 sources
(contre 17 691 le 10/10). Le plafond etait a 40 000 et **il etait atteint**.

### 3.2 APRES — PAS ENCORE MESURE, ET JE NE VAIS PAS L'INVENTER

L'atelier refuse d'executer Python et le programme ne tourne pas ici. **Je n'ai aucun
chiffre d'apres a te donner.** Ce qui existe, c'est :

* ce qui est **garanti par le code** (verifiable en le lisant) :
  * une tranche de grand tiroir est bornee par le budget de 20 s, verifie a chaque
    paquet de 64 messages — donc de l'ordre de 20 a 25 s au pire, au lieu de 1 461 s ;
  * le premier message apres un redemarrage ne recalcule plus les ~30 000 empreintes :
    elles sont relues du disque ;
  * l'injection vise 13 000 caracteres au lieu d'un plafond de 40 000 atteint ;
* ce qui sera **mesure pour de vrai** par le script de controle, des que tu auras
  echange quelques messages en v164.

### 3.3 Comment obtenir les chiffres d'apres

```
python controle_plomberie_v164.py
python controle_plomberie_v164.py 2026-10-13
```

Le script lit le carnet en lecture seule, separe tout seul l'AVANT et l'APRES (les lignes
de la v164 portent `"v164": true`), et affiche VERT ou ROUGE pour chaque promesse. S'il
n'y a pas encore de mesures v164, **il le dit** au lieu d'annoncer un vert.

Les nouvelles mesures ecrites dans le carnet a chaque tour :

* grand tiroir : `travail_s`, `attente_s`, `par_passage_s`, `reste_a_faire`, `tranche_s` ;
* biblio2 : `cout` = `{arbre_s, besoin_ia_s, facettes_s, pertinences_s, texte_s,
  empreintes_calculees, fiches_notees, en_cache}`.

C'est cette derniere ligne qui dira, noir sur blanc, ou passent les minutes d'un tour.

---

## 4. LES MORCEAUX TOUCHES (tous dans `luciana.py`, aucun autre fichier du programme)

| Fonction / endroit | Ce qui change |
|---|---|
| en-tete du moteur de sens | bloc de diagnostic v164 + 5 reglages (`SENS_TRANCHE_SECONDES`, `SENS_BOUCLE_SOMMEIL`, `SENS_CALME_SECONDES`, `SENS_PETIT_CACHE_PLAFOND`, `SENS_PRECHAUFFE_PAR_TRANCHE`) |
| `FICHIER_SENS_CACHE_CLES` / `_VECTEURS` | **nouveaux** : le cache d'empreintes sur le disque |
| `_TOUR`, `_tour_commence`, `_tour_termine`, `_le_calme_est_revenu` | **nouveaux** : le temoin de tour |
| `_petit_cache_poser_lot`, `_petit_cache_charger`, `_petit_cache_sauver` | **nouveaux** : fini le vidage total, cache garde sur le disque |
| `_sens_charger_index` | pose la reserve au lieu d'un tableau exact |
| `_sens_poser_reserve`, `_sens_place_pour` | **nouveaux** : la place reservee d'avance |
| `_sens_ajouter` | `np.vstack` -> ecriture dans la reserve |
| `_sens_vider_index` | remet aussi la reserve a zero |
| `_signature_fichier`, `_SENS_EMPREINTE_FICHIERS`, `_SENS_RESTE` | **nouveaux** : ne pas relire un fichier qui n'a pas bouge |
| `sens_indexer` | plus de `_verrou_tour` ; budget de temps ; fichiers inchanges sautes |
| `sens_installer_moteur` | relit le cache d'empreintes du disque |
| `_boucle_memoire_sens` | ne travaille que dans le calme, par tranches, mesure honnete, pre-chauffage |
| `_sens_prechauffer_les_fiches` | **nouveau** : le pre-chauffage pendant les temps morts |
| `sens_classer` | table d'empreintes du tour, plus de vidage total |
| `_biblio2_arbre` | **nouveau** : l'arbre relu seulement s'il a bouge |
| `_biblio2_bouts_de_fiche` | **nouveau** : le decoupage d'une fiche, calcule une fois |
| `_ColleMemo` | **nouveau** : `_colle` calcule une fois au lieu de deux |
| `_biblio2_pertinences` | table d'empreintes du tour ; plus de vidage total ; `colle` en parametre |
| `_biblio2_coupe_propre` | **nouveau** : couper un extrait proprement, avec « […] » |
| `_biblio2_construire_texte` | cible ~13 000, doublons retires, part par source, jamais une source en moins |
| `_biblio2_memoire` | arbre en cache, memo de `_colle`, chronometre par etape |
| `_biblio2_candidats` | recoit le memo au lieu du module (meme appel, meme resultat) |
| `repondre` | previent le fil de fond du debut et de la fin du tour |
| le badge, en haut de l'ecran | **v162 -> v164** |

Aucun fichier `biblio2_*.py` n'a ete modifie. Aucun fichier de donnees n'a ete touche.

---

## 5. LES DEUX FICHIERS AJOUTES

* `controle_plomberie_v164.py` — le script de controle (lecture seule).
* `RAPPORT_plomberie_v164_2026-10-12.md` — ce rapport.

Deux fichiers de brouillon sont restes dans le dossier parce que l'atelier a refuse de les
effacer : `_mesure_plomberie.py` et `_analyse_12_10.py`. Ils ne servent a rien et ne sont
appeles par personne ; tu peux les supprimer.
