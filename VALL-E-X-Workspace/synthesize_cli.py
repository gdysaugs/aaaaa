import argparse
from utils.generation import SAMPLE_RATE, generate_audio, preload_models
from scipy.io.wavfile import write as write_wav
import os
import time

def main():
    parser = argparse.ArgumentParser(description="Synthesize audio from text using VALL-E X.")
    parser.add_argument("--text", type=str, required=True, help="Text to synthesize.")
    parser.add_argument("--prompt_name", type=str, required=True, help="Name of the voice prompt to use (must exist in /app/customs).")
    parser.add_argument("--output_filename", type=str, default="output_cli.wav", help="Filename for the output audio in /app/output directory.")
    parser.add_argument("--language", type=str, default="en", choices=["en", "zh", "ja", "mix"], help="Language of the text or 'mix' for code-switching.")

    args = parser.parse_args()

    print("Loading models...")
    preload_models()

    output_path = os.path.join("/app/output", args.output_filename)

    print(f"Synthesizing audio for text: \"{args.text}\" using prompt: {args.prompt_name}")
    start_time = time.time()
    audio_array = generate_audio(args.text, prompt=args.prompt_name, language=args.language)
    end_time = time.time()
    print(f"Audio synthesis completed in {end_time - start_time:.2f} seconds.")

    write_wav(output_path, SAMPLE_RATE, audio_array)
    print(f"Audio saved to {output_path}")

if __name__ == "__main__":
    main() 