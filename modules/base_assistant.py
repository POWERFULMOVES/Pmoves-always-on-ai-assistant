from typing import List, Dict
import logging
import os
from modules.llm_provider import get_llm_response
from modules.utils import build_file_name_session
from RealtimeTTS import TextToAudioStream, SystemEngine
from elevenlabs import play
from elevenlabs.client import ElevenLabs
import pyttsx3
import time
from modules.assistant_config import get_config
from modules.gradio_tts import GradioTTS
import simpleaudio as sa


class PlainAssistant:
    def __init__(self, logger: logging.Logger, session_id: str):
        self.logger = logger
        self.session_id = session_id
        self.conversation_history = []

        # Get voice configuration
        self.voice_type = get_config("base_assistant.voice")
        self.elevenlabs_voice = get_config("base_assistant.elevenlabs_voice")

        # Initialize appropriate TTS engine
        if self.voice_type == "local":
            self.logger.info("🔊 Initializing local TTS engine")
            self.engine = pyttsx3.init()
            self.engine.setProperty("rate", 150)  # Speed of speech
            self.engine.setProperty("volume", 1.0)  # Volume level
        elif self.voice_type == "realtime-tts":
            self.logger.info("🔊 Initializing RealtimeTTS engine")
            self.engine = SystemEngine()
            self.stream = TextToAudioStream(
                self.engine, frames_per_buffer=256, playout_chunk_size=1024
            )
        elif self.voice_type == "elevenlabs":
            self.logger.info("🔊 Initializing ElevenLabs TTS engine")
            self.elevenlabs_client = ElevenLabs(api_key=os.getenv("ELEVEN_API_KEY"))
        elif self.voice_type == "gradio":
            self.logger.info("🔊 Initializing Gradio TTS engine")
            self.gradio_tts_client = GradioTTS()
        else:
            raise ValueError(f"Unsupported voice type: {self.voice_type}")

    def process_text(self, text: str) -> str:
        """Process text input and generate response"""
        try:
            # Check if text matches our last response
            if (
                self.conversation_history
                and text.strip().lower()
                in self.conversation_history[-1]["content"].lower()
            ):
                self.logger.info("🤖 Ignoring own speech input")
                return ""

            # Add user message to conversation history
            self.conversation_history.append({"role": "user", "content": text})
            
            # Create a string representation of the conversation history for the prompt
            prompt_history = "\n".join([f"{msg['role']}: {msg['content']}" for msg in self.conversation_history])

            # Generate response using configured brain
            self.logger.info(f"🤖 Processing text with configured brain...")
            response = get_llm_response(prompt=prompt_history, assistant_type="base_assistant")

            # Add assistant response to history
            self.conversation_history.append({"role": "assistant", "content": response})

            # Speak the response
            self.speak(response)

            return response

        except Exception as e:
            self.logger.error(f"❌ Error occurred: {str(e)}")
            raise

    def speak(self, text: str):
        """Convert text to speech using configured engine"""
        try:
            self.logger.info(f"🔊 Speaking: {text}")

            if self.voice_type == "local":
                self.engine.say(text)
                self.engine.runAndWait()

            elif self.voice_type == "realtime-tts":
                self.stream.feed(text)
                self.stream.play()

            elif self.voice_type == "elevenlabs":
                audio = self.elevenlabs_client.generate(
                    text=text,
                    voice=self.elevenlabs_voice,
                    model="eleven_turbo_v2",
                    stream=False,
                )
                play(audio)
            
            elif self.voice_type == "gradio":
                audio_file = build_file_name_session("response.wav", self.session_id)
                self.gradio_tts_client.say(text, audio_file)
                
                # Play the audio file
                wave_obj = sa.WaveObject.from_wave_file(audio_file)
                play_obj = wave_obj.play()
                play_obj.wait_done()
                os.remove(audio_file)

            self.logger.info(f"🔊 Spoken: {text}")

        except Exception as e:
            self.logger.error(f"❌ Error in speech synthesis: {str(e)}")
            raise
