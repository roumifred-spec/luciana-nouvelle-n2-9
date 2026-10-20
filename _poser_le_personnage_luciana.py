# -*- coding: utf-8 -*-
"""DONNE A LUCIANA SON PERSONNAGE ANIME (la meme chose que chez Luminita, sa petite soeur).

CE QUE CE SCRIPT FAIT, ET RIEN D'AUTRE : il ajoute a luciana.py le PERSONNAGE ANIME, en cinq
morceaux, chacun pose a un endroit precis et verifie avant d'ecrire :

   1. le programme    : le dossier "apparence" livre a cote de luciana.py, la liste des huit
                        boucles, et la petite fonction qui retrouve le fichier d'une boucle ;
   2. l'habillage     : le bloc #personnage (z-index:0, pointer-events:none, taille en part
                        de l'ecran) ;
   3. la page         : les huit balises <video>, posees EN DEHORS du bloc .app ;
   4. le mouvement    : quelle boucle tourne, et ou elle se tient dans la fenetre ;
   5. le serveur      : l'adresse /personnage, qui sert une boucle et SEULEMENT une boucle.

IL NE TOUCHE A RIEN D'AUTRE. Ni les pastilles et leur croix, ni le carnet a deux niveaux, ni la
ligne d'etat de la memoire, ni Valider/Annuler, ni la communication, ni la voix, ni le micro, ni
les langues, ni les souvenirs, ni le bloc de dictee de Chrome. Il n'ajoute, il n'enleve rien.

AVANT D'ECRIRE QUOI QUE CE SOIT, IL REFUSE DE TRAVAILLER SI :
   - luciana.py n'est pas la v100 (le badge de la page doit dire v100) ;
   - une trace de la dictee locale Whisper (v101 a v104, abandonnee par Fred) traine dedans ;
   - un seul des cinq points d'accroche est introuvable, ou se trouve plus d'une fois ;
   - le personnage est deja pose (il ne le pose pas deux fois).
Dans ces cas-la il s'arrete et il le dit. Il n'ecrit rien a moitie : le fichier n'est remplace
qu'une fois les cinq morceaux poses ET le resultat compile.

AVANT : lancer  python _poser_la_base_v100.py   (il met la bonne base et fait la sauvegarde)
POUR LE LANCER :  python _poser_le_personnage_luciana.py
APRES  : lancer  python _verif_personnage_luciana.py   (le controle)

LES HUIT FICHIERS VIDEO a deposer dans le dossier "apparence", a cote de luciana.py :
    personnage_1_marche.webm   personnage_2_parle.webm   personnage_3_regarde.webm
    activite_01.webm  activite_02.webm  activite_03.webm  activite_04.webm  activite_05.webm
Si l'un manque, RIEN NE CASSE : la page s'ouvre normalement et se passe de cette boucle-la.
"""
import os
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
CIBLE = os.path.join(ICI, "luciana.py")


# =====================================================================================
# 1) LE PROGRAMME : le dossier livre, les huit boucles, et la fonction qui les retrouve.
#    Pose JUSTE AVANT le texte de sa personnalite, c'est-a-dire juste apres la mecanique
#    du portrait, a laquelle on ne touche pas.
# =====================================================================================
ACCROCHE_PY = '\nPERSONNALITE = """Tu es Luciana,'

BLOC_PY = r'''
# ---------- SON PERSONNAGE ANIME : HUIT boucles video, fond transparent (04/10/2026) ----------
# C'est la MEME chose que chez Luminita, sa petite soeur : de petites videos detourees (VP9 avec
# un VRAI canal alpha, donc un vrai fond transparent et pas un rectangle) qui tournent en boucle
# et qui la montrent, ELLE, posee sur la page. Elle passe DERRIERE TOUTES LES ECRITURES et ne
# prend aucun clic.
#
# LES TROIS BOUCLES D'ETAT (ce qu'elle fait AVEC NOUS) :
#   personnage_1_marche.webm    elle marche, elle reflechit
#   personnage_2_parle.webm     elle parle face camera, levres qui bougent  -> SA VOIX SORT
#   personnage_3_regarde.webm   elle s'arrete et te regarde                 -> ELLE T'ECOUTE
#
# LES CINQ OCCUPATIONS : quand elle n'est ni en train de parler ni en train d'ecouter, elle VIT.
# La page tire AU HASARD, pour une duree elle aussi AU HASARD, dans le melange "la marche + ces
# cinq occupations", et elle ne rejoue JAMAIS deux fois de suite la meme.
#   activite_01.webm ... activite_05.webm
#
# Huit fichiers en tout : c'est exactement le nombre de boucles fabriquees pour Luciana. Chez
# Luminita il y en a treize ; c'est le seul ecart, et il ne change rien a la mecanique.
#
# Elles voyagent AVEC le programme, dans le dossier "apparence" pose A COTE de ce fichier,
# exactement comme chez Luminita. AUCUN CHEMIN EN DUR vers le PC de qui que ce soit : tout part
# de DOSSIER_PROG (le dossier ou se trouve ce fichier, ou qu'il ait ete copie).
# A NE PAS CONFONDRE avec DOSSIER_APPARENCE (plus haut), qui est dans le dossier PRIVE de Fred
# et qui garde le portrait qu'il a choisi : celui-la ne bouge pas, on n'y touche pas.
#
# SI UN FICHIER MANQUE, RIEN NE CASSE : la page se charge normalement, la route repond
# simplement "pas trouve", et la page retire d'elle-meme cette boucle de ses tirages. Pas
# d'icone cassee : une balise <video> sans source reste transparente.
DOSSIER_APPARENCE_LIVREE = os.path.join(DOSSIER_PROG, "apparence")
PERSONNAGE_BOUCLES = {
    "marche":  "personnage_1_marche.webm",
    "parle":   "personnage_2_parle.webm",
    "regarde": "personnage_3_regarde.webm",
}
# Les cinq occupations s'ajoutent au MEME tableau : la route /personnage et le controle du nom
# n'ont donc rien a apprendre de nouveau, et un mot cle reste un mot cle.
for _n in range(1, 6):
    PERSONNAGE_BOUCLES["activite_%02d" % _n] = "activite_%02d.webm" % _n
del _n


def _boucle_personnage(nom):
    """Le fichier d'une des boucles animees, sinon None.

    'nom' arrive depuis la PAGE : on ne s'en sert JAMAIS pour fabriquer un chemin. On le cherche
    dans le petit tableau ci-dessus, et c'est tout. Impossible, donc, de se faire servir un
    autre fichier du disque en trafiquant l'adresse."""
    fichier = PERSONNAGE_BOUCLES.get(nom)
    if not fichier:
        return None
    chemin = os.path.join(DOSSIER_APPARENCE_LIVREE, fichier)
    return chemin if os.path.isfile(chemin) else None

'''


# =====================================================================================
# 2) L'HABILLAGE. Pose juste apres l'animation du cadre du portrait, donc dans la partie
#    "la scene" : on AJOUTE un bloc, on ne modifie aucune ligne existante.
# =====================================================================================
ACCROCHE_CSS = ("  @keyframes flotte{0%,100%{transform:translateY(0) rotate(0)} "
                "50%{transform:translateY(-12px) rotate(.25deg)}}\n")

BLOC_CSS = r"""
  /* ------- LE PERSONNAGE ANIME : POSE SUR LA PAGE, ET TOUJOURS DERRIERE LES ECRITURES -------
     04/10/2026. La meme chose que chez Luminita, sa petite soeur. Huit petites boucles video
     detourees, a vrai fond transparent (voir PERSONNAGE_BOUCLES dans le programme). C'est le
     script, plus bas, qui choisit laquelle tourne selon ce qu'elle est en train de faire.

     LE POINT IMPORTANT, celui sur lequel Fred a insiste chez Luminita : ELLE PASSE DERRIERE
     TOUT LE TEXTE. Trois choses s'en chargent ENSEMBLE, et aucune ne suffirait seule :
       1. z-index:0 ET une place HORS du bloc .app. Toute l'interface vit dans .app, qui est en
          z-index:1 : messages, bulles, panneaux, historique, boutons sont donc dessines
          PAR-DESSUS elle, sans exception et sans avoir a toucher a leurs z-index.
       2. pointer-events:none : aucun clic, aucune selection de texte ne l'atteint. On ecrit et
          on clique A TRAVERS elle, meme quand elle passe devant un bouton.
       3. aucun fond du tout : le .webm a un vrai canal alpha, on ne met donc aucune couleur ni
          aucune bordure derriere elle. Pas de rectangle.
     Et ca reste vrai MEME PENDANT QU'ELLE BOUGE : la promenade ne touche QUE translateX. Rien
     ici ne cree de calque qui remonterait au-dessus de .app (aucun opacity < 1, aucun filter,
     aucun z-index positif, aucune animation sur z-index).

     left:50% n'est que son POINT DE DEPART. C'est le script (voir "SA PLACE DANS LA FENETRE")
     qui la decale sur un COTE, en part de la largeur de la fenetre, et toujours par le seul
     translateX. Elle ne se poste JAMAIS au milieu : le centre est reserve aux ecritures. */
  #personnage{
    position:fixed; bottom:0; left:50%; height:min(74vh,640px);
    transform:translateX(-50%); transform-origin:50% 100%;
    z-index:0; pointer-events:none; will-change:transform;}
  #personnage video{height:100%; display:block; background:transparent;}
  #personnage video.hors{display:none;}
  /* Elle se fait plus discrete quand l'ecran a peu de place. On ne reduit que du decor, JAMAIS
     un bouton. Tout est en part de l'ecran : c'est juste sur n'importe quelle taille. */
  @media (max-width:640px){ #personnage{height:min(56vh,420px);} }
  @media (max-height:780px){ #personnage{height:min(60vh,440px);} }
  @media (max-height:640px){ #personnage{height:min(52vh,330px);} }
  @media (max-height:520px){ #personnage{height:min(46vh,260px);} }
"""


# =====================================================================================
# 3) LA PAGE : les huit balises <video>, EN DEHORS du bloc .app.
# =====================================================================================
ACCROCHE_HTML = '  <div class="ambiance"></div>\n  <div class="app">'

BLOC_HTML = r"""  <div class="ambiance"></div>

  <!-- ------- ELLE, ANIMEE : SON PERSONNAGE (04/10/2026) -------
       Huit petites boucles video detourees, a vrai fond transparent : pas de cadre, pas de
       rectangle, rien autour d'elle.

       SA PLACE DANS LA PAGE EST VOULUE : ce bloc est DEHORS du bloc .app, juste avant lui.
       Comme .app est en z-index:1 et elle en z-index:0, absolument tout ce qui s'affiche
       (texte, bulles, messages, panneaux, historique, boutons) passe DEVANT elle,
       automatiquement et definitivement : il n'y a aucun z-index a regler ailleurs, et il n'y
       aura rien a refaire quand on ajoutera un nouveau panneau plus tard. NE PAS LA DEPLACER
       DANS .app : elle passerait alors devant une partie du texte.

       Les huit balises sont chargees des le depart et tournent en boucle ; le script en montre
       UNE SEULE a la fois (classe "hors") et met TOUTES les autres en pause. On evite ainsi le
       petit noir au changement d'etat (la boucle est deja prete quand on l'affiche) et les
       boucles cachees, etant en pause, ne chauffent pas le portable.
       aria-hidden : c'est du decor, le lecteur d'ecran n'a rien a annoncer ici. -->
  <div id="personnage" aria-hidden="true">
    <video id="boucleMarche"  class="hors" src="/personnage?r=marche"  loop muted playsinline autoplay preload="auto"></video>
    <video id="boucleRegarde" class="hors" src="/personnage?r=regarde" loop muted playsinline autoplay preload="auto"></video>
    <video id="boucleParle"   class="hors" src="/personnage?r=parle"   loop muted playsinline autoplay preload="auto"></video>
    <!-- SES CINQ OCCUPATIONS. Elles ne sont liees a AUCUN etat precis : elles sont tirees au
         hasard avec la marche des qu'elle n'est ni en train de parler ni en train d'ecouter.
         C'est justement ce qui fait qu'on ne voit aucun rythme. -->
    <video id="boucleActivite01" class="hors" src="/personnage?r=activite_01" loop muted playsinline autoplay preload="auto"></video>
    <video id="boucleActivite02" class="hors" src="/personnage?r=activite_02" loop muted playsinline autoplay preload="auto"></video>
    <video id="boucleActivite03" class="hors" src="/personnage?r=activite_03" loop muted playsinline autoplay preload="auto"></video>
    <video id="boucleActivite04" class="hors" src="/personnage?r=activite_04" loop muted playsinline autoplay preload="auto"></video>
    <video id="boucleActivite05" class="hors" src="/personnage?r=activite_05" loop muted playsinline autoplay preload="auto"></video>
  </div>

  <div class="app">"""


# =====================================================================================
# 4) LE MOUVEMENT. Pose juste apres les variables d'etat de la page (dont 'ecoute'), et
#    juste avant la petite fonction d'aide : exactement la meme place que chez Luminita.
#    ON NE TOUCHE A AUCUNE LIGNE QUI ENVOIE, QUI PARLE OU QUI ECOUTE : on se contente de
#    RELIRE, six fois par seconde, deux choses qui existaient deja dans la page.
# =====================================================================================
ACCROCHE_JS = ("  let ecoute = false;      // le micro est en train d'ecouter\n\n"
               "  function aide(t){")

BLOC_JS = r"""  let ecoute = false;      // le micro est en train d'ecouter

  // ---------- SON PERSONNAGE ANIME : LA BONNE BOUCLE AU BON MOMENT (04/10/2026) ----------
  // Repris tel quel de Luminita, sa petite soeur, ou Fred l'a vu tourner et l'a valide (y
  // compris la correction du 2e passage : voir l'ordre de priorite, juste en dessous).
  //
  // L'ORDRE EST LE SUIVANT, SANS AUCUNE EXCEPTION :
  //    1. SA VOIX SORT        -> 'parle', immobile sur un cote, bouche visible. Aucune
  //                              condition attachee : ni le point d'interrogation, ni le micro
  //                              (qui reste ouvert MEME pendant qu'elle parle - c'est
  //                              precisement le piege qui, chez Luminita, l'empechait de
  //                              bouger les levres quand on regardait le micro en premier).
  //    2. LE MICRO EST OUVERT -> 'regarde', immobile sur un cote : c'est nous qui parlons.
  //    3. TOUT LE RESTE       -> ses occupations (elle vient de finir, elle reflechit, ou il
  //                              ne se passe rien). Elle se deplace alors sur les cotes.
  //
  // POURQUOI ON NE FAIT QUE REGARDER, SANS RIEN MODIFIER AILLEURS : son etat est DEJA ecrit
  // dans la page, a des endroits qui existaient bien avant ce chantier :
  //    body.parle = DU SON SORT EN CE MOMENT. C'est un fait, pas une estimation : la classe
  //                 est posee quand le son demarre et retiree quand il se termine (onstart /
  //                 onend, et aussi quand on coupe la voix).
  //    ecoute     = le micro tourne.
  // On ne touche donc pas une seule ligne des fonctions qui envoient, qui parlent ou qui
  // ecoutent. Le bloc de dictee de Chrome, en particulier, n'est pas effleure.
  const BOUCLES_PERSO = {marche:'boucleMarche', parle:'boucleParle', regarde:'boucleRegarde',
    activite_01:'boucleActivite01', activite_02:'boucleActivite02', activite_03:'boucleActivite03',
    activite_04:'boucleActivite04', activite_05:'boucleActivite05'};
  const couchePerso = document.getElementById('personnage');
  let persoEtat = '';
  let persoPoste = false;   // true = elle est postee sur un cote (elle parle, ou elle t'ecoute)

  // LE GARDE-FOU : SI UN FICHIER VIDEO MANQUE, LA PAGE CONTINUE NORMALEMENT.
  // Le serveur repond "pas trouve" et la balise <video> previent par un evenement 'error'. On
  // raye alors cette boucle de la liste, sans un mot a l'ecran et sans rien casser : elle ne
  // sera plus tiree au sort, et une boucle d'etat manquante est remplacee par une autre.
  const boucleAbsente = {};
  for (const cle in BOUCLES_PERSO){
    const v = document.getElementById(BOUCLES_PERSO[cle]);
    if (!v){ boucleAbsente[cle] = true; continue; }
    v.addEventListener('error', ()=>{ boucleAbsente[cle] = true; });
  }
  function boucleDispo(nom){ return !!BOUCLES_PERSO[nom] && !boucleAbsente[nom]; }

  // Quand la boucle voulue n'est pas la, on prend la premiere autre qui soit la : elle reste
  // ainsi postee sur le cote au lieu de disparaitre d'un coup.
  function immobile(voulue){
    const ordre = [voulue, 'parle', 'regarde', 'marche'];
    for (let i = 0; i < ordre.length; i++){ if (boucleDispo(ordre[i])) return ordre[i]; }
    return voulue;   // plus aucune boucle : la page tourne quand meme, on ne voit personne
  }

  // ----- SES OCCUPATIONS : "QUE CE SOIT PAS PROGRAMME" (la demande de Fred chez Luminita) -----
  // Quand elle n'est ni en train de parler ni en train d'ecouter, elle VIT. Le melange, c'est
  // sa marche PLUS ses cinq occupations. On y pioche AU HASARD, pour une duree AU HASARD :
  // aucun enchainement n'est ecrit a l'avance, donc aucun rythme ne se voit.
  const OCCUPATIONS = ['marche',
    'activite_01', 'activite_02', 'activite_03', 'activite_04', 'activite_05'];
  const OCCUPATION_MINI = 6000;    // elle garde une occupation au moins 6 s...
  const OCCUPATION_MAXI = 14000;   // ...et au plus 14 s, tire au hasard entre les deux
  let occupationEnCours = '';
  let occupationJusqua = 0;

  function occupationsLa(){
    const d = OCCUPATIONS.filter(boucleDispo);
    return d.length ? d : OCCUPATIONS;   // si tout manque, on n'empeche rien : la page continue
  }

  // ON NE REJOUE JAMAIS DEUX FOIS DE SUITE LA MEME : si le tirage retombe sur celle qui vient
  // d'etre jouee, ON RETIRE. Le petit compteur n'est qu'une ceinture de securite : il evite une
  // boucle infinie si la liste se retrouvait un jour reduite a une seule entree.
  function tirerOccupation(maintenant){
    const liste = occupationsLa();
    let tirage = liste[Math.floor(Math.random() * liste.length)];
    for (let essai = 0; essai < 24 && tirage === occupationEnCours && liste.length > 1; essai++){
      tirage = liste[Math.floor(Math.random() * liste.length)];
    }
    occupationEnCours = tirage;
    occupationJusqua = maintenant + OCCUPATION_MINI + Math.random() * (OCCUPATION_MAXI - OCCUPATION_MINI);
    return tirage;
  }

  function occupationDuMoment(){
    const maintenant = Date.now();
    if (!occupationEnCours || maintenant >= occupationJusqua) return tirerOccupation(maintenant);
    return occupationEnCours;
  }

  function etatVoulu(){
    // 1. SA VOIX SORT : elle parle. C'est la PREMIERE question posee, et sans condition.
    if (body.classList.contains('parle')){ persoPoste = true; return immobile('parle'); }
    // 2. LE MICRO EST OUVERT, elle ne parle pas : c'est nous qui parlons, elle nous regarde.
    if (ecoute){ persoPoste = true; return immobile('regarde'); }
    // 3. Tout le reste : elle repart a ses occupations.
    persoPoste = false;
    return occupationDuMoment();
  }

  function montrerBoucle(nom){
    if (nom === persoEtat) return;
    // En se postant (elle parle, elle ecoute), on remet le minuteur des occupations a zero :
    // en repartant, elle prendra donc une occupation fraichement tiree, et non le reste d'une
    // ancienne.
    if (persoPoste) occupationJusqua = 0;
    persoEtat = nom;
    for (const cle in BOUCLES_PERSO){
      const v = document.getElementById(BOUCLES_PERSO[cle]);
      if (!v) continue;
      if (cle === nom){
        v.classList.remove('hors');
        try{ v.currentTime = 0; }catch(e){}  // une occupation se revoit depuis son debut
        const p = v.play();                 // muted + playsinline : aucun navigateur ne refuse
        if (p && p.catch) p.catch(()=>{});  // et si l'un refuse quand meme, la page continue
      } else {
        v.classList.add('hors');
        try{ v.pause(); }catch(e){}         // les boucles cachees ne chauffent pas le portable
      }
    }
  }
  if (couchePerso){
    montrerBoucle('marche');
    setInterval(()=>{ try{ montrerBoucle(etatVoulu()); }catch(e){} }, 160);
  }

  // ---------- SA PLACE DANS LA FENETRE : SUR UN COTE, JAMAIS AU MILIEU ----------
  // La regle etablie chez Luminita, apres l'essai de Fred : comme le texte passe DEVANT elle,
  // au centre on ne la voyait plus du tout. LA BANDE CENTRALE N'EST DONC PAS UNE PLACE
  // POSSIBLE, le centre est reserve aux ecritures :
  //    elle parle / elle t'ecoute / elle te dit bonjour  ->  elle se poste sur UN COTE et elle
  //                                                          y reste IMMOBILE, bouche visible ;
  //    elle est a ses occupations                        ->  elle flane doucement dans les
  //                                                          ZONES LATERALES, et quand elle
  //                                                          change de bord elle TRAVERSE d'un
  //                                                          trait, sans s'arreter au milieu.
  //
  // Elle reste DERRIERE LE TEXTE exactement comme avant : on ne touche QUE translateX, rien
  // d'autre. TOUT EST EN PART DE LA LARGEUR DE LA FENETRE, jamais en pixels fixes : la page est
  // juste aussi bien sur un grand ecran que sur un portable, et comme on relit innerWidth a
  // chaque image, ses places se recalculent toutes seules si on redimensionne la fenetre.
  if (couchePerso){
    const COTE_GAUCHE = 0.115;         // ou se tient le milieu de sa silhouette, bord gauche
    const COTE_DROIT  = 0.885;         // ... et bord droit
    const FLANERIE    = 0.05;          // de combien elle flane autour de son bord
    const AVANT_TRAVERSEE = 7000;      // elle reste au moins 7 s du meme cote
    const APRES_TRAVERSEE = 15000;     // ... et 15 s au plus

    let persoX = 0;              // son decalage par rapport au CENTRE de la fenetre, en pixels
    let cote = 1;                // -1 = elle est au bord gauche, +1 = elle est au bord droit
    let depart = 0;              // le debut de sa flanerie du moment
    let prochaineTraversee = 0;  // le moment ou elle se decidera a passer de l'autre cote
    let demiPerso = 0, demiLue = -9999;   // sa demi-largeur, et quand on l'a mesuree

    // Sa demi-largeur sert a ne pas la laisser sortir de l'ecran. On ne la mesure que deux fois
    // par seconde : la relire a chaque image obligerait le navigateur a tout remesurer.
    function demiLargeur(maintenant){
      if (maintenant - demiLue > 500){ demiLue = maintenant; demiPerso = couchePerso.offsetWidth / 2; }
      return demiPerso || window.innerWidth * 0.11;
    }

    // OU SE TENIR : on donne une place en part de la largeur (0 = bord gauche, 1 = bord droit)
    // et on recoit le decalage translateX correspondant. La garde empeche DEUX choses a la
    // fois : qu'elle sorte de l'ecran, et que sur une fenetre etroite on la ramene au centre
    // (elle ne depasse jamais 22 % / 78 % de la largeur, donc elle n'entre pas dans le texte).
    function versDecalage(part, maintenant){
      const W = window.innerWidth;
      const garde = Math.min(demiLargeur(maintenant) * 0.75, W * 0.22);
      let x = part * W;
      if (x < garde) x = garde;
      if (x > W - garde) x = W - garde;
      return x - W / 2;
    }

    // L'ACCUEIL, LE COUCOU DU DEMARRAGE : son bonjour est deja ecrit dans la bulle alors qu'elle
    // n'a encore rien repondu. C'est precisement le moment ou il faut la voir sur un cote : ce
    // texte-la est long, et au milieu elle disparaitrait entierement derriere.
    function ditBonjour(){
      return !derniereReponse && !!(parole && parole.textContent.trim());
    }

    function promenade(maintenant){
      requestAnimationFrame(promenade);
      const W = window.innerWidth;
      let cible;
      if (!persoPoste && !ditBonjour()){
        // ELLE FLANE SUR SON BORD, et de temps en temps elle part vers l'autre.
        if (!depart){ depart = maintenant; prochaineTraversee = maintenant + AVANT_TRAVERSEE; }
        if (maintenant > prochaineTraversee){
          cote = -cote;          // elle s'en va vers l'autre bord : la traversee ne s'arrete pas
          prochaineTraversee = maintenant + AVANT_TRAVERSEE
                             + Math.random() * (APRES_TRAVERSEE - AVANT_TRAVERSEE);
        }
        const flanerie = Math.sin((maintenant - depart) / 1000 * 0.5) * FLANERIE;
        cible = versDecalage((cote < 0 ? COTE_GAUCHE : COTE_DROIT) + flanerie, maintenant);
      } else {
        // ELLE PARLE, ELLE T'ECOUTE, OU ELLE TE DIT BONJOUR : elle se poste sur un cote et elle
        // y reste. Elle choisit LE COTE OU ELLE EST DEJA, pour ne pas sauter pour rien ; et si
        // elle etait en pleine traversee (encore dans la bande centrale), elle CONTINUE jusqu'au
        // bord qu'elle visait plutot que de revenir en arriere.
        depart = 0;
        if (Math.abs(persoX) > W * 0.12) cote = persoX < 0 ? -1 : 1;
        cible = versDecalage(cote < 0 ? COTE_GAUCHE : COTE_DROIT, maintenant);
      }
      persoX += (cible - persoX) * 0.05;   // elle glisse vers sa place, elle ne saute jamais
      couchePerso.style.transform = 'translateX(calc(-50% + ' + persoX.toFixed(1) + 'px))';
    }
    requestAnimationFrame(promenade);
  }

  function aide(t){"""


# =====================================================================================
# 5) LE SERVEUR : l'adresse /personnage. Elle ne sait faire qu'une chose : servir une des
#    huit boucles livrees. Elle ne lit aucune donnee, n'ecrit rien, et ne prend JAMAIS un
#    nom de fichier (voir _boucle_personnage). Elle est posee apres /portrait, derriere le
#    meme controle du code d'acces que tout le reste de do_GET.
# =====================================================================================
ACCROCHE_ROUTE = '        elif self.path == "/voix_el_liste":'

BLOC_ROUTE = r'''        elif self.path.split("?")[0] == "/personnage":
            # UNE DES HUIT BOUCLES ANIMEES (04/10/2026). L'adresse ressemble a
            # /personnage?r=marche : 'r' est un MOT CLE (marche, parle, regarde,
            # activite_01 ... activite_05), jamais un nom de fichier et jamais un chemin.
            # _boucle_personnage() le cherche dans son petit tableau : on ne peut donc pas se
            # faire servir autre chose du disque en trafiquant l'adresse.
            nom = ""
            if "?" in self.path:
                nom = (urllib.parse.parse_qs(self.path.split("?", 1)[1]).get("r") or [""])[0]
            chemin = _boucle_personnage(nom)
            try:
                data = open(chemin, "rb").read() if chemin else None
            except OSError:
                data = None
            if data is None:
                # La boucle n'est pas (encore) la : on le dit proprement. La page se charge
                # normalement, il n'y a juste pas de personnage. RIEN NE CASSE.
                self.send_response(404)
                self._no_cache()
                self.end_headers()
                return
            self.send_response(200)
            self.send_header("Content-Type", "video/webm")
            self.send_header("Content-Length", str(len(data)))
            self.send_header("Cache-Control", "max-age=86400")
            self.end_headers()
            self.wfile.write(data)
        elif self.path == "/voix_el_liste":'''


MORCEAUX = [
    ("1/5  le programme : les huit boucles et leur dossier livre", ACCROCHE_PY,
     BLOC_PY + ACCROCHE_PY.lstrip("\n")),
    ("2/5  l'habillage : #personnage, derriere les ecritures", ACCROCHE_CSS,
     ACCROCHE_CSS + BLOC_CSS),
    ("3/5  la page : les huit balises video, hors du bloc .app", ACCROCHE_HTML, BLOC_HTML),
    ("4/5  le mouvement : la bonne boucle, et sa place sur un cote", ACCROCHE_JS, BLOC_JS),
    ("5/5  le serveur : l'adresse /personnage", ACCROCHE_ROUTE, BLOC_ROUTE),
]


def main():
    if not os.path.isfile(CIBLE):
        print("ECHEC : je ne trouve pas %s" % CIBLE)
        return 1

    # On lit SANS toucher aux fins de ligne (newline=""), et on ecrira pareil : le fichier ne
    # doit pas changer d'un bout a l'autre juste parce qu'on y ajoute un bloc. Si jamais il
    # etait en fins de ligne Windows, on y met nos morceaux dans le meme style.
    with open(CIBLE, "r", encoding="utf-8", newline="") as f:
        src = f.read()
    avant = len(src)
    fin_de_ligne = "\r\n" if "\r\n" in src else "\n"

    print("=== LES REFUS (on controle AVANT d'ecrire quoi que ce soit) ===")

    if "&middot; v100" not in src:
        print("  REFUS : luciana.py n'est pas la v100 (le badge de la page ne dit pas v100).")
        print("          Lance d'abord : python _poser_la_base_v100.py")
        return 1
    print("  [OK] la base est bien la v100")

    traces = [m for m in ("etatDictee", "moteurDictee", "dicteeLocale", "/dictee",
                          "wBasculerSurChrome") if m in src]
    if traces:
        print("  REFUS : la dictee locale Whisper (abandonnee par Fred) est encore la : %s"
              % ", ".join(traces))
        print("          Lance d'abord : python _poser_la_base_v100.py")
        return 1
    print("  [OK] aucune trace de la dictee locale Whisper (v101 a v104)")

    if "PERSONNAGE_BOUCLES" in src or 'id="personnage"' in src:
        print("  REFUS : le personnage est deja pose. Je ne le pose pas deux fois.")
        return 1
    print("  [OK] le personnage n'est pas encore pose")

    morceaux = [(t, a.replace("\n", fin_de_ligne), r.replace("\n", fin_de_ligne))
                for t, a, r in MORCEAUX]
    for titre, accroche, _ in morceaux:
        n = src.count(accroche)
        if n != 1:
            print("  REFUS : le point d'accroche du morceau %s se trouve %d fois (il en faut"
                  " exactement 1)." % (titre.split()[0], n))
            print("          Le fichier n'est pas celui que j'attends. Je n'ecris rien.")
            return 1
    print("  [OK] les cinq points d'accroche sont la, et une seule fois chacun")

    print("\n=== LES CINQ MORCEAUX ===")
    for titre, accroche, remplacement in morceaux:
        src = src.replace(accroche, remplacement, 1)
        print("  pose : %s" % titre)

    print("\n=== LE CONTROLE AVANT D'ECRIRE ===")
    attendus = ["DOSSIER_APPARENCE_LIVREE = os.path.join(DOSSIER_PROG,", "PERSONNAGE_BOUCLES = {",
                "def _boucle_personnage(nom):", "  #personnage{", "z-index:0; pointer-events:none;",
                '<div id="personnage" aria-hidden="true">', 'id="boucleActivite05"',
                "const BOUCLES_PERSO = {", "function etatVoulu(){", "function promenade(maintenant){",
                'elif self.path.split("?")[0] == "/personnage":']
    manquants = [a for a in attendus if a not in src]
    if manquants:
        print("  RATE : %s" % ", ".join(manquants))
        print("  Je n'ecris rien. luciana.py n'a pas ete touche.")
        return 1
    print("  [OK] les %d reperes du personnage sont dans le texte prepare" % len(attendus))

    # LE PERSONNAGE DOIT ETRE HORS DU BLOC .app : on le verifie sur le texte, avant d'ecrire.
    i_perso = src.find('<div id="personnage" aria-hidden="true">')
    i_app = src.find('<div class="app">')
    if not (0 < i_perso < i_app):
        print("  RATE : le personnage n'est pas AVANT le bloc .app. Je n'ecris rien.")
        return 1
    print("  [OK] le personnage est bien pose EN DEHORS (et avant) du bloc .app")

    # ON COMPILE LE TEXTE AVANT D'ECRIRE QUOI QUE CE SOIT. Si le resultat avait la moindre
    # faute, luciana.py ne serait meme pas touche.
    try:
        compile(src, CIBLE, "exec")
    except SyntaxError as ex:
        print("  RATE : le resultat ne compile pas : %s (ligne %s)" % (ex.msg, ex.lineno))
        print("  Je n'ecris rien. luciana.py n'a pas ete touche.")
        return 1
    print("  [OK] le resultat compile")

    # On ecrit a cote, puis on bascule d'un coup : jamais de fichier a moitie ecrit.
    provisoire = CIBLE + ".nouveau"
    with open(provisoire, "w", encoding="utf-8", newline="") as f:
        f.write(src)
        f.flush()
        os.fsync(f.fileno())
    os.replace(provisoire, CIBLE)
    print("\nluciana.py est ecrit : %d octets avant, %d apres (+%d)."
          % (avant, len(src), len(src) - avant))

    print("\n=== CE QU'IL RESTE A FAIRE A LA MAIN ===")
    dossier = os.path.join(ICI, "apparence")
    print("Deposer les HUIT fichiers video dans : %s" % dossier)
    for f in ("personnage_1_marche.webm", "personnage_2_parle.webm", "personnage_3_regarde.webm",
              "activite_01.webm", "activite_02.webm", "activite_03.webm", "activite_04.webm",
              "activite_05.webm"):
        etat = "deja la" if os.path.isfile(os.path.join(dossier, f)) else "A DEPOSER"
        print("    %-28s %s" % (f, etat))
    print("Si l'un manque, rien ne casse : la page s'ouvre et se passe de cette boucle-la.")
    print("\nControle : python _verif_personnage_luciana.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
