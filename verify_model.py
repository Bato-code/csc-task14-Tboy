from translator_engine import translator

def test_translation():
    test_text = "Artificial Intelligence is the future of technology."
    print(f"English: {test_text}")
    try:
        translation = translator.translate(test_text)
        print(f"French: {translation}")
        if "Intelligence Artificielle" in translation or "intelligence artificielle" in translation:
            print("SUCCESS: Translation is accurate.")
        else:
            print("WARNING: Translation might be incorrect.")
    except Exception as e:
        print(f"FAILURE: Error during translation: {e}")

if __name__ == "__main__":
    test_translation()
