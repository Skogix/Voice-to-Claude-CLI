#!/usr/bin/env python3
"""
Voice-to-Claude-CLI: Local voice transcription using whisper.cpp
"""
import sys
import tempfile
import requests
import sounddevice as sd
import scipy.io.wavfile as wav

# Configuration
SAMPLE_RATE = 16000  # Whisper expects 16kHz audio
DURATION = 5  # Default recording duration in seconds
WHISPER_URL = "http://127.0.0.1:2022/v1/audio/transcriptions"


class VoiceTranscriber:
    def __init__(self):
        # Check if whisper.cpp server is running
        try:
            response = requests.get("http://127.0.0.1:2022/health", timeout=2)
            if response.status_code == 200:
                print("✓ Connected to whisper.cpp server")
            else:
                raise ConnectionError("Whisper server returned unexpected status")
        except requests.exceptions.RequestException:
            print("✗ Error: whisper.cpp server is not running on port 2022")
            print("\nPlease start the whisper server:")
            print("cd /tmp/whisper.cpp")
            print("./build/bin/whisper-server --model models/ggml-base.en.bin \\")
            print("  --host 127.0.0.1 --port 2022 \\")
            print("  --inference-path '/v1/audio/transcriptions' \\")
            print("  --threads 4 --processors 1 --convert --print-progress")
            sys.exit(1)

    def record_audio(self, duration=DURATION):
        """Record audio from microphone"""
        print(f"\nRecording for {duration} seconds... Speak now!")
        audio_data = sd.rec(int(duration * SAMPLE_RATE),
                           samplerate=SAMPLE_RATE,
                           channels=1,
                           dtype='int16')
        sd.wait()  # Wait until recording is finished
        print("Recording finished!")
        return audio_data

    def transcribe_audio(self, audio_data):
        """Convert audio to text using whisper.cpp HTTP API"""
        # Save audio to temporary WAV file
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
            wav.write(tmp_file.name, SAMPLE_RATE, audio_data)
            tmp_filename = tmp_file.name

        try:
            # Transcribe using whisper.cpp server
            print("Transcribing...")
            with open(tmp_filename, 'rb') as audio_file:
                files = {'file': ('audio.wav', audio_file, 'audio/wav')}
                data = {'model': 'whisper-1'}  # Required by OpenAI-compatible API

                response = requests.post(WHISPER_URL, files=files, data=data, timeout=30)
                response.raise_for_status()

                result = response.json()
                transcribed_text = result.get("text", "").strip()
                return transcribed_text
        except requests.exceptions.RequestException as e:
            print(f"Error transcribing audio: {e}")
            return ""
        finally:
            # Clean up temporary file
            import os
            os.unlink(tmp_filename)

    def run_interactive(self):
        """Run interactive voice transcription session"""
        print("\n" + "="*60)
        print("Voice Transcription (whisper.cpp)")
        print("="*60)
        print("\nCommands:")
        print("  - Press ENTER to start recording")
        print("  - Type 'quit' or 'exit' to end session")
        print("="*60 + "\n")

        while True:
            try:
                user_input = input("\n[Press ENTER to record, or type 'quit' to exit]: ").strip()

                # Handle commands
                if user_input.lower() in ['quit', 'exit']:
                    print("\nGoodbye!")
                    break
                elif user_input:
                    # Ignore other typed input
                    print("Press ENTER to record, or type 'quit' to exit")
                    continue
                else:
                    # Record and transcribe
                    audio_data = self.record_audio()
                    message = self.transcribe_audio(audio_data)

                    # Display transcription
                    if message:
                        print("\n" + "-"*60)
                        print("Transcription:")
                        print("-"*60)
                        print(message)
                        print("-"*60)
                    else:
                        print("No speech detected. Please try again.")

            except KeyboardInterrupt:
                print("\n\nSession interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"\nError: {e}")
                print("Please try again.")


def main():
    try:
        transcriber = VoiceTranscriber()
        transcriber.run_interactive()
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
