# CHANTIER DU 11/10/2026 (soir) — FAIRE ARRIVER LES QUESTIONS DE L'ARCHIVISTE CHEZ LUCIANA

> **A LIRE D'ABORD, EN UNE PHRASE :** la chaine des questions est **installee et branchee
> dans luciana.py**, mais elle est **ETEINTE**, et **je n'ai pas pu lancer les tests** —
> Python m'a ete refuse dans cet atelier. Il y a un bouton `Tester les questions.bat` a
> double-cliquer : **tant qu'il n'est pas vert, n'allume pas.**

---

## 1. CE QUI A ETE MESURE (pas suppose)

Mesure faite sur le disque, ce soir, avant d'ecrire une seule ligne.

| Constat | Resultat |
|---|---|
| `luciana.py` | 34 232 lignes, 2 162 365 octets |
| `en_suspens`, `le_lot_attend`, `bloc_pour_l_assistante`, `bloc_pour_le_proprietaire`, `ranger_les_reponses`, `garder_les_questions`, `memoire_et_questions` dans `luciana.py` | **0 occurrence** — ton constat est exact |
| `biblio2_pont.py`, `biblio2_questions.py` chez Luciana | **absents** |
| `en_suspens` dans les modules | present : `biblio2_archiviste.py` (9x), `biblio2_plan.py` (7x), `biblio2_reprise.py` (3x), `biblio2_bibliothecaire.py` (1x) |

**Le diagnostic precis, qui est un peu different de « rien n'existe » :** ta base
**produit** bien des fiches `en_suspens` (archiviste, lignes 354-404), elle les **compte**
(`compter()`, ligne 439), elle les **affiche** (plan ligne 342, reprise ligne 379) — mais
**rien ne les transforme en question**, et rien ne fait redescendre une reponse. Le doute
etait note, et il restait note. D'ou tes 395 fiches muettes.

### L'etat de ta memoire 2 (lu, jamais ecrit)
`C:\Users\Fred\Luciana\bibliotheque2` contient : `arbre.json`, `BRANCHE.txt`,
`curseur.txt`, `marque_page.json`, `avancee.json`.

**`BRANCHE.txt` EXISTE : ta memoire 2 est DEJA allumee.** C'est le fait qui a decide de
toute l'architecture ci-dessous (voir §4, point A).
`plan.json` et `signal_plan.json`, eux, **n'existent pas encore**.

---

## 2. FICHIERS CREES ET MODIFIES — CHEMINS EXACTS

Tous dans `C:\Users\Fred\Desktop\Luciana_v161_memoire2_curseur\`.

### Sauvegarde (point 1 de ta demande)
Le bac a sable de cet atelier m'a **interdit de copier un fichier**. Mais tu avais deja
fait la sauvegarde ce soir a 19h05 : `luciana.py.SAUVEGARDE_2026-10-11_1905_avant_le_pont`.
**Je l'ai verifiee au SHA256 avant d'ecrire** — elle est identique a l'octet :

```
luciana.py                                          C82B5247...0A20B0AE
luciana.py.SAUVEGARDE_2026-10-11_1905_avant_le_pont C82B5247...0A20B0AE
```

C'est donc une vraie sauvegarde datee de l'etat d'avant mon intervention. Les quatre
modules `biblio2_*` existants **n'ont pas ete touches du tout** : rien a sauvegarder.

### Fichiers NEUFS (aucun risque : avant, ils n'existaient pas)
| Fichier | Role |
|---|---|
| `biblio2_questions.py` | La chaine des 4 temps, portee de Luminita et adaptee |
| `biblio2_pont.py` | L'orchestrateur : UN seul appel, son propre interrupteur, sa propre trace |
| `Brancher les questions.bat` | Allume la chaine (cree `QUESTIONS.txt`) |
| `Debrancher les questions.bat` | Eteint la chaine (enleve `QUESTIONS.txt`) |
| `Tester les questions.bat` | **Lance les tests et ecrit `RESULTAT_test_des_questions.txt`** |
| `_mesure_chaine_questions.py` | L'outil de mesure du §1, lecture seule. Supprimable. |

### Fichier MODIFIE : `luciana.py` — UN SEUL endroit
**Lignes 28179 a 28218**, juste apres le bloc qui remplit `bibliotheque_sens`, dans
`_repondre_tour()`.

**AVANT** (lignes 28174-28179) :
```python
    else:
        try:
            bibliotheque_sens, infos_sens = texte_bibliotheque_sens(...)
        except Exception as ex:
            infos_sens = {"erreur": str(ex)[:200]}
    try:
        rappel = rappel_automatique(message_utilisateur, hist, debut, chien)
```

**APRES** : exactement le meme code, avec ce bloc insere entre les deux (les commentaires
sont dans le fichier) :
```python
    try:
        import biblio2_pont as _pont_questions
        _sa_derniere_reponse = ""
        for _m in reversed(list(hist)[:-1]):
            if isinstance(_m, dict) and _m.get("role") == "assistant":
                _sa_derniere_reponse = str(_m.get("content") or "")
                break
        _bloc_questions = _pont_questions.questions_du_tour(message_utilisateur,
                                                            _sa_derniere_reponse)
        if _bloc_questions:
            bibliotheque_sens = ((bibliotheque_sens + "\n\n" + _bloc_questions)
                                 if bibliotheque_sens else _bloc_questions)
            try:
                infos_sens = dict(infos_sens or {})
                infos_sens["questions_de_l_archiviste"] = len(_bloc_questions)
            except Exception:
                pass
    except Exception:
        pass
```

**Aucune ligne existante n'a ete supprimee ni reecrite. Aucune fonction existante n'a
change de comportement.** On ne fait qu'**ajouter du texte** a une variable qui partait
deja, et seulement si le pont rend quelque chose.

### Ce que je n'ai PAS touche (tes interdits)
- `C:\Users\Fred\Lumi_appli` et tout ce qu'il contient : **jamais ouvert en ecriture**,
  seulement lu.
- `C:\Users\Fred\Luciana\bibliotheque2` : **lecture seule**, pas une ecriture. En
  particulier **`QUESTIONS.txt` n'a PAS ete cree** : c'est a toi d'allumer.
- `reglage_biblio2.json` : **inchange** (c'est pour ca que §4-D existe).
- Les 4 modules `biblio2_archiviste / bibliothecaire / plan / reglages` : **inchanges**.
- L'avalee : **jamais relancee**.

---

## 3. VERIFICATION FONCTION PAR FONCTION (point 2 de ta demande)

Chaque fonction que la version de Luminita appelle, verifiee dans **ta** base.

| Appel | Chez Luciana | Verdict |
|---|---|---|
| `arch.toutes_les_fiches(arbre)` | ligne 126, rend `[(cat, sous, fiche)]` | **identique** |
| `arch.etiquette_de(cat, sous, fiche)` | ligne 270 | **identique** |
| `arch.DIVERS` / `arch.A_TRIER` | lignes 66-67 | **identique** |
| `arch.repere_de(source, texte)` | ligne 103 | **identique** |
| `arch.ranger(arbre, souvenir, jugement)` | ligne 336 | **identique** |
| `arch.valider_jugement(j)` | ligne 170, rend `(sans_doute, propre, raison)` | **identique** |
| `arch.compter(arbre)` | ligne 427, a bien `fiches` et `en_suspens` | **identique** |
| `arch.arbre_charger` / `arbre_sauver` | lignes 313 / 322 | **identique** |
| `reglages.DOSSIER_BIBLIO2` | ligne 37 = `~/Luciana/bibliotheque2` | **identique, et deja le bon dossier** |
| `reglages.FICHIER_ARBRE`, `FICHIER_MARQUEUR_BRANCHE`, `FICHIER_MARQUE_PAGE` | lignes 38, 44, 39 | **identique** |
| `reglages.reglages_questions()` | **ABSENT** | adapte, voir §4-D |
| `reglages.FICHIER_QUESTIONS` / `FICHIER_LOT_PROPRIO` / `FICHIER_REPONSES` | **ABSENTS** | adapte, voir §4-D |
| `plan.texte_pour_l_assistante(plan)` | **ABSENT** — chez toi la fonction s'appelle **`texte_pour_luciana`** (ligne 333) | ecarte, voir §4-C |
| `bib.lire_le_besoin / chercher / construire_texte / noter / servir_avec_curseur` | lignes 475, 347, 331, 193, 393 — **tous presents** | **ecartes quand meme**, voir §4-B |

---

## 4. LES ADAPTATIONS, ET POURQUOI (le coeur du travail)

### A. DEUX INTERRUPTEURS, PAS UN — parce que ta memoire 2 est deja allumee
Le pont de Luminita s'allume avec `BRANCHE.txt`. **Chez toi ce fichier existe deja.** Si
j'avais recopie ca, la chaine serait partie **au prochain message**, sans que tu aies rien
decide : 395 questions ecrites d'un coup dans ton arbre, et un bloc de questions dans ta
conversation, par surprise.

La chaine a donc **son propre marqueur** : `~/Luciana/bibliotheque2/QUESTIONS.txt`.
Tant qu'il n'existe pas, `questions_du_tour()` rend `None` **a sa deuxieme ligne** et ne lit
rien d'autre. **Poser l'appel dans `luciana.py` ne change donc rien du tout aujourd'hui.**

### B. LE PONT NE PORTE QUE LES QUESTIONS, PAS LA MEMOIRE — l'adaptation la plus importante
Le pont de Luminita fait **deux** choses : il ramene la memoire (bibliothecaire a facettes +
curseur + plan) **et** il fait tourner la chaine.

**Chez toi, la moitie « memoire » existe deja et elle marche** : c'est `_biblio2_memoire()`
dans `luciana.py`, lignes 27413 a 27886 (~470 lignes), avec son propre curseur, son propre
filet, sa propre trace, son propre `plan_deja_vu.txt`. Elle est appelee ligne 28169.

Recopier cette moitie aurait fait trois degats :
1. le bloc de souvenirs serait parti **deux fois** dans le meme message ;
2. le plan serait remonte deux fois, et les **deux** `plan_deja_vu.txt` se seraient marche
   dessus (chacun croyant avoir deja servi l'empreinte que l'autre venait d'ecrire) ;
3. une fonction qui marche aujourd'hui aurait change de comportement — ton interdit n°4.

**Donc : le pont porte uniquement la chaine des questions.** Ta memoire continue de passer
exactement par ou elle passait hier.

### C. LE PONT NE TOUCHE PAS AU PLAN
Deux raisons qui vont dans le meme sens :
- la fonction n'a pas le meme nom chez toi (`texte_pour_luciana`, pas
  `texte_pour_l_assistante`) ;
- surtout : **`plan.json` n'existe pas encore chez toi**, et `_biblio2_avec_le_plan()`
  (luciana.py ligne 27659) colle « LE PLAN DE TA MEMOIRE A CHANGE » en tete **des que ce
  fichier apparait**. Refaire le plan depuis la chaine aurait donc fait changer le
  comportement d'une fonction qui marche, sans que tu l'aies demande.

La chaine ecrit l'arbre, elle ne refait pas le plan. Rien ne devient plus perime
qu'aujourd'hui, puisqu'aujourd'hui il n'y a pas de plan du tout.

### D. LES REGLAGES : lus avec `getattr`, pour ne rien avoir a modifier
Ton `biblio2_reglages.py` ne connait ni `reglages_questions()`, ni les trois chemins de la
chaine. Plutot que d'y toucher (et de toucher a `reglage_biblio2.json`, que tu as interdit),
`biblio2_questions.py` les demande avec `getattr` : **s'ils existent un jour ils sont pris,
sinon on prend les valeurs par defaut d'ici** — 5 questions par tour, 40 maxi dans un lot.
Les trois fichiers sont fabriques a partir de `DOSSIER_BIBLIO2`, donc
**`~/Luciana/bibliotheque2`** (point 3 de ta demande : le chemin de Luminita n'apparait
nulle part dans le code livre).

### E. LES NOMS DE CHAMPS DES FICHES : verifies, et identiques
J'avais d'abord cru a une difference : ton archiviste ecrit le motif du doute sous **deux**
noms, `pourquoi_en_suspens` (ligne 376) et `alerte_luciana` (ligne 404). **Verification
faite : c'est faux.** La ligne 404 est dans le **rapport** que `ranger()` rend a
l'appelant, pas dans la fiche. La fiche posee sur le disque (lignes 370-381) ne porte que
`en_suspens` et `pourquoi_en_suspens` — **exactement les noms que la chaine attend.**

Il n'y avait donc rien a adapter ici. J'ai quand meme laisse dans le code une ligne qui
efface `alerte_luciana` **s'il est present sur la fiche** : elle ne fait rien aujourd'hui,
et elle protege si l'archiviste se mettait un jour a l'y ecrire.

**Verifie aussi, et c'est important :** les nouveaux champs que la chaine ajoute aux fiches
(`question`, `question_etat`, `question_reponse`...) **ne peuvent pas fuiter dans le bloc de
memoire** envoye a Luciana. `_biblio2_construire_texte()` (luciana.py ligne 27770) ne lit
que `texte` et `resume`. Pas un caractere gaspille, et rien ne change a l'ecran.

### F. GARDE-FOU ANTI-BLOCAGE (n'existe pas chez Luminita — ajoute)
Si Luciana repond a cote du format (sans `1)`), ses 5 questions repartent **telles quelles**
au tour suivant, puis au suivant... et **les 5 memes questions bloquent la file pour
toujours**, les 390 autres derriere. Au bout de **3 fois** sans reponse lisible, la question
passe simplement dans ton lot. Rien n'est perdu, rien ne bloque.

### G. UN VRAI DEFAUT CORRIGE : le harcelement du proprietaire
En relisant le deroule tour par tour, j'ai trouve ceci dans la version d'origine : **une
question a laquelle TU viens de repondre « je ne sais pas » restait dans l'etat « posee au
proprietaire »... et repartait donc dans le lot du tour suivant.** Tu te la serais vue
reposer **a chaque message**, indefiniment — exactement le harcelement que ta regle
interdit.

Le test d'origine ne pouvait pas voir ce defaut : son lot d'essai ne contenait qu'une seule
question, donc le cas ne se presentait jamais.

**Correction :** une question que tu declines **s'endort 7 jours**. Elle n'est pas jetee,
elle reste lisible dans `questions.json` (champ `dort_jusqu_au`), et elle reviendra d'elle-
meme plus tard. Tu as la paix entre temps.

### H. LA CHAINE SE TAIT PENDANT UN RANGEMENT (ajoute)
L'archiviste et le pont ecrivent **tous les deux** `arbre.json`. S'ils ecrivent en meme
temps, le dernier ecrase le travail de l'autre, et on perd soit des fiches rangees soit des
reponses. Si `marque_page.json` a bouge dans les **90 dernieres secondes**, le pont se tait
et reprend tout seul apres.

---

## 5. LES TESTS — **JE N'AI PAS PU LES LANCER. JE NE DIS DONC PAS QU'ILS SONT VERTS.**

**Python m'a ete refuse dans cet atelier.** J'ai essaye six fois, de quatre facons
differentes (`python fichier.py`, `python -c`, `python -m py_compile`, via `bash` et via
PowerShell) : chaque fois la reponse a ete « cette commande demande une autorisation ».
Copier et supprimer un fichier m'ont ete refuses aussi.

**Donc, honnetement :**

| | Etat |
|---|---|
| Tests ecrits | **oui** — 31 controles dans `biblio2_questions.py`, 24 dans `biblio2_pont.py` |
| Tests **executes** | **NON. Aucun.** |
| `luciana.py` compile toujours ? | **NON VERIFIE PAR LA MACHINE.** Verifie a la lecture seulement (indentation a 4 espaces, dans le corps de `_repondre_tour`, bloc entierement sous `try`). |
| Chiffres reels (combien de questions posees, etc.) | **je ne les ai pas.** Les annoncer serait une invention. |

### Ce que le test fera quand tu le lanceras
Il monte une bibliotheque bidon de **9 fiches, dont 7 en suspens**, dans un dossier
`_demo_pont_questions` **a cote du code** — ta memoire reelle n'est ouverte ni en lecture ni
en ecriture — et il imprime les chiffres : combien de fiches en suspens recoivent une
question, combien de questions sont posees a l'assistante, combien partent dans ton lot,
combien sont tranchees, et combien de fiches il y a au depart et a l'arrivee.

Il verifie aussi, entre autres : que la memoire 2 branchee **ne suffit pas** a allumer la
chaine (§4-A), qu'aucune fiche n'est perdue, qu'une fiche deplacee garde son repere, que le
garde-fou du §4-F se declenche, et que la correction du §4-G tient.

### Les deux controles que j'ai deja vus echouer — et corriges
En relisant le deroule, deux de mes propres attentes etaient fausses, toutes les deux a
cause du defaut du §4-G. Elles sont corrigees dans le code livre, mais **je les ai trouvees
a la lecture, pas a l'execution** — c'est exactement pour ca qu'il faut lancer le test.

---

## 6. LA MARCHE A SUIVRE EXACTE POUR ACTIVER

**Dans cet ordre. Ne saute pas l'etape 1.**

1. **Double-clique `Tester les questions.bat`.**
   Il fait trois choses : il verifie que `luciana.py` compile, il lance le test de la brique,
   il lance le test du pont. Il ecrit tout dans `RESULTAT_test_des_questions.txt`.

2. **Si l'ecran dit « QUELQUE CHOSE RATE » : ARRETE-TOI.**
   N'allume pas. Envoie-moi `RESULTAT_test_des_questions.txt` et je corrige.
   *Si c'est `luciana.py` qui ne compile pas : ferme Luciana, remets la sauvegarde
   `luciana.py.SAUVEGARDE_2026-10-11_1905_avant_le_pont` par-dessus `luciana.py`, et tu es
   revenu a ce soir 19h05 exactement.*

3. **Si tout est vert : ferme Luciana et relance-la.** (Le nouveau bloc est dans
   `luciana.py`, il faut donc relancer **une fois**.) A ce stade **rien n'a change** : la
   chaine est eteinte.

4. **Double-clique `Brancher les questions.bat`.** Pas besoin de relancer : des ton message
   suivant, les questions arrivent.

5. **Ce que tu verras, au premier message apres l'allumage :** Luciana recoit 5 questions de
   son archiviste (elle, pas toi). Elle repond a ce qu'elle sait. Ce qu'elle ignore
   s'accumule, et t'est pose **en un seul lot**, jamais une par une.

6. **Pour eteindre, a tout moment :** `Debrancher les questions.bat`. Immediat, sans
   relancer. Les questions deja ecrites et les reponses deja donnees restent : si tu
   rebranches, la chaine reprend ou elle s'etait arretee.

### Ou regarder ce qui se passe
- `~/Luciana/bibliotheque2/trace_des_questions.jsonl` — une ligne a **chaque** message, avec
  l'avant/apres en chiffres. Fini les pannes muettes.
- `~/Luciana/bibliotheque2/questions.json` — les questions qui attendent encore.
- `~/Luciana/bibliotheque2/lot_pour_le_proprietaire.json` — le lot en cours.
- `~/Luciana/bibliotheque2/reponses.json` — qui a tranche quoi, et quand.

### Le rythme a prevoir
5 questions par tour. **395 fiches en retard = environ 79 messages** pour tout passer en
revue, et ton lot est plafonne a 40 questions. C'est volontairement lent : c'est ce qui
evite de te noyer. Si tu veux aller plus vite, dis-le-moi — le nombre est a un seul endroit
(`DEFAUT_QUESTIONS_PAR_TOUR`, en haut de `biblio2_questions.py`).

---

## 7. LES RISQUES QUE JE CONNAIS, DITS FRANCHEMENT

1. **Les tests ne sont pas passes.** C'est le risque n°1 et il est entierement leve par
   l'etape 1 du §6.
2. **Au premier allumage, l'arbre grossit.** `amorcer()` ecrit une question sur chacune des
   395 fiches en suspens, d'un coup, puis reecrit `arbre.json`. Ca devrait prendre moins
   d'une seconde, mais c'est la plus grosse ecriture que la chaine fera jamais.
3. **Deux ecritures concurrentes.** Le garde-fou du §4-H couvre le cas normal (90 s apres le
   marque-page). Il ne couvre pas un rangement qui serait reste bloque plus longtemps sans
   rien ecrire. **Le plus sage reste de ne pas allumer les questions pendant que
   « Ranger TOUTE ma memoire » tourne.**
4. **Luciana peut repondre a cote du format.** Couvert par le §4-F : au bout de 3 fois, la
   question part dans ton lot plutot que de bloquer la file.
5. **Un message de toi qui commence par « 1) » pendant qu'un lot attend** sera lu comme une
   reponse au lot. Une fiche sans question ouverte n'est jamais touchee, et un numero
   inconnu est ignore et trace — mais c'est le point ou je trouve la conception la plus
   fragile, et je prefere te le dire.
