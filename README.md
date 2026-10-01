# On-Premise Document Extraction with Local Vision-Language Models

A fully local, CPU-based proof-of-concept for extracting predefined information fields from scanned document images using vision-language models through Ollama.

The application provides a web interface for uploading images and reviewing extracted information. It demonstrates that confidential document images can be processed entirely on-premise, without external APIs or cloud processing.

Gemma 3 4B was selected for the prototype after comparing it with LLaVA 7B and Granite 3.2 Vision 2B across extraction quality, runtime, and resource efficiency.

## Features

- Upload scanned document images through a drag-and-drop interface

- Process images locally using Gemma 3 4B through Ollama

- Run model inference on CPU

- Extract seller name, address, contact number, and purchase date from receipt images

- Display extracted information in a readable format

## Prerequisites

- Python 3.8+
- Ollama installed and running locally
- Gemma 3 4B model pulled in Ollama

## Setup Instructions

1. Clone this repository
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Make sure Ollama is running locally with the Llama 3.2 Vision model:
   ```
   ollama pull gemma3:4b
   ```
4. Ensure Ollama is running locally

    If Ollama is not already running, start it in a separate terminal:
    ```
   ollama serve
   ```


5. Run the application:
   ```
   python app/app.py
   ```

6. Open your browser and navigate to:
   ```
   http://127.0.0.1:5000
   ```

## Using the Application

1. Drag and drop a receipt image onto the upload area, or click to select a file.
2. Click "Extract Information" to process the image.
3. Review the extracted seller name, address, contact number, and purchase date displayed below the image.

## Ollama API Integration

The application communicates with the local Ollama service via its HTTP API:
- Default API endpoint: http://localhost:11434/api/generate
- Selected model: gemma3:4b
- Image input: Base64-encoded image sent with the extraction prompt

Image processing and model inference take place locally, without sending document content to external APIs or cloud services.
## Troubleshooting

- If you encounter connection errors to Ollama, ensure the service is running by checking:
  ```
  curl http://localhost:11434/api/tags
  ```
- If the service is not running, start it:

    If the vision model is not available, pull it with:
    ```
    ollama serve
    ```

- If the vision model is not available, pull it with:
  ```
  ollama pull gemma3:4b
  ```

- Confirm that it appears in the installed model list:
    ```
    ollama list
    ```
- Check the Flask server logs for detailed error information 