# app.py

import streamlit as st
import plotly.graph_objects as go

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


# =========================
# 코드 계산
# =========================

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
# Plotly 지판 그리기
# =========================

def draw_fretboard(chord_notes, root_note):

    fretboard = generate_fretboard()

    fig = go.Figure()

    # 줄 그리기
    for string in range(4):
        fig.add_shape(
            type="line",
            x0=0,
            y0=string,
            x1=12,
            y1=string,
            line=dict(width=4)
        )

    # 프렛 그리기
    for fret in range(13):
        fig.add_shape(
            type="line",
            x0=fret,
            y0=0,
            x1=fret,
            y1=3,
            line=dict(width=2)
        )

    # 음 표시
    for string_idx, string_notes in enumerate(fretboard):

        for fret_idx, note in enumerate(string_notes):

            if note in chord_notes:

                color = "red" if note == root_note else "lightblue"

                fig.add_trace(
                    go.Scatter(
                        x=[fret_idx],
                        y=[string_idx],
                        mode="markers+text",
                        marker=dict(
                            size=28,
                            color=color
                        ),
                        text=[note],
                        textposition="middle center",
                        showlegend=False
                    )
                )

    fig.update_layout(
        height=350,
        width=1000,
        plot_bgcolor="white",
        margin=dict(l=20, r=20, t=40, b=20),
        xaxis=dict(
            range=[-0.5, 12.5],
            tickvals=list(range(13)),
            title="Fret"
        ),
        yaxis=dict(
            range=[3.5, -0.5],
            tickvals=[0, 1, 2, 3],
            ticktext=["E", "A", "D", "G"],
            title="String"
        )
    )

    return fig


# =========================
# Streamlit UI
# =========================

st.set_page_config(page_title="Bass Chord Tone Finder")

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

st.subheader(f"{root}{chord_type} Chord")

st.write("Chord Notes:")
st.write(", ".join(chord_notes))

fig = draw_fretboard(chord_notes, root)

st.plotly_chart(fig, use_container_width=True)
