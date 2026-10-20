# COMMENT REVENIR EN ARRIERE (chantier du 11/10/2026, le soir, 2e partie)

## D'ABORD, CE QU'IL FAUT SAVOIR

La chaine des questions a **son propre interrupteur**. Pour tout arreter **tout de suite,
sans toucher a un seul fichier de code** : double-clique **`Debrancher les questions.bat`**.
Immediat, sans redemarrage. Les questions deja ecrites et les reponses deja donnees
restent sur place.

Dans 99 % des cas, c'est la seule chose a faire. Ce qui suit ne sert que si tu veux
remettre le code exactement dans l'etat d'avant ce chantier.

---

## LES SAUVEGARDES QUI EXISTENT

| Fichier touche | Sauvegarde |
|---|---|
| `biblio2_pont.py` | `SAUVEGARDE_biblio2_pont_AVANT_canal_cache_2026-10-11_2145.py` — copie faite AVANT la premiere ecriture. Contenu identique ; seules les fins de ligne sont en LF au lieu de CRLF (d'ou 607 octets de moins, un par ligne). Python lit les deux sans difference. |
| `biblio2_questions.py` | **pas touche du tout.** Rien a restaurer. SHA256 inchange : `035866F5 9DDBF259 A297F6AD FDAEB6FD 0092DAE7 8681DF9C D7A9F946 B46394F9` |
| `luciana.py` | **PAS DE COPIE DATEE — je dois le dire franchement.** Toutes les facons de copier un fichier m'ont ete refusees dans cet atelier (`Copy-Item`, `cp`, `xcopy`, `cmd copy`, redirection) : le controle de securite refuse le dossier qu'il declare lui-meme autorise. Le fichier fait 2,1 Mo, je ne pouvais pas le recopier a la main. |

**Empreinte de `luciana.py` AVANT mes deux ajouts** (relevee avant la premiere ecriture) :

```
SHA256  338631D6 B7FCB219 898B560E 0E7161D7 4A5D55D0 D94D4FFD 6A8842E6 52C04ED0
```

Le fichier etait a ce moment-la **identique a ce qui est dans le depot** (l'arbre de
travail etait propre). Le point de retour existe donc, meme sans copie datee.

---

## LES DEUX AJOUTS DANS `luciana.py`, ET RIEN D'AUTRE

Aucune ligne existante n'a ete supprimee ni reecrite. Deux ajouts, tous les deux
entierement sous un `try` : pour revenir en arriere, il suffit de les effacer.

### AJOUT 1 — dans le `try` deja greffe hier soir (vers la ligne 28209)

Effacer ces 11 lignes, qui sont **entre** `questions_du_tour(...)` et `if _bloc_questions:` :

```python
        #  LE CANAL CACHE (ajoute le 11/10/2026 au soir, DANS CE MEME try). On ajoute au bloc
        #  la consigne qui lui dit OU mettre ses reponses : entre deux marqueurs, a la toute
        #  fin de son message, parce que le programme va les y ramasser et LES DECOUPER avant
        #  l'affichage. Sans ce canal, ses reponses n'avaient aucun endroit ou aller : elles
        #  ne pouvaient arriver que dans sa reponse visible, et Fred refuse de voir ces
        #  questions -- d'ou les sept passages a "tranchees: 0". Purement additif : si la
        #  fonction manque ou leve, on garde le bloc exactement tel qu'il etait.
        try:
            _bloc_questions = _pont_questions.avec_le_canal_cache(_bloc_questions)
        except Exception:
            pass
```

### AJOUT 2 — juste apres la recolte des `[AVIS CONSIGNE ...]` (vers la ligne 29008)

Effacer le bloc de commentaire `LA CHAINE DES QUESTIONS, L'AUTRE MOITIE` **et** les cinq
lignes qui le suivent :

```python
    try:
        import biblio2_pont as _pont_questions_sortie
        texte = _pont_questions_sortie.recolter_les_reponses_aux_questions(texte) or texte
    except Exception:
        pass
```

Il doit alors rester, a la suite l'un de l'autre :

```python
    try:
        texte, _avis_consignes_du_tour = recolter_les_avis_consignes(texte, message_utilisateur)
    except Exception:
        pass
    # LE COMPTEUR, et il ne monte QUE sur un tour concerne (...)
```

---

## POUR REVENIR A AVANT TOUTE LA CHAINE DES QUESTIONS (hier soir 19h05)

`luciana.py.SAUVEGARDE_2026-10-11_1905_avant_le_pont` est toujours la. Le recopier
par-dessus `luciana.py` ramene a l'etat d'avant la greffe de la chaine, celle d'hier soir
comprise.
