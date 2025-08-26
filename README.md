# SpeakWise AI 🗣️✨

SpeakWise AI is an intelligent, AI-powered conversation partner designed to help you improve your English speaking skills. Get real-time, multi-layered feedback on your pronunciation, grammar, and phrasing in a natural, conversational setting.

---

### [Gif of SpeakWise AI in action]

*(A short GIF demonstrating the app's workflow would be perfect here!)*

## 🚀 Introduction

Practicing a new language can be challenging, especially without a conversation partner. SpeakWise AI solves this by providing a safe and insightful space to speak English freely. Unlike standard transcription tools that autocorrect you, SpeakWise AI captures exactly what you say and provides three layers of feedback from a powerful AI tutor: a natural conversational reply, a more fluent way to phrase your sentence, and a detailed grammatical analysis.

## ⭐ Key Features

* **🎙️ Real-time Transcription:** Captures your speech without any auto-correction, showing you exactly what you said.
* **🧠 Tri-Mode AI Feedback:** For every sentence you speak, you get:
    1.  **A Conversational Reply:** The AI responds naturally to keep the conversation flowing.
    2.  **A Phrase Suggestion:** Offers a more natural or grammatically correct version of your sentence.
    3.  **Detailed Analysis:** Provides a clear, bulleted breakdown of your grammatical errors.
* **🔊 Text-to-Speech:** The AI's conversational replies are spoken back to you, creating a realistic listening and speaking loop.
* **📚 Persistent Chat History:** All your conversations are saved locally in your browser, allowing you to track your progress over time.

## 🛠️ Technology Stack

This project combines a modern web frontend with a powerful Python backend.

* **Backend:** **FastAPI**, **Python 3.9+**, **Uvicorn**, **Google Gemini API**
* **Frontend:** **HTML5**, **CSS3**, **Vanilla JavaScript**
* **APIs:** **Web Speech API** (for Speech-to-Text) & **Speech Synthesis API** (for Text-to-Speech)
* **Storage:** **Browser `localStorage`** for saving chat history.

## ⚙️ System Architecture

The application works through a simple but powerful client-server architecture:

1.  **Client (Browser):** The Web Speech API captures user audio and transcribes it to raw text.
2.  **API Request:** The frontend sends this text to the FastAPI backend.
3.  **Backend (FastAPI):** The server receives the text, wraps it in a "smart prompt," and sends it to the Gemini API.
4.  **AI Processing:** Gemini processes the prompt and returns a structured JSON object with the three layers of feedback.
5.  **API Response:** The FastAPI server forwards this structured JSON back to the client.
6.  **Client (Browser):** JavaScript parses the JSON, displays the feedback in the chat UI, and uses the Speech Synthesis API to speak the conversational reply.



## 🔧 Setup and Local Installation

To run this project on your local machine, follow these steps:

**1. Clone the Repository**
```bash
git clone [https://github.com/Manish9250/SpeakWise-AI.git](https://github.com/Manish9250/SpeakWise-AI.git)
cd SpeakWise-AI
```
**2. Set Up the Backend**

- Create a Python virtual environment:
  
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

- Install the required dependencies:
```bash
pip install -r requirements.txt
```

- Create a .env file in the root directory and add your Gemini API key:
```bash
GEMINI_API_KEY="YOUR_GEMINI_API_KEY_HERE"
```
- Run the FastAPI server:

```bash
uvicorn main:app --reload
```
The backend will now be running at http://127.0.0.1:8000.

**3. Launch the Frontend**

- Navigate to the frontend directory.

- Open the index.html file in your web browser (Google Chrome is recommended for best Web Speech API compatibility).

## 💬 How to Use
1. Open index.html in your browser.

2. Click the "Start Listening" button.

3. Allow the browser to access your microphone.

4. Speak a sentence in English.

5. Click "Stop Listening."

6. Watch as your raw transcription and the AI's detailed feedback appear in the chat!

## 🙌 How to Contribute
Contributions are welcome! If you have ideas for new features or improvements, please feel free to:

1. Fork the repository.

2. Create a new branch (git checkout -b feature/YourAmazingFeature).

3. Commit your changes (git commit -m 'Add some YourAmazingFeature').

4. Push to the branch (git push origin feature/YourAmazingFeature).

5. Open a Pull Request.

## 📄 License
This project is licensed under the MIT License. See the LICENSE file for more details.

Created with ❤️ by [Manish Kumar](https://github.com/Manish9250)
