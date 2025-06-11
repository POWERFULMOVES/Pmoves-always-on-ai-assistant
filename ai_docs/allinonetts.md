api_name: /generate_unified_tts
copy
from gradio_client import Client, handle_file

client = Client("http://127.0.0.1:7860/")
result = client.predict(
		text_input="Hello! This is a demonstration of the ULTIMATE TTS STUDIO. You can choose between ChatterboxTTS and Fish Speach for custom voice cloning or Kokoro TTS for high-quality pre-trained voices.",
		tts_engine="ChatterboxTTS",
		chatterbox_ref_audio=handle_file('https://github.com/gradio-app/gradio/raw/main/test/test_files/audio_sample.wav'),
		chatterbox_exaggeration=0.5,
		chatterbox_temperature=0.8,
		chatterbox_cfg_weight=0.5,
		chatterbox_chunk_size=300,
		chatterbox_seed=0,
		kokoro_voice="af_heart",
		kokoro_speed=1,
		fish_ref_audio=handle_file('https://github.com/gradio-app/gradio/raw/main/test/test_files/audio_sample.wav'),
		fish_ref_text=None,
		fish_temperature=0.8,
		fish_top_p=0.8,
		fish_repetition_penalty=1.1,
		fish_max_tokens=1024,
		fish_seed=None,
		gain_db=0,
		enable_eq=False,
		eq_bass=0,
		eq_mid=0,
		eq_treble=0,
		enable_reverb=False,
		reverb_room=0.3,
		reverb_damping=0.5,
		reverb_wet=0.3,
		enable_echo=False,
		echo_delay=0.3,
		echo_decay=0.5,
		enable_pitch=False,
		pitch_semitones=0,
		api_name="/generate_unified_tts"
)
print(result)
Accepts 31 parameters:
text_input str Default: "Hello! This is a demonstration of the ULTIMATE TTS STUDIO. You can choose between ChatterboxTTS and Fish Speach for custom voice cloning or Kokoro TTS for high-quality pre-trained voices."

The input value that is provided in the "📝 Text to synthesize" Textbox component.
tts_engine Literal['ChatterboxTTS', 'Kokoro TTS', 'Fish Speech'] Default: "ChatterboxTTS"

The input value that is provided in the "🎯 Select TTS Engine" Radio component.
chatterbox_ref_audio filepath Default: handle_file('https://github.com/gradio-app/gradio/raw/main/test/test_files/audio_sample.wav')

The input value that is provided in the "🎤 Reference Audio File (Optional)" Audio component. The FileData class is a subclass of the GradioModel class that represents a file object within a Gradio interface. It is used to store file data and metadata when a file is uploaded. Attributes: path: The server file path where the file is stored. url: The normalized server URL pointing to the file. size: The size of the file in bytes. orig_name: The original filename before upload. mime_type: The MIME type of the file. is_stream: Indicates whether the file is a stream. meta: Additional metadata used internally (should not be changed).

chatterbox_exaggeration float Default: 0.5

The input value that is provided in the "🎭 Exaggeration" Slider component.
chatterbox_temperature float Default: 0.8

The input value that is provided in the "🌡️ Temperature" Slider component.
chatterbox_cfg_weight float Default: 0.5

The input value that is provided in the "⚡ CFG Weight" Slider component.
chatterbox_chunk_size float Default: 300

The input value that is provided in the "📄 Chunk Size" Slider component.
chatterbox_seed float Default: 0

The input value that is provided in the "🎲 Seed (0=random)" Number component.
kokoro_voice Literal['af_heart', 'af_bella', 'af_nicole', 'af_aoede', 'af_kore', 'af_sarah', 'af_nova', 'af_sky', 'af_alloy', 'af_jessica', 'af_river', 'am_michael', 'am_fenrir', 'am_puck', 'am_echo', 'am_eric', 'am_liam', 'am_onyx', 'am_santa', 'am_adam', 'bf_emma', 'bf_isabella', 'bf_alice', 'bf_lily', 'bm_george', 'bm_fable', 'bm_lewis', 'bm_daniel', 'pf_dora', 'pm_alex', 'pm_santa', 'if_sara', 'im_nicola'] Default: "af_heart"

The input value that is provided in the "🎭 Select Voice" Dropdown component.
kokoro_speed float Default: 1

The input value that is provided in the "⚡ Speech Speed" Slider component.
fish_ref_audio filepath Default: handle_file('https://github.com/gradio-app/gradio/raw/main/test/test_files/audio_sample.wav')

The input value that is provided in the "🎤 Reference Audio File (Optional)" Audio component. The FileData class is a subclass of the GradioModel class that represents a file object within a Gradio interface. It is used to store file data and metadata when a file is uploaded. Attributes: path: The server file path where the file is stored. url: The normalized server URL pointing to the file. size: The size of the file in bytes. orig_name: The original filename before upload. mime_type: The MIME type of the file. is_stream: Indicates whether the file is a stream. meta: Additional metadata used internally (should not be changed).

fish_ref_text str | None Default: None

The input value that is provided in the "🗣️ Reference Text (Optional)" Textbox component.
fish_temperature float Default: 0.8

The input value that is provided in the "🌡️ Temperature" Slider component.
fish_top_p float Default: 0.8

The input value that is provided in the "🎭 Top P" Slider component.
fish_repetition_penalty float Default: 1.1

The input value that is provided in the "🔄 Repetition Penalty" Slider component.
fish_max_tokens float Default: 1024

The input value that is provided in the "🔢 Max Tokens" Slider component.
fish_seed float | None Default: None

The input value that is provided in the "🎲 Seed (None=random)" Number component.
gain_db float Default: 0

The input value that is provided in the "🎚️ Gain/Volume (dB)" Slider component.
enable_eq bool Default: False

The input value that is provided in the "Enable 3-Band EQ" Checkbox component.
eq_bass float Default: 0

The input value that is provided in the "🔈 Bass (dB)" Slider component.
eq_mid float Default: 0

The input value that is provided in the "🔉 Mid (dB)" Slider component.
eq_treble float Default: 0

The input value that is provided in the "🔊 Treble (dB)" Slider component.
enable_reverb bool Default: False

The input value that is provided in the "Enable Reverb" Checkbox component.
reverb_room float Default: 0.3

The input value that is provided in the "Room Size" Slider component.
reverb_damping float Default: 0.5

The input value that is provided in the "Damping" Slider component.
reverb_wet float Default: 0.3

The input value that is provided in the "Reverb Amount" Slider component.
enable_echo bool Default: False

The input value that is provided in the "Enable Echo" Checkbox component.
echo_delay float Default: 0.3

The input value that is provided in the "Echo Delay (s)" Slider component.
echo_decay float Default: 0.5

The input value that is provided in the "Echo Decay" Slider component.
enable_pitch bool Default: False

The input value that is provided in the "Enable Pitch Shift" Checkbox component.
pitch_semitones float Default: 0

The input value that is provided in the "Pitch (semitones)" Slider component.
Returns tuple of 2 elements
[0] filepath

The output value that appears in the "🎵 Generated Audio" Audio component.

[1] str

The output value that appears in the "📊 Status" Textbox component.
🎯 Choosing the Right Engine
ChatterboxTTS - Best for:

Custom voice cloning from reference audio
Matching specific speaking styles or accents
Creating voices from short audio samples
Fine control over speech characteristics
Kokoro TTS - Best for:

High-quality pre-trained voices
Consistent voice quality
Multiple language support
Faster generation (no reference audio needed)
Fish Speech - Best for:

Text-to-speech synthesis from text
Natural-sounding voice generation
Customization of speech characteristics
Advanced audio processing controls
💡 Pro Tips
Reference Audio: Use clear, 3-10 second samples for ChatterboxTTS and Fish Speech
Text Length: Kokoro has a 5000 character limit, ChatterboxTTS and Fish Speech can handle longer texts
Effects: Apply reverb for space, echo for depth, pitch shift for character voices
Voice Mixing: Blend Kokoro voices with formulas like "af_heart * 0.7 + af_bella * 0.3"
Fish Speech Quality: Uses clean, unprocessed output for best natural sound. Use Audio Effects section for any enhancements.
🎵 Audio Effects Guide
Gain/Volume: Boost or reduce overall audio level (-20 to +20 dB)
3-Band EQ: Fine-tune frequency response
Bass: Low frequencies (80-250 Hz) - warmth and fullness
Mid: Mid frequencies (250-4000 Hz) - clarity and presence
Treble: High frequencies (4000+ Hz) - brightness and air
Reverb: Simulates room acoustics (church, hall, studio)
Echo: Adds depth and space to voice
Pitch Shift: Change voice character (±12 semitones)
🎛️ EQ Tips
Boost Bass (+3 to +6 dB): Warmer, fuller voice
Cut Bass (-3 to -6 dB): Cleaner, less muddy sound
Boost Mid (+2 to +4 dB): More vocal presence and clarity
Boost Treble (+2 to +5 dB): Brighter, more articulate speech
Subtle is better: Small adjustments (1-3 dB) often work best