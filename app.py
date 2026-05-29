import streamlit as st

# =========================
# 페이지 설정
# =========================

st.set_page_config(
    page_title="Bass Chord Tone Finder",
    layout="wide"
)

# =========================
# 음악 이론 데이터
# =========================

NOTES = [
    "C", "C#", "D", "D#", "E",
    "F", "F#", "G", "G#", "A", "A#", "B"
]

CHORD_TYPES = {
    "maj": [0, 4, 7],
    "min": [0, 3, 7],
    "7": [0, 4, 7, 10],
    "maj7": [0, 4, 7, 11],
    "m7": [0, 3, 7, 10]
}

# 베이스 튜닝 (위에서 아래)
TUNING = ["G", "D", "A", "E"]


# =========================
# 함수
# =========================

def get_note_index(note):
    return NOTES.index(note)


def build_chord(root, chord_type):

    root_index = get_note_index(root)

    intervals = CHORD_TYPES[chord_type]

    chord_notes = []

    for interval in intervals:

        note_index = (root_index + interval) % 12

        chord_notes.append(
            NOTES[note_index]
        )

    return chord_notes


def generate_fretboard(max_fret=12):

    fretboard = []

    for string_note in TUNING:

        string_notes = []

        start_index = get_note_index(string_note)

        for fret in range(max_fret + 1):

            note = NOTES[
                (start_index + fret) % 12
            ]

            string_notes.append(note)

        fretboard.append(string_notes)

    return fretboard


# =========================
# UI
# =========================

st.title("🎸 Bass Chord Tone Finder")

col1, col2 = st.columns(2)

with col1:

    root = st.selectbox(
        "Root Note",
        NOTES
    )

with col2:

    chord_type = st.selectbox(
        "Chord Type",
        list(CHORD_TYPES.keys())
    )

# =========================
# 코드 계산
# =========================

chord_notes = build_chord(
    root,
    chord_type
)

st.subheader(
    f"{root}{chord_type}"
)

st.write(
    "Chord Notes:"
)

st.success(
    " • ".join(chord_notes)
)

# =========================
# 지판 출력
# =========================

st.subheader("Fretboard")

fretboard = generate_fretboard()

# 프렛 헤더
header = "| STRING |"

for fret in range(13):
    header += f" {fret:^6} |"

st.markdown(f"```{header}```")

# 각 줄 출력
for string_index, string_notes in enumerate(fretboard):

    line = f"|   {TUNING[string_index]}    |"

    for note in string_notes:

        # 루트음
        if note == root:
            display = f"[{note}]"

        # 코드톤
        elif note in chord_notes:
            display = f" {note} "

        # 기타 음
        else:
            display = " -- "

        line += f" {display:^6} |"

    st.markdown(f"```{line}```")

# =========================
# 설명
# =========================

st.info(
    """
    [Root] = 루트음  
    일반 음 = 코드톤  
    -- = 코드에 포함되지 않는 음
    """
)
