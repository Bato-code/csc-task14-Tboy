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

# Initialize session state for direction
if 'direction' not in st.session_state:
    st.session_state.direction = "en-fr"
if 'last_translation' not in st.session_state:
    st.session_state.last_translation = ""

def swap_languages():
    st.session_state.direction = "fr-en" if st.session_state.direction == "en-fr" else "en-fr"
    st.session_state.last_translation = ""

def main():
    # Render stylized header with student metadata
    render_header("Gbapre Timothy Tubolayefa", "20231407812", "CYB")

    # Define labels based on direction
    src_label = "English" if st.session_state.direction == "en-fr" else "French"
    tar_label = "French" if st.session_state.direction == "en-fr" else "English"

    # Main Translation Interface wrapped in Glass Card
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    
    # Audio input
    st.markdown(f"### Voice Input ({src_label})")
    audio_value = st.audio_input("Speak", label_visibility="collapsed")
    
    if audio_value is not None:
        audio_bytes = audio_value.getvalue()
        if st.session_state.get('last_audio_bytes') != audio_bytes:
            st.session_state.last_audio_bytes = audio_bytes
            with st.spinner("Transcribing..."):
                with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                    tmp.write(audio_bytes)
                    tmp_path = tmp.name
                try:
                    transcribed = translator.transcribe_audio(tmp_path)
                    if transcribed:
                        st.session_state.text_input = transcribed
                        st.rerun()
                except Exception as e:
                    st.error(f"Transcription error: {e}")
                finally:
                    if os.path.exists(tmp_path):
                        os.remove(tmp_path)

    st.markdown("<br>", unsafe_allow_html=True)

    # Layout with language swap in middle
    col1, col_mid, col2 = st.columns([7, 1, 7])

    with col1:
        st.markdown(f"### {src_label}")
        if 'text_input' not in st.session_state:
            st.session_state.text_input = ""

        input_text = st.text_area(
            label=f"Input {src_label}",
            placeholder=f"Enter {src_label} text here...",
            value=st.session_state.text_input,
            height=250,
            label_visibility="collapsed",
            key="text_area_input" # Changed key to avoid conflict
        )
        # Syncing state
        st.session_state.text_input = input_text
        
    with col_mid:
        if st.button("⇄", help="Swap Languages", key="swap_languages_btn"):
            swap_languages()
            st.rerun()

    with col2:
        st.markdown(f"### {tar_label}")
        output_placeholder = st.empty()
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Process translation button
    if st.button("TRANSLATE NOW", type="primary", use_container_width=True):
        if st.session_state.text_input.strip():
            with st.spinner("Translating..."):
                try:
                    translation = translator.translate(st.session_state.text_input, direction=st.session_state.direction)
                    st.session_state.last_translation = translation
                    
                    target_lang_code = "fr" if st.session_state.direction == "en-fr" else "en"
                    audio_fp = translator.generate_audio(translation, lang=target_lang_code)
                    if audio_fp:
                        st.session_state.last_translation_audio = audio_fp.getvalue()
                    else:
                        st.session_state.last_translation_audio = None
                except Exception as e:
                    st.error(f"Translation Error: {e}")
        else:
            st.warning("Please enter text or record audio to translate.")

    with col2:
        output_placeholder.text_area(
            label=f"{src_label} output",
            value=st.session_state.last_translation,
            height=250,
            disabled=True,
            label_visibility="collapsed"
        )

        if st.session_state.get('last_translation_audio') is not None:
            st.audio(st.session_state.last_translation_audio, format="audio/mp3")

    st.markdown('</div>', unsafe_allow_html=True) # End Glass Card

    # Simplified History wrapped in its own card
    if 'history' not in st.session_state:
        st.session_state.history = []
    
    if st.session_state.last_translation and (not st.session_state.history or st.session_state.history[-1]['tar'] != st.session_state.last_translation):
        st.session_state.history.append({
            "dir": st.session_state.direction,
            "src": st.session_state.text_input,
            "tar": st.session_state.last_translation
        })

    if st.session_state.history:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### Translation History")
        for item in reversed(st.session_state.history[-3:]):
            direction_label = item.get('dir', '??').upper()
            src_text = item.get('src', '')[:50]
            tar_text = item.get('tar', '')[:50]
            st.markdown(f"""
            <div style="background: rgba(255,255,255,0.03); padding: 10px; border-radius: 10px; margin-bottom: 8px; border-left: 4px solid #6366f1;">
                <span style="color: #6366f1; font-weight: bold;">{direction_label}:</span> {src_text}... → {tar_text}...
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
