# CHANTIER DU 11/10/2026 (soir, 2e partie) — LES DEUX MAILLONS QUI MANQUAIENT

## 0. LES TESTS QUI RATENT, AVANT TOUT LE RESTE

**JE N'AI PAS PU JOUER LES CONTROLES. JE NE DIS DONC AUCUN VERT.**

Python m'a ete refuse dans cet atelier, comme la derniere fois. Essaye, chaque fois refuse :
`python -V`, `python -m py_compile`, `python biblio2_pont.py`, `py -3 -m py_compile`, via
Bash **et** via PowerShell. **`luciana.py` n'a donc pas ete compile par la machine** : je
l'ai verifie a la relecture seulement (indentation a 4 espaces, dans le corps de
`_repondre_tour`, les deux ajouts entierement sous `try`).

**Copier un fichier m'a aussi ete refuse** : `Copy-Item`, `cp`, `xcopy`, `cmd copy`,
redirection `>`. Le controle de securite refuse le dossier qu'il declare lui-meme
autorise. Consequences exactes au §4.

| | Etat |
|---|---|
| Controles ecrits | **oui** — 19 controles neufs dans `biblio2_pont.py`, plus les 24 d'hier |
| Controles **joues** | **NON. Aucun.** |
| `luciana.py` compile ? | **NON VERIFIE PAR LA MACHINE** |

**La marche a suivre : double-clique `Tester les questions.bat`.** Il n'a pas eu besoin
d'etre modifie : il compile `luciana.py`, joue la brique, joue le pont — et les 19
controles neufs sont dedans. **Tant qu'il n'est pas vert, ne rallume pas.**

---

## 1. LA CAUSE DU MANQUE N°1 — ELLE EST CERTAINE

**Les reponses de l'assistante n'etaient pas « mal lues ». Il n'y avait rien a lire.**

Ta mesure, aux sept passages :

```
"reponses_de_l_assistante": {"tranchees": 0, "parties_au_lot": 0, "numeros_inconnus": []}
```

**Ce sont les trois zeros ENSEMBLE qui donnent la preuve.** Regarde
`ranger_les_reponses()` (`biblio2_questions.py`, lignes 626-672) : elle lit les lignes
numerotees, puis pour chaque numero trouve, soit elle tranche (`tranchees` monte), soit la
question part au lot (`parties_au_lot` monte), soit le numero n'existe pas
(`numeros_inconnus` se remplit). **Il n'y a pas de quatrieme sortie.** Donc trois zeros =
**le lecteur n'a trouve AUCUNE ligne numerotee**.

Et c'etait inevitable. `biblio2_pont.py` ligne 278 (version d'hier) :

```python
r = questions.ranger_les_reponses(arbre, reperes_poses, sa_derniere_reponse,
                                  par="l_assistante")
```

`sa_derniere_reponse` vient de `luciana.py` ligne 28203 : c'est **le dernier message
« assistant » de l'historique**, c'est-a-dire **sa reponse visible a l'ecran, celle que tu
lis**. La chaine allait donc chercher ses reponses **dans ce que tu vois**.

**C'etait une contradiction qu'aucun reglage ne pouvait resoudre :**

- si elle repond aux questions dans sa reponse visible → **tu vois defiler la masse des
  questions de l'archiviste**, ce que tu refuses ;
- si elle ne les y met pas → **il n'y a rien a lire**, les 420 questions restent ouvertes
  pour toujours.

Elle a choisi la deuxieme, et **elle a eu raison**. Les 415 restaient `ouverte` et les 5
`posee_a_l_assistante` indefiniment, exactement comme tu l'as mesure.

---

## 2. LA CAUSE DU MANQUE N°2 — UNE MOITIE CERTAINE, UNE MOITIE QUE JE N'AI PAS TROUVEE

### Tes trois questions, repondues dans l'ordre

| Ta question | Reponse, verifiee dans le code |
|---|---|
| La fonction qui fabrique le lot est-elle appelee du tout ? | **OUI.** `biblio2_pont.py` ligne 339 : `questions.bloc_pour_le_proprietaire(arbre, ecrire=True)` |
| Seulement dans les scripts de demo ? | **NON.** Elle est appelee dans `questions_du_tour()`, a chaque message |
| Le pont de Luciana l'expose-t-il ? | **OUI**, il l'appelle lui-meme |

**Donc le lot ne se fabriquait pas parce qu'il etait VIDE**, et le fichier n'etait alors
pas ecrit du tout (`bloc_pour_le_proprietaire`, ligne 706 : `if not file: return "", []`
— l'ecriture est plus bas, ligne 723). C'est exactement pour ca que
`lot_pour_le_proprietaire.json` n'existait dans **aucun** dossier reel : il n'a jamais eu
une seule question a mettre dedans.

### Pourquoi il etait vide : deux portes, une fermee a coup sur

Il n'y a que **deux** chemins vers l'etat `a_poser_au_proprietaire` :

1. **l'assistante dit « je ne sais pas »** (`ranger_la_reponse`, ligne 584). **Cette porte
   etait fermee a 100 %** : c'est la cause n°1. Elle ne pouvait jamais dire « je ne sais
   pas », puisque sa reponse n'etait jamais lue.
2. **le garde-fou des 3 relances** (`_passer_au_lot_les_restees_sans_reponse`, ligne 201).

### CE QUE JE N'AI PAS TROUVE, ET JE LE DIS FRANCHEMENT

**En lisant le code, la porte n°2 aurait du s'ouvrir a ton 4e passage** (21h25) : le
compteur `question_fois_posee` monte de 1 a chaque passage (ligne 196), et a 3 la question
part au lot. Tes sept passages auraient donc du produire
`"passees_au_lot_faute_de_reponse": 5`.

**Tu mesures que ca ne s'est jamais produit, et je ne sais pas expliquer pourquoi a partir
du code seul.** Le test d'hier joue ce garde-fou et il est cense passer. Je ne peux pas
lire ta memoire reelle depuis cet atelier, et **je n'invente pas une cause**.

**Les deux endroits exacts ou la reponse se trouve**, si tu veux qu'on la cherche :
`trace_des_questions.jsonl` → le champ `passees_au_lot_faute_de_reponse` ; et `arbre.json`
→ le champ `question_fois_posee` sur les 5 premieres fiches (vaut-il 0, ou 7 ?).

**Et je l'ai rendu sans objet** : la porte n°1 est maintenant grande ouverte, et j'ai
ajoute une **troisieme** porte, immediate, qui ne depend d'aucun compteur (§3).

---

## 3. CE QUI A ETE CHANGE

### A. LE CANAL CACHE — un endroit a elle pour repondre

Deux marqueurs, qu'**elle** ecrit a la toute fin de son message :

```
[REPONSES A MON ARCHIVISTE]
1) ...
2) ...
[FIN REPONSES A MON ARCHIVISTE]
```

Le programme **lit** ce bloc, fait redescendre chaque reponse sur sa fiche, et **DECOUPE le
bloc de ce qui part a l'ecran et dans la memoire**. Tu ne vois rien, et les reponses
arrivent quand meme.

**Ce n'est pas une invention** : `luciana.py` fait exactement ca depuis la v136 pour les
marques `[AVIS #...]` (`recolter_les_avis`, ligne 4402), au meme endroit du meme tour. On
reprend un procede qui a deja fait la preuve qu'il tient.

**Lecture volontairement tolerante** (`_numeros_lisibles`) : `**1)**`, `- 1)`, `  2.`,
`3 -`, `• 1.` sont tous lus. Sans ca on retombait sur le meme defaut en silence.

### B. LA TROISIEME PORTE — ce qu'elle ne tranche pas part chez toi, tout seul

Une question posee a l'assistante n'a plus que **trois** sorties, et il n'y en a pas
d'autre :

| Elle... | Resultat |
|---|---|
| repond quelque chose | la fiche est **tranchee**, elle n'est plus en suspens |
| dit qu'elle ne sait pas | la question part dans **ton lot** |
| **n'en parle pas du tout** | la question part dans **ton lot** ← **NEUF** |

C'est cette troisieme ligne qui rend la chose **obligatoire** : plus rien de ce qu'elle n'a
pas tranche ne peut rester en l'air, et ca ne depend d'aucun compteur.

### C. LE LOT T'EST POSE PAR LE PROGRAMME, PLUS PAR SA VIGILANCE

**C'etait le vrai defaut de conception.** Avant, le lot partait dans **son prompt** avec
cette consigne (`CONSIGNE_DU_LOT`) :

> « pose-le au proprietaire, tel quel, en une seule fois, dans ta reponse »

**Le lot n'arrivait donc chez toi que si elle y pensait** — exactement la vigilance que ta
regle interdit (« c'est ca que le systeme doit t'OBLIGER a faire »). Pire : les fiches
etaient marquees « posee au proprietaire » meme si tu ne les avais jamais vues.

Maintenant, le lot est seulement **prepare** par `questions_du_tour()`, et c'est **le
programme lui-meme** qui l'ecrit sous sa reponse, **d'un seul coup, une seule fois**
(`recolter_les_reponses_aux_questions`). Elle n'a plus rien a relayer et plus rien a
oublier. `CONSIGNE_DU_LOT` est laissee dans le fichier, annotee **NE PAS LA REBRANCHER**.

### D. UN DEFAUT QUE J'AI TROUVE EN TRACANT LE TOUR SUIVANT, ET CORRIGE

Le lot que le programme ecrit a l'ecran est **numerote lui aussi** (« 1) ... 2) ... »), et
il entre dans la memoire avec sa reponse. Au tour suivant, l'ancien chemin (ligne 278)
aurait relu ces numeros **comme si c'etaient ses reponses** — et aurait tranche 5 fiches
qui allaient tres bien, avec des questions en guise de reponses.

**Correction** : la numerotation est oubliee a chaque tour apres le ramassage. Ce qui n'a
pas ete tranche est simplement repose au tour suivant, avec une numerotation neuve. Rien
n'est perdu. (Un controle neuf verifie ce point precis.)

### E. TA REGLE N°4 EST TENUE PAR LE PROGRAMME

Tu ne vois **jamais** : les marqueurs, les questions de l'archiviste, ses reponses. Trois
controles neufs verifient ce point sur le texte exact qui t'arrive. Seul le lot de ce
qu'elle **n'a pas su trancher** te parvient, regroupe.

### F. LE DEFAUT DEJA CORRIGE HIER N'EST PAS REINTRODUIT

Une question a laquelle tu reponds « je ne sais pas » **s'endort 7 jours**. Un controle
neuf le verifie **apres** tous les changements de ce soir.

---

## 4. LES GARDE-FOUS — CE QUI EST TENU, ET CE QUI NE L'EST PAS

| Garde-fou | Etat |
|---|---|
| Une seule ecriture a la fois | **tenu** (7 ecritures, une par une) |
| Ne pas toucher au programme de Luminita | **tenu** — son dossier et son depot n'ont jamais ete ouverts, ni en lecture ni en ecriture |
| Ne rien ecrire dans les donnees de ta memoire | **tenu** — `C:\Users\Fred\Luciana\bibliotheque2` est hors de ma portee dans cet atelier (l'acces m'a ete refuse). Les controles tournent sur 6 fiches bidon dans `_demo_pont_questions`. **Les 420 vraies questions ne sont pas touchees.** |
| Ne pas relancer l'avalee, ne pas toucher a l'arbre ni aux seuils | **tenu** |
| Ne pas modifier les fonctions existantes | **tenu a une exception pres, dite franchement** : j'ai retire 1 ligne dans `questions_du_tour()` (etape 6) — celle qui poussait le lot dans son prompt. **C'etait le defaut lui-meme** : le laisser, c'etait te montrer le lot deux fois (une par elle, une par le programme). Tout le reste est purement ajoute. `biblio2_questions.py` n'a **pas ete touche du tout** (SHA256 inchange). |
| Les 20 lignes greffees dans `luciana.py` : rester dans le meme try | **tenu** — l'ajout du canal est dans ce meme `try`. Le ramassage de sortie a forcement son propre `try`, 800 lignes plus bas : la reponse n'existe pas encore a l'endroit du premier bloc. |
| Copie de sauvegarde datee de chaque fichier touche | **A MOITIE SEULEMENT. Lis le §5.** |

---

## 5. LES SAUVEGARDES — CE QUI EXISTE VRAIMENT

| Fichier | Sauvegarde |
|---|---|
| `biblio2_pont.py` | **oui** : `SAUVEGARDE_biblio2_pont_AVANT_canal_cache_2026-10-11_2145.py`, faite avant la premiere ecriture. Contenu fidele ; fins de ligne en LF au lieu de CRLF (607 octets de moins, un par ligne — Python lit les deux pareil). |
| `biblio2_questions.py` | **pas touche.** SHA256 inchange, verifie apres coup : `035866F5...B46394F9` |
| `luciana.py` | **PAS DE COPIE DATEE.** Toutes les commandes de copie m'ont ete refusees, et le fichier fait 2,1 Mo : je ne pouvais pas le recopier a la main. |

**Ce qui remplace la copie manquante**, et qui est utilisable :

- son **SHA256 d'avant mes deux ajouts** : `338631D6 B7FCB219 898B560E 0E7161D7 4A5D55D0
  D94D4FFD 6A8842E6 52C04ED0` ;
- il etait alors **identique a ce qui est dans le depot** (l'arbre de travail etait propre) :
  le point de retour existe ;
- **`ANNULER_le_canal_cache_2026-10-11.md`**, ecrit a cote, qui donne mot pour mot les deux
  blocs a effacer pour revenir en arriere ;
- et surtout : **`Debrancher les questions.bat`** arrete tout immediatement, sans toucher a
  une ligne de code.

---

## 6. LES CHIFFRES AVANT / APRES

### Ce que tu as mesure (AVANT) — tes chiffres, pas les miens

| | |
|---|---|
| Questions ecrites sur les fiches en suspens | 420 |
| `en_suspens_sans_question` | 0 |
| Questions posees a l'assistante, par passage | 5 |
| **Reponses reprises** | **0 — aux 7 passages** |
| `a_poser_au_proprietaire` | **0 — en permanence** |
| `posee_au_proprietaire` | **0 — en permanence** |
| `lot_pour_le_proprietaire.json` dans un dossier reel | **inexistant** |

### Ce que les controles neufs mesureront (APRES) — sur 6 fiches bidon

**Ces chiffres sont ceux que le test est ECRIT pour verifier. Ils ne sont pas mesures :
je n'ai pas pu lancer le test.** Ils s'afficheront quand tu double-cliqueras le bouton.

| | Depart | Arrivee |
|---|---|---|
| Fiches | 6 | 6 (aucune perdue) |
| Fiches en suspens | 6 | 4 |
| Reponses reprises → fiches **tranchees** | 0 | **2** |
| Questions dans le lot | 0 | **3** (1 « je ne sais pas » + 2 jamais mentionnees) |
| `lot_pour_le_proprietaire.json` | inexistant | **ecrit, avec 3 questions** |
| Lot pose **a l'ecran par le programme** | jamais | **1 fois, et 1 seule** |
| Tranchees apres ta reponse au lot | 0 | **4** |

**Les chiffres sur tes 420 vraies questions, je ne les ai pas, et les annoncer serait une
invention.**

---

## 7. CE QUE TU VERRAS, ET CE QUE TU NE VERRAS PAS

**Tu ne verras pas** : les questions de l'archiviste, les reponses de Luciana, les
marqueurs. Jamais.

**Tu verras**, de temps en temps, sous sa reponse normale, **un seul bloc** :

> J'ai mis de cote 3 chose(s) que je n'arrive pas a classer toute seule, et je te les
> demande TOUTES EN UNE SEULE FOIS […]

Tu reponds par numeros, quand tu veux. Ce que tu laisses de cote reste ou il est. Ce a quoi
tu reponds « je ne sais pas » **s'endort 7 jours**.

---

## 8. LES RISQUES QUE JE CONNAIS, DITS FRANCHEMENT

1. **Les controles ne sont pas passes.** Risque n°1, entierement leve par le bouton
   `Tester les questions.bat`.
2. **`luciana.py` n'a pas de copie datee** (§5). Les deux ajouts sont sous `try` et tiennent
   en 16 lignes effacables a la main.
3. **Elle peut ne pas ecrire le canal du tout.** Couvert : au bout de 3 fois, ses questions
   partent dans ton lot. Mais si le compteur du §2 est vraiment en panne chez toi, **elles
   stagneraient** jusqu'a ce qu'elle se mette a utiliser le canal. **C'est le point ou je te
   recommande de regarder le premier `trace_des_questions.jsonl` apres rallumage** : le champ
   `caracteres_dans_le_canal` dira en une seconde si le canal fonctionne.
4. **Un seul lot a la fois.** Si tu ne reponds jamais a un lot, il reste ouvert et aucun
   nouveau ne se forme : les autres questions attendent. C'est volontaire (tu ne veux pas
   etre noye) mais c'est aussi une limite : rien ne te relance.
5. **Un message de toi qui commence par « 1) » pendant qu'un lot attend** sera lu comme une
   reponse au lot. Une fiche sans question ouverte n'est jamais touchee, mais c'est le point
   de conception que je trouve le plus fragile, et je prefere te le redire.
