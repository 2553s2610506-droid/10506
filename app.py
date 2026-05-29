# realistic_bass_fretboard_streamlit_app

## app.py

```python
import streamlit as st

st.set_page_config(
    page_title="Bass Fretboard",
    layout="wide"
)

# =========================
# 음악 데이터
# =========================

NOTES = [
    "C", "C#", "D", "D#", "E",
    "F", "F#", "G", "G#", "A", "A#", "B"
]

CHORDS = {
    "maj": [0, 4, 7],
    "min": [0, 3, 7],
    "7": [0, 4, 7, 10],
    "maj7": [0, 4, 7, 11],
    "m7": [0, 3, 7, 10]
}

TUNING = ["E", "A", "D", "G"]


# =========================
# 함수
# =========================


def note_index(note):
    return NOTES.index(note)



def build_chord(root, chord_type):

    root_idx = note_index(root)

    intervals = CHORDS[chord_type]

    result = []

    for interval in intervals:

        idx = (root_idx + interval) % 12

        result.append(NOTES[idx])

    return result



def generate_fretboard(max_fret=12):

    fretboard = []

    for string_note in TUNING:

        row = []

        start_idx = note_index(string_note)

        for fret in range(max_fret + 1):

            note = NOTES[(start_idx + fret) % 12]

            row.append(note)

        fretboard.append(row)

    return fretboard


# =========================
# UI
# =========================

st.title("🎸 Bass Fretboard Visualizer")

col1, col2 = st.columns(2)

with col1:

    root = st.selectbox(
        "Root Note",
        NOTES
    )

with col2:

    chord_type = st.selectbox(
        "Chord Type",
        list(CHORDS.keys())
    )


chord_notes = build_chord(root, chord_type)

st.success(f"Chord Notes: {' • '.join(chord_notes)}")

fretboard = generate_fretboard()


# =========================
# CSS
# =========================

st.markdown(
    """
    <style>

    .fretboard {
        background: linear-gradient(
            to bottom,
            #5c3b1e,
            #3b2412
        );

        padding: 40px;

        border-radius: 20px;

        overflow-x: auto;

        border: 4px solid #222;
    }

    .string-row {
        display: flex;
        align-items: center;
        margin: 26px 0;
        position: relative;
    }

    .string-line {
        position: absolute;
        left: 0;
        right: 0;
        height: 4px;
        background: silver;
        z-index: 1;
    }

    .fret {
        width: 72px;
        height: 60px;

        border-right: 3px solid #cfcfcf;

        display: flex;
        justify-content: center;
        align-items: center;

        position: relative;

        z-index: 2;
    }

    .note {
        width: 42px;
        height: 42px;

        border-radius: 50%;

        display: flex;
        justify-content: center;
        align-items: center;

        font-weight: bold;

        color: white;

        background: #3498db;

        box-shadow: 0 0 10px rgba(0,0,0,0.5);
    }

    .root {
        background: #e74c3c;
    }

    .empty {
        width: 42px;
        height: 42px;
    }

    .fret-numbers {
        display: flex;
        margin-left: 30px;
        margin-bottom: 15px;
        color: white;
        font-weight: bold;
    }

    .fret-number {
        width: 72px;
        text-align: center;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================
# 프렛 번호
# =========================

fret_numbers_html = "<div class='fret-numbers'>"

for fret in range(13):
    fret_numbers_html += f"<div class='fret-number'>{fret}</div>"

fret_numbers_html += "</div>"


# =========================
# 지판 생성
# =========================

html = "<div class='fretboard'>"

html += fret_numbers_html

for string_notes in fretboard:

    html += "<div class='string-row'>"

    html += "<div class='string-line'></div>"

    for note in string_notes:

        html += "<div class='fret'>"

        if note == root:

            html += f"<div class='note root'>{note}</div>"

        elif note in chord_notes:

            html += f"<div class='note'>{note}</div>"

        else:

            html += "<div class='empty'></div>"

        html += "</div>"

    html += "</div>"

html += "</div>"

st.markdown(html, unsafe_allow_html=True)


# =========================
# 설명
# =========================

st.info(
    """
    🔴 빨간색 = 루트음

    🔵 파란색 = 코드톤
    """
)
```

---

## requirements.txt

```txt
streamlit
```

---

## 실행 방법

```bash
streamlit run app.py
```

---

## 특징

* 실제 베이스 지판 느낌
* 나무 색상 지판
* 금속 줄 표현
* 프렛 라인 구현
* 원형 코드톤 표시
* 루트음 빨간색 강조
* Streamlit 기본만 사용
* 외부 라이브러리 필요 없음
