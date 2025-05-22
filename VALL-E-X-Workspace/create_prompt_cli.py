import argparse
from utils.prompt_making import make_prompt
from utils.generation import preload_models

def main():
    parser = argparse.ArgumentParser(description="Create a voice prompt for VALL-E X.")
    parser.add_argument("--name", type=str, required=True, help="Name for the voice prompt.")
    parser.add_argument("--audio_path", type=str, required=True, help="Path to the audio prompt file (e.g., /app/custom_prompts/my_audio.wav).")
    parser.add_argument("--transcript", type=str, default=None, help="Transcript of the audio. If None, Whisper will be used.")
    
    args = parser.parse_args()

    print("Loading models...")
    preload_models() # Ensure models are loaded

    print(f"Creating voice prompt '{args.name}' from audio: {args.audio_path}")
    make_prompt(name=args.name, audio_prompt_path=args.audio_path, transcript=args.transcript)
    print(f"Voice prompt '{args.name}' created successfully in /app/customs/{args.name}.npz and /app/customs/{args.name}.txt")

if __name__ == "__main__":
    main() 