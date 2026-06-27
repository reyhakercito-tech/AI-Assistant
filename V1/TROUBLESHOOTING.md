# 🛠️ Troubleshooting Guide

Hey there! If you're running into issues, don't panic! :D This is an experimental project, so bugs are part of the adventure. Here are the most common hiccups and how to fix them:

---

### 1. "Fatal error in launcher" / Path issues
If you see this, it usually means your virtual environment (`venv`) is trying to look for Python in a location that no longer exists (like a previous project folder).
* **Fix:** 
    1. Delete the `venv` folder completely.
    2. Run `python -m venv venv` again to create a fresh one.
    3. Activate it and try installing/running again. Simple as that!

### 2. "ModuleNotFoundError" (e.g., No module named 'requests')
This means the libraries didn't install properly into your virtual environment.
* **Fix:** Make sure your `venv` is activated (you should see `(venv)` in your terminal prompt) and run:
    `python -m pip install -r requirements.txt`
    Using `python -m pip` forces the installation into the *current* environment rather than the global Python one.

### 3. Installation hangs or gets stuck
Some libraries like `TTS` or `torch` are quite heavy and can take a while to download and compile.
* **Fix:** Be patient and give it a couple of minutes. If it truly gets stuck, don't worry! Just close the terminal, reopen it, activate your `venv`, and run the installation command again. `pip` is smart enough to pick up where it left off.

### 4. LM Studio "Connection Error"
If the assistant says it can't connect, it’s usually because the local server isn't running.
* **Fix:** 
    1. Open LM Studio.
    2. Go to the "Local Server" tab.
    3. Ensure it's running on port `1234`. 
    4. Click "Start Server" if it's not active yet. :o

### 5. Still not working?
If you've tried all the above and it's still acting up, feel free to open an issue on the GitHub repository. Please include a screenshot or copy-paste the error message so I can help you out! 

Thanks for collaborating and happy coding! ;)