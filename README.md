

#  Assistive VoiceBot for the Visually Impaired

An intelligent **voice-based assistant** designed to help visually impaired users interact with their computer using **speech recognition, text-to-speech, and natural commands**.  
This bot can **tell the time/date, read PDFs aloud (including scanned ones via OCR), fetch live weather and news, and set reminders — all through voice.**

---

## ✨ Features

- 🎧 **Voice Interaction:** Speak commands and hear responses (hands-free experience)
- 🗣️ **Speech Recognition:** Converts user speech into text using Google Web Speech API
- 🔊 **Text-to-Speech:** Responds using `pyttsx3` (works offline)
- 🌤️ **Weather Updates:** Fetches current weather using OpenWeather API
- 📰 **Latest News:** Reads top headlines using NewsData API
- 📄 **PDF Reader with OCR:** Reads text from PDFs or scanned documents
- ⏰ **Reminders:** Set spoken reminders after a given number of minutes
- 🧠 **Error Handling:** Graceful error messages spoken aloud
- 🧩 **Modular Design:** Each functionality is cleanly separated

---

## 🛠️ Requirements

### Python Version
- Python **3.8 or above**

### Dependencies
Install all required packages using:

```bash
pip install -r requirements.txt
````

Example `requirements.txt`:

```
sounddevice
soundfile
speechrecognition
pyttsx3
requests
pytesseract
opencv-python
pdf2image
PyPDF2
Pillow
python-dotenv
```

### System Requirements

* **Microphone** and **Speakers** (for recording & playback)
* **Poppler** (for `pdf2image`)
* **Tesseract OCR** (for reading scanned PDFs)

#### Installing Poppler & Tesseract

**Windows:**

* [Poppler for Windows](https://github.com/oschwartz10612/poppler-windows/releases/)
* [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki)

Add both to your **PATH** environment variable.

**Linux / macOS:**

```bash
sudo apt install poppler-utils tesseract-ocr
```

---

## 🔑 Environment Variables

Create a `.env` file in the same folder as the script:

```
OPENWEATHER_API_KEY=your_openweather_api_key_here
NEWSAPI_KEY=your_newsapi_key_here
```

> ⚠️ Do **not** commit your `.env` file to GitHub. It contains private API keys.

---

## 🚀 Usage

1. **Run the program:**

   ```bash
   python voicebot.py
   ```

2. **Wait for the prompt:**

   ```
   VoiceBot ready. Press Enter to start speaking.
   ```

3. **Press Enter**, then **speak your command**.

---

## 🗣️ Supported Commands

| Command Example                 | Action Performed                                          |
| ------------------------------- | --------------------------------------------------------- |
| "What time is it?"              | Speaks current time                                       |
| "What's today's date?"          | Speaks current date                                       |
| "What's the weather in London?" | Reads current weather for the specified city              |
| "Read the PDF document"         | Reads aloud the text or scanned content from `sample.pdf` |
| "Read the document sample.pdf"  | Reads the specified PDF file                              |
| "Give me the news"              | Reads top news headlines                                  |
| "Remind me to take medicine"    | Asks for reminder time, then speaks reminder later        |
| "Stop" or "Exit"                | Quits the assistant safely                                |

---

## 📚 Example Interaction

```
Bot: VoiceBot ready. Press Enter to start speaking.

Press Enter to record...
You: What is the weather in Chennai?
Bot: Weather in Chennai: clear sky, 30.2 degrees Celsius.

Press Enter to record...
You: Read the PDF document.
Bot: Reading text from PDF... The document contains: "This agreement is made and entered into..."
```

---

## 🧩 File Structure

```
voicebot/
│
├── main.py           # Main program file
├── .env                  # Environment file (API keys)
└── sample.pdf            # Example document (optional)
```

---

## 🧠 How It Works

1. **Recording:** Captures voice via `sounddevice` and saves as `.wav`.
2. **Speech Recognition:** Converts audio to text using Google Web Speech.
3. **Command Parsing:** Detects intent (time, weather, news, etc.).
4. **Action Execution:** Calls the respective handler (API, PDF read, reminder).
5. **Speech Output:** Speaks results via `pyttsx3`.

---

## 🧰 Troubleshooting

| Issue                                    | Possible Cause           | Fix                                    |
| ---------------------------------------- | ------------------------ | -------------------------------------- |
| "Speech recognition service unavailable" | No internet or API issue | Check your network connection          |
| "Weather service not configured"         | Missing API key          | Add your OpenWeather API key to `.env` |
| "I couldn't record audio"                | No mic permission        | Enable microphone access               |
| OCR not working                          | Missing Tesseract        | Install and add Tesseract to PATH      |
| PDF reading fails                        | Missing Poppler          | Install Poppler utilities              |

---

## 👥 Contributors

* **You!**
  Feel free to improve and extend this assistant — add new commands, better NLP, or UI integration.

---

## 🪪 License

This project is released under the **MIT License**.
You are free to modify and distribute it for personal or educational use.

---

## 💬 Acknowledgements

* [SpeechRecognition](https://pypi.org/project/SpeechRecognition/)
* [pyttsx3](https://pypi.org/project/pyttsx3/)
* [OpenWeather API](https://openweathermap.org/api)
* [NewsData API](https://newsdata.io/)
* [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
* [Poppler](https://poppler.freedesktop.org/)
```
