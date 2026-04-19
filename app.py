import streamlit as st
import tempfile
import os
import imageio_ffmpeg

# Add ffmpeg to PATH so Whisper can find it
os.environ["PATH"] += os.pathsep + os.path.dirname(imageio_ffmpeg.get_ffmpeg_exe())

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

# Initialize session state
if 'direction' not in st.session_state:
    st.session_state.direction = "en-fr"
if 'last_translation' not in st.session_state:
    st.session_state.last_translation = ""
if 'text_input' not in st.session_state:
    st.session_state.text_input = ""
if 'last_audio_bytes' not in st.session_state:
    st.session_state.last_audio_bytes = None
if 'history' not in st.session_state:
    st.session_state.history = []
if 'last_translation_audio' not in st.session_state:
    st.session_state.last_translation_audio = None


def swap_languages():
    st.session_state.direction = "fr-en" if st.session_state.direction == "en-fr" else "en-fr"
    st.session_state.last_translation = ""
    st.session_state.text_input = ""
    st.session_state.last_translation_audio = None


def do_translate(text):
    """Run translation and audio generation, store results in session state."""
    try:
        translation = translator.translate(text, direction=st.session_state.direction)
        st.session_state.last_translation = translation

        target_lang_code = "fr" if st.session_state.direction == "en-fr" else "en"
        audio_fp = translator.generate_audio(translation, lang=target_lang_code)
        st.session_state.last_translation_audio = audio_fp.getvalue() if audio_fp else None

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

    # --- VOICE INPUT: fully automatic ---
    st.markdown(f"### 🎙️ Voice Input ({src_label})")
    audio_value = st.audio_input("Speak", label_visibility="collapsed")

    if audio_value is not None:
        audio_bytes = audio_value.getvalue()
        if st.session_state.last_audio_bytes != audio_bytes:
            st.session_state.last_audio_bytes = audio_bytes

            # Wipe previous results
            st.session_state.text_input = ""
            st.session_state.last_translation = ""
            st.session_state.last_translation_audio = None

            with st.spinner("Transcribing audio..."):
                with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                    tmp.write(audio_bytes)
                    tmp_path = tmp.name
                try:
                    transcribed = translator.transcribe_audio(tmp_path)
                    if transcribed:
                        st.session_state.text_input = transcribed
                except Exception as e:
                    st.error(f"Transcription error: {e}")
                finally:
                    if os.path.exists(tmp_path):
                        os.remove(tmp_path)

            # Auto-translate after transcription
            if st.session_state.text_input.strip():
                with st.spinner("Translating..."):
                    do_translate(st.session_state.text_input)

            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # --- LAYOUT ---
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
        st.session_state.text_input = input_text

    with col_mid:
        st.markdown("<div style='height: 100px;'></div>", unsafe_allow_html=True)
        if st.button("⇄", help="Swap Languages"):
            swap_languages()
            st.rerun()

    with col2:
        st.markdown(f"### {tar_label}")
        st.text_area(
            label=f"{tar_label} output",
            value=st.session_state.last_translation,
            height=250,
            disabled=True,
            label_visibility="collapsed"
        )
        if st.session_state.last_translation_audio is not None:
            st.audio(st.session_state.last_translation_audio, format="audio/mp3")

    st.markdown("<br>", unsafe_allow_html=True)

    # --- TRANSLATE BUTTON (manual, for typed text) ---
    if st.button("TRANSLATE NOW", type="primary", use_container_width=True):
        if st.session_state.text_input.strip():
            # Wipe previous translation before new one
            st.session_state.last_translation = ""
            st.session_state.last_translation_audio = None
            with st.spinner("Translating..."):
                do_translate(st.session_state.text_input)
            st.rerun()
        else:
            st.warning("Please enter text or record audio to translate.")

    st.markdown('</div>', unsafe_allow_html=True)

    # --- HISTORY ---
    if st.session_state.history:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### Translation History")
        for item in reversed(st.session_state.history[-3:]):
            direction_label = item.get('dir', '??').upper()
            src_text = item.get('src', '')[:50]
            tar_text = item.get('tar', '')[:50]
            st.markdown(f"""
            <div style="background: rgba(255,255,255,0.03); padding: 10px; border-radius: 10px; margin-bottom: 8px; border-left: 4px solid #6366f1;">
                <span style="color: #6366f1; font-weight: bold;">{direction_label}:</span>
                <span style="color: #f8fafc;"> {src_text}...</span>
                <span style="color: #a855f7;"> → </span>
                <span style="color: #f8fafc;">{tar_text}...</span>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
