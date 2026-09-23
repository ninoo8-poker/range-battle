import json
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Range Trainer", page_icon="♠️", layout="wide")

HANDS = [
["AA","AKs","AQs","AJs","ATs","A9s","A8s","A7s","A6s","A5s","A4s","A3s","A2s"],
["AKo","KK","KQs","KJs","KTs","K9s","K8s","K7s","K6s","K5s","K4s","K3s","K2s"],
["AQo","KQo","QQ","QJs","QTs","Q9s","Q8s","Q7s","Q6s","Q5s","Q4s","Q3s","Q2s"],
["AJo","KJo","QJo","JJ","JTs","J9s","J8s","J7s","J6s","J5s","J4s","J3s","J2s"],
["ATo","KTo","QTo","JTo","TT","T9s","T8s","T7s","T6s","T5s","T4s","T3s","T2s"],
["A9o","K9o","Q9o","J9o","T9o","99","98s","97s","96s","95s","94s","93s","92s"],
["A8o","K8o","Q8o","J8o","T8o","98o","88","87s","86s","85s","84s","83s","82s"],
["A7o","K7o","Q7o","J7o","T7o","97o","87o","77","76s","75s","74s","73s","72s"],
["A6o","K6o","Q6o","J6o","T6o","96o","86o","76o","66","65s","64s","63s","62s"],
["A5o","K5o","Q5o","J5o","T5o","95o","85o","75o","65o","55","54s","53s","52s"],
["A4o","K4o","Q4o","J4o","T4o","94o","84o","74o","64o","54o","44","43s","42s"],
["A3o","K3o","Q3o","J3o","T3o","93o","83o","73o","63o","53o","43o","33","32s"],
["A2o","K2o","Q2o","J2o","T2o","92o","82o","72o","62o","52o","42o","32o","22"],
]

# Prototype reference data transcribed from the screenshots supplied in the conversation.
DATA = {
    "50bb": {
        "LJ": [
            "1111111111110","1111111100000","1111111000000","1111111000000","1111111100000","1000011100000","0000001100000","0000001100000","0000000100000","0000000001000","0000000001000","0000000000100","0000000000001",
        ],
        "HJ": [
            "1111111111111","1111111111100","1111111110000","1111111100000","1111111100000","1100111100000","1000001110000","0000001100000","0000000100000","0000000001000","0000000001000","0000000000100","0000000000001",
        ],
        "CO": [
            "1111111111111","1111111111110","1111111111100","1111111100000","1111111100000","1111111100000","1100011100000","1000011100000","1000000100000","1000000001000","0000000001000","0000000000100","0000000000001",
        ],
    },
    "100bb": {},
}

st.markdown("""
<style>
.block-container {max-width: 1180px; padding-top: 1.5rem;}
</style>
""", unsafe_allow_html=True)

st.title("♠️ Range Trainer")
st.caption("6-max MTT · entraînement aux ranges · mode solo")

c1, c2, c3 = st.columns(3)
depth = c1.selectbox("Profondeur", ["50bb", "100bb"])
spots = list(DATA[depth].keys())
spot = c2.selectbox("Spot", spots if spots else ["À ajouter"])
action = c3.selectbox("Action testée", ["OPEN", "FOLD", "RAISE"])

if not spots:
    st.warning("Les ranges 100bb ne sont pas encore intégrés dans cette version de test.")
    st.stop()

reference = DATA[depth][spot]
reference_json = json.dumps(reference)
hands_json = json.dumps(HANDS)

st.markdown(f"### {spot} · {depth} · {action}")
st.caption("Clique-glisse sur la grille pour sélectionner plusieurs mains. Relâche la souris, puis valide pour afficher les bonnes réponses et les erreurs.")

html = f"""
<!doctype html>
<html><head><meta charset='utf-8'>
<style>
* {{ box-sizing:border-box; }}
body {{ margin:0; font-family:Arial,sans-serif; background:transparent; color:#e9f1f3; user-select:none; }}
.wrap {{ max-width:920px; margin:auto; }}
.legend {{ display:flex; flex-wrap:wrap; gap:10px 18px; margin:0 0 10px; font-size:13px; color:#b8c8cc; }}
.leg {{ display:flex; align-items:center; gap:6px; }}
.dot {{ width:13px; height:13px; border-radius:3px; border:1px solid #587177; display:inline-block; }}
.dot.sel {{ background:#5b8def; border-color:#7ba5ff; }}
.dot.ok {{ background:#31a56d; border-color:#52c88e; }}
.dot.err {{ background:#d05b5b; border-color:#ee8585; }}
.grid {{ display:grid; grid-template-columns:repeat(13,minmax(32px,1fr)); gap:3px; touch-action:none; }}
.cell {{ aspect-ratio:1/1; min-width:0; border:1px solid #40565b; border-radius:4px; background:#16262a; color:#dce7e9; display:flex; align-items:center; justify-content:center; font-size:clamp(8px,1.25vw,13px); font-weight:600; cursor:crosshair; transition:.05s; }}
.cell:hover {{ border-color:#9fb3b8; }}
.cell.selected {{ background:#5b8def; border-color:#8fb0ff; color:white; }}
.cell.expected {{ background:#31a56d; border-color:#52c88e; color:white; }}
.cell.missed {{ background:#d05b5b; border-color:#ee8585; color:white; }}
.cell.falsepos {{ background:#d18b45; border-color:#e8aa68; color:white; }}
.cell.neutral {{ background:#18282c; color:#9fb0b4; }}
.actions {{ display:flex; gap:10px; margin-top:14px; flex-wrap:wrap; }}
button.ctrl {{ border:0; border-radius:7px; padding:10px 16px; font-weight:700; cursor:pointer; background:#2b7380; color:white; }}
button.ctrl.secondary {{ background:#293d42; }}
button.ctrl:disabled {{ opacity:.55; cursor:default; }}
.result {{ margin-top:13px; padding:12px 14px; border-radius:8px; background:#16272b; font-size:15px; }}
.small {{ margin-top:7px; color:#9fb0b4; font-size:12px; }}
@media(max-width:600px) {{ .grid {{ gap:2px; }} .cell {{ font-size:8px; border-radius:3px; }} }}
</style></head>
<body>
<div class='wrap'>
  <div class='legend'>
    <span class='leg'><span class='dot sel'></span> sélection</span>
    <span class='leg'><span class='dot ok'></span> correct</span>
    <span class='leg'><span class='dot err'></span> erreur / main manquée</span>
    <span class='leg'><span class='dot' style='background:#d18b45;border-color:#e8aa68'></span> main sélectionnée en trop</span>
  </div>
  <div id='grid' class='grid'></div>
  <div class='actions'>
    <button id='validate' class='ctrl'>✅ Valider le range</button>
    <button id='clear' class='ctrl secondary'>Effacer la sélection</button>
    <button id='new' class='ctrl secondary'>🔄 Nouvelle manche</button>
  </div>
  <div id='result' class='result'>Sélectionne les mains avec le clic-glissé.</div>
  <div class='small'>Astuce : clique dans une case et fais glisser la souris sur les autres cases. Un clic simple fonctionne aussi.</div>
</div>
<script>
const hands = {hands_json};
const ref = {reference_json};
const action = {json.dumps(action)};
const grid = document.getElementById('grid');
const result = document.getElementById('result');
const validate = document.getElementById('validate');
const clear = document.getElementById('clear');
const newBtn = document.getElementById('new');
let selected = new Set();
let dragging = false;
let paintMode = true;
let validated = false;

for (let r=0;r<13;r++) {{
  for (let c=0;c<13;c++) {{
    const b=document.createElement('button');
    b.type='button'; b.className='cell'; b.textContent=hands[r][c];
    b.dataset.key=r+'-'+c;
    b.addEventListener('pointerdown', e => {{
      if (validated) return;
      e.preventDefault();
      dragging=true;
      paintMode=!selected.has(b.dataset.key);
      b.setPointerCapture?.(e.pointerId);
      setCell(b, paintMode);
    }});
    b.addEventListener('pointerenter', e => {{
      if (dragging && !validated) setCell(b, paintMode);
    }});
    b.addEventListener('pointerup', () => {{ dragging=false; }});
    b.addEventListener('click', e => e.preventDefault());
    grid.appendChild(b);
  }}
}}
window.addEventListener('pointerup',()=>dragging=false);

function setCell(b,on) {{
  const k=b.dataset.key;
  if(on) {{ selected.add(k); b.classList.add('selected'); }}
  else {{ selected.delete(k); b.classList.remove('selected'); }}
  result.textContent=selected.size+' main'+(selected.size>1?'s':'')+' sélectionnée'+(selected.size>1?'s':'')+'.';
}}

function expected(r,c) {{
  return ref[r][c] === '1' ? 'OPEN' : 'FOLD';
}}

validate.addEventListener('click',()=>{{
  if (validated) return;
  let correct=0, missed=0, falsepos=0;
  const cells=[...document.querySelectorAll('.cell')];
  cells.forEach(b=>{{
    const [r,c]=b.dataset.key.split('-').map(Number);
    const exp=expected(r,c);
    const isSel=selected.has(b.dataset.key);
    const isCorrect = action==='OPEN' ? (isSel && exp==='OPEN') : (action==='FOLD' ? (!isSel && exp==='FOLD') : false);
    if (isCorrect) {{ correct++; b.classList.remove('selected'); b.classList.add('expected'); }}
    else if (exp==='OPEN' && !isSel) {{ missed++; b.classList.add('missed'); }}
    else if (exp==='FOLD' && isSel) {{ falsepos++; b.classList.add('falsepos'); }}
    else {{ b.classList.add('neutral'); }}
  }});
  validated=true;
  validate.disabled=true; clear.disabled=true;
  const total=169;
  const pct=Math.round(100*correct/total);
  result.innerHTML='<b>Résultat : '+correct+'/'+total+' · '+pct+' %</b><br><span style="color:#52c88e">Vert = correct</span> · <span style="color:#ee8585">Rouge = main attendue mais manquée</span> · <span style="color:#e8aa68">Orange = main sélectionnée en trop</span><br><span class="small">Mains manquées : '+missed+' · Mains en trop : '+falsepos+'</span>';
}});

function reset() {{
  selected.clear(); validated=false;
  document.querySelectorAll('.cell').forEach(b=>{{b.className='cell';}});
  validate.disabled=false; clear.disabled=false;
  result.textContent='Sélectionne les mains avec le clic-glissé.';
}}
clear.addEventListener('click',()=>{{ if(!validated) {{ selected.clear(); document.querySelectorAll('.cell').forEach(b=>b.classList.remove('selected')); result.textContent='Sélection effacée.'; }} }});
newBtn.addEventListener('click',reset);
</script>
</body></html>
"""

components.html(html, height=670, scrolling=False)

st.info("⚠️ Cette version améliore l'interface de sélection et de correction. Les ranges de référence restent ceux actuellement transcrits pour 50bb LJ/HJ/CO ; ils devront être complétés avec tes captures pour avoir une correction fidèle.")
