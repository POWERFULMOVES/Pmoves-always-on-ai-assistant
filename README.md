# "Always-On" AI Assistant
> A pattern for a highly configurable, always-on AI Assistant powered by multiple Language Models and Text-to-Speech engines.

![ada-deepseek-v3.png](./images/ada-deepseek-v3.png)

## 🚀 Quick Start

1.  **Environment Setup**:
    -   Copy the example environment file: `cp .env.sample .env`
    -   Update `.env` with your API keys (`DEEPSEEK_API_KEY`, `ELEVEN_API_KEY`, etc.).

2.  **Install Dependencies**:
    -   `uv sync`
    -   (Optional) To manage python versions: `uv python install 3.11`

3.  **Configuration**:
    -   Review and customize `assistant_config.yml`. This is the central control panel for your assistants. Here you can define and switch between different "brains" (LLMs) and "voices" (TTS engines).

4.  **Launch the Assistant**:
    -   To use the new management commands, start the assistant by pointing it to the correct command file:
        ```bash
        uv run python main_typer_assistant.py awaken --typer-file commands/voice_management.py --scratchpad scratchpad.md --mode execute
        ```

##  Assistant Architecture
> The assistant's capabilities are defined in `assistant_config.yml`.

### 🧠 Brains (Language Models)
The assistant supports multiple LLM providers. You can define different models in the `brains` section of the config and switch between them conversationally.

-   **Providers**: `Deepseek`, `Ollama`, `LM Studio` (or any other OpenAI-compatible endpoint).
-   **Configuration**: Define each brain in the `brains:` section of `assistant_config.yml`.
-   **Switching**: Each assistant (`typer_assistant` and `base_assistant`) has an `active_brain` key to specify which brain to use.

### 🎤 Mouth (Text-to-Speech)
The assistant uses a highly flexible, multi-engine TTS system powered by a Gradio backend.

-   **Engines**: Supports multiple TTS models like `ChatterboxTTS`, `Kokoro TTS`, and `Fish Speech`.
-   **Multi-Instance Support**: You can run multiple TTS instances on different URLs and define them in the `gradio_tts.engines` section of the config.
-   **Voice Cloning**: Use the `reference_audio` path to specify a `.wav` file for voice cloning with `ChatterboxTTS` or `Fish Speech`.
-   **Audio Effects**: Apply post-processing effects like `reverb`, `echo`, `EQ`, and `pitch shifting`, configured in the `gradio_tts.effects` section.

### 👂 Ears (Speech-to-Text)
-   **Engine**: `RealtimeSTT` provides fast and accurate local speech-to-text.

## Conversational Commands
When the Typer assistant is running with `commands/voice_management.py`, you can use the following commands by speaking to the assistant (e.g., "Ada, set the active voice to 'morgan'").

### Voice Cloning Management
-   **`add-voice`**: Adds a new voice sample for cloning.
    -   *Example*: "add a new voice named 'morgan' from the file path '/path/to/morgan.wav'"
-   **`list-voices`**: Shows all available voice samples from the `voices/` directory.
-   **`set-voice`**: Sets the active voice to use for cloning.
    -   *Example*: "set the active voice to 'morgan'"

### TTS Engine Management
-   **`list-engines`**: Lists all configured TTS engine instances from your config.
-   **`set-engine`**: Switches the active TTS engine.
    -   *Example*: "set the active engine to 'chatterbox_clone'"

### Brain (LLM) Management
-   **`list-brains`**: Lists all configured LLM brains from your config.
-   **`set-brain`**: Switches the active brain for an assistant.
    -   *Example*: "set the brain for the typer assistant to 'lmstudio_default'"

## Base Assistant
For a direct, conversational chat session (without the Typer commands), run:
```bash
uv run python main_base_assistant.py chat
```

## Resources
- **Local STT**: [RealtimeSTT](https://github.com/KoljaB/RealtimeSTT)
- **Whisper Implementation**: [faster-whisper](https://github.com/SYSTRAN/faster-whisper)
- **ElevenLabs Voices**: [ElevenLabs Models](https://elevenlabs.io/docs/developer-guides/models#older-models)