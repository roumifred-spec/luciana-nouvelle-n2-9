# -*- coding: utf-8 -*-
"""LA NOUVELLE LUCIANA (N2, 19/10/2026) : l'ECRAN, la voix, le personnage, les boutons et TOUS les
outils de la V198, sans changement -- et des COULISSES neuves (coeur.py) : le trajet d'un message, la
memoire, l'apprentissage, le choix des outils.

Ce fichier ne fait que BRANCHER :
  - il charge l'ancien programme (luciana.py) comme il est, sans en changer une ligne ;
  - il remplace le trajet d'un message (/chat) par celui du coeur ;
  - ce que l'ancien programme ecrivait dans son ancienne memoire (rapports de chantier, clics de Fred,
    choses finies) part dans la NOUVELLE memoire ;
  - il ajoute a l'ecran : le dictaphone de Luminita (Chrome ecrit, Gemini corrige) et, dans le panneau
    « Etat », toutes les coulisses en quantites.
Sa memoire est dans ~/Luciana_neuve. Les cles, Gmail, la voix, les chantiers restent dans ~/Luciana.
"""
import os, sys, json, time, io, base64, threading, shutil, importlib.util, urllib.request, urllib.error

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(ICI)
sys.path.insert(0, ICI)
sys.path.insert(0, RACINE)
VERSION = "nouvelle N2.8e"
PORT = 8002          # la meme adresse que d'habitude (iPhone, Tailscale) : une seule Luciana a la fois


def charger_l_ancienne():
    spec = importlib.util.spec_from_file_location("luciana", os.path.join(RACINE, "luciana.py"))
    mod = importlib.util.module_from_spec(spec)
    sys.modules["luciana"] = mod
    spec.loader.exec_module(mod)
    return mod


L = charger_l_ancienne()
import coeur
coeur.brancher(L)

# --- Ce que la V198 ecrivait dans son ancienne memoire part dans la nouvelle ---------------------
# --- LA NOUNOU EST RETIREE (demande de Fred, 19/10/2026) : elle retenait ses ecritures dans ses vieux
#     fichiers en attendant un clic. On prend l'interrupteur que la V198 a deja (celui de Luminita) :
#     la nounou « n'existe pas » ici -> plus aucun blocage, plus de bouton ni de ligne « A valider ».
L.nounou_existe = lambda: False
L.ajouter_note_memoire = coeur.note_du_programme
L.confier_a_l_archiviste = coeur.confier
L.repondre = coeur.repondre
L.ajouter_a_la_memoire = lambda moi, elle, actions=None, note_lignes=None: (
    coeur.note_du_programme("%s\n%s" % (moi or "", elle or "")))


# =====================================================================================
#  LE DICTAPHONE (Luminita V205) : Chrome ecrit en direct, Gemini reecoute LE SON et corrige.
# =====================================================================================
F_DICTAPHONE = os.path.join(coeur.DOSSIER, "dictaphone.json")
DICTEE_MODELE = "gemini-3.7-flash"
DICTEE_NOMS_PROPRES = ("Luminita", "Luciana", "Fred", "Daniela", "Madigane", "Aaron", "Altin", "Angelova",
                       "WhatsApp", "Satisfaire International", "Paysera", "eMAG", "Annecy", "Braila", "Brăila")
DICTEE_MIMES = {"audio/wav", "audio/x-wav", "audio/webm", "audio/ogg", "audio/mp4", "audio/mpeg", "audio/aac",
                "audio/flac", "video/webm"}
DICTEE_CONSIGNE = (
    "Tu es une oreille, rien d'autre. ECOUTE cet enregistrement et ECRIS EXACTEMENT ce qui "
    "est dit, mot pour mot.\n"
    "REGLES ABSOLUES :\n"
    "- tu ecris SEULEMENT la transcription, sans un mot d'introduction, sans guillemets, "
    "sans commentaire, sans traduction ;\n"
    "- la personne peut avoir un ACCENT TRES FORT : ce n'est pas une raison pour deviner "
    "autre chose. Tu ecris ce que tu entends vraiment, meme si c'est maladroit ;\n"
    "- tu n'ameliores rien, tu ne corriges aucune faute, tu n'ajoutes aucun mot ;\n"
    "- TU N'INVENTES AUCUN MOT, JAMAIS. Si tu n'entends aucune parole (un souffle, une "
    "respiration, un bruit de piece, un silence), tu ne reponds RIEN DU TOUT : pas un "
    "mot, pas une phrase, pas une explication, pas d'excuse. Une reponse vide vaut "
    "infiniment mieux qu'un mot invente ;\n"
    "- tu n'ajoutes jamais un nom, un prenom ou un mot que tu n'as pas VRAIMENT entendu, "
    "meme s'il rendrait la phrase plus jolie ou plus logique ;\n"
    "- si tu n'entends aucune parole et qu'il te faut absolument ecrire quelque chose, tu "
    "ecris exactement : (aucune parole).\n"
    "La langue attendue est : francais. Si la personne parle une AUTRE langue, ecris quand "
    "meme ce que tu entends vraiment.\n")
_SANS_REFLEXION_REFUSE = {"oui": False}


def dictaphone_payant():
    d = coeur.lire_json(F_DICTAPHONE, {})
    return bool(d.get("payant", True))


def dictaphone(son_b64, mime):
    cle = L.lire_cle_gemini()
    if not cle:
        return {"ok": False, "err": "Il me manque la cle Gemini : le texte de Chrome reste."}
    try:
        son = base64.b64decode(son_b64 or "")
    except Exception:
        son = b""
    if not son:
        return {"ok": False, "err": "Je n'ai recu aucun son."}
    if len(son) > 12 * 1024 * 1024:
        return {"ok": False, "err": "Morceau de son trop gros."}
    mime = str(mime or "").split(";")[0].strip().lower()
    mime = mime if mime in DICTEE_MIMES else "audio/wav"
    parts = [{"text": DICTEE_CONSIGNE},
             {"text": "NOMS PROPRES A ECRIRE EXACTEMENT COMME CECI quand tu les entends dans ce son "
                      "(respecte les majuscules, n'en invente aucun autre, et n'ecris pas cette liste "
                      "dans ta reponse) : %s" % ", ".join(DICTEE_NOMS_PROPRES)},
             {"inline_data": {"mime_type": mime, "data": base64.b64encode(son).decode("ascii")}}]
    corps = {"contents": [{"role": "user", "parts": parts}],
             "generationConfig": {"temperature": 0, "maxOutputTokens": 4000}}
    if not _SANS_REFLEXION_REFUSE["oui"]:
        corps["generationConfig"]["thinkingConfig"] = {"thinkingBudget": 0}
    url = "https://generativelanguage.googleapis.com/v1beta/models/%s:generateContent" % DICTEE_MODELE

    def demander(c):
        req = urllib.request.Request(url, data=json.dumps(c).encode("utf-8"), method="POST",
                                     headers={"Content-Type": "application/json", "x-goog-api-key": cle})
        with urllib.request.urlopen(req, timeout=120) as r:
            return json.loads(r.read().decode("utf-8"))
    try:
        try:
            d = demander(corps)
        except urllib.error.HTTPError as ex:
            detail = ex.read().decode("utf-8", "replace")[:400]
            if ex.code == 400 and "thinking" in detail.lower() and "thinkingConfig" in corps["generationConfig"]:
                _SANS_REFLEXION_REFUSE["oui"] = True
                corps["generationConfig"].pop("thinkingConfig", None)
                d = demander(corps)
            else:
                return {"ok": False, "err": "Google a refuse ce morceau (code %s) : %s" % (ex.code, detail[:200])}
    except Exception as ex:
        return {"ok": False, "err": "Pas de reponse de Google : %s" % str(ex)[:200]}
    coeur.compter("morceaux_dictes")
    try:
        cand = (d.get("candidates") or [{}])[0]
        texte = "\n".join(str(p.get("text") or "") for p in (cand.get("content") or {}).get("parts") or []).strip()
    except Exception:
        texte = ""
    if not texte or texte.strip().lower().strip(".") in ("(aucune parole)", "aucune parole"):
        return {"ok": False, "err": "aucune parole"}
    return {"ok": True, "texte": texte}


# =====================================================================================
#  L'ECRAN : celui de la V198, mot pour mot, avec trois ajouts (badge, panneau, dictaphone)
# =====================================================================================
def _remplacer(page, avant, apres, quoi):
    if page.count(avant) != 1:
        raise RuntimeError("Ecran V198 : je ne retrouve pas « %s » (%d fois) -- rien n'est change." % (quoi, page.count(avant)))
    return page.replace(avant, apres)


CSS_AJOUT = r"""
  /* NOUVELLE LUCIANA : le panneau Etat montre les coulisses (plus large, defilant) */
  #panneauTechnique{width:min(94vw,700px); max-height:80vh; overflow:auto;}
  #ligneCoulisses{margin-top:6px; font-size:.74rem; line-height:1.45; white-space:pre-wrap; opacity:.95;}
  /* LE DICTAPHONE (Luminita V205) : le curseur gratuit / payant, juste au-dessus de la barre */
  #zoneDicta{display:flex; align-items:center; gap:10px; flex-wrap:wrap; padding:0 16px 8px;}
  #curseurDicta{display:inline-flex; align-items:center; gap:8px; font-size:.84rem;
    padding:5px 12px 5px 13px; border-radius:999px; border:1px solid rgba(255,255,255,.16);
    background:rgba(255,255,255,.06); color:var(--creme);}
  #curseurDicta .mot{opacity:.52; transition:.2s;}
  #curseurDicta .mot.choisi{opacity:1; font-weight:700; color:#fff;}
  #etatDicta{font-size:.82rem; opacity:.82; flex:1 1 180px; min-width:120px;}
  #etatDicta.mauvais{color:#f3b0b0; opacity:1;}
  .interrupteur{position:relative; display:inline-block; width:46px; height:26px; flex:0 0 auto;}
  .interrupteur input{position:absolute; opacity:0; width:100%; height:100%; margin:0; cursor:pointer;}
  .interrupteur .glissiere{position:absolute; inset:0; border-radius:999px; cursor:pointer;
    background:rgba(255,255,255,.18); border:1px solid rgba(255,255,255,.22); transition:.2s;}
  .interrupteur .glissiere::before{content:""; position:absolute; width:20px; height:20px; left:2px; top:2px;
    border-radius:50%; background:#fbf3ec; transition:.2s;}
  .interrupteur input:checked + .glissiere{background:linear-gradient(145deg,#e9c48a,#c79a58);}
  .interrupteur input:checked + .glissiere::before{transform:translateX(20px);}
</style>"""

ZONE_DICTA = r"""<div id="zoneDicta">
      <span id="curseurDicta" title="Gratuit = Chrome seul ecoute et ecrit (zero euro). Payant = Chrome ecrit en direct ET Gemini reecoute le son derriere pour corriger les mots (meilleur avec un accent, chaque phrase coute).">
        <span class="mot" id="motGratuit">gratuit</span>
        <label class="interrupteur"><input type="checkbox" id="interDicta" aria-label="payant ou gratuit"><span class="glissiere"></span></label>
        <span class="mot" id="motPayant">payant (Gemini corrige)</span>
      </span>
      <span id="etatDicta"></span>
    </div>
    <div class="barre">"""

# LA DICTEE HYBRIDE (Luminita V205) : le modele de la barre = prefixe + valide + chromeLibre + interim.
HYB = r"""
  const hyb = {actif: false, prefixe: '', valide: [], chromeLibre: [], interim: ''};
  function hybRendre(){
    const bouts = []; const ajouter = (t)=>{ const x = String(t || '').trim(); if (x) bouts.push(x); };
    ajouter(hyb.prefixe); hyb.valide.forEach(ajouter); hyb.chromeLibre.forEach(ajouter); ajouter(hyb.interim);
    champ.value = bouts.join(' '); bufFinal = champ.value;
    try{ majBrouillonBarre(); }catch(e){}
  }
  function hybAbsorberEdition(){
    try{ if (!hyb.actif) return; hyb.prefixe = champ.value; hyb.valide = []; hyb.chromeLibre = []; hyb.interim = ''; }catch(e){}
  }
  window.lumDicteeHybrideDemarrer = function(){ hyb.actif = true; hyb.prefixe = champ.value || ''; hyb.valide = []; hyb.chromeLibre = []; hyb.interim = ''; };
  window.lumDicteeCloreSiFini = function(){
    if (!hyb.actif) return; if (ecoute) return;
    try{ if (window.lumDicteeEnMarche && window.lumDicteeEnMarche()) return; }catch(e){}
    try{ if (window.lumDicteeEnVol && window.lumDicteeEnVol() > 0) return; }catch(e){}
    window.lumDicteeHybrideClore();
  };
  window.lumDicteeHybrideClore = function(sansProposer){
    if (!hyb.actif) return; hyb.actif = false; hyb.prefixe = champ.value; hyb.valide = []; hyb.chromeLibre = []; hyb.interim = '';
    if (sansProposer) return; if (champ.value.trim()) proposerEnvoi(champ.value.trim());
  };
  window.lumDicteeChromeEnAttente = function(){ return hyb.actif && !!(hyb.chromeLibre.length || hyb.interim.trim()); };
  window.lumDicteeMorceauCorrige = function(texte){
    const t = String(texte || '').trim(); if (!t) return;
    if (!hyb.actif){ champ.value = ((champ.value || '').trim() + ' ' + t).trim(); bufFinal = champ.value; return; }
    hyb.valide.push(t); hyb.chromeLibre = []; hybRendre();
  };
  window.lumDicteeMorceauRate = function(){
    if (!hyb.actif) return;
    hyb.chromeLibre.forEach(function(x){ if (String(x || '').trim()) hyb.valide.push(String(x).trim()); });
    hyb.chromeLibre = []; hybRendre();
  };
  window.lumChromeEcoute = function(){ return !!ecoute; };

  if (Reco){"""

MICRO_CLIC = r"""micro.addEventListener('click', async ()=>{
    const sonTourne = !!(window.lumDicteeEnMarche && window.lumDicteeEnMarche());
    if (sonTourne || ecoute){
      if (sonTourne) window.lumDicteeArreter();
      if (ecoute) arreterEcoute();
      ecoute = false; body.classList.remove('ecoute'); micro.classList.remove('actif');
      aide("Micro coupe. Ta phrase est dans la barre : relis, corrige, et envoie quand tu veux.");
      return;
    }
    if (body.classList.contains('parle')) faireTaire();
    if (window.lumDicteeVoulue && window.lumDicteeVoulue()){
      const avecChrome = !!reco;
      if (avecChrome && window.lumDicteeHybrideDemarrer) window.lumDicteeHybrideDemarrer();
      const ok = await window.lumDicteeDemarrer();
      if (!ok){ if (avecChrome && window.lumDicteeHybrideClore) window.lumDicteeHybrideClore(true); return; }
      if (avecChrome) demarrerEcoute();
      const chromeEcrit = avecChrome && ecoute;
      if (!chromeEcrit){
        ecoute = true; body.classList.add('ecoute'); micro.classList.add('actif');
        if (avecChrome && window.lumDicteeHybrideClore) window.lumDicteeHybrideClore(true);
      }
      aide(chromeEcrit
        ? "Je t'ecoute et j'ecris au fur et a mesure. Gemini reecoute le son derriere moi et corrige les mots : je n'envoie rien toute seule."
        : "Je t'ecoute. Le texte arrivera par morceaux de quelques secondes, le temps que Gemini ecoute.");
      return;
    }
    if (!reco){
      champ.focus();
      aide("Sur telephone : touche le champ, puis le petit micro de ton clavier, et parle-moi.");
      return;
    }
    if (ecoute){ arreterEcoute(); return; }
    demarrerEcoute();
  });
  champ.addEventListener('input', ()=>{ bufFinal = champ.value; hybAbsorberEdition(); });"""

# LE DEUXIEME SCRIPT (Luminita V205) : l'enregistreur par morceaux coupes aux silences + la file vers Gemini.
SCRIPT_DICTAPHONE = r"""
<script>
(function(){
  function $(id){ return document.getElementById(id); }
  const inter = $('interDicta'), etat = $('etatDicta'), motG = $('motGratuit'), motP = $('motPayant');
  if (!inter) return;
  let file = Promise.resolve(), enVol = 0, enEcoute = false;
  function dire(t, mauvais){ if (!etat) return; etat.textContent = t || ''; etat.classList.toggle('mauvais', !!mauvais); }
  function peindre(p){ inter.checked = !!p; motG.classList.toggle('choisi', !p); motP.classList.toggle('choisi', !!p); }
  peindre(!!window.DICTAPHONE_PAYANT);
  function majIndicateur(){
    if (enVol > 0){ dire(enEcoute ? "J'ecris... (Gemini corrige derriere moi)" : "Je termine la correction du dernier morceau..."); return; }
    if (enEcoute){ dire("Je t'ecoute... reclique sur le micro pour arreter."); return; }
    dire('');
  }
  const enr = (function(){
    const SEG_MIN_MS=2000, SEG_MAX_MS=6000, SEG_SILENCE_MS=500, SEUIL_SILENCE=0.012, SEUIL_PAROLE=0.010,
          MIN_TRAMES_PAROLE=4, PIC_MIN_VOIX=0.020, TOTAL_MAX_MS=600000;
    let flux=null, rec=null, bouts=[], mime='', ctx=null, an=null, tampon=null, minuteur=null, debutSeg=0,
        silDepuis=0, parle=false, trames=0, pic=0, arret=false, surSeg=null, debutTotal=0;
    function possible(){ return !!(navigator.mediaDevices && navigator.mediaDevices.getUserMedia && window.MediaRecorder); }
    function format(){ const e=['audio/webm;codecs=opus','audio/webm','audio/ogg;codecs=opus','audio/ogg','audio/mp4','audio/aac'];
      for (const t of e){ try{ if (MediaRecorder.isTypeSupported(t)) return t; }catch(x){} } return ''; }
    function b64(o){ let s=''; for (let i=0;i<o.length;i+=0x8000) s+=String.fromCharCode.apply(null,o.subarray(i,i+0x8000)); return btoa(s); }
    function wav(c, taux){ const n=c.length, buf=new ArrayBuffer(44+n*2), v=new DataView(buf);
      const m=(p,t)=>{ for (let i=0;i<t.length;i++) v.setUint8(p+i,t.charCodeAt(i)); };
      m(0,'RIFF'); v.setUint32(4,36+n*2,true); m(8,'WAVE'); m(12,'fmt '); v.setUint32(16,16,true); v.setUint16(20,1,true);
      v.setUint16(22,1,true); v.setUint32(24,taux,true); v.setUint32(28,taux*2,true); v.setUint16(32,2,true); v.setUint16(34,16,true);
      m(36,'data'); v.setUint32(40,n*2,true);
      for (let i=0;i<n;i++){ const x=Math.max(-1,Math.min(1,c[i])); v.setInt16(44+i*2, x<0?x*0x8000:x*0x7FFF, true); }
      return new Uint8Array(buf); }
    async function enWav(blob, mo){
      try{ const AC=window.AudioContext||window.webkitAudioContext, OAC=window.OfflineAudioContext||window.webkitOfflineAudioContext;
        const brut=await blob.arrayBuffer(); const c=new AC(); const son=await c.decodeAudioData(brut.slice(0)); try{ c.close(); }catch(e){}
        const off=new OAC(1, Math.max(1, Math.round(son.duration*16000)), 16000); const src=off.createBufferSource();
        src.buffer=son; src.connect(off.destination); src.start(0); const r=await off.startRendering();
        return {son: b64(wav(r.getChannelData(0), 16000)), mime: 'audio/wav'};
      }catch(e){ try{ return {son: b64(new Uint8Array(await blob.arrayBuffer())), mime: (mo||'audio/webm').split(';')[0]}; }catch(e2){ return null; } } }
    function niveau(){ if (!an || !tampon) return 1; try{ an.getFloatTimeDomainData(tampon); }catch(e){ return 1; }
      let s=0; for (let i=0;i<tampon.length;i++) s+=tampon[i]*tampon[i]; return Math.sqrt(s/tampon.length); }
    function menage(){ rec=null; clearInterval(minuteur); minuteur=null; try{ if (flux) flux.getTracks().forEach(p=>p.stop()); }catch(e){}
      flux=null; try{ if (ctx) ctx.close(); }catch(e){} ctx=null; an=null; tampon=null; }
    function morceau(){ if (arret || !flux) return; const t=format();
      rec = t ? new MediaRecorder(flux,{mimeType:t}) : new MediaRecorder(flux); mime = rec.mimeType || t || 'audio/webm';
      bouts=[]; debutSeg=Date.now(); silDepuis=0; parle=false; trames=0; pic=0;
      rec.ondataavailable = e=>{ if (e.data && e.data.size) bouts.push(e.data); };
      rec.onstop = async ()=>{ const blob=new Blob(bouts,{type:mime}); bouts=[]; const voix=parle;
        if (!arret) morceau(); else menage();
        if (!voix || !blob.size || blob.size < 1500 || !surSeg) return;
        const p = await enWav(blob, mime); if (p){ try{ surSeg(p); }catch(e){} } };
      rec.start(); }
    async function demarrer(cb){ if (!possible()) return false; if (flux) return false;
      flux = await navigator.mediaDevices.getUserMedia({audio:{echoCancellation:true, noiseSuppression:true}});
      surSeg=cb; arret=false; debutTotal=Date.now();
      try{ const AC=window.AudioContext||window.webkitAudioContext; ctx=new AC(); const src=ctx.createMediaStreamSource(flux);
        an=ctx.createAnalyser(); an.fftSize=1024; tampon=new Float32Array(an.fftSize); src.connect(an); }catch(e){ ctx=null; an=null; tampon=null; }
      morceau();
      minuteur = setInterval(()=>{ if (arret || !rec) return; if (Date.now()-debutTotal > TOTAL_MAX_MS){ arreter(); return; }
        const n=niveau(); if (n>pic) pic=n; if (n>=SEUIL_PAROLE) trames++;
        parle = (pic>=PIC_MIN_VOIX && trames>=MIN_TRAMES_PAROLE);
        if (n>=SEUIL_SILENCE) silDepuis=0; else if (!silDepuis) silDepuis=Date.now();
        const duree=Date.now()-debutSeg, blanc=silDepuis?Date.now()-silDepuis:0;
        if (duree>=SEG_MAX_MS || (duree>=SEG_MIN_MS && blanc>=SEG_SILENCE_MS)){ try{ rec.stop(); }catch(e){} } }, 100);
      return true; }
    function arreter(){ if (arret) return; arret=true; clearInterval(minuteur); minuteur=null;
      if (rec){ try{ rec.stop(); }catch(e){ menage(); } } else menage(); }
    return {possible, demarrer, arreter, enCours: ()=>!!flux && !arret};
  })();
  async function attendreChrome(){ if (!window.lumDicteeChromeEnAttente) return;
    for (let i=0;i<8 && !window.lumDicteeChromeEnAttente();i++) await new Promise(r=>setTimeout(r,100)); }
  async function envoyerUnMorceau(p){
    const r = await fetch('/dictaphone', {method:'POST', headers:{'Content-Type':'application/json'},
      body: JSON.stringify({son: p.son, mime: p.mime})});
    const d = await r.json(); await attendreChrome();
    if (!d.ok){ if (window.lumDicteeMorceauRate) window.lumDicteeMorceauRate();
      if (String(d.err||'').indexOf('aucune parole') >= 0) return; dire(d.err || "Je n'ai rien compris a ce morceau.", true); return; }
    if (window.lumDicteeMorceauCorrige) window.lumDicteeMorceauCorrige(d.texte);
  }
  function morceauPret(p){ enVol++; majIndicateur();
    file = file.then(()=>envoyerUnMorceau(p)).catch(()=>{ if (window.lumDicteeMorceauRate) window.lumDicteeMorceauRate();
      dire("La page n'a pas pu joindre le programme.", true); }).then(()=>{ enVol--; majIndicateur();
      if (window.lumDicteeCloreSiFini) window.lumDicteeCloreSiFini(); }); }
  window.lumDicteeVoulue = function(){ if (inter.checked) return true; return !(window.SpeechRecognition || window.webkitSpeechRecognition); };
  window.lumDicteeEnMarche = function(){ return enr.enCours(); };
  window.lumDicteeEnVol = function(){ return enVol; };
  window.lumDicteeDemarrer = async function(){
    if (enr.enCours()) return true;
    if (!enr.possible()){ dire("Ce navigateur ne sait pas enregistrer de son. Ouvre ma page avec Chrome.", true); return false; }
    try{ if (!(await enr.demarrer(morceauPret))){ dire("Je termine le morceau en cours... reclique dans une seconde."); return false; } }
    catch(e){ dire("Le micro n'est pas autorise. Clique sur le petit cadenas en haut de Chrome et dis oui.", true); return false; }
    enEcoute = true; majIndicateur(); return true;
  };
  window.lumDicteeArreter = function(){ try{ enr.arreter(); }catch(e){} enEcoute = false; majIndicateur();
    if (window.lumDicteeCloreSiFini) window.lumDicteeCloreSiFini(); };
  inter.addEventListener('change', async function(){
    const veut = inter.checked; peindre(veut);
    const chromeEcoute = !!(window.lumChromeEcoute && window.lumChromeEcoute()), sonEnMarche = enr.enCours();
    if (veut && chromeEcoute && !sonEnMarche){ if (window.lumDicteeHybrideDemarrer) window.lumDicteeHybrideDemarrer();
      if (!(await window.lumDicteeDemarrer()) && window.lumDicteeHybrideClore) window.lumDicteeHybrideClore(true); }
    if (!veut && sonEnMarche) window.lumDicteeArreter();
    dire(veut ? "Payant : j'ecris en direct et Gemini reecoute le son derriere pour corriger." : "Gratuit : Chrome seul ecoute et ecrit. Zero euro.");
    try{ const r = await fetch('/config_dictaphone', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({payant: veut})});
      const d = await r.json(); peindre(!!d.payant); }catch(e){ dire("Je n'ai pas pu garder ce choix.", true); }
  });
})();
</script>
</body>"""


def fabriquer_l_ecran():
    page = L.PAGE
    page = _remplacer(page, "ton amie &middot; V198", "ton amie &middot; " + VERSION, "le badge")
    page = _remplacer(page, "</style>", CSS_AJOUT, "la fin du style")
    page = _remplacer(page, '<div class="barre">', ZONE_DICTA, "la barre")
    page = _remplacer(page, '<div id="titreTechnique">Etat technique &mdash; a nous lire en cas de panne</div>',
                      '<div id="titreTechnique">Etat &mdash; les coulisses de Luciana</div>\n'
                      '      <div id="ligneCoulisses"></div>', "le titre du panneau")
    page = _remplacer(page, "      const mem = d.memoire || null;",
                      "      const lc = document.getElementById('ligneCoulisses');\n"
                      "      if (lc) lc.textContent = (d.coulisses || []).join('\\n');\n"
                      "      const mem = d.memoire || null;", "le panneau (coulisses)")
    # le micro : la dictee hybride de Luminita
    page = _remplacer(page, "  function oublierDicteeEnvoyee(){\n    bufFinal = '';\n    motsDejaPartis = textesSession.map(nbMots);\n  }",
                      "  function oublierDicteeEnvoyee(){\n    bufFinal = '';\n    motsDejaPartis = textesSession.map(nbMots);\n"
                      "    hybAbsorberEdition();\n  }", "oublierDicteeEnvoyee")
    page = _remplacer(page, "\n  if (Reco){", HYB, "if (Reco)")
    page = _remplacer(page, "      bufFinal += finalNew;\n      champ.value = (bufFinal + interim).trim();",
                      "      if (hyb.actif){\n        if (finalNew.trim()) hyb.chromeLibre.push(finalNew.trim());\n"
                      "        hyb.interim = interim; hybRendre();\n        motProvisoireEnCours = !!interim.trim();\n"
                      "        if (champ.value){ relancerMinuteur(); fredAParle(); }\n        return;\n      }\n"
                      "      bufFinal += finalNew;\n      champ.value = (bufFinal + interim).trim();", "reco.onresult")
    page = _remplacer(page, "      motProvisoireEnCours = false;\n      // v96 : Chrome coupe tout seul",
                      "      motProvisoireEnCours = false;\n"
                      "      if (hyb.actif && hyb.interim.trim()){ hyb.chromeLibre.push(hyb.interim.trim()); hyb.interim = ''; hybRendre(); }\n"
                      "      // v96 : Chrome coupe tout seul", "reco.onend (debut)")
    page = _remplacer(page, "      if (champ.value.trim()) proposerEnvoi(champ.value.trim());\n    };\n    reco.onerror",
                      "      if (hyb.actif) window.lumDicteeCloreSiFini();\n"
                      "      else if (champ.value.trim()) proposerEnvoi(champ.value.trim());\n    };\n    reco.onerror",
                      "reco.onend (fin)")
    debut = page.index("  micro.addEventListener('click', ()=>{")
    fin = page.index("  champ.addEventListener('input', ()=>{ bufFinal = champ.value; });") + \
        len("  champ.addEventListener('input', ()=>{ bufFinal = champ.value; });")
    page = page[:debut] + "  " + MICRO_CLIC + page[fin:]
    page = _remplacer(page, "<script>\n", "<script>\n  window.DICTAPHONE_PAYANT = __DICTAPHONE_PAYANT__;\n", "le premier script")
    idx = page.rindex("</body>")
    page = page[:idx] + SCRIPT_DICTAPHONE + page[idx + len("</body>"):]
    return page


PAGE_NEUVE = fabriquer_l_ecran()
L.PAGE = PAGE_NEUVE


# =====================================================================================
#  LES ADRESSES : celles de la V198, sauf le trajet d'un message, le panneau et le dictaphone
# =====================================================================================
class Handler(L.Handler):
    def _json(self, d):
        corps = json.dumps(d, ensure_ascii=False).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self._no_cache()
        self.end_headers()
        self.wfile.write(corps)

    def _corps(self):
        n = int(self.headers.get("Content-Length", 0) or 0)
        try:
            return json.loads(self.rfile.read(n) or b"{}")
        except Exception:
            return {}

    def do_GET(self):
        chemin = self.path.split("?")[0]
        if (chemin == "/" or self.path.startswith("/?")) and self._a_le_code():
            L.PAGE = PAGE_NEUVE.replace("__DICTAPHONE_PAYANT__", "true" if dictaphone_payant() else "false")
            return super().do_GET()
        if chemin == "/etat_travaux" and self._a_le_code():
            vrai, tampon = self.wfile, io.BytesIO()
            self.wfile = tampon
            try:
                super().do_GET()
            finally:
                self.wfile = vrai
            brut = tampon.getvalue().split(b"\r\n\r\n", 1)
            try:
                d = json.loads(brut[1].decode("utf-8")) if len(brut) == 2 else {}
            except Exception:
                d = {}
            # les anciennes lignes de l'ancienne memoire n'ont plus de sens : elles disparaissent
            for k in ("memoire", "journee", "pas_repondu"):
                d[k] = None
            try:
                d["coulisses"] = coeur.coulisses()
            except Exception as ex:
                d["coulisses"] = ["(panneau des coulisses en panne : %s)" % ex]
            return self._json(d)
        return super().do_GET()

    def do_POST(self):
        if self.path == "/acces" or not self._a_le_code():
            return super().do_POST()
        if self.path == "/chat":
            data = self._corps()
            msg = (data.get("message") or "").strip()
            image = None
            brut = data.get("image")
            if brut:
                mt, b64 = "image/jpeg", brut
                if isinstance(brut, str) and brut.startswith("data:"):
                    try:
                        entete, b64 = brut.split(",", 1)
                        mt = entete.split(":", 1)[1].split(";", 1)[0] or mt
                    except Exception:
                        b64 = brut
                image = {"media_type": mt, "data": b64}
            debut = time.time()
            try:
                rep = coeur.repondre(msg, image=image)
            except Exception as e:
                rep = "Oups, petit souci de mon cote : " + str(e)
            try:
                brs = L.brouillons_a_valider(debut)
            except Exception:
                brs = []
            try:
                cout = L.dernier_tour()
            except Exception:
                cout = None
            return self._json({"reply": rep, "brouillons": brs, "cout": cout})
        if self.path == "/dictaphone":
            d = self._corps()
            return self._json(dictaphone(d.get("son"), d.get("mime")))
        if self.path == "/config_dictaphone":
            d = self._corps()
            coeur.ecrire_json(F_DICTAPHONE, {"payant": bool(d.get("payant")), "change_le": coeur.maintenant()})
            if poser_mes_verites():                  # sa fiche « mon micro » dit le NOUVEAU reglage
                try:
                    coeur.MOTEUR.indexer(coeur.fiches())
                except Exception:
                    pass
            return self._json({"ok": True, "payant": dictaphone_payant()})
        return super().do_POST()


def sauvegarde_du_jour():
    """Une copie par jour de la nouvelle memoire (conversation, bibliotheque, rappels)."""
    try:
        dest = os.path.join(coeur.DOSSIER, "sauvegardes", time.strftime("%Y-%m-%d"))
        if not os.path.isdir(dest):
            os.makedirs(dest, exist_ok=True)
            for nom in ("conversation.jsonl", "bibliotheque.jsonl", "rangement.json", "rappels.json"):
                src = os.path.join(coeur.DOSSIER, nom)
                if os.path.exists(src):
                    shutil.copy2(src, os.path.join(dest, nom))
    except Exception:
        pass


# =====================================================================================
#  CE QU'ELLE EST VRAIMENT AUJOURD'HUI : des fiches ecrites par le PROGRAMME (jamais par elle),
#  datees, remises a jour quand ca change. Sans elles, sur elle-meme elle n'avait que de VIEUX messages
#  (ex. la dictee Windows Win+H, abandonnee) et elle les racontait comme si c'etait en place.
# =====================================================================================
def verites_du_programme():
    payant = dictaphone_payant()
    return {
        "micro": ("Mon micro (le dictaphone) : comment il marche VRAIMENT aujourd'hui",
                  "Verite ecrite par le programme (nouvelle Luciana %s). Le bouton micro de ma page : Chrome ecrit les "
                  "mots EN DIRECT pendant que Fred parle. Ensuite, si le reglage « Correction Gemini » est sur OUI, Gemini "
                  "(%s) reecoute le SON par morceaux de 2 a 6 secondes, coupes aux silences, et remplace le texte de Chrome "
                  "par ce qu'il a vraiment entendu ; un morceau sans vraie voix n'est jamais envoye ; si Gemini rate, le texte "
                  "de Chrome reste. REGLAGE ACTUEL : Correction Gemini = %s. Il faut la cle « gemini ». "
                  "CE QUI N'EST PAS EN PLACE : la dictee Windows (Win+H) a ete essayee en V203 et ABANDONNEE par Fred le "
                  "19/10/2026 (« c'est une catastrophe ») ; il n'y a aucun selecteur de langue qui commande le micro. "
                  "Si Fred dit que la dictee ecrit mal : je ne devine pas la cause, je lui demande UN exemple exact (ce qu'il "
                  "a dit / ce qui s'est ecrit) et je lui dis si la Correction Gemini est sur oui ou non."
                  % (VERSION, DICTEE_MODELE, "OUI" if payant else "NON (seulement Chrome)")),
        "moi": ("Qui je suis aujourd'hui : la nouvelle Luciana, et ce qui n'existe pas",
                "Verite ecrite par le programme. Je suis la nouvelle Luciana (%s), sur le PC de Fred : l'ecran et les "
                "outils de la V198, avec un coeur neuf (une seule bibliotheque dans ~/Luciana_neuve ; a chaque message mon "
                "bibliothecaire lit les fiches proches et relit ma reponse avec toutes les regles de Fred ; j'apprends apres "
                "chaque echange). LUMINITA est un AUTRE programme : le produit que Fred vend a ses clientes, sur leurs PC ; "
                "je ne suis pas Luminita. LUMINITO N'EXISTE PAS : c'est seulement une idee de Fred (un personnage de petit "
                "mecano), rien n'est fabrique. Quand Fred me parle de « mon » dictaphone, de « ma » page, de « mes » "
                "reglages, il parle de MOI, Luciana, sauf s'il nomme Luminita." % VERSION),
    }


def poser_mes_verites():
    """Ecrit (ou remplace) les fiches « verite du programme ». L'ancienne version est marquee, jamais effacee."""
    try:
        import hashlib
        toutes = coeur.fiches(toutes=True)
        n = 0
        for cle, (sujet, texte) in verites_du_programme().items():
            source = "verite_du_programme:%s:%s" % (cle, hashlib.sha1(texte.encode("utf-8")).hexdigest()[:12])
            if any(f.get("source") == source and f.get("etat", "active") == "active" for f in toutes):
                continue
            for f in toutes:
                if str(f.get("source", "")).startswith("verite_du_programme:%s:" % cle) and f.get("etat", "active") == "active":
                    coeur.ajouter_ligne(coeur.F_FICHES, dict(f, etat="remplacee", remplacee_le=coeur.maintenant()))
            coeur._FICHES["liste"] = None
            coeur.ecrire_fiche("capacite", sujet, texte, source=source)
            n += 1
        if n:
            coeur._FICHES["liste"] = None
            coeur.ecrire_lisible()
        return n
    except Exception as ex:
        print("  ATTENTION : ses fiches « verite du programme » n'ont pas pu etre ecrites (%s)." % str(ex)[:200])
        return 0


def preparer_en_fond():
    """Les empreintes de sens de la bibliotheque (une seule fois par fiche) et celles des outils."""
    poser_mes_verites()
    try:
        coeur.MOTEUR.indexer(coeur.fiches())
        coeur.proposer_outils("demarrage", L.lire_cerveau(), 1)
    except Exception:
        pass
    try:
        if not coeur.reglages().get("bibliotheque_rangee"):
            raise StopIteration                          # eteint tant que les pieces 3 a 6 ne sont pas faites
        st = coeur.classement.ranger_le_neuf()          # l'archiviste range ce qui est neuf (piece 2)
        if st.get("rangees") or st.get("divisions"):
            print("  Mon plan : %d fiche(s) rangee(s), %d tiroir(s) divise(s)." % (st["rangees"], st["divisions"]))
    except Exception:
        pass
    print("  Moteur de sens (Google) : %s" % ("pret" if not coeur.MOTEUR.panne
                                              else "EN PANNE -> recherche par les mots (%s)" % coeur.MOTEUR.panne))


def main():
    sauvegarde_du_jour()
    from http.server import ThreadingHTTPServer
    for boucle in (L._boucle_sauvegarde_auto, L._boucle_veilleur, L._boucle_suivi_correspondance,
                   L._boucle_veilleur_travaux, coeur.boucle_horloge, preparer_en_fond, coeur.ranger_si_besoin):
        threading.Thread(target=boucle, daemon=True).start()
    try:
        srv = ThreadingHTTPServer(("0.0.0.0", PORT), Handler)
    except OSError as ex:
        print("  Impossible d'ouvrir le port %d (%s). Ferme l'autre Luciana et relance." % (PORT, ex))
        return
    srv.daemon_threads = True
    L._PORT_ACTUEL[0] = PORT
    nb = len(coeur.fiches())
    print("\n  LA NOUVELLE LUCIANA (%s) est reveillee.  <3" % VERSION)
    print("  Sur ce PC : http://127.0.0.1:%d" % PORT)
    ip = L._ip_locale()
    if ip:
        print("  Sur ton telephone (meme WiFi ou Tailscale) : http://%s:%d" % (ip, PORT))
    print("  Sa memoire : %s (%d fiche(s) dans sa bibliotheque)" % (coeur.DOSSIER, nb))
    print("  Ses outils : %d (tous ceux de la V198, sauf son ancienne memoire)" % len(coeur.catalogue(L.lire_cerveau())))
    print("  Cerveau : %s" % L._info_cerveau(L.lire_cerveau()).get("libelle"))
    print("")
    print("  +---------------------------------------------------------+")
    print("  |  CODE D'ACCES pour le telephone : %-6s                |" % L.CODE_ACCES)
    print("  |  (a taper une seule fois sur le tel ; le PC n'en a pas  |")
    print("  |   besoin. Personne ne peut me commander sans ce code.)  |")
    print("  +---------------------------------------------------------+")
    print("")
    print("  (Sur le PC, utilise Google Chrome pour que le micro marche.)")
    print("  Pour l'arreter : ferme cette fenetre.\n")
    threading.Timer(1.0, lambda: __import__("webbrowser").open("http://127.0.0.1:%d" % PORT)).start()
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
