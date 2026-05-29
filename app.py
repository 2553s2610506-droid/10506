import streamlit as st
import matplotlib.pyplot as plt

# =========================
# 음악 이론
# =========================

NOTES = [
    "C", "C#", "D", "D#", "E",
    "F", "F#", "G", "G#", "A", "A#", "B"
]

CHORD_FORMULAS = {
    "maj": [0, 4, 7],
    "min": [0, 3, 7],
    "7": [0, 4, 7, 10],
    "maj7": [0, 4, 7, 11],
    "m7": [0, 3, 7, 10],
}

TUNING = ["E", "A", "D", "G"]


def get_note_index(note):
    return NOTES.index(note)


def build_chord(root, chord_type):
    root_index = get_note_index(root)
    intervals = CHORD_FORMULAS[chord_type]

    chord_notes = []

    for interval in intervals:
        note_index = (root_index + interval) % 12
        chord_notes.append(NOTES[note_index])

    return chord_notes


# =========================
# 지판 생성
# =========================

def generate_fretboard(max_fret=12):
    fretboard = []

    for string_note in TUNING:
        string_notes = []

        start_index = get_note_index(string_note)

        for fret in range(max_fret + 1):
            note = NOTES[(start_index + fret) % 12]
            string_notes.append(note)

        fretboard.append(string_notes)

    return fretboard


# =========================
# 지판 그리기
# =========================

def draw_fretboard(chord_notes, root_note):

    fretboard = generate_fretboard()

    fig, ax = plt.subplots(figsize=(14, 4))

    num_strings = 4
    num_frets = 12

    # 줄
    for string in range(num_strings):
        ax.plot([0, num_frets], [string, string], linewidth=2)

    # 프렛
    for fret in range(num_frets + 1):
        ax.plot([fret, fret], [0, num_strings - 1], linewidth=1)

    # 음 표시
    for string_idx, string_notes in enumerate(fretboard):

        for fret_idx, note in enumerate(string_notes):

            if note in chord_notes:

                color = "red" if note == root_note else "skyblue"

                ax.scatter(
                    fret_idx,
                    string_idx,
                    s=500,
                    color=color
                )

                ax.text(
                    fret_idx,
                    string_idx,
                    note,
                    ha="center",
                    va="center",
                    fontsize=10,
                    fontweight="bold"
                )

    # 꾸미기
    ax.set_xlim(-0.5, num_frets + 0.5)
    ax.set_ylim(-0.5, num_strings - 0.5)

    ax.set_xticks(range(num_frets + 1))
    ax.set_yticks(range(num_strings))

    ax.set_yticklabels(["E", "A", "D", "G"])

    ax.invert_yaxis()

    ax.set_title("Bass Fretboard Chord Tones")

    plt.tight_layout()

    return fig


# =========================
# Streamlit UI
# =========================

st.set_page_config(page_title="Bass Chord Finder")

st.title("🎸 Bass Chord Tone Finder")

root = st.selectbox(
    "Root Note",
    NOTES
)

chord_type = st.selectbox(
    "Chord Type",
    list(CHORD_FORMULAS.keys())
)

chord_notes = build_chord(root, chord_type)

st.subheader("Chord Notes")
st.write(" - ".join(chord_notes))

fig = draw_fretboard(chord_notes, root)

st.pyplot(fig)
