 Install the Python client (docs) if you don't already have it installed.

copy
$ pip install gradio_client
2. Find the API endpoint below corresponding to your desired function in the app. Copy the code snippet, replacing the placeholder values with your own input data. Or use the 
API Recorder

 to automatically generate your API requests.

api_name: /partial
copy
from gradio_client import Client, handle_file

client = Client("http://127.0.0.1:7860/")
result = client.predict(
		text="Hello!!",
		reference_id="Hello!!",
		reference_audio=handle_file('https://github.com/gradio-app/gradio/raw/main/test/test_files/audio_sample.wav'),
		reference_text="",
		max_new_tokens=0,
		chunk_length=300,
		top_p=0.8,
		repetition_penalty=1.1,
		temperature=0.8,
		seed=0,
		use_memory_cache="on",
		api_name="/partial"
)
print(result)
Accepts 11 parameters:
text str Required

The input value that is provided in the "Input Text" Textbox component.
reference_id str Required

The input value that is provided in the "Reference ID" Textbox component.
reference_audio filepath Required

The input value that is provided in the "Reference Audio" Audio component. The FileData class is a subclass of the GradioModel class that represents a file object within a Gradio interface. It is used to store file data and metadata when a file is uploaded. Attributes: path: The server file path where the file is stored. url: The normalized server URL pointing to the file. size: The size of the file in bytes. orig_name: The original filename before upload. mime_type: The MIME type of the file. is_stream: Indicates whether the file is a stream. meta: Additional metadata used internally (should not be changed).

reference_text str Default: ""

The input value that is provided in the "Reference Text" Textbox component.
max_new_tokens float Default: 0

The input value that is provided in the "Maximum tokens per batch, 0 means no limit" Slider component.
chunk_length float Default: 300

The input value that is provided in the "Iterative Prompt Length, 0 means off" Slider component.
top_p float Default: 0.8

The input value that is provided in the "Top-P" Slider component.
repetition_penalty float Default: 1.1

The input value that is provided in the "Repetition Penalty" Slider component.
temperature float Default: 0.8

The input value that is provided in the "Temperature" Slider component.
seed float Default: 0

The input value that is provided in the "Seed" Number component.
use_memory_cache Literal['on', 'off'] Default: "on"

The input value that is provided in the "Use Memory Cache" Radio component.
Returns tuple of 2 elements
[0] filepath

The output value that appears in the "Generated Audio" Audio component.

[1] str

The output value that appears in the "Error Message" Html component.