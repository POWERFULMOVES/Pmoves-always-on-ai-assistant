import typer
import os
import shutil
import yaml
from typing import List

app = typer.Typer()
VOICES_DIR = "voices"
CONFIG_FILE = "assistant_config.yml"

@app.command("add-voice")
def add_voice(
    voice_name: str = typer.Option(..., "--name", "-n", help="Name of the voice to add."),
    file_path: str = typer.Option(..., "--file", "-f", help="Path to the audio file for the voice."),
):
    """Adds a new voice for cloning."""
    if not os.path.exists(file_path):
        print(f"❌ Error: File not found at {file_path}")
        raise typer.Exit(code=1)

    if not os.path.exists(VOICES_DIR):
        os.makedirs(VOICES_DIR)

    file_extension = os.path.splitext(file_path)[1]
    destination_path = os.path.join(VOICES_DIR, f"{voice_name}{file_extension}")
    
    try:
        shutil.copy(file_path, destination_path)
        print(f"✅ Voice '{voice_name}' added from {file_path}")
    except Exception as e:
        print(f"❌ Error adding voice: {e}")
        raise typer.Exit(code=1)

@app.command("list-voices")
def list_voices():
    """Lists all available voices."""
    if not os.path.exists(VOICES_DIR) or not os.listdir(VOICES_DIR):
        print("🤷 No voices found. Add one with the 'add-voice' command.")
        return

    print("Available voices:")
    for voice_file in os.listdir(VOICES_DIR):
        print(f"  - {os.path.splitext(voice_file)[0]}")

@app.command("set-voice")
def set_voice(
    voice_name: str = typer.Argument(..., help="Name of the voice to set as active.")
):
    """Sets the active voice for cloning in the assistant configuration."""
    voice_file_found = None
    for file in os.listdir(VOICES_DIR):
        if os.path.splitext(file)[0] == voice_name:
            voice_file_found = file
            break
    
    if not voice_file_found:
        print(f"❌ Error: Voice '{voice_name}' not found.")
        list_voices()
        raise typer.Exit(code=1)

    voice_path = os.path.join(VOICES_DIR, voice_file_found)

    try:
        with open(CONFIG_FILE, 'r') as f:
            config = yaml.safe_load(f)

        if 'gradio_tts' not in config:
            config['gradio_tts'] = {}
        
        config['gradio_tts']['reference_audio'] = voice_path
        
        with open(CONFIG_FILE, 'w') as f:
            yaml.dump(config, f)
        
        print(f"✅ Active voice set to '{voice_name}' ({voice_path})")

    except Exception as e:
        print(f"❌ Error updating config file: {e}")
        raise typer.Exit(code=1)

@app.command("list-engines")
def list_engines():
    """Lists all configured TTS engines."""
    try:
        with open(CONFIG_FILE, 'r') as f:
            config = yaml.safe_load(f)
        
        engines = config.get('gradio_tts', {}).get('engines', {})
        if not engines:
            print("🤷 No engines found in the configuration.")
            return

        active_engine = config.get('gradio_tts', {}).get('active_engine')
        print("Available TTS engines:")
        for engine_name, engine_config in engines.items():
            details = f"type: {engine_config.get('type', 'N/A')}, url: {engine_config.get('server_url', 'N/A')}"
            if engine_name == active_engine:
                print(f"  - {engine_name} (active) -> {details}")
            else:
                print(f"  - {engine_name} -> {details}")

    except Exception as e:
        print(f"❌ Error reading config file: {e}")
        raise typer.Exit(code=1)

@app.command("set-engine")
def set_engine(
    engine_name: str = typer.Argument(..., help="Name of the engine to set as active.")
):
    """Sets the active TTS engine in the assistant configuration."""
    try:
        with open(CONFIG_FILE, 'r') as f:
            config = yaml.safe_load(f)

        engines = config.get('gradio_tts', {}).get('engines', {})
        if engine_name not in engines:
            print(f"❌ Error: Engine '{engine_name}' not found in configuration.")
            list_engines()
            raise typer.Exit(code=1)

        config['gradio_tts']['active_engine'] = engine_name
        
        with open(CONFIG_FILE, 'w') as f:
            yaml.dump(config, f)
        
        print(f"✅ Active TTS engine set to '{engine_name}'")

    except Exception as e:
        print(f"❌ Error updating config file: {e}")
        raise typer.Exit(code=1)

@app.command("list-brains")
def list_brains():
    """Lists all configured brains."""
    try:
        with open(CONFIG_FILE, 'r') as f:
            config = yaml.safe_load(f)
        
        brains = config.get('brains', {})
        if not brains:
            print("🤷 No brains found in the configuration.")
            return

        typer_brain = config.get('typer_assistant', {}).get('active_brain')
        base_brain = config.get('base_assistant', {}).get('active_brain')

        print("Available Brains:")
        for brain_name, brain_config in brains.items():
            details = f"type: {brain_config.get('type', 'N/A')}, model: {brain_config.get('model', 'N/A')}"
            active_for = []
            if brain_name == typer_brain:
                active_for.append("Typer Assistant")
            if brain_name == base_brain:
                active_for.append("Base Assistant")
            
            if active_for:
                print(f"  - {brain_name} (active for {', '.join(active_for)}) -> {details}")
            else:
                print(f"  - {brain_name} -> {details}")

    except Exception as e:
        print(f"❌ Error reading config file: {e}")
        raise typer.Exit(code=1)

@app.command("set-brain")
def set_brain(
    assistant: str = typer.Option(..., "--assistant", "-a", help="The assistant to configure ('typer' or 'base')."),
    brain_name: str = typer.Argument(..., help="Name of the brain to set as active.")
):
    """Sets the active brain for an assistant."""
    assistant_key = f"{assistant.lower()}_assistant"
    if assistant.lower() not in ["typer", "base"]:
        print("❌ Error: Assistant must be 'typer' or 'base'.")
        raise typer.Exit(code=1)

    try:
        with open(CONFIG_FILE, 'r') as f:
            config = yaml.safe_load(f)

        brains = config.get('brains', {})
        if brain_name not in brains:
            print(f"❌ Error: Brain '{brain_name}' not found in configuration.")
            list_brains()
            raise typer.Exit(code=1)

        config[assistant_key]['active_brain'] = brain_name
        
        with open(CONFIG_FILE, 'w') as f:
            yaml.dump(config, f)
        
        print(f"✅ Active brain for {assistant} assistant set to '{brain_name}'")

    except Exception as e:
        print(f"❌ Error updating config file: {e}")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app() 