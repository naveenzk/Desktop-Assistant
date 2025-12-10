# 🧠 Man – Your Personal Desktop Assistant

This project is a Python-based desktop voice assistant named **MAN**, designed to perform a wide variety of tasks using natural language commands.

The assistant combines:

* Speech interaction
* Automation of desktop and web tasks
* Data analysis with machine learning
* Information retrieval (weather, Wikipedia, currency conversion)
* Multimedia playback and reminders

The **frontend** is built using **Eel (HTML/CSS/JavaScript)** by *Mr. Data Scientist* on YouTube.

---

## ✨ Features

✅ **Voice Commands**
✅ **Play YouTube Videos**
✅ **Wikipedia Search**
✅ **Weather Reports**
✅ **Currency Conversion**
✅ **WhatsApp Messaging**
✅ **Timer and Alarm Sounds**
✅ **Machine Learning on CSV Files**
✅ **Small Talk Responses**
✅ **Translation**
✅ **Opening Applications and Websites**

---

## 🛠 Technologies Used

* **Python 3**

  * `eel` – For frontend integration
  * `playsound` / `pygame` – For audio
  * `sqlite3` – Local database of commands
  * `pywhatkit` – YouTube & WhatsApp
  * `pandas`, `scikit-learn`, `numpy` – Data analysis & ML
  * `wikipedia` – Information retrieval
  * `requests` – Web APIs
  * `deep_translator` – Translations
* **Frontend (Eel)**

  * HTML / CSS / JavaScript

---

## 🗂 Directory Structure

```
project_root/
│
├── www/                          # Frontend files
│   ├── index.html
│   ├── assets/
│   │   ├── audio/
│   │   │   ├── start_sound.mp3
│   │   │   ├── alarm.wav
│   │   │   └── timer.mp3
│   │   └── ...
│
├── engine/
│   ├── command.py               # Contains the `speak()` function
│   │ 
│   └── features.py
│
├── man.db                       # SQLite database storing commands
│
├── main.py                      # Main assistant logic (your code)
│
└── requirements.txt             # Dependencies
```

---

## ⚙️ Setup Instructions

1. **Clone the Repository**

   ```bash
   git clone https://github.com/your-username/man-assistant.git
   cd man-assistant
   ```

2. **Create a Virtual Environment (Recommended)**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure API Keys**

   * **Weather**: Update `WEATHER_API_KEY` in `main.py`
   * **Currency Conversion**: Update `CURRENCY_API_KEY` in `main.py`

5. **Prepare the SQLite Database**

   * Make sure `man.db` exists.
   * Tables:

     * `sys_command(name, path)` – For launching apps.
     * `web_command(name, url)` – For websites.

6. **Run the Assistant**

   ```bash
   python main.py
   ```

---

## 🧩 Example Commands

* **Open Applications / Websites**

  * *"Man open Chrome"*
  * *"Man open YouTube"*

* **Play YouTube Video**

  * *"Man play lo-fi beats on YouTube"*

* **Wikipedia Search**

  * *"Man search about Alan Turing"*

* **Weather**

  * *"Man what's the weather in London?"*

* **Currency Conversion**

  * *"Man convert 100 USD to EUR"*

* **Send WhatsApp Message**

  * *"Man send WhatsApp message to Aiman saying Hello!"*

* **Set Timer**

  * *"Man set a timer for 30 seconds"*

* **Translate**

  * *"Man translate Hello to Spanish"*

---

## 🧠 Extending the Assistant

You can:

* Add more **small talk** patterns in `small_talk_responses()`
* Train different **ML models** in `analyzeAndPredictCSV_live()`
* Register more commands in `sys_command` and `web_command`
* Integrate more APIs (e.g., news, stock prices)

---

## 💡 Credits

* Inspiration: [Mr. Data Scientist](https://www.youtube.com/@MrDataScientist)
* Libraries: Python ecosystem (see requirements)

---

## 📄 License

This project is for educational and personal use. You can modify and adapt it freely.

---


