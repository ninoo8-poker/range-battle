const hands = [["AA", "AKs", "AQs", "AJs", "ATs", "A9s", "A8s", "A7s", "A6s", "A5s", "A4s", "A3s", "A2s"], ["AKo", "KK", "KQs", "KJs", "KTs", "K9s", "K8s", "K7s", "K6s", "K5s", "K4s", "K3s", "K2s"], ["AQo", "KQo", "QQ", "QJs", "QTs", "Q9s", "Q8s", "Q7s", "Q6s", "Q5s", "Q4s", "Q3s", "Q2s"], ["AJo", "KJo", "QJo", "JJ", "JTs", "J9s", "J8s", "J7s", "J6s", "J5s", "J4s", "J3s", "J2s"], ["ATo", "KTo", "QTo", "JTo", "TT", "T9s", "T8s", "T7s", "T6s", "T5s", "T4s", "T3s", "T2s"], ["A9o", "K9o", "Q9o", "J9o", "T9o", "99", "98s", "97s", "96s", "95s", "94s", "93s", "92s"], ["A8o", "K8o", "Q8o", "J8o", "T8o", "98o", "88", "87s", "86s", "85s", "84s", "83s", "82s"], ["A7o", "K7o", "Q7o", "J7o", "T7o", "97o", "87o", "77", "76s", "75s", "74s", "73s", "72s"], ["A6o", "K6o", "Q6o", "J6o", "T6o", "96o", "86o", "76o", "66", "65s", "64s", "63s", "62s"], ["A5o", "K5o", "Q5o", "J5o", "T5o", "95o", "85o", "75o", "65o", "55", "54s", "53s", "52s"], ["A4o", "K4o", "Q4o", "J4o", "T4o", "94o", "84o", "74o", "64o", "54o", "44", "43s", "42s"], ["A3o", "K3o", "Q3o", "J3o", "T3o", "93o", "83o", "73o", "63o", "53o", "43o", "33", "32s"], ["A2o", "K2o", "Q2o", "J2o", "T2o", "92o", "82o", "72o", "62o", "52o", "42o", "32o", "22"]];
const DATA = {"50": {"LJ": {"action": "OPEN", "mask": ["1111111111110", "1111111100000", "1111111000000", "1111111000000", "1111111100000", "1000011100000", "0000001100000", "0000001100000", "0000000100000", "0000000001000", "0000000001000", "0000000000100", "0000000000001"]}, "HJ": {"action": "OPEN", "mask": ["1111111111111", "1111111111100", "1111111110000", "1111111100000", "1111111100000", "1100111100000", "1000001110000", "0000001100000", "0000000100000", "0000000001000", "0000000001000", "0000000000100", "0000000000001"]}, "CO": {"action": "OPEN", "mask": ["1111111111111", "1111111111110", "1111111111100", "1111111100000", "1111111100000", "1111111100000", "1100011100000", "1000011100000", "1000000100000", "1000000001000", "0000000001000", "0000000000100", "0000000000001"]}}, "100": {}};

const board = document.getElementById("board");
const depth = document.getElementById("depth");
const spot = document.getElementById("spot");
const action = document.getElementById("action");
const validate = document.getElementById("validate");
const newRound = document.getElementById("newRound");
const nextRound = document.getElementById("nextRound");
const result = document.getElementById("result");
const resultText = document.getElementById("resultText");

let selected = new Set();
let locked = false;
let stats = {score:0, correct:0, wrong:0};

function currentSpot(){
  return DATA[depth.value]?.[spot.value] || null;
}

function fillSpots(){
  const spots = Object.keys(DATA[depth.value] || {});
  spot.innerHTML = "";
  spots.forEach(s => {
    const o=document.createElement("option"); o.value=s; o.textContent=s; spot.appendChild(o);
  });
  if(!spots.length){
    const o=document.createElement("option"); o.textContent="Autres spots à ajouter"; o.value="";
    spot.appendChild(o);
  }
  selected.clear();
  render();
}

function render(){
  board.innerHTML="";
  const cfg=currentSpot();
  hands.forEach((row,r)=>row.forEach((hand,c)=>{
    const cell=document.createElement("button");
    cell.className="cell " + ((cfg && cfg.mask[r][c]==="1") ? "range" : "fold");
    cell.textContent=hand;
    cell.dataset.key=r+"-"+c;
    if(selected.has(cell.dataset.key)) cell.classList.add("selected");
    cell.addEventListener("click",()=>{
      if(locked) return;
      const key=cell.dataset.key;
      if(selected.has(key)) selected.delete(key); else selected.add(key);
      cell.classList.toggle("selected");
    });
    board.appendChild(cell);
  }));
  document.getElementById("spotLabel").textContent=`6-max MTT · ${depth.value}bb · ${spot.value || "spot"}`;
  const a=action.value;
  document.getElementById("instruction").textContent =
    a==="OPEN" ? "Sélectionne toutes les mains que tu OPEN." :
    a==="FOLD" ? "Sélectionne toutes les mains que tu FOLD." :
    "Sélectionne toutes les mains avec lesquelles tu RAISE.";
}

function validateRound(){
  const cfg=currentSpot();
  if(!cfg){
    resultText.textContent="Ce spot n'est pas encore configuré. Ajoute son range de référence dans DATA.";
    result.classList.remove("hidden"); return;
  }
  // Current Open spots: range = OPEN, outside range = FOLD.
  // RAISE is kept as a third action in the interface for future spots.
  const wanted = action.value;
  let correct=0, wrong=0, total=169;
  [...board.children].forEach((cell,idx)=>{
    const r=Math.floor(idx/13), c=idx%13;
    const inRange=cfg.mask[r][c]==="1";
    const expected = inRange ? "OPEN" : "FOLD";
    const chosen = selected.has(r+"-"+c) ? wanted : "FOLD";
    const ok = chosen===expected;
    if(ok){ correct++; cell.classList.add("correct"); }
    else { wrong++; cell.classList.add("incorrect"); }
    cell.disabled=true;
  });
  locked=true;
  const pct=Math.round(correct/total*100);
  stats.correct+=correct; stats.wrong+=wrong; stats.score+=correct;
  document.getElementById("score").textContent=stats.score;
  document.getElementById("correct").textContent=stats.correct;
  document.getElementById("wrong").textContent=stats.wrong;
  document.getElementById("accuracy").textContent=Math.round(stats.correct/(stats.correct+stats.wrong)*100)+"%";
  resultText.innerHTML=`<strong>${correct} / ${total} bonnes cases — ${pct}%</strong><br><span>Vert = correct · rouge = erreur</span>`;
  result.classList.remove("hidden");
}

function resetRound(){
  selected.clear(); locked=false; result.classList.add("hidden"); render();
}

depth.addEventListener("change",fillSpots);
spot.addEventListener("change",resetRound);
action.addEventListener("change",render);
validate.addEventListener("click",validateRound);
newRound.addEventListener("click",resetRound);
nextRound.addEventListener("click",resetRound);

fillSpots();
