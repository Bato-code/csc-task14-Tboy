import torch
import transformers
import streamlit as st
import whisper
import io
from gtts import gTTS
from transformers import MarianMTModel, MarianTokenizer

# Silence transformers progress bars to avoid OSError on some environments
transformers.utils.logging.set_verbosity_error()

class TranslatorEngine:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.models = {}
        self.tokenizers = {}
        self.whisper_model = None

    def load_model(self, direction="en-fr"):
        """Loads the model and tokenizer based on direction."""
        model_name = "Helsinki-NLP/opus-mt-en-fr" if direction == "en-fr" else "Helsinki-NLP/opus-mt-fr-en"
        
        if model_name not in self.models:
            self.tokenizers[model_name] = MarianTokenizer.from_pretrained(model_name)
            self.models[model_name] = MarianMTModel.from_pretrained(model_name).to(self.device)
        
        return self.tokenizers[model_name], self.models[model_name]

    @st.cache_resource(show_spinner=False)
    def get_resources_cached(_self, direction):
        """Cached version for Streamlit."""
        return _self.load_model(direction)

    def translate(self, text, direction="en-fr"):
        """Translates text between English and French."""
        if not text.strip():
            return ""
        
        tokenizer, model = self.get_resources_cached(direction)
        
        inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True).to(self.device)
        
        with torch.no_grad():
            translated_tokens = model.generate(**inputs)
        
        result = tokenizer.batch_decode(translated_tokens, skip_special_tokens=True)[0]
        return result

    def load_whisper(self):
        if self.whisper_model is None:
            # Load tiny whisper model for much faster CPU execution
            self.whisper_model = whisper.load_model("tiny", device=self.device)
        return self.whisper_model

    @st.cache_resource(show_spinner=False)
    def get_whisper_cached(_self):
        return _self.load_whisper()

    def transcribe_audio(self, audio_file_path):
        """Transcribes audio from a file path using Whisper."""
        model = self.get_whisper_cached()
        result = model.transcribe(audio_file_path)
        return result.get("text", "").strip()

    def generate_audio(self, text, lang="fr"):
        """Generates TTS audio stream from text using gTTS."""
        if not text.strip():
            return None
        try:
            tts = gTTS(text=text, lang=lang, slow=False)
            fp = io.BytesIO()
            tts.write_to_fp(fp)
            fp.seek(0)
            return fp
        except Exception as e:
            print(f"TTS Error: {e}")
            return None

# Singleton instance
translator = TranslatorEngine()
