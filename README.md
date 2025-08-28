# SpeakWise AI 🗣️✨

SpeakWise AI is an intelligent, AI-powered conversation partner designed to help you improve your English speaking skills. Get real-time, multi-layered feedback on your pronunciation, grammar, and phrasing in a natural, conversational setting. This project is built with a focus on being fully self-hosted, private, and free to run.

---

## 🚀 Introduction

Practicing a new language can be challenging, especially without a conversation partner. SpeakWise AI solves this by providing a safe and insightful space to speak English freely. Unlike standard tools, SpeakWise AI captures the nuances of your speech—including pauses and hesitations—and provides three layers of feedback from a powerful AI tutor: a natural conversational reply, a more fluent way to phrase your sentence, and a detailed grammatical analysis, all delivered with a high-quality, natural-sounding AI voice.

## ⭐ Key Features

* **🎙️ High-Fidelity Audio Capture:** Records your voice using the browser's MediaRecorder API, preserving the quality of your speech.

* **🧠 Self-Hosted Transcription with Pause Detection:** Uses the powerful, self-hosted Whisper model to transcribe your speech, accurately representing pauses and hesitations.

* **🤖 Advanced AI Feedback:** Leverages the Gemini API to provide three distinct layers of feedback for every utterance:

    1. **A natural, conversational reply**.

    2. **A suggested rephrasing for better fluency.**

    3. **A detailed analysis of grammatical errors.**

* **🔊 Natural AI Voice:** Generates the AI's spoken response using a self-hosted, high-quality Coqui TTS model, providing a realistic and engaging listening experience.

* **🔒 Private & Free:** All AI processing (except for the text analysis) runs locally on your own server. No audio ever leaves your machine, and there are no recurring costs.

* **🌑 Sleek Dark-Mode UI:** A clean, minimalist, and modern user interface designed for a focused learning experience.

## 🛠️ Technology Stack

This project combines a modern web frontend with a powerful, self-hosted Python backend.

* **Backend:** **FastAPI**, **Python 3.12**, **Uvicorn**

* **AI Models (Self-Hosted):**

    * **Speech-to-Text:** `faster-whisper`

    * **Text-to-Speech:** `Coqui TTS`

* **AI Analysis (API):** **Google Gemini API**

* **Frontend:** **HTML5**, **Tailwind CSS**, **Vanilla JavaScript**

* **APIs:** **Web `MediaRecorder` API (for Audio Capture)**

## ⚙️ System Architecture

1. **Client (Browser):** The `MediaRecorder` API captures user audio and uploads the file to the backend.

2. **Backend (FastAPI):**

    * Receives the audio file.
    
    * Uses the local Whisper model to transcribe the audio, calculatin word-level timestamps to detect pauses.
    
    * Sends the pause-aware text transcript to the Gemini API for analysis.
    
    * Receives the structured JSON feedback (reply, suggestion, analysis) from Gemini.
    
    * Uses the local Coqui TTS model to convert the conversational reply text into a high-quality .wav file.
    
    * Saves the audio file and sends the filename back to the client along with the Gemini feedback.

3. **Client (Browser):**

    * Receives the JSON response.
    
    * Displays the user's transcript and the AI's detailed feedback.
    
    * Fetches and plays the generated AI audio file from a separate backend endpoint.

## 🔧 Setup and Local Installation

To run this project on your local machine, follow these steps:

**Prerequisites:**

* **Python 3.12:** This project requires Python 3.12. You can check your version with `python --version`.

* **Git:** For cloning the repository.

1. **Clone the Repository**


git clone [https://github.com/Manish9250/SpeakWise-AI.git](https://github.com/Manish9250/SpeakWise-AI.git)
```bash
cd SpeakWise-AI
```

2. **Set Up the Backend**

* Navigate to the backend directory:

```bash
cd backend
```

* Create and activate a Python 3.12 virtual environment:

```bash
python3.10 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

* Install the required dependencies:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```
* Create a .env file in the backend directory and add your Gemini API key:
```bash
GEMINI_API_KEY="YOUR_GEMINI_API_KEY_HERE"
```
* Run the FastAPI server:
```bash
uvicorn main:app --reload
```

**Note:** The first time you run the server, it will automatically download the Whisper and Coqui TTS models. This is a one-time download and may take several minutes and a few gigabytes of disk space.

3. **Launch the Frontend**

* While the backend server is running, open a web browser and navigate to:

```bash
[http://127.0.0.1:8000](http://127.0.0.1:8000)
```

## 🚀 What's Next?

This project is a solid foundation. Here are some ideas for future improvements:

* **Chat History:** Implement `localStorage` on the frontend to save and load conversations.

* **Voice Selection:** Allow the user to choose from different pre-trained Coqui TTS voices.

* **Real-time Streaming:** Re-architect the backend and frontend to use WebSockets for real-time, streaming transcription and TTS.

* **UI Enhancements:** Add animations, loading indicators, and a more dynamic layout.

## 🙌 How to Contribute

Contributions are welcome! If you have ideas for new features or improvements, please feel free to open an issue or submit a pull request.

## 📄 License

This project is licensed under the MIT License. See the LICENSE file for more details.

Created with ❤️ by [Manish Kumar](https://github.com/Manish9250)