from gradio_client import Client, handle_file
import gradio_client
import logging
import time
from modules.assistant_config import get_config
import os

class GradioTTS:
    def __init__(self,
                 ):
        active_engine_name = get_config("gradio_tts.active_engine")
        engine_config = get_config(f"gradio_tts.engines.{active_engine_name}")
        
        if not engine_config:
            raise ValueError(f"Configuration for active engine '{active_engine_name}' not found.")

        server_url = engine_config.get("server_url", "http://127.0.0.1:7860/")
        self.client = Client(server_url)
        self.last_inference_time = 0
        self.engine_type = engine_config.get("type")
        
        self.tts_engine_map = {
            "chatterbox": "ChatterboxTTS",
            "kokoro": "Kokoro TTS",
            "fish": "Fish Speech"
        }

    def say(self, text: str, file_path: str) -> None:
        """
        Generates audio from text using the Gradio Unified TTS API and saves it to a file.
        """
        try:
            start_time = time.time()
            
            active_engine_name = get_config("gradio_tts.active_engine")
            engine_config = get_config(f"gradio_tts.engines.{active_engine_name}")
            effects_config = get_config("gradio_tts.effects")
            
            ref_audio_path = get_config("gradio_tts.reference_audio")
            if not os.path.exists(ref_audio_path):
                logging.warning(f"Reference audio file not found at {ref_audio_path}. Using placeholder.")
                ref_audio = handle_file('https://github.com/gradio-app/gradio/raw/main/test/test_files/audio_sample.wav')
            else:
                ref_audio = handle_file(ref_audio_path)
            
            tts_engine_name = self.tts_engine_map.get(self.engine_type)

            if not tts_engine_name:
                raise ValueError(f"Unsupported TTS engine type in config: {self.engine_type}")

            result = self.client.predict(
                text_input=text,
                tts_engine=tts_engine_name,
                chatterbox_ref_audio=ref_audio,
                chatterbox_exaggeration=engine_config.get("exaggeration"),
                chatterbox_temperature=engine_config.get("temperature"),
                chatterbox_cfg_weight=engine_config.get("cfg_weight"),
                chatterbox_chunk_size=engine_config.get("chunk_size"),
                chatterbox_seed=engine_config.get("seed"),
                kokoro_voice=engine_config.get("voice"),
                kokoro_speed=engine_config.get("speed"),
                fish_ref_audio=ref_audio,
                fish_ref_text=None,
                fish_temperature=engine_config.get("temperature"),
                fish_top_p=engine_config.get("top_p"),
                fish_repetition_penalty=engine_config.get("repetition_penalty"),
                fish_max_tokens=engine_config.get("max_tokens"),
                fish_seed=None,
                gain_db=effects_config.get("gain_db", 0),
                enable_eq=effects_config.get("enable_eq", False),
                eq_bass=effects_config.get("eq_bass", 0),
                eq_mid=effects_config.get("eq_mid", 0),
                eq_treble=effects_config.get("eq_treble", 0),
                enable_reverb=effects_config.get("enable_reverb", False),
                reverb_room=effects_config.get("reverb_room", 0.3),
                reverb_damping=effects_config.get("reverb_damping", 0.5),
                reverb_wet=effects_config.get("reverb_wet", 0.3),
                enable_echo=effects_config.get("enable_echo", False),
                echo_delay=effects_config.get("echo_delay", 0.3),
                echo_decay=effects_config.get("echo_decay", 0.5),
                enable_pitch=effects_config.get("enable_pitch", False),
                pitch_semitones=effects_config.get("pitch_semitones", 0),
                api_name="/generate_unified_tts"
            )
            end_time = time.time()
            self.last_inference_time = end_time - start_time
            logging.info(f"Gradio TTS inference time: {self.last_inference_time:.2f}s")
            
            generated_audio_path = result[0]

            import shutil
            shutil.copy(generated_audio_path, file_path)
            
            logging.info(f"Audio saved to {file_path}")

        except Exception as e:
            logging.error(f"Error during Gradio TTS generation: {e}")
            if isinstance(e, gradio_client.exceptions.AppError):
                logging.error(f"Gradio App Error details: {e}")


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    # Ensure you have a reference audio file for testing, e.g., 'reference.wav'
    if not os.path.exists("reference.wav"):
        import requests
        url = 'https://github.com/gradio-app/gradio/raw/main/test/test_files/audio_sample.wav'
        r = requests.get(url)
        with open("reference.wav", 'wb') as f:
            f.write(r.content)
        print("Downloaded a sample reference audio file as reference.wav")

    # Update config for test
    from modules.assistant_config import _CONFIG, _save_config
    # Load the config and set the reference audio for the test
    config = _CONFIG
    # Make sure the test points to the correct URL if you are running it
    # This will now be read from the active engine's config
    # config['gradio_tts']['engines']['kokoro_default']['server_url'] = 'http://100.91.242.98:42003/'
    config['gradio_tts']['reference_audio'] = 'reference.wav'
    
    # Example of switching engine preset for testing
    config['gradio_tts']['active_engine'] = 'kokoro_default'

    # Example of using an effect
    config['gradio_tts']['effects']['enable_reverb'] = True
    config['gradio_tts']['effects']['reverb_room'] = 0.8
    _save_config(config)

    tts = GradioTTS()
    text_to_speak = "Hello, this is a test of the all in one Gradio TTS API with a multi-engine setup."
    output_filename = "test_gradio_allinone.wav"
    tts.say(text_to_speak, output_filename)
    print(f"Test audio saved to {output_filename}") 