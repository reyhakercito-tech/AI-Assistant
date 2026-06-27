# 🎙️ AI Character Voice Assistant

An interactive, local voice assistant that uses Local LLMs (via LM Studio) and XTTS v2 to emulate the personality and voice of ANY character you want.

⚠️ Work in Progress: This project is in an experimental stage and may encounter bugs. I am actively working on stability, so if you run into any issues or have ideas to improve it, please feel free to open an issue or submit a pull request. I’m happy to collaborate!

## 🚀 Features
* **Fully Customizable:** Easily switch characters by editing a simple `config.json` file.
* **Local Processing:** 100% privacy using local LLMs (no internet connection required for inference).
* **Dynamic Feedback:** Plays a background "thinking" audio transition while the model generates the response.
* **Compatibility:** Includes scientific patches to maintain compatibility with PyTorch 2.6+.

## 🛠️ Prerequisites
1. **Python 3.10+**.
2. **[LM Studio](https://lmstudio.ai/)** installed and running a model as a local server on port `1234`.
3. **Voice Samples:** 1 to 3 reference audio files (`.wav`) of the character you want to clone.

## 📦 Setup & Installation

0. **Clone the repository:**
   git clone https://github.com/reyhakercito-tech/AI-Assistant.git
   cd AI-Assistant

1. Create and activate a virtual environment:

 ### Windows:
   python -m venv venv
   venv\Scripts\activate
 ### Linux/macOS:
   python3 -m venv venv
   source venv/bin/activate
 
2. Install Dependencies:
 pip install -r requirements.txt
    (Note: If pip doesn't work on Linux/macOS, try using pip3 install -r requirements.txt)

## ⚙️ Configuration
  Go to a folder named data in the root of the project.
  
  Place your character's voice samples (e.g., YourCharacter_1.wav, YourCharacter_2.wav...) inside the data folder.
  (I've included 3 samples as a reference; they're in Spanish, so don't worry if you don't understand them!).

  Open config.json and customize it so it matches your character, it should look like this:

  {
    "character_name": "YourCharacter",
    "model_name": "Your-LM-Studio-Model-Name",
    "language": "es",
    "thinking_phrase": "Let me think...",
    "system_prompt": "You are [Character]. Respond logically and ALWAYS speak in [Your Language]...",
    "voice_samples": [
        "YourCharacter_1.wav",
        "YourCharacter_2.wav",
        "YourCharacter_3.wav"
    ]
  }


3. ▶️ Usage

  Start your local server in LM Studio on port 1234.

  Run the assistant:

    python main.py

  Type in the terminal to chat with your character! Type exit to close the program.

## Errors
 Having trouble? Check out the TROUBLESHOOTING.md guide for quick fixes!