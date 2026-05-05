import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="¿Quién quiere ser millonario? | Riesgo psicosocial",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Oculta elementos visuales propios de Streamlit para que el juego se vea como app completa.
st.markdown("""
<style>
[data-testid="stHeader"] { display: none; }
[data-testid="stToolbar"] { display: none; }
[data-testid="stDecoration"] { display: none; }
.block-container {
    padding: 0 !important;
    max-width: 100% !important;
}
html, body, [data-testid="stAppViewContainer"] {
    background: #07102c;
}
iframe {
    display: block;
}
</style>
""", unsafe_allow_html=True)

GAME_HTML = r"""<meta charset="UTF-8" />
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }

  :root{
    --bg-1:#07102c;
    --bg-2:#101f58;
    --card:#0e1a46cc;
    --card-2:#13255fcc;
    --gold:#f3c64f;
    --gold-2:#ffdf86;
    --text:#f8fbff;
    --muted:rgba(255,255,255,.62);
    --soft:rgba(255,255,255,.12);
    --soft-2:rgba(255,255,255,.08);
    --ok:#33c56b;
    --bad:#ef5c5c;
    --blue:#66a6ff;
    --shadow:0 24px 80px rgba(0,0,0,.45);
    --radius:22px;
    --font-sans: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  }

  body{
    background:
      radial-gradient(circle at 15% 20%, rgba(243,198,79,.12), transparent 20%),
      radial-gradient(circle at 85% 15%, rgba(102,166,255,.14), transparent 22%),
      radial-gradient(circle at 50% 80%, rgba(255,255,255,.05), transparent 25%),
      linear-gradient(135deg, var(--bg-1), var(--bg-2));
    font-family: var(--font-sans);
    color: var(--text);
    min-height: 100vh;
    padding: 24px;
  }

  #root{
    max-width: 1180px;
    margin: 0 auto;
    min-height: 720px;
    border-radius: 28px;
    overflow: hidden;
    border: 1px solid rgba(255,255,255,.08);
    background:
      linear-gradient(180deg, rgba(255,255,255,.05), rgba(255,255,255,.02)),
      rgba(8, 14, 40, 0.75);
    backdrop-filter: blur(12px);
    box-shadow: var(--shadow);
    position: relative;
  }

  #root::before{
    content:"";
    position:absolute;
    inset:0;
    pointer-events:none;
    background:
      radial-gradient(circle at top left, rgba(255,255,255,.06), transparent 24%),
      radial-gradient(circle at bottom right, rgba(243,198,79,.08), transparent 24%);
  }

  .screen{
    display:none;
    min-height: 720px;
    animation: fade .35s ease;
  }
  .screen.on{ display:flex; }

  @keyframes fade{
    from{ opacity:0; transform:translateY(10px); }
    to{ opacity:1; transform:translateY(0); }
  }

  #s-intro{
    flex-direction:column;
    align-items:center;
    justify-content:center;
    text-align:center;
    gap:18px;
    padding:40px 28px;
    position:relative;
  }

  .intro-badge{
    width:136px;height:136px;border-radius:50%;
    display:flex;align-items:center;justify-content:center;
    background: radial-gradient(circle at 30% 30%, rgba(255,223,134,.22), rgba(243,198,79,.05));
    border:2px solid rgba(243,198,79,.55);
    box-shadow:
      0 0 0 10px rgba(243,198,79,.06),
      0 0 40px rgba(243,198,79,.15);
  }

  .intro-kicker{
    font-size:12px;
    letter-spacing:2px;
    text-transform:uppercase;
    color:var(--gold-2);
    opacity:.9;
  }

  .intro-title{
    font-size: clamp(30px, 5vw, 52px);
    font-weight: 800;
    line-height: 1.05;
    max-width: 760px;
  }

  .intro-title span{
    display:block;
    color:var(--gold);
    font-size: clamp(18px, 2.8vw, 28px);
    font-weight:600;
    margin-top:10px;
  }

  .intro-sub{
    max-width:760px;
    font-size:15px;
    line-height:1.8;
    color:var(--muted);
  }

  .intro-pills{
    display:flex;
    flex-wrap:wrap;
    justify-content:center;
    gap:10px;
    max-width:800px;
    margin-top:8px;
  }

  .pill{
    padding:9px 14px;
    border-radius:999px;
    border:1px solid rgba(243,198,79,.28);
    background: rgba(243,198,79,.08);
    color: var(--gold-2);
    font-size:13px;
  }

  .prize-preview{
    display:grid;
    grid-template-columns: repeat(5, minmax(90px, 1fr));
    gap:10px;
    width:100%;
    max-width:820px;
    margin-top:10px;
  }

  .pp{
    font-size:12px;
    padding:10px 12px;
    border-radius:14px;
    border:1px solid rgba(255,255,255,.1);
    background: rgba(255,255,255,.05);
    color: rgba(255,255,255,.85);
  }

  .btn-main{
    border:none;
    cursor:pointer;
    border-radius:999px;
    padding:15px 28px;
    font-size:15px;
    font-weight:700;
    transition:.18s ease;
  }

  .btn-main:hover{ transform:translateY(-2px) scale(1.02); }

  .btn-gold{
    background: linear-gradient(180deg, #ffdf86, #f3c64f);
    color:#111a3c;
    box-shadow: 0 12px 30px rgba(243,198,79,.22);
  }

  #s-game{
    display:none;
    padding:28px;
  }
  #s-game.on{
    display:grid;
    grid-template-columns: 1.8fr .95fr;
    gap:22px;
  }

  .game-main,
  .game-side{
    border-radius:24px;
    border:1px solid rgba(255,255,255,.08);
    background: linear-gradient(180deg, rgba(255,255,255,.06), rgba(255,255,255,.03));
    backdrop-filter: blur(10px);
  }

  .game-main{
    padding:22px;
    display:flex;
    flex-direction:column;
    gap:16px;
  }

  .game-side{ padding:18px; }

  .top-head{
    display:flex;
    align-items:center;
    justify-content:space-between;
    gap:12px;
    flex-wrap:wrap;
  }

  .logo-line{ display:flex; flex-direction:column; gap:6px; }

  .small-kicker{
    font-size:11px;
    letter-spacing:1.5px;
    text-transform:uppercase;
    color:rgba(255,255,255,.55);
  }

  .game-title{ font-size:22px; font-weight:800; }

  .head-badges{ display:flex; gap:10px; flex-wrap:wrap; }

  .badge{
    padding:10px 14px;
    border-radius:999px;
    background: rgba(255,255,255,.07);
    border:1px solid rgba(255,255,255,.1);
    font-size:13px;
    color:#fff;
  }

  .badge.gold{
    background: rgba(243,198,79,.12);
    border-color: rgba(243,198,79,.35);
    color: var(--gold-2);
    font-weight:700;
  }

  .progress-wrap{
    display:flex;
    flex-direction:column;
    gap:10px;
    margin-top:4px;
  }

  .progress-top{
    display:flex;
    justify-content:space-between;
    gap:10px;
    align-items:center;
    flex-wrap:wrap;
  }

  .q-label{ font-size:13px; color:rgba(255,255,255,.66); }

  .dim-chip{
    display:inline-flex;
    align-items:center;
    gap:8px;
    padding:8px 12px;
    border-radius:999px;
    background: rgba(102,166,255,.12);
    border:1px solid rgba(102,166,255,.3);
    color:#cde1ff;
    font-size:12px;
  }

  .progress-row{
    display:grid;
    grid-template-columns: repeat(10, 1fr);
    gap:6px;
  }

  .prog-seg{
    height:8px;
    border-radius:999px;
    background:rgba(255,255,255,.1);
    transition:.25s;
  }
  .prog-seg.done{
    background:linear-gradient(90deg, #f3c64f, #ffdf86);
    box-shadow:0 0 12px rgba(243,198,79,.25);
  }
  .prog-seg.cur{
    background:linear-gradient(90deg, rgba(243,198,79,.5), rgba(255,223,134,.95));
  }

  .prize-now{
    text-align:center;
    padding:14px 18px;
    border-radius:18px;
    background: linear-gradient(180deg, rgba(243,198,79,.13), rgba(243,198,79,.06));
    border:1px solid rgba(243,198,79,.28);
  }
  .prize-now .label{
    font-size:12px;
    color:rgba(255,255,255,.6);
    margin-bottom:4px;
  }
  .prize-now .value{
    font-size:32px;
    font-weight:900;
    color:var(--gold-2);
    letter-spacing:.5px;
  }

  .q-box{
    position:relative;
    padding:24px 22px;
    border-radius:20px;
    background:
      radial-gradient(circle at top center, rgba(243,198,79,.08), transparent 40%),
      rgba(255,255,255,.05);
    border:1px solid rgba(255,255,255,.08);
    font-size:20px;
    line-height:1.6;
    text-align:center;
    min-height:130px;
    display:flex;
    align-items:center;
    justify-content:center;
    font-weight:600;
  }

  .opts{
    display:grid;
    grid-template-columns: 1fr 1fr;
    gap:12px;
  }

  .opt{
    width:100%;
    display:flex;
    align-items:flex-start;
    gap:12px;
    padding:16px;
    border-radius:18px;
    border:1px solid rgba(255,255,255,.12);
    background: rgba(255,255,255,.05);
    color:#fff;
    text-align:left;
    cursor:pointer;
    transition:.18s ease;
    min-height:84px;
    font-size:14px;
  }

  .opt:hover:not(:disabled){
    transform:translateY(-2px);
    background: rgba(243,198,79,.09);
    border-color: rgba(243,198,79,.38);
    box-shadow:0 10px 20px rgba(0,0,0,.18);
  }

  .opt:disabled{ cursor:default; }

  .ltr{
    width:34px;
    height:34px;
    border-radius:50%;
    display:flex;
    align-items:center;
    justify-content:center;
    flex-shrink:0;
    font-size:13px;
    font-weight:800;
    color:#0a153d;
    background:linear-gradient(180deg, #ffdf86, #f3c64f);
    box-shadow:0 6px 16px rgba(243,198,79,.18);
  }

  .opt.sel{
    border-color:rgba(102,166,255,.8);
    background:rgba(102,166,255,.14);
    box-shadow:0 0 0 2px rgba(102,166,255,.18);
  }
  .opt.ok{
    border-color:rgba(51,197,107,.8);
    background:rgba(51,197,107,.16);
    color:#d8ffe7;
  }
  .opt.no{
    border-color:rgba(239,92,92,.85);
    background:rgba(239,92,92,.16);
    color:#ffe0e0;
  }
  .opt.gone{ visibility:hidden; }

  .feedback-box{
    display:none;
    border-radius:18px;
    padding:15px 16px;
    font-size:14px;
    line-height:1.7;
    border:1px solid rgba(255,255,255,.12);
    background:rgba(255,255,255,.05);
  }
  .feedback-box.show{ display:block; }
  .fb-ok{
    border-color: rgba(51,197,107,.5);
    color:#c7ffdb;
    background: rgba(51,197,107,.12);
  }
  .fb-no{
    border-color: rgba(239,92,92,.5);
    color:#ffd7d7;
    background: rgba(239,92,92,.10);
  }

  .utility-block{
    display:grid;
    grid-template-columns: 1fr;
    gap:14px;
  }

  .lifelines{
    display:grid;
    grid-template-columns: repeat(3, 1fr);
    gap:10px;
  }

  .ll{
    border:none;
    cursor:pointer;
    display:flex;
    flex-direction:column;
    align-items:center;
    justify-content:center;
    gap:5px;
    min-height:78px;
    border-radius:18px;
    background: rgba(255,255,255,.06);
    border:1px solid rgba(255,255,255,.12);
    color:white;
    transition:.18s ease;
    font-size:12px;
    font-weight:600;
  }

  .ll:hover:not(.used){
    transform:translateY(-2px);
    background: rgba(243,198,79,.10);
    border-color: rgba(243,198,79,.45);
  }

  .ll.used{
    opacity:.35;
    filter:grayscale(1);
    cursor:default;
  }

  .ll-icon{ font-size:24px; line-height:1; }

  .aud-wrap,
  .phone-box{
    width:100%;
    display:none;
    border-radius:18px;
    background: rgba(255,255,255,.05);
    border:1px solid rgba(255,255,255,.1);
    padding:16px;
  }

  .aud-title{
    text-align:center;
    font-size:13px;
    color:rgba(255,255,255,.7);
    margin-bottom:10px;
    font-weight:700;
  }

  .aud-bars{
    display:flex;
    align-items:flex-end;
    justify-content:center;
    gap:14px;
    min-height:120px;
  }

  .aud-col{
    display:flex;
    flex-direction:column;
    align-items:center;
    gap:6px;
    min-width:56px;
  }

  .aud-bar{
    width:48px;
    border-radius:10px 10px 4px 4px;
    min-height:6px;
    transition:height .45s ease;
    box-shadow:0 8px 18px rgba(0,0,0,.18);
  }

  .aud-p, .aud-l{ font-size:12px; color:rgba(255,255,255,.7); }

  .phone-box{
    font-size:14px;
    line-height:1.75;
    color:rgba(255,255,255,.9);
  }

  .action-row{
    display:flex;
    gap:10px;
    justify-content:center;
    flex-wrap:wrap;
  }

  .btn-confirm,
  .btn-next,
  .btn-walk{ display:none; }

  .btn-confirm.show,
  .btn-next.show,
  .btn-walk.show{ display:inline-flex; }

  .btn-confirm,
  .btn-next,
  .btn-walk{
    border:none;
    padding:13px 20px;
    border-radius:999px;
    font-size:14px;
    font-weight:700;
    cursor:pointer;
    transition:.18s ease;
  }

  .btn-confirm{
    background:linear-gradient(180deg, #ffdf86, #f3c64f);
    color:#10183a;
  }

  .btn-next{
    background:rgba(255,255,255,.08);
    color:#fff;
    border:1px solid rgba(255,255,255,.12);
  }

  .btn-walk{
    background:transparent;
    color:rgba(255,255,255,.7);
    border:1px solid rgba(255,255,255,.18);
  }

  .btn-confirm:hover,
  .btn-next:hover,
  .btn-walk:hover{ transform:translateY(-2px); }

  .side-title{
    font-size:14px;
    letter-spacing:1.4px;
    text-transform:uppercase;
    color:rgba(255,255,255,.6);
    margin-bottom:14px;
  }

  .prize-ladder{
    display:flex;
    flex-direction:column-reverse;
    gap:8px;
  }

  .ladder-item{
    display:flex;
    align-items:center;
    justify-content:space-between;
    gap:10px;
    padding:12px 14px;
    border-radius:14px;
    background: rgba(255,255,255,.04);
    border:1px solid rgba(255,255,255,.08);
    transition:.18s ease;
  }

  .ladder-item .num{
    font-size:12px;
    color:rgba(255,255,255,.55);
    min-width:28px;
  }

  .ladder-item .money{ font-size:14px; font-weight:700; }

  .ladder-item.active{
    background: rgba(243,198,79,.14);
    border-color: rgba(243,198,79,.4);
    box-shadow:0 0 0 1px rgba(243,198,79,.18);
  }

  .ladder-item.active .money{ color:var(--gold-2); }

  .ladder-item.done{
    background: rgba(51,197,107,.10);
    border-color: rgba(51,197,107,.26);
  }

  .side-mini{
    margin-top:18px;
    display:grid;
    grid-template-columns:1fr;
    gap:10px;
  }

  .mini-card{
    border-radius:16px;
    padding:14px;
    background: rgba(255,255,255,.04);
    border:1px solid rgba(255,255,255,.08);
  }

  .mini-k{
    font-size:11px;
    text-transform:uppercase;
    color:rgba(255,255,255,.48);
    letter-spacing:1.2px;
    margin-bottom:6px;
  }

  .mini-v{ font-size:18px; font-weight:800; }

  #s-result{
    flex-direction:column;
    align-items:center;
    justify-content:center;
    text-align:center;
    gap:16px;
    padding:36px 24px;
  }

  .res-icon{
    font-size:72px;
    line-height:1;
    filter: drop-shadow(0 10px 20px rgba(243,198,79,.18));
  }

  .res-title{
    font-size:38px;
    font-weight:900;
    color:var(--gold-2);
  }

  .res-amount{
    font-size:48px;
    font-weight:900;
    letter-spacing:.5px;
  }

  .res-sub{
    max-width:660px;
    font-size:15px;
    line-height:1.8;
    color:var(--muted);
  }

  .stat-row{
    display:grid;
    grid-template-columns: repeat(3, minmax(160px, 1fr));
    gap:12px;
    width:100%;
    max-width:720px;
    margin-top:6px;
  }

  .stat{
    border-radius:18px;
    padding:18px;
    background: rgba(255,255,255,.05);
    border:1px solid rgba(255,255,255,.1);
  }

  .stat-n{
    font-size:28px;
    font-weight:900;
    color:var(--gold-2);
  }

  .stat-l{
    font-size:12px;
    color:rgba(255,255,255,.55);
    margin-top:4px;
    text-transform:uppercase;
    letter-spacing:1px;
  }

  .medal-list{
    display:flex;
    flex-direction:column;
    gap:8px;
    max-width:700px;
    width:100%;
    text-align:left;
    margin-top:6px;
  }

  .medal-list div{
    padding:12px 14px;
    border-radius:14px;
    background: rgba(255,255,255,.05);
    border:1px solid rgba(255,255,255,.08);
    color:rgba(255,255,255,.9);
  }

  @media (max-width: 940px){
    #s-game.on{ grid-template-columns:1fr; }
    .opts{ grid-template-columns:1fr; }
    .prize-preview{ grid-template-columns: repeat(2, 1fr); }
    .stat-row{ grid-template-columns:1fr; }
    .lifelines{ grid-template-columns:1fr; }
  }
</style>

<div id="root">
  <div id="s-intro" class="screen on">
    <div class="intro-badge">
      <svg width="76" height="76" viewBox="0 0 60 60" fill="none" xmlns="http://www.w3.org/2000/svg">
        <circle cx="30" cy="30" r="27" stroke="#f3c64f" stroke-width="2.5"/>
        <text x="30" y="41" text-anchor="middle" font-size="28" fill="#f3c64f" font-weight="bold">?</text>
      </svg>
    </div>

    <div class="intro-kicker">Juego interactivo</div>
    <div class="intro-title">
      ¿Quién quiere ser millonario?
      <span>Factores de riesgo psicosocial</span>
    </div>

    <div class="intro-sub">
      Pon a prueba tus conocimientos sobre las demandas del trabajo en la batería de evaluación de riesgo psicosocial. 
      Avanza de nivel, usa tus comodines con estrategia y llega hasta el gran premio.
    </div>

    <div class="intro-pills">
      <div class="pill">10 preguntas</div>
      <div class="pill">Dificultad progresiva</div>
      <div class="pill">3 comodines</div>
      <div class="pill">Retroalimentación inmediata</div>
    </div>

    <div class="prize-preview" id="prize-preview"></div>

    <button class="btn-main btn-gold" onclick="startGame()">🎯 Quiero jugar</button>
  </div>

  <div id="s-game" class="screen">
    <div class="game-main">
      <div class="top-head">
        <div class="logo-line">
          <div class="small-kicker">Modo concurso</div>
          <div class="game-title">Reto de riesgo psicosocial</div>
        </div>
        <div class="head-badges">
          <div class="badge" id="score-badge">$0</div>
          <div class="badge gold" id="current-prize-badge">Premio: $100</div>
        </div>
      </div>

      <div class="progress-wrap">
        <div class="progress-top">
          <div class="q-label" id="q-label">Pregunta 1 de 10</div>
          <div class="dim-chip" id="dim-chip">Concepto base</div>
        </div>
        <div class="progress-row" id="progress-row"></div>
      </div>

      <div class="prize-now">
        <div class="label">Premio actual</div>
        <div class="value" id="prize-now">$100</div>
      </div>

      <div class="q-box" id="q-box">Cargando...</div>
      <div class="opts" id="opts"></div>
      <div class="feedback-box" id="feedback-box"></div>

      <div class="utility-block">
        <div class="lifelines">
          <button class="ll" id="ll-5050" onclick="do5050()"><span class="ll-icon">½</span><span>50/50</span></button>
          <button class="ll" id="ll-pub" onclick="doPublic()"><span class="ll-icon">👥</span><span>Público</span></button>
          <button class="ll" id="ll-tel" onclick="doPhone()"><span class="ll-icon">📞</span><span>Teléfono</span></button>
        </div>
        <div class="aud-wrap" id="aud-wrap">
          <div class="aud-title">Voto del público</div>
          <div class="aud-bars" id="aud-bars"></div>
        </div>
        <div class="phone-box" id="phone-box"></div>
      </div>

      <div class="action-row">
        <button class="btn-walk" id="btn-walk" onclick="walkAway()">Retirarme</button>
        <button class="btn-confirm" id="btn-confirm" onclick="confirmAns()">Confirmar respuesta</button>
        <button class="btn-next" id="btn-next" onclick="nextQ()">Siguiente pregunta →</button>
      </div>
    </div>

    <div class="game-side">
      <div class="side-title">Escalera de premios</div>
      <div class="prize-ladder" id="prize-ladder"></div>
      <div class="side-mini">
        <div class="mini-card"><div class="mini-k">Respuestas correctas</div><div class="mini-v" id="mini-correct">0 / 10</div></div>
        <div class="mini-card"><div class="mini-k">Comodines usados</div><div class="mini-v" id="mini-ll">0 / 3</div></div>
        <div class="mini-card"><div class="mini-k">Piso seguro</div><div class="mini-v" id="mini-safe">Ninguno</div></div>
      </div>
    </div>
  </div>

  <div id="s-result" class="screen">
    <div class="res-icon" id="res-icon">🏆</div>
    <div class="res-title" id="res-title">¡Experto!</div>
    <div class="res-amount" id="res-amount">$1.000.000</div>
    <div class="res-sub" id="res-sub">Completaste el reto con éxito.</div>

    <div class="stat-row">
      <div class="stat"><div class="stat-n" id="stat-correct">0</div><div class="stat-l">Correctas</div></div>
      <div class="stat"><div class="stat-n" id="stat-score">$0</div><div class="stat-l">Premio</div></div>
      <div class="stat"><div class="stat-n" id="stat-ll">0</div><div class="stat-l">Comodines usados</div></div>
    </div>

    <div class="medal-list" id="medal-list"></div>
    <button class="btn-main btn-gold" onclick="restart()">🔁 Jugar de nuevo</button>
  </div>
</div>

<script>
  var QS = [
    {q:"¿Qué son las condiciones intralaborales?",opts:["Factores personales del trabajador","Características del trabajo que afectan la salud","Actividades realizadas fuera del trabajo","Normas legales del sistema laboral"],cor:1,dim:"Concepto base",prize:"$100",fb_ok:"¡Exacto! Las condiciones intralaborales son las características propias del trabajo y del entorno laboral que influyen directamente en la salud y el bienestar del trabajador.",fb_no:"Incorrecto. Las condiciones intralaborales son características del trabajo que pueden afectar la salud. No son factores personales ni actividades externas."},
    {q:"¿Qué son las demandas del trabajo según la batería de riesgo psicosocial?",opts:["Beneficios y compensaciones laborales","Exigencias del trabajo hacia el individuo","El tiempo libre disponible para el empleado","Las relaciones sociales dentro de la empresa"],cor:1,dim:"Demandas del trabajo",prize:"$200",fb_ok:"¡Perfecto! Las demandas del trabajo son todas las exigencias que el trabajo impone al trabajador en términos de esfuerzo, dedicación, habilidades y recursos.",fb_no:"Incorrecto. Las demandas del trabajo son las exigencias que impone el trabajo sobre el individuo, no sus beneficios ni su tiempo libre."},
    {q:"¿Cuándo se convierte en riesgo una demanda cuantitativa?",opts:["Cuando hay poca cantidad de trabajo asignado","Cuando el tiempo disponible es insuficiente para la carga de trabajo","Cuando se incluyen pausas activas en la jornada","Cuando el trabajo asignado es sencillo de realizar"],cor:1,dim:"Demandas cuantitativas",prize:"$500",fb_ok:"¡Correcto! La demanda cuantitativa se convierte en factor de riesgo cuando el volumen de trabajo supera el tiempo disponible, generando sobrecarga.",fb_no:"Incorrecto. Es un riesgo cuando el tiempo es insuficiente para la cantidad de trabajo asignada. Eso crea sobrecarga cuantitativa."},
    {q:"¿Qué tipo de procesos evalúan las demandas de carga mental?",opts:["La fuerza y resistencia física del trabajador","Procesos cognitivos como atención, memoria y análisis","Las relaciones sociales en el entorno laboral","Las condiciones ambientales del puesto de trabajo"],cor:1,dim:"Carga mental",prize:"$1.000",fb_ok:"¡Excelente! La carga mental evalúa los procesos cognitivos: concentración, atención sostenida, memoria, análisis y toma de decisiones que exige el trabajo.",fb_no:"Incorrecto. La carga mental se refiere a procesos cognitivos, no a la fuerza física ni al ambiente."},
    {q:"¿Cuál de los siguientes es un ejemplo claro de demanda emocional en el trabajo?",opts:["Levantar objetos pesados durante el turno","Revisar y corregir informes estadísticos","Atender pacientes en situaciones de crisis o sufrimiento","Trabajar a alta velocidad en una línea de producción"],cor:2,dim:"Demandas emocionales",prize:"$2.000",fb_ok:"¡Muy bien! Atender personas en crisis exige controlar las propias emociones y las ajenas. Eso es una demanda emocional intensa.",fb_no:"Incorrecto. La demanda emocional surge cuando el trabajo exige manejar emociones propias o ajenas, especialmente en situaciones difíciles como la atención de personas en crisis."},
    {q:"¿Qué implica la responsabilidad del cargo como dimensión de riesgo psicosocial?",opts:["Delegar todas las tareas a subordinados","No asumir las consecuencias de los propios errores","Asumir consecuencias importantes derivadas del trabajo propio","Trabajar el menor tiempo posible para evitar errores"],cor:2,dim:"Responsabilidad del cargo",prize:"$5.000",fb_ok:"¡Correcto! La responsabilidad del cargo implica asumir consecuencias significativas por las decisiones y resultados del propio trabajo.",fb_no:"Incorrecto. La responsabilidad del cargo significa asumir consecuencias importantes."},
    {q:"¿Qué factor pertenece a la dimensión de demandas ambientales y de esfuerzo físico?",opts:["El estrés emocional derivado de la atención al público","Ruido excesivo, temperatura extrema y condiciones físicas del entorno","La cantidad y velocidad de trabajo requerida","Los horarios rotativos y turnos nocturnos"],cor:1,dim:"Demandas ambientales",prize:"$10.000",fb_ok:"¡Exacto! Las demandas ambientales incluyen condiciones físicas del entorno: ruido, temperatura, iluminación, vibraciones y el esfuerzo físico requerido por el cargo.",fb_no:"Incorrecto. Las demandas ambientales son condiciones físicas del entorno."},
    {q:"¿En qué situación la jornada de trabajo se considera un factor de riesgo psicosocial?",opts:["Cuando el trabajador tiene descansos regulares y programados","Cuando se presentan jornadas largas sin pausas ni recuperación adecuada","Cuando existe flexibilidad horaria acordada con el trabajador","Cuando el ambiente de trabajo es positivo y colaborativo"],cor:1,dim:"Jornada de trabajo",prize:"$25.000",fb_ok:"¡Correcto! Las jornadas extensas sin descanso adecuado impiden la recuperación del trabajador y se convierten en riesgo.",fb_no:"Incorrecto. La jornada es un riesgo cuando es larga y sin pausas. La flexibilidad y los descansos son factores protectores."},
    {q:"¿Qué describe correctamente el concepto de consistencia de rol en la batería psicosocial?",opts:["Recibir un salario justo y consistente con el cargo","La compatibilidad y coherencia entre las distintas exigencias del cargo","La cantidad total de tareas asignadas al trabajador","El tiempo libre disponible para actividades personales"],cor:1,dim:"Consistencia de rol",prize:"$50.000",fb_ok:"¡Excelente! La consistencia de rol es la coherencia entre las exigencias del trabajo. Cuando hay contradicciones, se generan conflictos de rol.",fb_no:"Incorrecto. La consistencia de rol es sobre la coherencia entre exigencias del cargo."},
    {q:"¿Cuál es la conclusión más precisa sobre las demandas del trabajo según la batería de riesgo psicosocial?",opts:["Las demandas del trabajo no tienen impacto real en la salud del trabajador","Las demandas del trabajo deben eliminarse por completo del entorno laboral","Son aspectos necesarios del trabajo pero pueden generar riesgo si no se gestionan adecuadamente","Las demandas del trabajo solo generan consecuencias para la productividad de la empresa"],cor:2,dim:"Conclusión integral",prize:"$1.000.000",fb_ok:"¡Respuesta experta! Las demandas son inherentes a cualquier actividad laboral. El riesgo surge cuando superan la capacidad de respuesta del trabajador y no se gestionan bien.",fb_no:"Incorrecto. Las demandas son necesarias para el trabajo, pero se convierten en riesgo si se gestionan mal o superan la capacidad del trabajador."}
  ];

  var MILESTONES = [4, 8];
  var BAR_COLS = ["#f3c64f","#66a6ff","#ff9d6c","#48d29a"];
  var NAMES = ["Dra. Gómez","Prof. Martínez","Ing. Herrera","Lic. Morales","Dr. Castillo"];
  var cQ = 0, selOpt = null, score = 0, correctCount = 0;
  var llUsed = {f5050:false, pub:false, tel:false}, llCount = 0;
  var hidden = [], answered = false;

  function show(id){ document.querySelectorAll(".screen").forEach(function(s){ s.classList.remove("on"); }); document.getElementById(id).classList.add("on"); }
  function moneyToNumber(str){ return parseInt(str.replace(/\D/g,""), 10) || 0; }
  function formatMoney(n){ return "$" + n.toLocaleString("es-CO"); }

  function buildPreview(){ var c=document.getElementById("prize-preview"); c.innerHTML=""; QS.forEach(function(q,i){ var d=document.createElement("div"); d.className="pp"; d.textContent="P"+(i+1)+" · "+q.prize; c.appendChild(d); }); }
  function buildProgress(){ var r=document.getElementById("progress-row"); r.innerHTML=""; QS.forEach(function(_,i){ var d=document.createElement("div"); d.className="prog-seg"+(i===cQ?" cur":""); d.id="ps-"+i; r.appendChild(d); }); }
  function updateProgress(){ QS.forEach(function(_,i){ var el=document.getElementById("ps-"+i); if(!el)return; el.className="prog-seg"+(i<cQ?" done":i===cQ?" cur":""); }); }
  function buildLadder(){ var c=document.getElementById("prize-ladder"); c.innerHTML=""; QS.forEach(function(q,i){ var item=document.createElement("div"); item.className="ladder-item"; item.id="ladder-"+i; item.innerHTML='<div class="num">P'+(i+1)+'</div><div class="money">'+q.prize+'</div>'; c.appendChild(item); }); updateLadder(); }
  function updateLadder(){ QS.forEach(function(_,i){ var el=document.getElementById("ladder-"+i); if(!el)return; el.className="ladder-item"+(i<cQ?" done":"")+(i===cQ?" active":""); }); }
  function getSafe(){ var s=""; MILESTONES.forEach(function(m){ if(cQ>m)s=QS[m].prize; }); return s; }
  function updateMiniStats(){ document.getElementById("mini-correct").textContent=correctCount+" / "+QS.length; document.getElementById("mini-ll").textContent=llCount+" / 3"; document.getElementById("mini-safe").textContent=getSafe()||"Ninguno"; }

  function startGame(){
    cQ=0; selOpt=null; score=0; correctCount=0; llUsed={f5050:false,pub:false,tel:false}; llCount=0; hidden=[]; answered=false;
    ["ll-5050","ll-pub","ll-tel"].forEach(function(id){ document.getElementById(id).classList.remove("used"); });
    buildProgress(); buildLadder(); updateMiniStats(); renderQ(); show("s-game");
  }

  function renderQ(){
    var q=QS[cQ]; hidden=[]; answered=false; selOpt=null;
    document.getElementById("q-label").textContent="Pregunta "+(cQ+1)+" de "+QS.length;
    document.getElementById("dim-chip").textContent=q.dim;
    document.getElementById("prize-now").textContent=q.prize;
    document.getElementById("current-prize-badge").textContent="Premio: "+q.prize;
    document.getElementById("score-badge").textContent=formatMoney(score);
    document.getElementById("q-box").textContent=q.q;
    document.getElementById("feedback-box").className="feedback-box";
    document.getElementById("feedback-box").textContent="";
    document.getElementById("aud-wrap").style.display="none";
    document.getElementById("phone-box").style.display="none";
    document.getElementById("btn-confirm").classList.remove("show");
    document.getElementById("btn-next").classList.remove("show");
    document.getElementById("btn-walk").classList.remove("show");
    updateProgress(); updateLadder(); updateMiniStats();

    var area=document.getElementById("opts"); area.innerHTML="";
    var letters=["A","B","C","D"];
    q.opts.forEach(function(o,i){
      var btn=document.createElement("button"); btn.className="opt"; btn.id="opt-"+i;
      var ltr=document.createElement("div"); ltr.className="ltr"; ltr.textContent=letters[i];
      var sp=document.createElement("span"); sp.textContent=o;
      btn.appendChild(ltr); btn.appendChild(sp);
      btn.onclick=(function(idx){ return function(){ selectOpt(idx); }; })(i);
      area.appendChild(btn);
    });
  }

  function selectOpt(i){
    if(answered)return;
    var btn=document.getElementById("opt-"+i);
    if(btn.classList.contains("gone"))return;
    document.querySelectorAll(".opt").forEach(function(b){ b.classList.remove("sel"); });
    btn.classList.add("sel"); selOpt=i;
    document.getElementById("btn-confirm").classList.add("show");
    document.getElementById("btn-walk").classList.add("show");
  }

  function confirmAns(){
    if(selOpt===null||answered)return;
    answered=true;
    var q=QS[cQ]; var isOk=selOpt===q.cor;
    document.querySelectorAll(".opt").forEach(function(b){ b.disabled=true; });
    document.getElementById("btn-confirm").classList.remove("show");
    document.getElementById("btn-walk").classList.remove("show");
    if(!isOk)document.getElementById("opt-"+selOpt).classList.add("no");
    document.getElementById("opt-"+q.cor).classList.add("ok");
    var fb=document.getElementById("feedback-box");
    fb.className="feedback-box show "+(isOk?"fb-ok":"fb-no");
    fb.textContent=(isOk?"✓ ":"✗ ")+(isOk?q.fb_ok:q.fb_no);
    if(isOk){ score=moneyToNumber(q.prize); correctCount++; document.getElementById("score-badge").textContent=formatMoney(score); }
    updateMiniStats();
    setTimeout(function(){
      var nb=document.getElementById("btn-next"); nb.classList.add("show");
      if(!isOk){ var safe=getSafe(); nb.textContent=safe?"Ver resultado (salvavidas: "+safe+") →":"Ver resultado →"; nb.onclick=function(){ endGame(false); }; }
      else if(cQ===QS.length-1){ nb.textContent="Ver mi resultado final →"; nb.onclick=function(){ endGame(true); }; }
      else { nb.textContent="Siguiente pregunta →"; nb.onclick=function(){ nextQ(); }; }
    },350);
  }

  function nextQ(){ cQ++; renderQ(); }
  function walkAway(){ var prize=cQ>0?QS[cQ-1].prize:"$0"; endGame("walk",prize); }

  function endGame(type, walkPrize){
    var g=function(id){ return document.getElementById(id); };
    if(type===true){
      g("res-icon").textContent="🏆"; g("res-title").textContent="¡Experto en riesgo psicosocial!"; g("res-amount").textContent=QS[QS.length-1].prize;
      g("res-sub").textContent="Respondiste correctamente las 10 preguntas. Dominas las demandas del trabajo según la batería de evaluación.";
    } else if(type==="walk"){
      g("res-icon").textContent="💼"; g("res-title").textContent="Decidiste retirarte"; g("res-amount").textContent=walkPrize||"$0";
      g("res-sub").textContent="Una decisión inteligente. Supiste asegurar tu premio y jugar estratégicamente."; score=moneyToNumber(walkPrize||"$0");
    } else {
      var safe=getSafe(); g("res-icon").textContent="📚"; g("res-title").textContent="¡Sigue aprendiendo!"; g("res-amount").textContent=safe||"$0";
      g("res-sub").textContent="Fallaste en la pregunta "+(cQ+1)+". "+(safe?"Conservas "+safe+" gracias al piso seguro.":"Repasa la batería de riesgo psicosocial e inténtalo de nuevo.");
      score=moneyToNumber(safe||"$0");
    }
    g("stat-correct").textContent=correctCount; g("stat-score").textContent=formatMoney(score); g("stat-ll").textContent=llCount;
    var medals=[];
    if(correctCount===10)medals.push("🥇 Puntuación perfecta — 10 de 10");
    if(correctCount>=7&&correctCount<10)medals.push("🎯 Gran conocimiento — "+correctCount+" respuestas correctas");
    if(correctCount>=5&&correctCount<7)medals.push("💪 Buen nivel — "+correctCount+" respuestas correctas");
    if(llCount===0&&type!=="walk")medals.push("💎 Jugaste sin usar comodines");
    if(llCount===3)medals.push("📞 Usaste todos los comodines");
    if(correctCount<5)medals.push("📖 Recomendación: revisar la batería completa de riesgo psicosocial");
    g("medal-list").innerHTML=medals.map(function(m){ return "<div>"+m+"</div>"; }).join("");
    show("s-result");
  }

  function do5050(){
    if(llUsed.f5050||answered)return;
    llUsed.f5050=true; llCount++; document.getElementById("ll-5050").classList.add("used");
    var q=QS[cQ];
    var wrong=[0,1,2,3].filter(function(i){ return i!==q.cor&&hidden.indexOf(i)===-1; });
    wrong.sort(function(){ return Math.random()-0.5; });
    wrong.slice(0,2).forEach(function(i){ document.getElementById("opt-"+i).classList.add("gone"); hidden.push(i); });
    updateMiniStats();
  }

  function doPublic(){
    if(llUsed.pub||answered)return;
    llUsed.pub=true; llCount++; document.getElementById("ll-pub").classList.add("used");
    var q=QS[cQ]; var avail=[0,1,2,3].filter(function(i){ return hidden.indexOf(i)===-1; });
    var pcts={}; var total=0;
    avail.forEach(function(i){ pcts[i]=i===q.cor?Math.floor(Math.random()*20)+58:Math.floor(Math.random()*10)+3; total+=pcts[i]; });
    avail.forEach(function(i){ pcts[i]=Math.round(pcts[i]/total*100); });
    var letters=["A","B","C","D"]; var bars=document.getElementById("aud-bars");
    bars.innerHTML=avail.map(function(i){ return '<div class="aud-col"><div class="aud-p">'+pcts[i]+'%</div><div class="aud-bar" style="height:'+pcts[i]+'px;background:'+BAR_COLS[i]+'"></div><div class="aud-l">'+letters[i]+'</div></div>'; }).join("");
    document.getElementById("aud-wrap").style.display="block";
    updateMiniStats();
  }

  function doPhone(){
    if(llUsed.tel||answered)return;
    llUsed.tel=true; llCount++; document.getElementById("ll-tel").classList.add("used");
    var q=QS[cQ]; var name=NAMES[Math.floor(Math.random()*NAMES.length)]; var letters=["A","B","C","D"]; var r=Math.random(); var msg;
    if(r>0.55) msg="“"+name+" dice: He estudiado este tema y estoy bastante seguro de que la respuesta correcta es la opción "+letters[q.cor]+". Confío en eso.”";
    else if(r>0.25) msg="“"+name+" dice: Creo que podría ser la opción "+letters[q.cor]+", aunque no te lo puedo garantizar al 100%...”";
    else msg="“"+name+" dice: Este tema es complejo. Yo diría "+letters[q.cor]+", pero revisa bien antes de decidir.”";
    var pb=document.getElementById("phone-box"); pb.style.display="block"; pb.innerHTML="<strong>📞 Llamada a un experto</strong><br><br>"+msg;
    updateMiniStats();
  }

  function restart(){ startGame(); }
  buildPreview();
</script>"""

components.html(GAME_HTML, height=900, scrolling=True)
