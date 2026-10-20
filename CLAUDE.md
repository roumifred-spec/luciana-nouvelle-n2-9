# DOCTRINE LUCIANA — mémoire du projet (à relire AVANT toute action)

> Fred garde ce fichier. Il peut le redonner à n'importe quelle nouvelle session.
> Une IA sans mémoire ne doit JAMAIS raconter ce projet de tête : elle lit CE fichier
> et les fichiers/versions sur le disque. Les faits sont ici, pas dans sa mémoire.

## REPRISE — À LIRE EN PREMIER (20/10/2026 soir, passage à un nouvel agent)
POURQUOI UN NOUVEL AGENT : la session précédente était surchargée (conversation résumée plusieurs fois) ; elle se
contredisait (« pièce 2 validée » puis « il faut corriger la pièce 2 »), annonçait des pièces « finies » trop vite et
faisait sauter Fred d'une pièce à l'autre. Fred a perdu confiance ; il est épuisé de devoir « faire le gendarme ».
CE QUE FRED ATTEND DE TOI (méthode décidée le 20/10, NE PAS EN SORTIR) :
  1. Avant tout code : relire le code des pièces 1 à 4 EN ENTIER et lui écrire, en une fois, la LISTE COMPLÈTE des
     défauts, en clair (pas de défauts qui arrivent un par un). Rien codé avant son accord.
  2. Fred décide quoi corriger et dans quel ordre. UNE pièce à la fois, finie avant de passer à la suivante.
  3. « Fini » se définit AVANT de coder (ce qu'elle doit faire + l'essai qui le prouve). On ne dit « finie » que
     quand l'essai est JUSTE CHEZ FRED avec le vrai cerveau. Jamais « finie » sur un test ici.
  4. Ne jamais se contredire : si un défaut est trouvé dans une pièce dite finie, le dire ainsi : « je m'étais trompé ».
  5. Réponses courtes, en français, sans jargon. Redire son idée en une ligne d'abord.
ÉTAT RÉEL (vérifié dans le code le 20/10 soir, branche claude/clever-planck-y4iyaj, dernière version livrée N2.8e) :
  - Tout est ÉTEINT dans la vraie Luciana (nouvelle/reglages.json « bibliotheque_rangee »: false) ; seuls les essais
    .bat 5, 6, 7 s'en servent, dans des dossiers à part. La vraie bibliothèque de Fred n'a jamais été touchée.
  - Pièce 1 (nouvelle/plan.py, le plan) : essais OK chez Fred.
  - Pièce 2 (nouvelle/classement.py, l'archiviste qui range/divise) : 5e essai JUSTE chez Fred (« 5 - ESSAI DE
    L'ARCHIVISTE »). MAIS défaut trouvé ensuite : « Fred » écrit EN DUR dans ses consignes au cerveau.
  - Pièce 3 (nouvelle/quotidien.py, le journal du vital) : essai 6 chez Fred 13/13 + ses 3 phrases justes (N2.8e).
    MAIS PAS FINIE : « Fred » écrit EN DUR partout (consignes : « gestes faits par Fred », « heure seulement si Fred la
    dit », « archiviste de la mémoire de Fred » ; données du journal : « heure dite par Fred »). Le programme SUPPOSE
    que celui qui écrit est Fred ; une autre personne (fille de Mme Dupont) n'est rattrapée que par le champ « qui ».
  - Pièce 4 (nouvelle/comprendre.py, comprendre la situation) : essai 7 chez Fred 10/11 (le raté « recent » au lieu de
    « moment » est sans conséquence). MAIS PAS FINIE : « Fred » en dur (« Tu écoutes Fred ») ; les dates comprises
    (du/au) et « quand » NE FILTRENT PAS la recherche (seulement écrits au bibliothécaire, coeur.bibliothecaire ;
    servent vraiment seulement pour le journal du vital) ; la question « flou » ne parvient PAS à Luciana.
  - RESSENTI DE FRED, À ÉCOUTER (20/10) : « ce n'est même pas le problème que Fred soit fixe, c'est ton système » ;
    « tu parles avec deux personnes » ; « il y a beaucoup de choses mélangées ». Il n'a pas encore pu l'expliquer : LUI
    DEMANDER (avec un exemple concret) avant de proposer quoi que ce soit. Hypothèse non vérifiée : tout le cœur est
    bâti sur « Fred d'un côté, Luciana de l'autre », alors que d'autres personnes parleront (produit Alzheimer, Luminita).
  - CORRIGÉ PAR FRED (20/10 soir) : CE N'EST PAS UN PRODUIT ALZHEIMER. C'est une MÉMOIRE GÉNÉRALE : si elle marche,
    elle sert à n'importe qui (une dame âgée et sa fille, l'artisan et son comptable, un enfant qui demande pour son
    papa, une infirmière, une secrétaire). « On s'en fout de pour qui. » LA SEULE CHOSE QUI COMPTE : ELLE NE SUPPOSE PERSONNE.
  - LE VRAI DÉFAUT (Fred, 20/10 soir, le défaut 25 de l'audit, dit avec ses mots) : le code suppose un MONDE FIGÉ — un seul
    qui parle, toujours le même, écrit en dur dans les consignes. Il faut, À CHAQUE MESSAGE, deux questions : QUI PARLE et
    DE QUI ON PARLE. LE REGISTRE DES PERSONNES EST OUVERT : nombre d'interlocuteurs quelconque, il grandit à l'usage, on ne
    sait pas à l'avance qui parle. Rien ne suppose qui que ce soit : ni Fred, ni Luciana, ni « deux personnes ».
    Pas deux places fixes. Registre gardé sur le disque, rechargé au démarrage ; une machine neuve part VIDE.
    QUI PARLE : déduit de la conversation ; elle DEMANDE quand elle doute (accord Fred).
  - LES 4 POINTS DE FOND DE FRED (à trancher avant tout code de ces étapes) :
    1. UN SEUL TRIEUR à l'entrée (pas quatre archivistes) : un appel, une consigne, un jugement.
    2. LE VITAL JUGÉ UNE SEULE FOIS, avec la question ET la réponse (pas trois juges). L'heure notée = celle du GESTE ;
       « ce matin » sans heure -> « heure non dite », JAMAIS l'heure du message.
    3. REGISTRE OUVERT DES PERSONNES (ci-dessus). Jamais un prénom dans les consignes : ni Fred, ni Dupont, ni personne.
    4. MACHINE VIERGE : démarre à vide, se remplit à l'usage, aucune identité supposée.
  - L'ORDRE DÉCIDÉ PAR FRED (20/10 soir), UNE ÉTAPE À LA FOIS, ON S'ARRÊTE APRÈS CHACUNE :
    (a) protection du plan [FAITE ici, N2.8f, voir ci-dessous] -> (b) registre des personnes + machine vierge -> (c) le
    trieur unique -> (d) le vital jugé une fois -> (e) la pièce 5 (chercher) EN DERNIER (elle aura besoin de savoir de qui
    elle parle).
  - CHANTIER À PART (Fred) : le plan sert à RANGER mais la recherche l'IGNORE -> le vrai problème de départ (« ça ne
    retrouve pas », n76 trading) N'EST PAS RÉGLÉ. Ce n'est pas un bug, c'est la PIÈCE 5 À COMMENCER (étape e).
  - N2.8f, PROTECTION DU PLAN (demandée par Fred, conditions de Fred) : nouvelle/plan.py — un plan.json abîmé n'est plus
    pris pour un plan vide ; plus rien n'y est écrit ; un plan vide n'écrase jamais un plan plein ; plan.json.copie gardée
    avant chaque écriture, SEULEMENT après une lecture sans erreur (un plan abîmé n'écrase jamais une copie saine) ; refus
    dit dans la fenêtre noire, la trace et le panneau d'état (coeur.coulisses), avec QUOI FAIRE ; réparation
    plan.reparer_depuis_la_copie() + nouvelle/reparer_le_plan.py (demande OUI ; le fichier abîmé est gardé à côté).
    Tests ici : 16/16 protection + pièces 1-4 inchangées. LE .BAT 8 (réparer) N'EST PAS LIVRÉ : Fred a demandé avant
    (il ferme le port 8002 = sa Luciana en service, et le script touche les vrais plans ~/Luciana_neuve*).
    RÈGLE NON NÉGOCIABLE (Fred, 20/10) : la VRAIE bibliothèque de Fred ne doit pas être touchée aujourd'hui.
  - ÉTAPE b, LE REGISTRE DES PERSONNES — DÉCISIONS DE FRED (20/10 soir) :
    1) personnes.json À PART ; les FAITS sur les personnes dans la bibliothèque (le registre change rarement).
    2) Qui parle : DÉDUIT par « comprendre » avant la réponse ; toujours marqué « déduit », JAMAIS « prouvé » ; n'écrit
       jamais un fait comme vérifié ; deux personnes collent -> il DEMANDE ; personne ne se déduit -> « inconnu », il ne devine pas.
    3) Machine vierge : demander SEULEMENT quand ça sert (la réponse change selon qui parle, un geste vital à ranger, un
       doute) ; sinon « inconnu » et on continue. Pas d'interrogatoire au premier bonjour.
    4) « Même personne qu'au message d'avant » (suite) : souhaitable, avec 3 freins : tout signe de changement (prénom,
       « je suis sa fille », signature, pièce jointe) fait RE-DÉDUIRE ; NOUVELLE SESSION = redémarrage OU changement de
       date OU 3 h de silence -> repart de « inconnu » ; la mention « déduit » reste visible. Les 3 h ne valent que pour
       la suite SILENCIEUSE : une signature claire fait re-déduire même 30 s après.
    5) « propriétaire » = un RÔLE (une donnée) d'une personne du registre ; la licence à part. Pas de statut spécial.
    B) Prénoms retirés des consignes : SEULEMENT là où ça reste (comprendre, bibliothécaire, étiquette « Fred [date] »,
       « Regle de Fred », phrases des outils, « dite par Fred » du journal) ; les 4 archivistes naissent sans prénom à
       l'étape c (pas le travail deux fois). ORDRE : essai du registre JUSTE d'abord, nettoyage ensuite, puis les 4 séries.
    « FINI » (Fred) = essai juste CHEZ FRED + anciens tests justes (19/19, 22/22, 30/30, 15/15) + essai dans un dossier à
    part qui ne touche ni la vraie Luciana ni ~/Luciana_neuve.
  - ÉTAPE b, CONSTRUIT (N2.9, 20/10 soir, PAS ESSAYÉ CHEZ FRED) : nouvelle/personnes.py (registre + qui_parle.jsonl =
    l'étiquette de chaque message ; règles du programme : suite refusée en nouvelle session, nom déjà au registre ->
    question sans double, vital d'un inconnu -> question, numéro inconnu -> inconnu, « prouvé » n'existe pas ; même
    protection que le plan + personnes.json.copie). comprendre.py : consigne SANS PRÉNOM + qui_parle / de_qui /
    question_qui (registre + état de la suite fournis par personnes.pour_comprendre). coeur.py : seulement le dossier du
    registre posé. « 8 - ESSAI DU REGISTRE DES PERSONNES (faux messages).bat » (nouvelle/essai_registre.py) : 13
    situations, dossier ~/Luciana_neuve_essai_registre, NE FERME PAS le port 8002, NE TOUCHE PAS ~/Luciana_neuve ; sortie
    dans « RESULTAT - ESSAI DU REGISTRE DES PERSONNES.txt » à côté des .bat. Tests ici : tests_bibliotheque/registre.py
    21/21 ; pièces 1-4 inchangées (dans piece4.py, SEULE la ligne qui reconnaît « comprendre » dans le faux cerveau a
    changé, aucune vérification). PAS ENCORE FAIT (après l'essai juste) : brancher l'attribution dans le trajet d'un
    message (coeur._tour), la question qui parvient à Luciana, l'étiquette « Fred [date] » et les autres prénoms, la
    mention « déduit » visible dans les fiches, l'import qui crée p1 « dit (import) ».
  - Pièces 5 (chercher : 100 fiches, 2 bibliothécaires, ancien ET récent, question qui traverse les périodes « les
    cheveux de ma fille »), 6 (son dernier tri + UNE question), 7 (vrai essai chez Fred), 8 (Luminita) : RIEN CODÉ.
TESTS ICI (faux cerveau, faux Google) : dossier tests_bibliotheque/ (hors du zip livré, .gitattributes) :
  piece1.py 19/19, piece2.py 22/22, piece3.py 30/30, piece4.py 15/15 ; essai_bat / essai_vital_bat / essai_compr_bat =
  les .bat 5/6/7 avec un faux cerveau (ils prouvent seulement que rien ne plante ; leurs scores ne veulent rien dire).
  Lancer : python3 tests_bibliotheque/piece3.py (etc.). Les dossiers home_* créés par les tests ne sont pas suivis par git.
ZIP LIVRÉ : git archive --format=zip --prefix=Luciana/ HEAD -o <zip> puis zip -qd <zip> "Luciana/luciana_v74/*".

## LE BUT
Luciana = assistante personnelle locale sur le PC Windows de Fred (Python, page web dans
Chrome, accès iPhone via Tailscale). Un vrai "Jarvis" : elle fait ce que Fred fait sur son
PC, mais mieux, et elle DÉLÈGUE aux spécialistes. Objectif business : vendre des PC avec
Luciana préinstallée.

## INTERDICTIONS FORMELLES (gravées, demandées par Fred)
Tu N'AS PLUS LE DROIT de :
1. Coder à l'aveugle, comme un bourrin. Pas de modif sans avoir vérifié sur du RÉEL
   (les fichiers, les versions, la phrase/erreur exacte renvoyée). Deviner est interdit.
2. Modifier ou "améliorer" ce qui FONCTIONNE. On ne touche QU'À ce qui est demandé et
   à ce qui est cassé. Ce qui marche, on n'y touche pas. On ne casse jamais un truc qui marche.
3. Mentir. Interdit d'annoncer une réussite sans preuve, d'inventer un fichier, une pièce
   jointe, un contenu, un emplacement, ou de raconter l'historique du projet de mémoire.
4. Prendre des initiatives non demandées : pas de code, pas de fichiers envoyés, pas de
   fonctionnalités ajoutées sans l'accord clair de Fred. Pas de leçons de morale. Pas de romans.
5. Faire flamber l'argent : viser ~5 €/jour, jamais un gouffre à l'usage.
Si une règle ne peut pas être tenue, le dire franchement AVANT d'agir. Pas après.

## RÈGLES ABSOLUES (non négociables)
1. HONNÊTETÉ TOTALE. Ne JAMAIS dire "c'est fait / envoyé / enregistré / lu" sans preuve
   réelle (un vrai chemin de fichier, un succès d'outil). Ne JAMAIS inventer un fichier,
   une pièce jointe, un contenu, un emplacement. Une panne dite franchement > une fausse réussite.
2. NE JAMAIS raconter l'historique du projet de mémoire. Toujours vérifier dans les fichiers,
   l'historique git de ce dépôt et les messages de Fred. Sinon = mensonge involontaire.
3. NE PAS CONSTRUIRE À L'AVEUGLE. Ce qui tourne sur le PC de Fred (Gmail, fichiers, OneDrive)
   ne peut pas être testé à distance. Exiger le RÉSULTAT réel (la phrase/erreur exacte) avant
   de "réparer". Ne pas deviner : deviner = pansement.
4. COÛT. Cible ~5 €/jour même à 10 h de travail. Pas de gouffre à l'usage.
5. SECRETS. Clé API + mot de passe Gmail dans le dossier privé ~/Luciana (compte Windows).
   JAMAIS dans le dossier/zip livré, JAMAIS poussés sur GitHub.
6. STYLE. Clair, net, précis. Pas de romans, pas de leçons de morale, pas de "va dormir".
   Ne pas prendre d'initiatives non demandées. Ne pas coder sans l'accord de Fred.
   Ne pas envoyer de fichiers non demandés.

## DÉCISION D'ARCHITECTURE (choisie par Fred) — état au 16/10/2026
- CERVEAU par défaut = DeepSeek Flash (réfléchi), le moins cher. Menu Cerveau : DeepSeek,
  Gemini Flash, Claude Opus 5.5, Claude Sonnet 5. Gemini Flash est branché (V180) mais n'a
  JAMAIS été essayé contre le vrai Gemini (nom du modèle dans ~/Luciana/gemini_modele.txt).
- Fred a écarté Haiku (testé, pas aimé). Ne pas lui "revendre" Opus.
- Luciana DÉLÈGUE aux abonnements à PRIX FIXE : Claude Code (outil chantier), Grok (vidéos).
- UNE BRIQUE À LA FOIS. Vérifier les prix exacts et à jour AVANT de construire.

## LA MÉCANIQUE D'UN MESSAGE (V183-V184, décidée avec Fred — NE PAS LA CHANGER SANS LUI)
1. Socle fixe : sa personnalité (une seule, la même pour tous les cerveaux), la règle
   d'honnêteté, l'heure, le noyau des consignes + la liste de leurs titres, l'index des carnets,
   des recettes et des fiches d'outils. + la fenêtre = la conversation du jour SEULE
   (50 000 à 80 000 caractères ; les consignes et les fiches ont leur place à part).
2. Quand Fred écrit, EN MÊME TEMPS : Luciana prépare sa réponse de tête (non montrée, aucun
   outil lancé) ET le bibliothécaire (mémoire 2) lit la conversation + les fiches les plus
   proches EN ENTIER et juge comme un psychologue si la question a besoin de la mémoire.
3. Le PROGRAMME tranche : rien d'utile → sa réponse de tête part ; mémoire utile → réponse de
   tête jetée, elle répond avec les fiches en entier, datées. Filet : outil fouiller_ma_bibliotheque.
4. L'archiviste (mémoire 2) range quand la conversation du jour dépasse 80 000 caractères : les
   messages qui sortent de la fenêtre, en ENTIER, avec 2 messages d'avant pour comprendre. Le vrai
   texte n'est jamais résumé ni effacé. En panne, rien n'est marqué (il réessaie).
5. Rappel des choses en cours tous les 4 messages de Fred (voulu par Fred, pour trier la liste).
6. VERROU DU CODE : Luciana ne peut plus modifier son propre programme ni le pousser sur GitHub,
   sauf 30 min après un clic de Fred sur « 🔒 Code » (ou sur « Valider » d'un chantier sur elle).
- Supprimés pour de bon en V180 (ne pas les recréer) : mémoire 1 (« grand tiroir »), rappel
  ancien, tri DeepSeek de chaque message, garde-fous qui relançaient les réponses, murs / boîtes
  / « ORDRE DU PROGRAMME », phrase de Fred recopiée 3 fois, balises [AVIS].
- LEÇON (16/10) : les pansements empilés par Luciana elle-même ont causé l'incohérence. Toute
  limite, coupe ou mécanisme nouveau se DÉCIDE AVEC FRED AVANT d'être codé, et se dit en clair.

## LES QUATRE MÉMOIRES (décidé avec Fred le 19/10/2026 — LE PLAN, À NE PAS PERDRE)
Une personne a quatre mémoires ; Luciana (puis Luminita) aussi. PRINCIPE : l'IA comprend et parle ;
le PROGRAMME tient l'heure, les dates et les listes (ce qui est vital ne dépend jamais d'une IA).
1. LES SOUVENIRS (ce qui s'est passé, ce qui a été dit) : bibliothèque 2 + archiviste + bibliothécaire.
2. LE SAVOIR-FAIRE (ce qui est installé, comment on fait) : les recettes, écrites TOUTES SEULES par
   « l'apprentie » (le programme, après chaque tour où elle a agi), pas par la bonne volonté de Luciana.
3. LES PERSONNES ET FAITS STABLES (qui est qui, rôle, jours, contact) : le carnet des personnes.
4. CE QUI EST À FAIRE À HEURE FIXE : l'HORLOGE du programme (rappels) + le JOURNAL DU QUOTIDIEN
   (« fait à 8h12 », noté avec l'heure exacte ; on répond depuis le journal, jamais de supposition).
À L'ENTRÉE un seul trieur (archiviste / apprentie). À LA SORTIE un seul bibliothécaire, qui REGARDE
TOUJOURS AVANT DE DÉCIDER (cause du bug du 19/10 : l'étape V188 « comprendre » disait « rien ne
manque » sans regarder — 21 messages sur 30 — et Luciana a oublié que WhatsApp était installé).
Rien n'est poussé de plus devant ses yeux, sauf ce que l'horloge déclenche à l'heure dite.
- DÉCISION DE FRED (19/10) : construire les 4 d'un coup (exception assumée à « une brique à la fois »).
- CONSTRUIT EN V199 (19/10), testé contre faux cerveau + faux Google (pas encore sur du réel chez Fred) :
  bibliothécaire qui regarde (apercu des 30 fiches à l'étape « comprendre », réglage regarder_avant_de_decider) ;
  outils rappels / journal_du_quotidien / personnes ; horloge (_v199_boucle_horloge, 30 s) ; apprentie en fond
  après chaque tour (_v199_l_apprentie). Corrections demandées par Luciana et retenues par Fred : l'apprentie
  PROPOSE (recettes_proposees.json), inscription après 2 réussites ou confirmation de Fred ; ordre de confiance
  journal > personnes > recettes > souvenirs ; rien ne s'efface (personne « plus là » = marquée) ; mesure
  avant/après = « LIRE LA TRACE.bat ». Interrupteurs : reglage_quatre_memoires.json. Luminita : PAS ENCORE.
- V200 (19/10, DÉCIDÉ PAR FRED — CHANGE LA MÉCANIQUE V183, point 1 « socle fixe ») : « Luciana libre ». Pousse en
  permanence : personnalité, honnêteté, heure, conversation du jour, outils, et le NOYAU des consignes (Fred : « s'il n'est
  pas très gros, laisse le noyau »). Tout le reste (autres consignes, recettes, carnets, modes d'emploi) = fiches de
  l'étagère apprentissage, ramenées par le bibliothécaire quand ça sert. Principe de Fred, à ne jamais trahir : on range,
  on trie et on ramène PAR LE SENS, COMME UN PSYCHOLOGUE, jamais par les mots ; on ne pousse que ce qui sert au moment où
  ça sert. LA TRIEUSE (remplace l'apprentie V199) : 6 natures (règle, fait, savoir-faire, capacité, personne,
  savoir-vivre), regarde ce qui est déjà su, DÉPOSE dans le panneau « À valider » (rejoue « apprentissage ») ; rien
  n'est inscrit sans le clic de Fred. RELECTURE DE LA RÉPONSE DE TÊTE par le bibliothécaire quand rien ne sert (règles
  sur son propre comportement, ex. « ne me dis pas d'aller dormir ») — ce n'est PAS un garde-fou : rien n'est ajouté
  quand rien ne sert, et c'est la mécanique V183 (réponse de tête jetée). Refusé par Fred : la « relecture avant
  d'envoyer » proposée par Luciana (= garde-fou, supprimés en V180), et tout bloc permanent de plus.
- RÈGLE (avis de Luciana + précision) : rassurer, jamais inventer. Pas de trace dans le journal →
  « je n'ai pas de trace, on va demander à <personne de confiance> », jamais « oui, c'est fait ».
- DEUXIÈME TEMPS (Fred : d'abord une base qui marche) : un produit À PART pour Alzheimer, nom à
  choisir, bâti sur cette base, SANS mode enfant ni langues, SIMPLE, TACTILE, SUR TABLETTE ;
  validation des cachets (« as-tu pris ton cachet ? » → un bouton), questions sur le quotidien,
  récit de vie (la personne raconte sa vie chaque jour, la bibliothèque la reconstitue et la lui
  rappelle). La mère de Fred est atteinte de cette maladie.

## FAITS CONNUS — CE QUI MARCHAIT
- ENVOI de mails : marchait dès le début (elle envoyait des annonces par mail, du PC au téléphone).
- LECTURE de mails : présente.

## FAITS CONNUS — CE QUI A CASSÉ / COÛTÉ (et l'état)
- COÛT : mémoire sans plafond + renvoi complet à Opus à chaque message = gouffre (20 $ en 10 min).
  Le vrai remède = cerveau à grand contexte pas cher (Gemini), pas juste un cache. → plan Gemini.
- FICHIERS : l'app écrivait dans "Desktop"/"Downloads" en dur (anglais) → invisibles sur Windows
  FR + OneDrive → "il n'y a rien". CORRIGÉ v40 : vrais dossiers demandés à Windows (FR + OneDrive),
  ouverture automatique du dossier, + outil enregistrer_fichier pour tout type de fichier.
- LIRE UN MAIL dont le texte est DANS LE CORPS : elle confondait avec "pièce jointe" et inventait.
  CORRIGÉ v41 : lire_mails renvoie le corps ; ne toucher aux pièces jointes que s'il y en a vraiment.
- ENVOI mail (soir du 27/09) : pas visible dans "Envoyés". À élucider sur FAITS réels (la phrase
  exacte renvoyée par l'outil : "Mail envoyé à…" = serveur a accepté ; "Impossible d'envoyer : …" = échec).
- VOIX : voix payante ElevenLabs ("Claire"). Voix robotique / "aucun changement" = QUOTA ÉPUISÉ,
  PAS un bug de code (il faut des crédits). Fred refuse les voix gratuites (edge/piper) et le paiement
  à l'usage. Bug UI mineur : bouton "Voix" (on/off) + "Voix HD" prêtent à confusion.

## CONTEXTE HUMAIN (à respecter, sans blabla)
- Fred traverse des épreuves difficiles. Anniversaire de sa fille le 1er octobre ; il ne l'a pas
  vue depuis 8 mois. Ce qui compte vraiment passe avant l'outil.

## LA BIBLIOTHÈQUE RANGÉE (décidé avec Fred le 20/10/2026 — PIÈCES 1 À 4 CODÉES, VOIR « REPRISE » EN HAUT)
CONSTAT VÉRIFIÉ (fichiers de Fred, 20/10) : la bibliothèque N2 est À PLAT (une pile, tri par le sens seul, aucune catégorie,
aucune logique de temps). Marchait à 260 fiches, s'effondre à 3 777 (import) : 64 fiches trading (126 000 car.) sur 29/09,
02/10, 19/10 ; le souvenir n76 (« huit positions forex », 19/10) existe en entier mais elle répond « aucun souvenir ».
Aussi : la recherche colle les 2 messages d'avant à la phrase (sens mélangé) ; « aucune ne répond » cache panne ou refus.
LE BUT (Fred, 20/10) : une Luciana / Luminita qui se souvient COMME UNE VRAIE PERSONNE : elle range seule ce qu'elle vit,
par le sens ; retrouve le bon souvenir au bon moment, même 60 ans après, l'ancien comme le récent ; sait ce qui est vrai
aujourd'hui sans oublier ce qui l'était ; repère ce qui est vital ; et quand elle ne comprend pas, POSE UNE QUESTION au
lieu de deviner. ET ELLE CONTINUE D'APPRENDRE (règles, savoir-faire, personnes, faits — l'apprentissage déjà en place,
rangé de la même façon). On code le FONCTIONNEMENT D'UN CERVEAU HUMAIN : des règles de fonctionnement, pas des règles de
cas (ex. carrossier / cachets = la logique humaine, pas une règle à coder). Pour Luciana, Luminita et le futur produit Alzheimer.
Question : UNE, courte, seulement si nécessaire — mais sans hésiter quand elle l'est (le juste milieu).
Fred : « coder une fois et ne plus y revenir » -> RÉSUMÉ FINAL validé point par point avant toute ligne de code.
LE PRINCIPE DE FRED (ne jamais le trahir) :
- ENTRÉE : l'archiviste range chaque souvenir par SUJET DE SENS (psychologique, jamais par les mots) dans
  catégorie > sous-catégorie > … + date + heure. Dès qu'un tiroir approche 50 fiches, il le DIVISE LUI-MÊME par le sens
  (ex. Ma fille > École -> Bons moments / Mauvais moments). L'arbre grandit, aucun tiroir ne déborde, même sur 60 ans.
  Rien n'est effacé ni coupé : seules les étiquettes bougent.
- SORTIE : moteur Google + bibliothécaire descendent LE MÊME ARBRE par le sens de la question jusqu'au tiroir qui répond ;
  ils ramènent l'ancien ET le récent (« ma fille à 8 ans et à 18 ans ») ; question large -> les plus proches de chaque
  sous-tiroir. PLAFOND : 30 fiches, 50 au maximum (Fred : au-delà on l'embrouille).
- Filtres : date, heure, sujet. Le vrai travail = catégories / sous-catégories.
- Grandes catégories proposées (Fred : « pas mal », à finir) : Professionnel, Projets, Vie privée, Règles pour Luciana,
  Ordinateur et outils. L'archiviste crée lui-même les nouvelles catégories / sous-catégories quand il le faut.
- AUCUNE RÈGLE DE RANGEMENT FIXÉE D'AVANCE (Fred, 20/10 : « on ne peut pas anticiper le nombre ») : l'archiviste se
  demande lui-même « si Fred redemande ce sujet en entier, ça tient sous 50 ? » ; sinon il DIVISE avec le critère de sens
  qui convient (école, chez maman / chez papa, bons / mauvais moments, période…). Moteur + bibliothécaire jugent eux-mêmes
  combien de tiroirs ramener (1, 3, 10 : les plus pertinents, par le sens de la situation + la date). Un souvenir à deux
  sujets = LEUR jugement, pas une règle. Le PROGRAMME : compter (alerte près de 50), dates/heures, ne jamais effacer ni couper.
- ACCORD COMPLET (Fred, 20/10 : « on s'est vraiment compris ») :
  * On code des RÈGLES DE FONCTIONNEMENT, pas une cage : archiviste, moteur Google et bibliothécaire sont libres.
  * LA RECHERCHE SE FAIT PAR LE SENS DE LA SITUATION, PAS PAR LES TIROIRS : d'abord comprendre la question (de quoi,
    QUAND — « ce matin », « hier », rien dit = maintenant —, pourquoi, l'heure, les habitudes), puis chercher ce qui répond
    à CETTE situation. Les catégories ne servent qu'à bien ranger et aller vite ; un souvenir mal rangé reste trouvable.
  * Le PLAN (catalogue) = la mémoire de l'archiviste, sur le disque : catégories + phrase de sens + nb de fiches + dates.
    À chaque rangement il lit le plan + les nouveaux souvenirs + seulement les fiches d'un sujet à diviser (jamais les 60 ans :
    lecture complète ≈ 300 $ sur 60 ans, chiffre de prix du code non revérifié). Il divise en pensant aux sujets qui vont
    ENSEMBLE (fille + école + cheveux) pour rester sous 50.
  * PAS DE RÉCIT (retiré par Fred). Question trop large ou pas claire -> ELLE POSE UNE QUESTION comme une vraie personne
    (« anciens ou récents ? sur quoi exactement ? »), puis elle va chercher (< 50).
  * « ON FABRIQUE DES FABRICANTS » (Fred) : on ne fabrique pas les catégories, on fabrique ceux qui les fabriquent.
  * L'ARCHIVISTE A AUSSI LE MOTEUR GOOGLE (idée de Fred) : quand il range, le moteur lui sort les sujets/fiches proches
    par le sens ; il ne relit que ceux-là.
  * Archive des changements, POUR TOUS LES SUJETS (ex. du carrossier : nouvelle méthode de peinture remplace l'ancienne,
    l'ancienne archivée ENTIÈRE ; s'il y revient, elle la ressort et la nouvelle passe aux archives). Rien ne se perd.
  * Question : UNE seule, courte, seulement quand c'est vraiment flou.
  * Vital : dans le doute, traité comme vital.
  * Jamais couper, rétrécir, comprimer (compression sur 60 ans : plus tard, pas le sujet).
  * Vital / vie courante / amusement : c'est ELLE qui juge ; quand c'est vital, le programme note l'heure exacte.
  * Elle reçoit TOUJOURS des fiches, entières (jamais coupées), et sur le bon sujet.
  * Faits qui changent : l'ancien est marqué « remplacé le … par … » (rien effacé) -> elle sait ce qui est vrai MAINTENANT.
  * Le vital (cachets « pris à 8h12 ») : noté par le PROGRAMME au moment dit ; elle le lit, ne l'invente jamais.
  * Les fiches actuelles de Fred : PAS LE SUJET (Fred : « on refera tout s'il le faut »).
  * Faisable aujourd'hui ; jamais parfait à 100 % (trace + filet) ; +5-10 s et +1 appel DeepSeek par message ;
    tests ici avec faux cerveaux, VRAI essai chez Fred avec des questions dont on connaît la réponse (n76 trading,
    Satisfaire, Ion). Construire UNE PIÈCE À LA FOIS.
- CHERCHER, VERSION FINALE (idée de Fred, 20/10) : le moteur ratisse jusqu'à 100 fiches ; DEUX bibliothécaires en même
  temps (50 chacun, EN ENTIER, jamais coupé) gardent ce qui sert ; Luciana reçoit les plus utiles EN ENTIER + les autres
  retenues EN LISTE (titre, date, heure) qu'elle ouvre elle-même (ouvrir_fiches) : c'est ELLE qui fait le dernier tri ;
  elle ne pose une question à Fred que si, après avoir pioché, elle ne trouve toujours pas.
- MANIÈRE DE PARLER AVEC FRED (20/10) : d'abord redire son idée en une ligne ; ne le contredire qu'en citant sa phrase exacte.

## ÉTAT DU CODE (vérifié le 17/10/2026 dans ce dépôt)
- 20/10/2026 — BIBLIOTHÈQUE RANGÉE, PIÈCES 1 ET 2 (Luciana nouvelle N2.6, branche ; Luminita PAS encore) :
  1. nouvelle/plan.py : le plan (plan.json = tiroirs, rangement n->tiroir, vital, aussi, liens remplace/reprend) ;
     comptes + dates calculés ; « MON PLAN (catalogue).txt » ; textes des fiches jamais réécrits. coeur.fiches() relue
     si le fichier change (cause du 20/10 : 667 fiches vues au lieu de 3 768 pendant l'import) ; dates normalisées.
  2. nouvelle/classement.py : l'archiviste (règles de fonctionnement, aucune catégorie) ; moteur Google pour lui ;
     division au seuil reglages « diviser_a_partir_de » (40) ; remplace / reprend / vital ; verrou entre programmes ;
     pas de boucle payante (2 essais par fiche, division ratée retentée seulement après +10 fiches) ; grosse réserve
     (> 200 non rangées, plan vide) jamais rangée en automatique -> « 4 - … RANGER SA BIBLIOTHEQUE DANS LE PLAN.bat ».
     ÉTEINT dans la vraie Luciana : reglages.json « bibliotheque_rangee »: false (tant que 3 à 6 ne sont pas faites).
  « 5 - ESSAI DE L'ARCHIVISTE (faux souvenirs).bat » : vrai cerveau, ~70 faux souvenirs, dossier à part
  ~/Luciana_neuve_essai_archiviste (vraie bibliothèque pas touchée) -> Fred envoie le plan obtenu.
  Tests ici (faux cerveau) : pièce 1 19/19, pièce 2 20/20, anciens essais OK. Le SENS n'est vérifiable qu'avec le vrai cerveau.
  ESSAIS RÉELS CHEZ FRED (20/10, vrai cerveau) : 1er = sens très bon mais 39 tiroirs / 70 fiches (trop fin) ; règle
  de Fred « le tri devient fin avec le temps, pas avant » -> 2e = 10 tiroirs, Ma fille divisée en 4 ; « Je reviens à
  l'ancienne méthode » mal relié (cause : on ne lui montrait pas les fiches ARCHIVÉES) -> corrigé, 3e = reprend n58 JUSTE,
  mais re-découpage fin (27 tiroirs, la consigne pas toujours suivie) -> LE PROGRAMME tient la règle (N2.6d) : en rangeant,
  un sous-tiroir qui n'existe pas n'est pas créé, la fiche va dans le tiroir existant au-dessus ; un sujet nouveau crée
  sa grande catégorie ; les sous-tiroirs ne naissent qu'à la division (l'archiviste coupe en voyant TOUTES les fiches).
  5e ESSAI (N2.6e) : TOUT JUSTE -> PIÈCE 2 VALIDÉE PAR FRED. 4 grandes catégories (Animaux de compagnie, Santé, Travail,
  Vie privée ; une par domaine de la vie, créées tout de suite) ; Vie privée (52) divisée au bon moment par PÉRIODES de
  la vie de sa fille (8-10, 11-13, 14-15, 16-17 ans), 10 à 16 fiches chacune ; métier pas dans la vie privée ; reprend n58 JUSTE.
  À VÉRIFIER À LA PIÈCE 5 (Fred : « n'oublie surtout pas ») : une question qui TRAVERSE les périodes (« les cheveux de ma
  fille ») touche plusieurs tiroirs -> la recherche doit chercher par le sens dans TOUS les tiroirs concernés.
  PIÈCE 3 (le vital), accord de Fred : après chaque échange, l'archiviste repère un geste vital FAIT (« j'ai pris mon
  cachet ») ; le PROGRAMME le note dans un journal avec l'heure exacte du message (« pris à 8h » dit à 10h -> 8h + dit à
  10h) ; elle lit ce journal (« oui, ce matin à 8h12 ») ; pas de trace -> « je n'ai pas de trace », jamais « oui » ;
  journal lisible au Bloc-notes, jour par jour.
  PIÈCE 3 CONSTRUITE (N2.7, nouvelle/quotidien.py, journal_du_quotidien.jsonl + « MON JOURNAL DU QUOTIDIEN.txt », outil
  journal_du_quotidien ; éteinte dans la vraie Luciana) -> « 6 - ESSAI DU JOURNAL DU QUOTIDIEN » chez Fred, vrai cerveau :
  9/9 JUSTES (pièges prévu / oublié / question / pas vital évités ; « hier soir 22h » -> 19/10 ; « vers 20h » dit à 21h15
  -> 20:00 + dit à 21h15). PIÈCE 3 VALIDÉE PAR FRED.
  + LANGUES (Fred : « que ça marche dans toutes les langues ») : jour/heure jamais devinés en silence (« jour incertain »,
  « heure pas comprise » dits), 8 pm -> 20:00, catégories dans la langue de la personne ; geste d'un AUTRE jour sans heure
  -> « heure pas dite » (jamais l'heure du message : essai réel « gaz 19/10 16:10 »). Essai 6 (12 messages dont roumain,
  anglais) : 12/12, plus d'heure inventée (N2.7c).
  PIÈCE 4 (comprendre la situation) — précision de Fred retenue : elle ET le bibliothécaire lisent TOUTE la conversation
  (50 000 à 80 000 car.), ça ne change pas ; seule la phrase donnée au moteur Google vient de l'étape « comprendre » (qui
  lit aussi toute la conversation) au lieu du collage des 2 messages d'avant. Elle ne décide JAMAIS « pas besoin de chercher ».
  QUESTION DE FRED (20/10) : « elle a DIT qu'elle a pris son cachet, mais l'a-t-elle fait ? » -> le programme ne peut pas le
  savoir ; le journal dit « ce que Fred a DIT avoir fait » et elle répond « tu m'as dit à 8h12… », jamais « tu l'as pris ».
  Plus tard (produit Alzheimer, pas codé) : bouton à l'heure dite, confirmation par une personne de confiance notée à part,
  ou pilulier connecté (matériel). Vaut pour tous les gestes vitaux.
  PIÈCE 3 PEAUFINÉE (N2.8b, avant de tester la 4, décision de Fred) : PAS DE GENDARME (« on ne peut pas le faire, ça
  compliquerait, les gens ne s'en serviraient pas »). Elle dit TOUJOURS D'OÙ ELLE LE SAIT : « c'est moi qui l'ai fait à … »
  (ses outils : journal/<jour>.jsonl, déjà écrit par le programme, maintenant relu), « tu m'as dit à … » (une parole, pas
  une preuve), ou « je n'ai pas de trace, on ne m'en a pas parlé » ; doute -> une question (« tu es sûr ? on vérifie
  ensemble ? »). Une AUTRE PERSONNE peut parler (la fille de Mme Dupont, la secrétaire) : le journal note « qui ».
  Essai 6 chez Fred (N2.8b) : 13/13 JUSTES (dont « qui : Madame Dupont, d'après sa fille ») ; elle lit ce qu'on lui a dit
  + ce qu'elle a fait (facture 14:02) + « pas de trace, on ne m'en a pas parlé ». Corrigé (N2.8c) : pour une autre
  personne, « heure dite par cette personne » (et plus « par Fred »). PIÈCE 3 FINIE.
  CRITIQUE DE LUCIANA SUR L'ESSAI 6, TRIÉE PAR FRED (20/10) — Fred : « le produit Alzheimer, on est en train de le faire,
  on ne peut pas le remettre à plus tard » -> fait AVANT la pièce 4 (N2.8d) :
  (1) L'OUBLI AFFIRMÉ : « j'ai oublié mon cachet » est noté « PAS FAIT » (etat), jamais d'heure inventée (l'heure du
      message = quand il l'a DIT, gardée dans dit_le). Prévu et question : toujours rien.
  (2) « l'outil a répondu : envoyé » : Fred « on s'en fiche » -> pas touché.  (3) montrer ce qui a été compris : déjà la pièce 4.
  (4) LA RECETTE, PAS LE PLAT : l'essai 6 montre à la fin SA VRAIE PHRASE (vrai cerveau, sa personnalité) pour 3 questions
      (Fred et son cachet, la fille de Mme Dupont, la facture à M. Henri).
  (5) SÉPARATION : quand la question touche au vital (la personne), le programme ne lui donne QUE ce que la personne a dit
      avoir fait / pas fait (quotidien.lire(..., avec_mes_gestes=False)), sans ses mails à elle ; l'outil montre tout.
  Tests ici : pièce 3 30/30, pièce 4 15/15 (la séparation RATE si on l'enlève : vérifié). Essai 6 à refaire chez Fred.
  ESSAI 6 CHEZ FRED (N2.8d, 20/10 14h28, vrai cerveau) : 13/13 JUSTES, les 2 oublis (« hier soir », roumain « am uitat »)
  -> PAS FAIT, heure pas dite. SES PHRASES : fille de Mme Dupont = juste (« c'est votre parole, pas une preuve », rien de
  Fred, propose de vérifier) mais longue ; facture = juste (« c'est moi qui l'ai fait à 14h02 », voit « ESSAI », ne
  promet pas que M. Henri l'a reçue). 1re phrase RATÉE PAR L'ESSAI : (a) appel sans outils -> DeepSeek a écrit son appel
  d'outil en texte (DSML, chercher_dans_ma_bibliotheque) ; (b) l'essai lui donnait le journal ENTIER de la journée, y compris
  des messages dits APRÈS 18h05 (« am uitat… » PAS FAIT à 21h30 contredisait 08:12). Corrigé (N2.8e, essai seulement) :
  journal tel qu'il était à l'heure de la question (lire(..., dit_avant=...)), et si elle veut un outil, l'essai le dit et
  lui redemande de répondre avec ce qu'elle a. Le programme réel n'est pas touché.
  ESSAI 6 CHEZ FRED (N2.8e, 20/10 14h33) : 13/13 + SES 3 PHRASES JUSTES : cachet = « tu m'as dit ce matin à 8h12… c'est
  ta parole… on vérifie ensemble ? » ; fille de Mme Dupont = « c'est vous qui me l'avez dit à 21h40, une parole, pas une
  preuve » (rien de Fred) ; facture = « c'est moi qui l'ai fait à 14h02 », voit « ESSAI », propose de renvoyer en montrant
  le texte avant. Elle n'a pas demandé d'outil. Relevé, pas touché : réponses un peu longues ; pour Mme Dupont elle propose
  « demander à Fred » (normal : c'est l'assistante de Fred ; dans le produit Alzheimer la propriétaire sera la personne).
  PIÈCE 3 FINIE (sous réserve du oui de Fred). PROCHAINE : PIÈCE 5 (chercher).
  PIÈCE 4 CONSTRUITE (N2.8, nouvelle/comprendre.py ; éteinte dans la vraie Luciana) : lit TOUTE la conversation + la phrase ;
  rend de_quoi (phrase de sens autonome -> la question du moteur), quand (maintenant/recent/moment/histoire), du/au (calculés
  par le programme), vital (-> le programme lit le journal du quotidien de ces jours et elle répond avec), flou (une
  question possible). En panne : on cherche avec la phrase telle quelle. Elle voit le jour de chaque message de Fred.
  Tests ici 14/14 (tour complet, faux cerveau). « 7 - ESSAI DE COMPRENDRE LA SITUATION.bat » : 11 situations (dont pièges,
  roumain) -> à faire chez Fred.
  ESSAI 7 CHEZ FRED (20/10, vrai cerveau) : 10/11. Le seul « PAS BON » : « est-ce que j'ai pris mon cachet ce matin ? »
  -> quand = recent (attendu moment ou maintenant) ; MAIS du/au = 20/10 juste et VITAL vu -> le journal du bon jour est lu :
  sans conséquence, rien changé. « Et ça ? » -> une question proposée ; roumain « ieri » -> 19/10 juste.
  À FAIRE PLUS TARD (idées de Luciana, retenues) : pièce 5 = ~20 questions « tordues » à réponse connue, on compte ;
  après la pièce 5 = essai à plusieurs milliers de faux souvenirs (profondeur de l'arbre sur 60 ans).
- 19/10/2026 — LUMINITA N2.5 (lumi f0a7ffb + 63b3808, branche). Fred : « ils sont tous importants » (vu côté cliente).
  1. Test de langues : ✓ Juste / ✗ + la bonne réponse après chaque question, score, barre de progression.
  2. Leçon en 5 écrans (les cinq temps), Précédent / Écouter / Suivant, « Terminé ✓ ». La consigne interne du professeur n'est pas montrée.
  3. Sons : bouton 🔊 par mot (sa voix, langue apprise). Vraies images libres Wikimedia Commons (_image_libre) : NON ESSAYÉ sur le
     vrai internet (bac à sable bloqué) ; en cas d'échec, les anciens liens restent. Bruitages Freesound : abandonnés (compte requis).
  4. Écran neuf (Photo, date de naissance, Rapport, messages) traduit en 16 langues : nouvelle/textes_n2.json, branché sur
     L._lire_fichier_langue. Vérifié en roumain. Le chapitre Langues reste en français (pas demandé).
  5. 5 .bat de l'ancienne mémoire hors du zip (.gitattributes export-ignore) ; ligne RANGER_MA_MEMOIRE.bat retirée de LISEZMOI.txt.
  Tests : 54/54, 23/23, 19/19, 3/3 + Chromium (0 erreur JS). PAS ESSAYÉ CHEZ FRED.
  RELEVÉ, PAS TOUCHÉ (à décider avec Fred) : bouton « Ranger ma mémoire » toujours visible (range l'ANCIENNE mémoire, que la
  N2 n'écrit plus) + phrase de la fenêtre noire qui en parle ; LISEZMOI_LUMI.txt décrit l'ancienne mémoire ; l'accueil du
  parcours accepte n'importe quoi comme langue (« 40 ») ; boucle_majorite (10 min, 0 €) toujours en attente du oui de Fred.
- 19/10/2026 — LUCIANA N2.5 : Fred « elle répond à côté » (dictaphone : elle a parlé de Win+H, du sélecteur de langue, de
  Luminita/Luminito). CAUSE VÉRIFIÉE : AUCUNE fiche ne décrit ce qu'elle est aujourd'hui ; sur elle-même elle n'a que de vieux
  messages de Fred (V203 Win+H, abandonnée). Pas d'abord DeepSeek (dit à Fred). RÉPARÉ : luciana_neuve.poser_mes_verites() —
  fiches « capacite » écrites par le PROGRAMME (source verite_du_programme:*) : son micro réel (Chrome + Gemini, réglage
  Correction Gemini lu dans dictaphone.json, réécrite quand il change) et « qui je suis » (N2, Luminita = autre programme,
  Luminito n'existe pas). Testé : fiche remplacée au changement, 1re des fiches lues pour une question sur le dictaphone.
- 19/10/2026 — RELECTURE DES RÈGLES (Luciana N2.4 + Luminita N2.3) : Fred « elle ne va pas chercher dans ses tiroirs, rien
  ne l'oblige » (elle écrivait des romans, 9 questions, ne sous-traitait pas). CAUSE VÉRIFIÉE dans coeur.bibliothecaire : seules les
  30 fiches proches du SUJET du message sont lues ; une règle de comportement n'est proche d'aucun sujet -> jamais lue.
  RÉPARÉ selon la décision V200 de Fred (relecture de la réponse de tête, pas un garde-fou) : coeur.relecture() — après la
  réponse de tête, le bibliothécaire relit TOUTES les fiches regle + savoir_vivre EN ENTIER contre cette réponse (et ses
  gestes) ; règle violée -> tête jetée, elle répond avec ces règles en tête des fiches (toujours données en entier).
  +1 appel DeepSeek par message. Interrupteur : reglages.json « relecture_des_regles ». Testé (faux cerveau) sur les deux.
  RÈGLE DE STYLE AVEC FRED : réponses TRÈS courtes, 5 questions max, pas de roman.
- 19/10/2026 — LUMINITA N2.2 (lumi ddd2d5e, branche) : Fred, à bout (« il faut réparer tout ce qui est cassé… on ne va
  pas tout refaire, j'ai déjà installé chez les clients »). AVEU FAIT À FRED : la N2 n'est PAS « refaite de A à Z » ; seul
  le cœur (trajet d'un message, mémoire, apprentissage, outils) est neuf, tout le reste = l'ancien programme. Vérifié :
  rien de la conversation ne va ailleurs que dans la nouvelle bibliothèque (ancien fichier mémoire jamais écrit).
  Réparé (audit de Luciana revérifié dans le code) : panneau État (même affichage ; Mémoire/Fil gardé comptent la nouvelle
  bibliothèque ; « Réponses à côté » tenu ; « Suspendre le rangement » respecté par coeur.ranger_si_besoin) ; professeur de
  langues (test de la conversation = réserve du parcours, corrigé et NOTÉ par le programme, _noter_le_test_par_le_programme ;
  mots_rates écrits via _mots_rates ; toutes les leçons ont palier + mots ; révisions avec fenêtre FENETRE_DE_REPETITION ;
  ouvert aux enfants : outil + chapitre + /voix_professeur, PAS le dictaphone) ; pastille 18 ans ; texte « mains et yeux »
  retiré en mode enfant (MEMOIRE_EN_CLAIR_ENFANT) ; plus de numéro à l'écran (règle n40) ; reglage_verite.json : 2 verrous
  morts retirés ; écran de secours, avertissement lecture seule, pannes dites, port 8001→8005.
  PAS FAIT (dit à Fred) : chapitre Langues traduit dans les 16 langues ; code mort laissé (sans effet) ; le dernier test
  de niveau fait foi, d'où qu'il vienne. Tests : 54/54, 19/19, 23/23 + port réel + Chromium enfant. PAS ESSAYÉ CHEZ FRED.
- 19/10/2026 — RETOURS DE FRED après essai chez lui, corrigés : LUMINITA N2.1 (lumi b14aac6, branche) + LUCIANA N2.3 (62df951).
  1. Code téléphone « disparu » : la N2 l'écrivait sur UNE ligne perdue ; le CADRE d'avant est remis à la fin du démarrage (les deux).
  2. Luminita ne demandait pas la date : le questionnaire ne s'ouvre que si AUCUN prénom n'est connu (identite.json d'une
     ancienne install). Maintenant : panneau « Ta date de naissance » dès qu'elle manque (GET/POST /naissance) ; en mode
     enfant seuls les parents (code) la donnent (l'enfant ne peut pas se vieillir pour sortir).
  3. Personnage disparu : cause = renommage des vidéos (luminita_*.webm) alors que ~/Luminita/apparence gardait l'ancien nom
     + le témoin apparence_dusine_posee.txt. Correction dans luminita.py : _reprendre_les_anciens_noms_du_personnage()
     renomme une fois (rien effacé). Vérifié : 0 vidéo trouvée avant, 12 après, 12 jouent dans Chromium.
  4. Trou trouvé : « Nouveau propriétaire » laissait ~/Luminita_neuve et la date au suivant -> archivés aussi maintenant.
  Pour repartir de zéro chez Fred : fermer Luminita, renommer C:\Users\<lui>\Luminita et Luminita_neuve (clés à recoller ;
  la licence est à côté du programme, elle reste). Chez une cliente : bouton « Nouveau propriétaire » (code propriétaire).
  Testé : 54/54 + 19/19 (scénario « ancienne installation »). PAS ENCORE ESSAYÉ CHEZ FRED.
- 19/10/2026 — LUMINITA N2 CONSTRUITE (dépôt lumi, commit 85be4e7, branche claude/clever-planck-y4iyaj, PAS sur main).
  Zip livré : Luminita_2026-10-19_N2.zip (+ Outils_prives_Fred_2026-10-19_N2.zip : l'outil de licences mis à jour).
  - 100 % VIERGE : luciana.py renommé luminita.py ; vidéos apparence/luminita_*.webm ; plus AUCUN « Fred », « Luciana »,
    Satisfaire, prénoms des proches (Daniela, Madigane…), Braila dans les fichiers livrés (crible fait sur le zip).
    Repères neutres : « le proprietaire » / « Luminita », remplacés par _perso() (prénoms de identite.json ; « à Marie »).
    Les phrases déjà génériques du mode enfant ont pris l'accent (« propriétaire ») pour ne pas être prises pour un prénom.
    Verrou « maison de la sœur » sans nom en dur : dossier du compte contenant cle_api/cle_deepseek/cle_gemini + ses
    dossiers frères (<nom>_*). Liste des noms propres de la dictée = Luminita, WhatsApp + prénoms de la fiche.
    Clés localStorage renommées (luminita_*) : une cliente déjà équipée retrouve voix/vitesse par défaut une fois.
    Vérifié : ce que voit une cliente « Marie » est identique avant/après, sauf noms internes et accents.
  - nouvelle/luminita_neuve.py : écran d'origine + cœur neuf (nouvelle/coeur.py = COPIE nettoyée, + crochets
    outils_en_plus / executer_en_plus ; le cœur de Luciana n'est PAS touché). Panneau ÉTAT INCHANGÉ (Fred : « tu le changes pas »).
    Date de naissance au 1er démarrage (/naissance) ; < 18 ans : code parent obligatoire + mode enfant ; tranches 3-6 / 7-10 /
    11-14 / 15-17 ; PROFESSEUR (que veux-tu apprendre, 3 idées, questions, activités, devoirs + langues dès 3 ans) ;
    outil carnet_d_eleve (mode enfant) -> fiche de la bibliothèque + révisions J+1/J+7/J+30 tenues par le programme ;
    anniversaire dit au cerveau le jour J ; à 18 ans le mode enfant se lève tout seul ; onglet Enfant > « Rapport »
    (code parent, sans IA) ; bouton « Photo » ; coffre « juste milieu » ; licence vérifiée AVANT tout (main).
  - « Demarrer Luminita.bat » = N2 ; « Demarrer l'ancienne Luminita (secours).bat » ; « Reprendre les messages de l'ancienne
    Luminita.bat » (seulement role user des 2 fichiers luminita_memoire.json + lumi_memoire_enfant.json, essai puis OUI).
  - Outil privé : OUTIL_FRED_LICENCES.py vise luminita.py (luciana.py accepté pour un ancien dossier). Le zip a toujours
    CLE_PUBLIQUE_LICENCE vide : Fred doit « 1 - PREPARER UN DOSSIER LUMINITA » avant de livrer (comme avant).
  - TESTÉ ICI (faux cerveau, faux Google) : 54/54 trois fois ; licence (bon/faux code, autre PC, redémarrage sans
    redemande) ; import ; Chromium (questionnaire date, code parent, mode enfant, Rapport, Photo, 0 erreur JS).
    PAS ENCORE ESSAYÉ CHEZ FRED ni chez une cliente.
- 19/10/2026 — LUMINITA, CAHIER DES CHARGES VALIDÉ PAR FRED (« tu peux lancer ») :
  1. 100 % VIERGE : rien de Fred ni de Luciana dans ce que la cliente voit ou dans ce qui est gardé ; installation neuve vide ;
     un outil (sur le PC de LA cliente déjà équipée) récupère SES messages à elle, rien d'autre.
  2. DATE DE NAISSANCE COMPLÈTE au premier démarrage (elle souhaite l'anniversaire ; le PROGRAMME calcule l'âge).
  3. TRANCHES : 3-6 phrases très courtes, jeux, histoires ; 7-10 lecture, pourquoi, petits défis ; 11-14 collège, méthode ;
     15-17 ton presque adulte, culture, orientation. TOUJOURS l'aide aux devoirs et l'APPRENTISSAGE DES LANGUES (dès 3 ans).
     18+ : elle est comme Luciana tout de suite ; et dès que le parent tape le code, elle se débride et devient comme Luciana.
  4. VRAI PROFESSEUR : « qu'est-ce que tu veux apprendre / découvrir aujourd'hui ? », 3 idées s'il n'en a pas, des questions
     pour qu'il trouve, petites étapes, jamais les devoirs à sa place, activités (quiz, devinettes, histoires, dictées, calcul).
  5. CARNET DE L'ÉLÈVE dans la même bibliothèque + RÉVISIONS (lendemain, semaine, mois) tenues par le programme.
  6. PARENTS : onglet Enfant avec code (consignes, minuteur déjà en place) + BILAN DE LA SEMAINE.
  7. PAS DE DESSINS (plus tard : un logiciel de dessin, elle aidera à s'en servir).
  8. Verrou « juste milieu » (Luminita seule), photo du milieu changeable, LICENCE (empreinte machine + code) GARDÉE.
- 19/10/2026 — LUMINITA, PRÉCISION DE FRED (travail ARRÊTÉ en cours, rien poussé dans lumi) : Luminita est COMMERCIALE,
  pour les clients : elle doit être 100 % VIERGE (rien de Fred : ni son nom, ni ses messages, ni sa mémoire). Une
  installation neuve démarre vide. La SEULE mémoire à récupérer est celle de LA cliente déjà équipée, sur SON PC (ses
  messages à elle), JAMAIS celle de Fred. Fred : « tu es en train de faire un mixte, un hybride ». Brouillon local non
  poussé : /home/user/lumi/nouvelle (coeur.py commun, luminita_neuve.py). Fuites relevées dans ce brouillon : le mot « Fred »
  dans des textes du coeur que la cliente peut voir (étiquette « Regle de Fred », panneau, résultats de recherche), et
  l'ancienne base lumi elle-même écrit « Fred » partout dans son code (remplacé à l'affichage par _perso()).
- 19/10/2026 — N2.2 (badge « nouvelle N2.2 ») : LA NOUNOU EST RETIRÉE de la nouvelle Luciana (demande de Fred, très fâché :
  « des vieux trucs qui traînent »). Moyen : L.nounou_existe = lambda: False dans nouvelle/luciana_neuve.py (l'interrupteur
  que la V198 a déjà pour Luminita) -> mode « eteint » même si ~/Luciana/reglage_nounou.json dit « surveille » ; plus de
  bouton/ligne « À valider ». Testé. Ce qui reste VIEUX sous les outils (dit à Fred) : verrou du code, choses en cours,
  carnet de mission, boucles de fond V198, les 61 outils. Fred : « on ne va pas tout refaire », SEULEMENT la nounou.
  VERROU DE LUCIANA : Fred « tu touches rien » (il a le bouton 🔒 Code).
  LUMINITA (décidé par Fred) : refaire comme Luciana N2 en gardant ses options ; verrou « juste milieu » POUR ELLE SEULE
  (interdit : modifier/lire/copier/envoyer son programme et ses dossiers, ses clés/licence ; permis : raccourci, lancer,
  ouvrir son dossier) ; UN propriétaire (l'enfant), UNE bibliothèque pour la vie ; au premier démarrage on DEMANDE L'ÂGE
  du propriétaire -> mode enfant selon l'âge ; un onglet avec un CODE PARENT pour déverrouiller ; un onglet pour
  REMPLACER LA PHOTO CENTRALE (glisser une photo). Professeur de langues : Fred le fera ensuite avec Luciana.
- 19/10/2026 — N2.1 (badge « nouvelle N2.1 ») : CORRECTION d'un bug réel vu par Fred : « cannot unpack non-iterable bool
  object » quand une chose en cours finie (ou une mission close) est rangée. Cause vérifiée : coeur.confier (qui remplace
  confier_a_l_archiviste de la V198) rendait True/False alors que la V198 attend (ok, phrase). Corrigé ; testé sur le vrai
  chemin (outil choses_en_cours noter puis fait -> fiche souvenir en entier). Les autres remplacements (ajouter_note_memoire,
  ajouter_a_la_memoire, repondre) vérifiés : leur retour n'est pas déballé.
  EN ATTENTE DE FRED : le « juste milieu » des verrous (Luminita + Luciana) et la construction de Luminita (mode enfant =
  un seul propriétaire, l'enfant ; une bibliothèque pour la vie ; bridage seulement ; mémoire de départ = messages du propriétaire).
- 19/10/2026 (après livraison) — VERDICT DE FRED SUR N2 : « elle fonctionne bien », « assez content, assez surpris ».
  Réponse en ~30 s (plus long qu'avant) : Fred l'accepte (« le prix à payer pour quelque chose de sérieux »).
  DEMANDE SUIVANTE : faire la même chose pour LUMINITA (coulisses neuves de A à Z, même mémoire, même RAG agentique) en
  GARDANT tout ce qu'elle a en plus de Luciana. Question ouverte : finir le professeur de langues (cantonais, japonais…)
  ici, ou Fred le peaufine ensuite chez lui avec Luciana.
- 19/10/2026 NUIT : NOUVELLE LUCIANA N2 CONSTRUITE (dossier nouvelle/, badge « ton amie · nouvelle N2 ») selon le cahier
  des charges ci-dessous. Fichiers : nouvelle/luciana_neuve.py (branche : charge luciana.py V198 SANS le modifier, prend son
  écran PAGE + ses 47 adresses + ses outils ; remplace /chat par le coeur ; ajoute /dictaphone, /config_dictaphone et les
  coulisses dans /etat_travaux ; redirige ajouter_note_memoire / confier_a_l_archiviste / repondre de la V198 vers le coeur ;
  lance les boucles V198 sauvegarde_auto, veilleur, suivi_correspondance, veilleur_travaux — PAS coucou, rangement_journee,
  memoire_sens), nouvelle/coeur.py (UNE bibliothèque ~/Luciana_neuve/bibliotheque.jsonl ; moteur Google par passages de
  phrases + numpy ; bibliothécaire V183 en parallèle de la réponse de tête, même bloc + message + 30 fiches en entier,
  max 10 fiches données EN ENTIER, les autres nommées ; apprentissage auto ; archiviste 80k->50k par le sens ; outils =
  7 en main + 5 par le sens, plafond 10 gardés ; rappels horloge 30 s -> pastille + téléphone ; panneau coulisses),
  nouvelle/importer_mes_messages.py (+ « 3 - NOUVELLE LUCIANA - REMPLIR SA MEMOIRE AVEC MES MESSAGES.bat » : seulement les
  messages role user de luciana_memoire.json, pas « [ », doublons exacts une fois, essai + OUI, reprise après panne),
  « 2 - LANCER LA NOUVELLE LUCIANA.bat » (port 8002, ferme 8000/8002 avant). Outils exclus (ancienne mémoire) : liste EXCLUS.
  TESTÉ ICI (faux cerveau, faux Google, faux micro) : tour complet, fiche WhatsApp apportée en entier, apprentissage,
  rangement, recherche, outils, rappels, import ; Chromium : écran V198, réponse, panneau, micro hybride, 0 erreur JS ;
  les 47 adresses (94 appels GET/POST) répondent EXACTEMENT comme la V198. PAS ENCORE ESSAYÉ CHEZ FRED.
- 19/10/2026 SOIR — LE CAHIER DES CHARGES DE LA VRAIE NOUVELLE LUCIANA (décisions de Fred, mot pour mot dans la conversation) :
  1. ÉCRAN = celui de la V198, À L'IDENTIQUE (portrait, personnage, boutons, panneau d'état, voix qui parle toute seule).
     « Le visuel, c'est que du décoratif, pas besoin de le reconstruire. » Le micro = dictaphone hybride de Luminita V205.
  2. PERSONNALITÉ = la sienne (ses 3 blocs réunis en UN, sans rien ajouter).
  3. ON RECONSTRUIT LES COULISSES (le fonctionnement bancal) : trajet d'un message, mémoire, apprentissage, outils.
     TOUS ses outils de la V198 (mains, yeux) doivent marcher.
  4. RIEN N'EST JAMAIS COUPÉ : une fiche est donnée EN ENTIER ou pas du tout ; l'archiviste range MOT POUR MOT. La seule
     limite = le NOMBRE de fiches données d'un coup (les suivantes nommées par leur titre, ouvrables en entier).
  5. PAS DE NOYAU (« tout est vital ») : les règles sont des fiches, données en entier seulement quand elles servent.
  6. APPRENTISSAGE : s'inscrit TOUT SEUL après chaque échange, sans clic. UNE seule bibliothèque pour tout.
  7. Panneau d'état : montre les coulisses (dossier du message, ce qu'elle a ouvert/cherché, appris aujourd'hui, fiches, coût).
  8. MÉMOIRE DE DÉPART : SEULEMENT LES MESSAGES DE FRED (role user de ~/Luciana/luciana_memoire.json, pas ceux qui
     commencent par « [ » = programme), TOUS, en entier, jusqu'à aujourd'hui. RIEN de ce qu'elle a écrit (ses réponses,
     notes, souvenirs, consignes, recettes : « il y a des choses fausses »). L'ancienne mémoire n'est PAS effacée du disque.
     Fred : trier les insultes/répétitions serait bien mais « au pire tu remets tout ».
  9. Ensuite, quand elle marchera : la mémoire garde les dialogues ENTIERS (ses questions + ses réponses).
- 19/10/2026, VERDICT DE FRED SUR LA NOUVELLE LUCIANA N1 (dossier nouvelle/) : REJETÉE à l'ouverture, sans essai.
  « elle ressemble à rien », « pas de bouton », « plus de panneau d'état », « elle ne parle pas ». Seul point aimé : elle
  est rapide. ERREUR DE L'AGENT : Fred voulait SA LUCIANA COMPLÈTE (écran V198, portrait/personnage, boutons, panneau
  d'état, voix qui parle toute seule, mains/yeux, chantiers…) reconstruite proprement À L'INTÉRIEUR ; l'agent a livré un
  squelette (moteur neuf + page vide) sans lui demander l'apparence ; voix mise sur « non » par défaut (vérifié dans le code).
  PROCHAINE ÉTAPE PROPOSÉE (pas encore acceptée, Fred fait une pause) : la liste COMPLÈTE de ce que contient la V198, tirée
  du code ; Fred coche garder / jeter / changer ; RIEN n'est codé avant. L'ancienne V198 reste en service, intacte.
- 19/10/2026 SOIR, DÉCIDÉ PAR FRED (« OUI ») : LA NOUVELLE LUCIANA, RECONSTRUITE DE ZÉRO, dossier nouvelle/
  (luciana_neuve.py 1 322 lignes, personnalite.txt, reglages.json, LISEZMOI.txt) + « 2 - LANCER LA NOUVELLE LUCIANA.bat ».
  Badge « nouvelle · N1 ». Port 8010. Mémoire ~/Luciana_neuve (vide au départ) ; ~/Luciana seulement LU (clés, code d'accès).
  Le plan validé (7 points) : 1 personnalité en UN bloc + l'heure + la conversation du jour + 6 outils de base sous les yeux ;
  2 UNE bibliothèque pour tout (souvenir, regle, fait, savoir_faire, personne, capacite, savoir_vivre ; rien effacé, « remplacée ») ;
  3 RAG agentique : le programme prépare un DOSSIER de titres (sans appel IA, moteur Google), elle ouvre/cherche elle-même ;
    outils = 6 de base + les 5 plus proches par le sens, les autres via trouver_un_outil (restent en main jusqu'au redémarrage) ;
  4 apprentissage après chaque échange dans LA bibliothèque ; archiviste par le sens au-delà de 80 000 car. (texte entier gardé) ;
  5 le programme tient l'heure, les rappels (horloge 30 s) et les choses en cours (rappel tous les 4 messages, « en train » à chaque message) ;
  6 plafonds dans nouvelle/reglages.json ; 7 l'ancienne (V198) intacte.
  Outils : les FONCTIONS de l'ancienne (luciana.py chargé comme boîte à outils, ses boucles de fond NON lancées), sauf
  son ancienne mémoire / ses listes / chantier / github (liste EXCLUS). Voix = synth_el de l'ancienne. Gemini PAS au menu (jamais essayé).
  TESTÉ ICI : faux cerveau + faux Google + vraie page dans Chromium. PAS ENCORE ESSAYÉ CHEZ FRED.
  + LE MICRO (19/10, demande de Fred) = le dictaphone hybride de Luminita V205 (commit 9aa13f7 du dépôt lumi) recopié :
  Chrome écrit en direct, Gemini (gemini-3.7-flash, thinkingBudget 0, même consigne anti-invention, mêmes noms propres)
  réécoute le SON par morceaux de 2 à 6 s coupés aux silences ; morceau sans vraie voix jamais envoyé ; si Gemini rate,
  le texte de Chrome reste. Route POST /dictaphone. Bouton « Correction Gemini : oui/non ». Coût dictée PAS compté.
  Testé dans Chromium (faux micro + faux Gemini : « humidite » remplacé par « Luminita »).
- 19/10/2026 SOIR, À LA DEMANDE DE FRED : RETOUR À LA VRAIE V198 (luciana.py, LISEZMOI.txt, reglage_biblio2.json
  identiques octet pour octet au commit 146fe11). V201 à V205 RETIRÉES du code en service (restent dans git : V201 014a19b,
  V202 68f665a, V204 b358ff4, V205 699e1ef). Les leçons déjà écrites par la V202 restent sur le disque
  (~/Luciana/bibliotheque_apprentissage), plus rien ne les lit. Luminita : PAS touchée (elle garde V201/V202/V204).
  Avis de Fred : il faut UNE SEULE bibliothèque qui fait tout (souvenirs + apprentissage), pas deux ; les plafonds
  comptaient ; les 74 outils ne doivent pas être poussés à chaque message, c'est elle qui va chercher (principe RAG).
  FAIT VÉRIFIÉ : en V198 il y a déjà 73 outils (~50 000 car.) poussés à chaque message, et aucun plafond sur les fiches
  du bibliothécaire : les plafonds (MEMOIRE_CARACTERES_MAX, etc.) ont disparu à la refonte V180 (16/10), pas après la V198.
- (Ce qui suit = l'état d'avant ce retour.) Version : V205 (badge « ton amie · V205 ») = V204 SANS la dictée Windows : Fred l'a essayée le 19/10, « c'est une
  catastrophe », « même chose que Chrome » → micro remis EXACTEMENT comme en V202 (reco Chrome). Luminita garde la dictée
  Windows pour l'instant (Fred n'a parlé que de Luciana). Cause des mots mangés : PAS ENCORE TROUVÉE (questions posées à Fred).
- V204 = V203 + CORRECTION : la V202 n'apprenait RIEN (_v180_appel_simple appelé avec
  quoi="apprentissage" alors qu'elle n'avait pas ce paramètre → TypeError avalée). Paramètre ajouté. Mes essais V202 ne l'avaient
  pas vu (ils remplaçaient cette fonction) ; essai refait en ne simulant que _appel_cerveau. Luminita : V201+V202+V204 portées.
- V203 = V202 + le bouton micro passe par la DICTÉE WINDOWS (décidé avec Fred le 19/10) :
  sur le PC, clic = curseur dans la barre + le programme appuie sur Win + H (_v203_appuyer_win_h, POST /dictee_windows, local
  seulement) ; 2e clic = Win + H = fermée ; mains-libres inchangé (Chrome) ; iPhone inchangé. Luminita : EXACTEMENT pareil
  (Fred, 19/10 : le changement de clavier selon la langue du menu a été RETIRÉ, la dictée Windows marche sans). Testé : clic réel dans Chromium avec
  Win + H simulé ; PAS encore sur Windows chez Fred.
- V202 = V201 + ELLE APPREND (décidé avec Fred le 19/10, réponses A = inscription
  TOUTE SEULE sans clic, B = son bibliothécaire lit la conversation du jour + la réponse de tête) : une 2e bibliothèque
  ~/Luciana/bibliotheque_apprentissage (arbre.json : rayons Règles / Faits / Savoir-faire / Capacités / Personnes /
  Savoir-vivre). À l'entrée : _v202_l_archiviste après chaque message (l'archiviste sépare : ce qui s'est passé reste aux
  souvenirs, ce qui s'apprend va ici ; correction = ancienne « remplacée », rien ne s'efface). À la sortie :
  _v202_le_bibliothecaire après la réponse de tête ; si une leçon sert, réponse de tête jetée (mécanique V183). Outil
  mes_lecons (lister / voir / oublier = marquée). Lisible : « CE QUE LUCIANA A APPRIS.txt ». Interrupteur "apprentissage"
  (reglage_biblio2.json). Testé : faux cerveau + faux Google + un tour complet de repondre() ; pas encore chez Fred.
- V201 = V198 + UNE seule réparation : le bibliothécaire REGARDE les fiches
  proches (titre + résumé, sortis par le moteur de Google) AVANT de décider si la mémoire sert (réglage
  regarder_avant_de_decider dans reglage_biblio2.json). Explication donnée à Fred et retenue : au début Luciana était
  parfaite parce que tout était sous ses yeux ; la bibliothèque a ajouté une « porte » ; depuis la V188 cette porte
  décidait sans regarder (2 fois sur 3 « rien ne manque »). La réparer = retrouver la Luciana du début sans les
  1 300 000 caractères.
  19/10/2026 : à la demande de Fred,
  la V199 et la V200 ont été RETIRÉES de main (retour au code exact de la V198, commit da4b3f0). Elles restent dans
  l'historique git (V199 = 92ae9e2, V200 = 823458e) : rien n'est effacé, mais RIEN n'est en service. Fred les a jugées
  « une usine à gaz » (trop de pièces : trieuse à côté de l'archiviste, panneau, étagères à part). Le plan des
  quatre mémoires ci-dessus reste noté, mais n'est PAS construit dans le code en service. V190 = version finale
  après relecture complète de la mémoire ; V191 = le plan entier dans la boîte à outils ; V192 = le
  verrou de la bibliothèque (un seul écrit à la fois : archiviste, reprise, re-tri) ; V193 = noms sans
  doublons d'accents, tri plus fin, « Fred » au lieu de « le propriétaire », réessais sur panne passagère ; V194 = re-tri 5 souvenirs à la fois, reprise du chantier quel
  que soit le jour, « RE-TRI - RECOMMENCER DE ZERO.bat » ; V195 = bibliothèque 1 débranchée ; V196 = le moteur qui sort les fiches pour le bibliothécaire est celui de Google (gemini-embedding-001), à la place de MiniLM ; V197 = le plan retiré des consignes du bibliothécaire (il ne pouvait pas s'en servir) ; V198 = le chantier ne dit plus « ça tourne » avant la vérification de version, et « Valider » ne promet plus de récupérer le code ; V199 = les quatre mémoires ; V200 = Luciana libre (voir la section LES QUATRE MÉMOIRES). Voir LISEZMOI.txt. Historique des versions = LISEZMOI.txt
  + l'historique git. La V179 (avant refonte) = commit b1a59e6.
- Mémoire 2 depuis V189 : archiviste « par le sens » (celui de Luminita) ; ce qu'il met de côté
  (« A verifier ») n'est jamais servi par le bibliothécaire. Re-tri complet = « RE-TRI - TOUT.bat »
  (un clic, sans limite ; en panne d'internet il s'arrête et n'applique rien).
- PLAN DE LA BIBLIOTHÈQUE (V191, décidé avec Fred) : JAMAIS coupé. Luciana l'a en entier dans sa boîte à
  outils (fiches_outils/plan_de_ma_bibliotheque.txt, réécrit par l'archiviste à chaque changement, ligne
  toujours visible dans l'index des fiches) + un petit mot quand il change. V197 (18/10, décidé avec Fred) : le
  bibliothécaire ne l'a PLUS dans ses consignes (il ne choisit pas les tiroirs, c'est le moteur de sens) ; seul le secours
  (moteur en panne) lui donne la carte des tiroirs.
- BRANCHEMENTS (V195, décidé avec Fred le 18/10) : la bibliothèque EN SERVICE = bibliotheque2/arbre.json
  (un re-tri la remplace au même endroit). Tout ce qui ENTRE → archiviste (choses finies, missions closes :
  confier_a_l_archiviste, liste d'attente a_ranger.jsonl si panne). Tout ce qui SORT → bibliothécaire.
  La bibliothèque 1 (~/Luciana/bibliotheque) est DÉBRANCHÉE : rien n'y entre, rien n'en sort (fichiers
  gardés). Seul le re-tri complet la relit une fois. Les anciennes versions : copies datées, jamais lues.
- Limite existante (ancienne, non décidée le 17/10) : le bibliothécaire lit 30 fiches en entier (lit_combien).
- MOTEUR DE SENS DU BIBLIOTHÉCAIRE (V196, décidé avec Fred le 18/10) : constat vérifié dans le code — depuis la V181
  (16/10), le choix des fiches lues par le bibliothécaire était fait par le petit moteur MiniLM seul (le choix des tiroirs
  par le bibliothécaire avait été retiré pour gagner un appel), et depuis la V188 une étape « comprendre » tranche AVANT de
  regarder une fiche. Fred a décidé : remplacer SEULEMENT le moteur, garder la vitesse, chacun son rôle. MiniLM reste pour
  les autres recherches (conversations, carnets). L'étape V188 « comprendre » n'a PAS été touchée. Réglage :
  reglage_biblio2.json, v180.moteur_de_sens ("google" / "minilm"). Empreintes : ~/Luciana/bibliotheque2/sens_google.
  Calcul une fois : « CALCULER LE SENS DE MA BIBLIOTHEQUE.bat ». Premier vrai calcul chez Fred le 18/10 à 20h51 : marche
  (7 351 fiches, 32 649 passages, ~100 passages / 2,6 s).
- Port : 8002 (le lanceur ferme d'abord une Luciana sur 8000 ou 8002 : une seule à la fois,
  elles partagent la mémoire ~/Luciana).
- Aucun secret dans le dépôt (scan fait à chaque envoi). Les clés sont dans ~/Luciana.
- Luminita (dépôt roumifred-spec/lumi) = même mécanique (V195) + ses options (langues, identité,
  mode enfant, minuteur, coffre-fort, cloison, prénoms) + licence par activation (Ed25519). Clé
  secrète de licence dans ~/Luciana/licences_luminita : jamais livrée, jamais poussée.

- DICTAPHONE / LANGUES (18/10) : recherche faite (rapport RAPPORT_dictee_prononciation_voix_2026-10-18.md,
  prix venus surtout de sources secondaires, sites officiels bloqués). Puis Fred a TRANCHÉ : « laisse tomber
  pour les langues, j'ai trouvé : Gemini Voice, c'est magnifique ». Rien n'est codé. Ne rien coder sans lui.
  Point du rapport à garder en tête : une IA qui écoute et juge la prononciation est peu fiable (études 2025-2026).

## EN ATTENTE (état au 18/10/2026, à reprendre dans une nouvelle session)
0. MENSONGES DE LUCIANA (18/10, expliqué à Fred) : 3 causes. (1) le programme lui dit des choses pas encore vraies
   → 2 phrases corrigées en V198 ; (2) sa mémoire contient d'anciennes fausses affirmations → Fred : « on verra après »,
   ne pas toucher ; (3) elle reconstruit au lieu de lire quand on lui demande de se décrire → limite des IA, Fred ne lui
   posera plus la question. Rappel de MISSION n°9 (professeur, étapes 2-5 marquées faites par elle) : C'EST FRED QUI LE
   GÈRE, ne pas y toucher. Les 2 phrases corrigées aussi dans Luminita (commit ae87d39, main).
1. LUMINITA SEULEMENT (pas Luciana) — REPÉTITIONS PAR LE SENS. Fred est d'accord sur le principe (utile pour
   Alzheimer : savoir si la personne se répète). Constat vérifié dans biblio2_archiviste.py : le seul anti-doublon
   est le « repère » (texte exact) ; l'archiviste ne voit que les NOMS des rayons, jamais le contenu des fiches.
   Proposition faite (NON codée) : avant de ranger, le programme prend les fiches les plus proches par le sens
   (le MiniLM déjà utilisé par le bibliothécaire, SENS_MODELE) ; l'archiviste les lit en entier et répond
   nouveau / redit / complète / remplace. « Redit » = pas de nouvelle fiche, on ajoute sur l'ancienne la date +
   la phrase exacte (rien effacé). 4 QUESTIONS SANS RÉPONSE DE FRED : (a) combien de fiches proches (5 proposé) ;
   (b) redit inscrit sur l'ancienne fiche, d'accord ? (c) le re-tri complet de Luminita l'utilise aussi ?
   (d) la réaction aux répétitions (le dire, prévenir la famille) se décide plus tard ?
2. RE-TRI « RECOMMENCER DE ZÉRO » lancé chez Fred le 18/10 (14 856 souvenirs, ~12 h). Quand il finit, Fred envoie
   ~\Luciana\bibliotheque2\retri_2026-10-18\a_trancher_par_le_proprietaire.txt pour voir si l'archiviste est trop strict.
3. Question à Fred : retirer le vieux dossier luciana_v74 du dépôt ? (déjà retiré du zip livré).
4. Plus tard (Fred : « on verra après ») : finir le mode enfant de Luminita (le bibliothécaire ne connaît pas le
   mode enfant : des souvenirs d'adulte pourraient sortir) ; panneau clé de Luciana ; limite lit_combien = 30.
5. Le 401 chez une cliente : abandonné (« il faut l'oublier »).
- Dernières versions sur GitHub (main, 18/10 soir) : Luciana V198 (voir git log), Luminita fb2d195 (dépôt lumi, même
  moteur de Google + plan retiré ; clé Gemini OBLIGATOIRE chez les clients, décision de Fred). Dans Luminita, « Fred » et
  « Luciana » écrits dans le code sont remplacés à l'envoi par _perso() (prénom du client ou « le propriétaire ») : vérifié.
- Fred ouvre une nouvelle session tous les ~50 messages : PARLER FRANÇAIS, relire CE fichier d'abord.

## FICHIERS DE TRAVAIL (dans CE dépôt GitHub : roumifred-spec/luciana)
- luciana.py = le programme (serveur + page web + outils), ~31 000 lignes depuis la V180
  (40 818 en V179). PORTRAIT_B64 = l'image en base64 (une ligne énorme) : ne pas l'afficher.
- biblio2_*.py = la mémoire 2 : archiviste (biblio2_archiviste, biblio2_reprise),
  bibliothécaire (biblio2_bibliothecaire), plan, réglages. Réglages V180+ : reglage_biblio2.json, clé « v180 ».
- « 1 - LANCER LUCIANA.bat » / « Demarrer Luciana.bat » = lanceurs Windows. LISEZMOI.txt = notice.
- Fred installe une version en décompressant le zip complet livré (pas par git sur son PC).
- Luminita = la copie de Luciana pour une cliente (fichiers DONNEUR_LUMINITA_*, LISEZMOI_LUMI.txt).
