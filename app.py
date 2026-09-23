import streamlit as st

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

# Temporary reference ranges transcribed from the screenshots already provided.
# 1 = OPEN, 0 = FOLD. These can be replaced/extended with the full reference data.
DATA = {
    "50bb": {
        "LJ": [
            "1111111111110","1111111100000","1111111000000",
            "1111111000000","1111111100000","1000011100000",
            "0000001100000","0000001100000","0000000100000",
            "0000000001000","0000000001000","0000000000100",
            "0000000000001",
        ],
        "HJ": [
            "1111111111111","1111111111100","1111111110000",
            "1111111100000","1111111100000","1100111100000",
            "1000001110000","0000001100000","0000000100000",
            "0000000001000","0000000001000","0000000000100",
            "0000000000001",
        ],
        "CO": [
            "1111111111111","1111111111110","1111111111100",
            "1111111100000","1111111100000","1111111100000",
            "1100011100000","1000011100000","1000000100000",
            "1000000001000","0000000001000","0000000000100",
            "0000000000001",
        ],
    },
    "100bb": {}
}

if "selected" not in st.session_state:
    st.session_state.selected = set()
if "score" not in st.session_state:
    st.session_state.score = 0
if "correct" not in st.session_state:
    st.session_state.correct = 0
if "wrong" not in st.session_state:
    st.session_state.wrong = 0
if "validated" not in st.session_state:
    st.session_state.validated = False

st.markdown("""
<style>
.main {background:#063e49}
.block-container {max-width:1050px;padding-top:2rem}
h1 {margin-bottom:0}
.small {color:#9fc2c7}
.range-cell button {
    width:100%; min-height:42px; padding:0;
}
div[data-testid="stHorizontalBlock"] {gap:.25rem}
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
st.markdown(f"### {spot} · {depth} · {action}")
st.caption("Sélectionne plusieurs cases, puis valide. Pour un spot OPEN, une case du range = OPEN ; hors range = FOLD.")

m1,m2,m3,m4 = st.columns(4)
m1.metric("Score", st.session_state.score)
m2.metric("Bonnes", st.session_state.correct)
m3.metric("Erreurs", st.session_state.wrong)
total_answered = st.session_state.correct + st.session_state.wrong
m4.metric("Précision", f"{round(100*st.session_state.correct/total_answered)}%" if total_answered else "—")

st.divider()

for r in range(13):
    cols = st.columns(13)
    for c in range(13):
        key = f"{r}-{c}"
        label = HANDS[r][c]
        selected = key in st.session_state.selected
        text = ("✓ " if selected else "") + label
        if cols[c].button(text, key=f"cell-{r}-{c}", use_container_width=True, disabled=st.session_state.validated):
            if key in st.session_state.selected:
                st.session_state.selected.remove(key)
            else:
                st.session_state.selected.add(key)
            st.rerun()

st.caption("🟧 Range de référence · ⬜ hors range · ✓ sélection actuelle")

b1, b2 = st.columns([1,1])
if b1.button("✅ Valider le range", type="primary", use_container_width=True, disabled=st.session_state.validated):
    correct = 0
    wrong = 0
    for r in range(13):
        for c in range(13):
            key = f"{r}-{c}"
            in_range = reference[r][c] == "1"
            expected = "OPEN" if in_range else "FOLD"
            chosen = action if key in st.session_state.selected else "FOLD"
            if chosen == expected:
                correct += 1
            else:
                wrong += 1
    st.session_state.score += correct
    st.session_state.correct += correct
    st.session_state.wrong += wrong
    st.session_state.validated = True
    st.rerun()

if b2.button("🔄 Nouvelle manche", use_container_width=True):
    st.session_state.selected = set()
    st.session_state.validated = False
    st.rerun()

if st.session_state.validated:
    total = 169
    last_correct = 0
    for r in range(13):
        for c in range(13):
            key = f"{r}-{c}"
            expected = "OPEN" if reference[r][c] == "1" else "FOLD"
            chosen = action if key in st.session_state.selected else "FOLD"
            last_correct += chosen == expected
    st.success(f"Résultat : {last_correct}/{total} bonnes cases — {round(100*last_correct/total)} %")
    st.info("Pour l'instant, la correction des spots OPEN est binaire OPEN/FOLD. Les spots avec RAISE seront ajoutés avec leur vraie logique à 3 actions.")
