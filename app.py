import streamlit as st
import tempfile
import os
import imageio_ffmpeg

import sys
import shutil

# Robust FFmpeg path resolution for Windows and other platforms
try:
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    ffmpeg_dir = os.path.dirname(os.path.abspath(ffmpeg_exe))
    if ffmpeg_dir not in os.environ["PATH"]:
        os.environ["PATH"] = ffmpeg_dir + os.pathsep + os.environ["PATH"]
    os.environ["FFMPEG_BINARY"] = ffmpeg_exe
except Exception as e:
    print(f"FFmpeg setup warning: {e}")

from translator_engine import translator
from style_utils import inject_custom_css, render_header

# Set page config
st.set_page_config(
    page_title="Ai voice translator",
    page_icon="🎙️",
    layout="wide"
)

# Apply premium styling
inject_custom_css()

# ---------- Session State Initialization ----------
def init_state():
    defaults = {
        "direction": "en-fr",
        "text_input": "",
        "last_translation": None,
        "last_translation_audio": None,
        "last_audio_bytes": None,
        "history": [],
        "committed_text": "",   # tracks the last text that was translated
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

init_state()

def swap_languages():
    st.session_state.direction = "fr-en" if st.session_state.direction == "en-fr" else "en-fr"
    st.session_state.last_translation = None
    st.session_state.last_translation_audio = None
    st.session_state.committed_text = ""

def clear_previous_results():
    """Wipe previous translation output and audio."""
    st.session_state.last_translation = None
    st.session_state.last_translation_audio = None

def run_translation(text):
    """Translate text and store results in session state."""
    clear_previous_results()
    try:
        translation = translator.translate(text, direction=st.session_state.direction)
        st.session_state.last_translation = translation
        st.session_state.committed_text = text

        target_lang_code = "fr" if st.session_state.direction == "en-fr" else "en"
        audio_fp = translator.generate_audio(translation, lang=target_lang_code)
        if audio_fp:
            st.session_state.last_translation_audio = audio_fp.getvalue()

        # Add to history
        if not st.session_state.history or st.session_state.history[-1]['tar'] != translation:
            st.session_state.history.append({
                "dir": st.session_state.direction,
                "src": text,
                "tar": translation
            })
    except Exception as e:
        st.error(f"Translation Error: {e}")

def main():
    render_header("Gbapre Timothy Tubolayefa", "20231407812", "CYB")

    src_label = "English" if st.session_state.direction == "en-fr" else "French"
    tar_label = "French" if st.session_state.direction == "en-fr" else "English"

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)

    # -------- Voice Input --------
    st.markdown(f"### Voice Input ({src_label})")
    audio_value = st.audio_input("Speak", label_visibility="collapsed")

    if audio_value is not None:
        audio_bytes = audio_value.getvalue()
        # Only process if this is a NEW recording
        if st.session_state.last_audio_bytes != audio_bytes:
            st.session_state.last_audio_bytes = audio_bytes
            # Wipe everything immediately
            clear_previous_results()
            st.session_state.text_input = ""

            transcribed = None
            with st.spinner("Transcribing your voice..."):
                with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                    tmp.write(audio_bytes)
                    tmp_path = tmp.name
                try:
                    transcribed = translator.transcribe_audio(tmp_path)
                except Exception as e:
                    st.error(f"Transcription error: {e}")
                finally:
                    if os.path.exists(tmp_path):
                        os.remove(tmp_path)

            if transcribed:
                # Write into BOTH session state vars — text_area_input is the widget key
                # and takes precedence over value= after rerun
                st.session_state.text_input = transcribed
                st.session_state["text_area_input"] = transcribed
                # Auto-translate immediately
                with st.spinner("Translating..."):
                    run_translation(transcribed)
                st.rerun()
            elif transcribed is not None:
                st.warning("No speech detected. Please try again.")

    st.markdown("<br>", unsafe_allow_html=True)

    # -------- Text Input / Output Row --------
    col1, col_mid, col2 = st.columns([7, 1, 7])

    with col1:
        st.markdown(f"### {src_label}")
        input_text = st.text_area(
            label=f"Input {src_label}",
            placeholder=f"Enter {src_label} text here...",
            value=st.session_state.text_input,
            height=250,
            label_visibility="collapsed",
            key="text_area_input"
        )
        # Detect if user changed text manually → wipe previous results
        if input_text != st.session_state.text_input:
            clear_previous_results()
        st.session_state.text_input = input_text

    with col_mid:
        if st.button("⇄", help="Swap Languages", key="swap_languages_btn"):
            swap_languages()
            st.rerun()

    with col2:
        st.markdown(f"### {tar_label}")
        output_placeholder = st.empty()

    st.markdown("<br>", unsafe_allow_html=True)

    # -------- Translate Button --------
    if st.button("TRANSLATE NOW", type="primary", use_container_width=True):
        if st.session_state.text_input.strip():
            with st.spinner("Translating..."):
                run_translation(st.session_state.text_input.strip())
        else:
            st.warning("Please enter text or record audio to translate.")

    # -------- Output Area --------
    with col2:
        output_placeholder.text_area(
            label=f"{tar_label} output",
            value=st.session_state.last_translation or "",
            height=250,
            disabled=True,
            label_visibility="collapsed"
        )
        if st.session_state.last_translation_audio:
            st.audio(st.session_state.last_translation_audio, format="audio/mp3")

    st.markdown('</div>', unsafe_allow_html=True)

    # -------- Translation History --------
    if st.session_state.history:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### Translation History")
        for item in reversed(st.session_state.history[-3:]):
            direction_label = item.get('dir', '??').upper()
            src_text = item.get('src', '')[:60]
            tar_text = item.get('tar', '')[:60]
            st.markdown(f"""
            <div style="background: rgba(255,255,255,0.03); padding: 10px; border-radius: 10px; margin-bottom: 8px; border-left: 4px solid #6366f1;">
                <span style="color: #6366f1; font-weight: bold;">{direction_label}:</span> {src_text}... → {tar_text}...
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
