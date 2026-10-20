# RAPPORT — « le fil gardé n'arrive pas » — 13/10/2026

**AUCUNE LIGNE DE CODE N'A ÉTÉ MODIFIÉE.** Le badge n'a pas été touché (il reste V166 dans ce
dépôt). Deux raisons, les deux vérifiées sur du réel, les deux expliquées ci-dessous. La doctrine
dit : « Si une règle ne peut pas être tenue, le dire franchement AVANT d'agir. Pas après. »

---

## 1. LE FICHIER À RÉPARER N'EST PAS CELUI QUE J'AI SOUS LA MAIN

| | cible annoncée | ce que j'ai réellement |
|---|---|---|
| chemin | `C:\Users\Fred\Desktop\Luciana_v161_memoire2_curseur\luciana.py` | `…\luciana_chantier_yp75hbno\luciana.py` |
| taille | ~2 322 500 octets | **2 300 600 octets** |
| badge | V171 | **V166** (ligne 31853) |
| « ordre de lire le fil gardé » (V171) | présent | **ABSENT** (0 occurrence) |

Le chemin du Bureau est refusé par le bac à sable de cette session : je ne peux ni le lire ni
l'écrire. Les sauvegardes les plus récentes du chantier (13/10 à 01h04 et 01h14) sont **toutes des
v166**. La V171 faite cette nuit n'est nulle part ici.

**Conséquence :** écrire la correction dans ce dépôt produirait un fichier V166 **sans** le travail
de la V171. En le réinstallant, Fred perdrait l'ordre posé cette nuit. C'est casser quelque chose
qui marche (interdiction n°2).

## 2. LE FIL GARDÉ ARRIVE DÉJÀ. CE N'EST PAS LUI QUI MANQUE.

Mesuré sur les fichiers réels de `C:\Users\Fred\Luciana` :

- `journee_rangee.json` → `"dernier": 6208` ; dernier rangement `2026-10-13 05:18`.
- `luciana_memoire.json` → **6242 messages**.
- Donc la fenêtre commence au message **6209** et il reste **33 messages** dedans
  (≈ 57 830 caractères, le chiffre du bandeau).

Chemin du code, lu ligne par ligne :

- ligne 3842 — `_debut_fenetre()` : `debut = dernier_message_range() + 1` → **6209**.
- lignes 30057-30074 — `messages` est construit à partir de **`hist[debut:]`** : les 33 messages
  du fil gardé.
- ligne 30562 — l'entête est collée **à l'intérieur de `messages[-1]`**, le dernier de ces
  33 messages.

**Le fil gardé part donc bien au cerveau : il EST la conversation elle-même.** Il n'est pas résumé
ni tronqué. Ce qui manque, ce n'est pas le fil : c'est un *bloc* portant son nom dans l'entête.

### Pourquoi on a cru qu'il manquait

Ligne **30369** :

```python
journee_liste, journee_detail = "", bibliotheque_sens
```

La variable s'appelle `journee_detail` (le détail du fil rangé) mais on y met
`bibliotheque_sens` (les passages choisis **par le sens**). Dans l'entête (lignes 30385-30386), à
l'emplacement réservé au fil, on lit donc des passages anciens choisis par le sens — exactement les
« 3 vieux passages des 7 et 9 octobre » constatés. Qui regarde l'entête conclut, de bonne foi, que
le fil a été remplacé par des extraits. Il ne l'a pas été : il est ailleurs dans le même message.

C'est écrit noir sur blanc dans le code depuis la v128, à la ligne 28954 :
`textes_journee_rangee()` « N'EST PLUS APPELÉE NULLE PART ».

### Pourquoi faire ce que demande la consigne coûterait très cher

Injecter le fil « EN ENTIER, comme un bloc obligatoire » dans l'entête enverrait les mêmes
**57 830 caractères une deuxième fois dans la même requête** — et l'entête est collée **après tous
les repères de cache** (lignes 30227-30228), donc cette copie est **payée plein tarif à chaque
message** : ≈ 17 000 jetons de plus par message, sans rien apporter de neuf.

C'est la règle n°4 / interdiction n°5 (cible ~5 €/jour, pas de gouffre à l'usage).

---

## AUTRES DÉFAUTS VUS — ÉCRITS, PAS RÉPARÉS (comme demandé)

1. **Ligne 30369 / ligne 30503** — le journal des coûts enregistre
   `journee_detail=len(journee_detail)`. Comme la variable contient en fait la bibliothèque, ce
   compteur étiquette des caractères de bibliothèque en « détail du fil rangé ». Toute lecture de
   `couts_appels.jsonl` sur cette colonne est donc fausse. C'est la racine de la confusion.
2. **Le mot « gardés » du bandeau** — `dernier_rangement.caracteres` vaut `14040` dans le fichier
   réel : c'est le nombre de caractères **rangés** (1 message), pas « gardés ». Les 57 830, eux,
   viennent de `_MESURE_JOURNEE`. Deux chiffres différents, un seul mot pour les deux.
3. **`_debut_fenetre()` n'a pas de garde-fou** (ligne 3842). Si `journee_rangee.json` portait un
   `"dernier"` supérieur au nombre réel de messages (mémoire restaurée, carnet plus récent que la
   mémoire), `hist[debut:]` serait **vide** et Luciana n'aurait alors vraiment plus aucun échange
   récent. Ce n'est **pas** le cas aujourd'hui (6208 < 6242), mais rien ne l'empêche.

## CE QU'IL FAUT DÉCIDER (à Fred)

- **A.** Me donner accès au vrai `luciana.py` V171 (le copier dans le dossier du chantier). Je
  refais le constat sur lui et, s'il y a un vrai défaut, je le corrige là où il est, badge V172.
- **B.** Si ce qui est voulu c'est seulement que l'emplacement du fil dans l'entête cesse de
  mentir : renommer / vider ce bloc, sans recopier le fil (zéro coût en plus).
- **C.** Si ce qui est voulu c'est que Luciana voie **plus loin** que les 33 derniers messages,
  alors ce n'est pas un bug : c'est le réglage « 50 000 caractères gardés », qu'il est interdit de
  toucher sans l'accord explicite de Fred.

## À SUPPRIMER

`_constat_fil.py` (racine du chantier) : script de mesure en **lecture seule** que j'ai écrit pour
ce constat. Le bac à sable m'a refusé sa suppression. Il ne sert plus à rien.
