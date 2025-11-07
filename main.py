
import os
import time
import threading
import logging
import datetime
from typing import Optional

import sounddevice as sd
import soundfile as sf
import speech_recognition as sr
import pyttsx3
import requests
import pytesseract
import cv2
from PyPDF2 import PdfReader
from pdf2image import convert_from_path
from PIL import Image
from dotenv import load_dotenv

# Load environment variables from .env (DO NOT COMMIT .env)
load_dotenv()

# ---------------------- CONFIG / SECRETS ----------------------
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "").strip()
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY", "").strip()

# ---------------------- Logging ----------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger("VoiceBot")

# ---------------------- TTS (pyttsx3 safe) ----------------------
engine = pyttsx3.init()  # cross-platform TTS engine
engine.setProperty("rate", 170)

def speak(text: str) -> None:
    """Speak text aloud (safe, no shell)."""
    try:
        if not text:
            return
        logger.info("Bot: %s", text)
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        logger.exception("TTS error: %s", e)

# ---------------------- RECORD AUDIO ----------------------
def record_audio(filename: str = "rec.wav", duration: float = 6.0, fs: int = 44100) -> Optional[str]:
    """Record audio using sounddevice and save to filename. Returns path or None on failure."""
    try:
        duration = max(0.5, min(duration, 60.0))  # clamp duration to [0.5, 60] seconds
        logger.info("Recording %s seconds to %s", duration, filename)
        audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype="float32")
        sd.wait()
        sf.write(filename, audio, fs)
        logger.info("Recording finished: %s", filename)
        return filename
    except Exception as e:
        logger.exception("Recording failed: %s", e)
        speak("I couldn't record audio due to an error.")
        return None

# ---------------------- SPEECH TO TEXT ----------------------
def transcribe_audio(path: str) -> str:
    """Transcribe a WAV file using Google Web Speech via SpeechRecognition.
    Returns transcript (lowercased) or empty string on failure."""
    r = sr.Recognizer()
    try:
        with sr.AudioFile(path) as source:
            audio = r.record(source)
        text = r.recognize_google(audio)
        text = text.lower().strip()
        logger.info("Transcription result: %s", text)
        return text
    except sr.UnknownValueError:
        logger.info("Speech not recognized.")
        return ""
    except sr.RequestError as e:
        logger.exception("Speech recognition request error: %s", e)
        speak("Speech recognition service is unavailable.")
        return ""
    except Exception as e:
        logger.exception("Unexpected transcription error: %s", e)
        return ""

# ---------------------- WEATHER ----------------------
def get_weather(city: str = "Chennai") -> None:
    if not OPENWEATHER_API_KEY:
        speak("Weather service is not configured. Please set OPENWEATHER_API_KEY in your .env file.")
        return

    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": OPENWEATHER_API_KEY, "units": "metric"}
    try:
        resp = requests.get(url, params=params, timeout=8)
        resp.raise_for_status()
        data = resp.json()
        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]
        speak(f"Weather in {city}: {desc}, {temp:.1f} degrees Celsius.")
    except requests.RequestException as e:
        logger.exception("Weather request failed: %s", e)
        speak("Sorry, I couldn't fetch the weather right now.")

# ---------------------- NEWS ----------------------
def get_news() -> None:
    if not NEWSAPI_KEY:
        speak("News service is not configured. Please set NEWSAPI_KEY in your .env file.")
        return

    # Example: using newsdata.io (replace with your provider & docs)
    url = "https://newsdata.io/api/1/news"
    params = {"apikey": NEWSAPI_KEY, "country": "in", "language": "en"}
    try:
        resp = requests.get(url, params=params, timeout=8)
        resp.raise_for_status()
        data = resp.json()
        results = data.get("results", [])
        if not results:
            speak("I couldn't find any news right now.")
            return

        speak("Here are the top three headlines.")
        for item in results[:3]:
            title = item.get("title")
            if title:
                speak(title)
            time.sleep(0.2)
    except requests.RequestException as e:
        logger.exception("News request failed: %s", e)
        speak("Sorry, I couldn't fetch the news right now.")

# ---------------------- OCR / PDF READING ----------------------
def read_text_from_pdf(pdf_path: str = "sample.pdf", ocr_language: str = "eng") -> None:
    speak("Reading text from PDF...")
    if not os.path.exists(pdf_path):
        speak("No PDF found. Place sample.pdf in this folder or provide a path.")
        return

    try:
        reader = PdfReader(pdf_path)
        full_text = []
        for page in reader.pages:
            text = page.extract_text()
            if text:
                full_text.append(text)
        extracted = "\n".join(full_text).strip()
    except Exception as e:
        logger.warning("PDF text extraction failed: %s", e)
        extracted = ""

    if extracted:
        # Limit how much is spoken to avoid huge reads
        to_say = extracted[:1200]
        speak("The document contains: " + to_say)
        return

    # Fallback to OCR for scanned PDFs
    try:
        # NOTE: pdf2image requires poppler installed. On Windows, specify poppler_path in convert_from_path if needed.
        images = convert_from_path(pdf_path)
        ocr_text = []
        for img in images:
            # Optionally convert to grayscale or preprocess for better OCR
            pil_img = img.convert("RGB")
            text = pytesseract.image_to_string(pil_img, lang=ocr_language)
            if text:
                ocr_text.append(text)
        ocr_result = "\n".join(ocr_text).strip()
        if ocr_result:
            speak("The scanned document says: " + (ocr_result[:1200]))
        else:
            speak("Sorry, I could not read anything from the PDF.")
    except Exception as e:
        logger.exception("OCR failed: %s", e)
        speak("I couldn't process the PDF with OCR. Ensure poppler and tesseract are installed.")

# ---------------------- REMINDERS ----------------------
def parse_minutes(txt: str) -> int:
    """Simple parser to extract minutes from user text. Defaults to 1 minute."""
    try:
        words = txt.split()
        for w in words:
            if w.isdigit():
                return int(w)
        if "half" in txt:
            return 30
        # support floats like "0.5" meaning 30 seconds -> treated as minutes
        try:
            if "." in txt:
                val = float(txt)
                return int(val * 60)  # user probably said hours -> convert to minutes
        except Exception:
            pass
    except Exception as e:
        logger.exception("parse_minutes error: %s", e)
    return 1

def set_reminder(reminder_text: str, minutes: int) -> None:
    """Set a reminder using threading.Timer."""
    if minutes <= 0:
        minutes = 1
    def fire():
        speak("Reminder: " + reminder_text)
    t = threading.Timer(minutes * 60, fire)
    t.daemon = True
    t.start()
    speak(f"Reminder set for {minutes} minute(s).")

# ---------------------- COMMAND HANDLER ----------------------
def handle_command(cmd: str) -> None:
    cmd = (cmd or "").lower()
    if "time" in cmd:
        speak("The time is " + datetime.datetime.now().strftime("%I:%M %p"))
    elif "date" in cmd:
        speak("Today's date is " + datetime.datetime.now().strftime("%B %d, %Y"))
    elif "weather" in cmd:
        # Optional: parse city from the command
        city = "chennai"
        if "in " in cmd:
            # crude city parse
            parts = cmd.split("in ")
            if len(parts) > 1:
                city = parts[-1].strip().split()[0]
        get_weather(city.capitalize())
    elif "news" in cmd or "headlines" in cmd:
        get_news()
    elif "pdf" in cmd or "read pdf" in cmd or "document" in cmd:
        read_text_from_pdf()
    elif "remind" in cmd or "reminder" in cmd:
        speak("What should I remind you about?")
        reminder = listen_once()
        if not reminder:
            speak("I didn't hear the reminder content.")
            return
        speak("In how many minutes?")
        mins_txt = listen_once()
        mins = parse_minutes(mins_txt)
        set_reminder(reminder, mins)
    elif "stop" in cmd or "exit" in cmd or "quit" in cmd:
        speak("Goodbye!")
        raise SystemExit(0)
    else:
        speak("Sorry, I didn't understand that. Try asking for time, weather, news, or PDF.")

# ---------------------- LISTEN ONCE ----------------------
def listen_once(record_seconds: float = 6.0) -> str:
    """Records and transcribes audio once. Returns the recognized text or empty string."""
    wav = record_audio(duration=record_seconds)
    if not wav:
        return ""
    txt = transcribe_audio(wav)
    logger.info("User said: %s", txt)
    # optional: remove audio after transcription to avoid leaving files around
    try:
        if os.path.exists(wav):
            os.remove(wav)
    except Exception:
        pass
    return txt

# ---------------------- MAIN ENTRYPOINT ----------------------
def main_loop():
    speak("VoiceBot ready. Press Enter to start speaking.")
    while True:
        try:
            input("\nPress Enter to record...")
            command = listen_once()
            if not command.strip():
                speak("I heard nothing.")
                continue
            handle_command(command)
        except KeyboardInterrupt:
            speak("Shutting down. Goodbye.")
            break
        except SystemExit:
            break
        except Exception as e:
            logger.exception("Main loop caught an exception: %s", e)
            speak("An error occurred. Try again.")

if __name__ == "__main__":
    main_loop()
