✅ Fix in 3 Steps
✅ 1. Clone Kokoro TTS using SSH or public HTTPS

Use this working command:

git clone https://github.com/NikolaJankovic/kokoro-tts.git


No login or token needed — it's public!

✅ 2. Install dependencies
cd kokoro-tts
pip3 install -r requirements.txt

✅ 3. Run Kokoro
python3 kokoro.py

✅ Bonus: Test Ollama Again

After resolving Kokoro:

ollama run gemma:2b

🧼 Optional: Clean Up Failed Clone

If you see a broken kokoro-tts folder, delete it:

rm -rf kokoro-tts


Then re-clone properly.

Let me know when you're ready to test TTS output (or if you want to route audio out to another device).




```bash
numpy
soundfile
torch
torchaudio
transformers
sentencepiece
huggingface-hub
pydub
```
✅ Next Step: Install Miniconda (Recommended)

Here’s a quick step-by-step to install Miniconda, the lightweight version of Anaconda:

💻 1. Download and Install Miniconda

Run these commands from your home directory:

cd ~
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh


Just follow the installer prompts:

Accept the license.

Let it install to the default path (e.g., ~/miniconda3).

Say yes to modifying your .bashrc to auto-activate conda.

✅ 2. Activate Conda

Once installed:

source ~/.bashrc
conda --version  # Should now show version

🛠️ 3. Create the Environment

Now retry:

conda create -n ava01 python=3.10
conda activate ava01


Then install your project requirements:

pip install -r requirements.txt


Let me know once Miniconda is installed and the environment is set up — and I can help you launch your first working prototype of your offline voice assistant (AvA01) 🎙️.

```bash
Run this command exactly as shown to activate Conda in your current shell session:

eval "$(/home/jsantiago/miniconda3/bin/conda shell.bash hook)"


After that, try:

conda --version


If that works, then continue with:

conda create -n ava01 python=3.10
conda activate ava01

✅ Optional: Make It Persistent

To avoid doing this every time, run:

conda init


Then restart your terminal or run:

source ~/.bashrc


Once you're in the ava01 environment, you'll be ready to install dependencies and finish setting up your offline voice agent 🎙️.

Let me know when you're in the environment and we’ll continue!
```


```bash
1. ✅ Ensure You Are in Your Conda Environment
conda activate ava01

2. ✅ Install Any Remaining Python Dependencies

You got a ModuleNotFoundError for bs4. Let’s install that and anything else:

pip install beautifulsoup4 ebooklib soundfile


Then verify all needed packages from requirements.txt are installed:

pip install -r kokoro_tts/requirements.txt

3. ✅ Run the Kokoro TTS Module

Navigate to your working directory and run:

python3 -m kokoro_tts


If this still throws import errors, try running from the parent directory, like you're doing now — that’s the correct structure for -m imports.

4. ✅ Confirm Audio Output Works

If the model runs correctly, but you can’t hear output, check:

Are you on the same machine with speakers?

Is your audio device enabled? Try testing audio:

speaker-test -t wav -c 2


If you're running headless, consider saving audio to a file and playing it locally:

# inside Python code
from playsound import playsound
playsound("output.wav")

5. ✅ Make It Repeatable (Optional)

You can automate launching the environment + TTS with a simple shell script:

#!/bin/bash
source ~/miniconda3/bin/activate ava01
cd ~/ava_voice_agent_setup
python3 -m kokoro_tts


Save as start_ava.sh, then run:

chmod +x start_ava.sh
./start_ava.sh

🧠 Final Tip: Want Full Voice Agent (STT + TTS + LLM)?

You’re building just the TTS part now (Kokoro), but the full agent also needs:

✅ Ollama running locally (gemma:2b)

🟡 Moonshine STT (for speech-to-text)

✅ FastRTC if doing real-time audio

🟢 n8n (optional for automation/workflow integration)

We can wire all this up when you're ready.****
```

# Weekend Start
```bash
Perfect — fresh terminal, clean start. Here's your step-by-step to get your AvA voice assistant up and running on Ubuntu.

🧠 Objective:

Run your local AvA voice assistant using:

🧠 Ollama (e.g., gemma:2b)

🗣️ Kokoro-TTS for voice output

🔁 Optional: voice input (STT later)

✅ PREREQUISITES
🔹 1. Update your system
sudo apt update && sudo apt upgrade -y

🔹 2. Install system dependencies (audio + build tools)
sudo apt install -y \
  git curl build-essential portaudio19-dev libportaudio2 \
  libportaudiocpp0 ffmpeg python3 python3-pip python3-venv

⚙️ ENVIRONMENT SETUP
🔹 3. Set up Python virtual environment
cd ~
mkdir ava_voice_agent_setup && cd ava_voice_agent_setup
python3 -m venv vAvA
source vAvA/bin/activate


Your prompt should now show (vAvA).

🔹 4. Clone or create Kokoro-TTS folder

If you're using your own local files:

mkdir kokoro_tts && cd kokoro_tts
touch __init__.py __main__.py requirements.txt


Paste your code into __init__.py and __main__.py as you had before.

Or if you're cloning from GitHub (fix auth or use token):

git clone https://github.com/NikolaJankovic/kokoro-tts.git
cd kokoro-tts

📦 PYTHON DEPENDENCIES
🔹 5. Install required packages

If using your requirements.txt:

pip install -r requirements.txt


Or manually install what you've needed so far:

pip install numpy ebooklib beautifulsoup4 sounddevice

🧠 LLM SETUP
🔹 6. Install Ollama
curl -fsSL https://ollama.com/install.sh | sh


Once installed, verify:

ollama --version

🔹 7. Start Ollama service (if not already)
ollama serve


Then in another terminal (or backgrounded):

ollama pull gemma:2b

▶️ RUN THE ASSISTANT
🔹 8. Run Kokoro-TTS

From the root of your project:

python3 -m kokoro_tts

📌 TROUBLESHOOTING

If you get missing module errors:

pip install <missing-package>


If audio doesn’t play:

sudo apt install libportaudio2
speaker-test -t wav

🏁 OPTIONAL NEXT STEPS

Add microphone input (speech_recognition, pyaudio, whisper, etc.)

Add a dashboard

Persist conversation history

Connect to APIs (weather, calendar, et
```

```bash
🔁 Option 2: Permanent Fix (recommended)

To fix this once and for all:

Add Miniconda to your .bashrc:

echo 'export PATH="$HOME/miniconda3/bin:$PATH"' >> ~/.bashrc


Then reload your shell:

source ~/.bashrc


Now conda should work everywhere.

✅ Recap Your Status:

✅ Miniconda is installed

❌ Shell doesn’t know where conda is (not in PATH)

✅ Easy fix: source ~/miniconda3/bin/activate or update .bashrc
```

```bash
✅ From Clean Terminal to Ava Voice Agent (Step-by-Step)
1. Create and Activate the Conda Environment
conda create -n ava01 python=3.10 -y
conda activate ava01

2. Move to Your Project Folder
cd ~/ava_voice_agent_setup

3. Install All Required Python Packages
pip install -r kokoro_tts/requirements.txt


✅ This installs things like:

numpy

ebooklib

sounddevice

transformers

torch

etc.

If you get any errors about missing modules after this step, we’ll handle them manually.

4. Pull the Model (if not already done)

If you haven’t pulled the Ollama model yet:

ollama pull gemma:2b


✅ This downloads the 2B model locally, no need to pull again if already downloaded.

5. Run the Agent

Once dependencies are installed and environment is activated:

python3 -m kokoro_tts


You should no longer see ModuleNotFoundError at this point — if you do, send me the error and we’ll patch it fast.

✅ Final Optional Step (Voice Activation)

If you want this to work with a mic/speaker:

Make sure your system has audio drivers accessible in Linux (especially on PowerEdge or remote via VNC).

You may need alsa-utils or pulseaudio.

Check microphone input with:

arecord -l


Let me know when you’ve completed Step 5 — or share the next error/log if one pops up.
```

```bash
✅ Fix: Use Conda's version of libstdc++
Step 1: Install the updated C++ runtime in your conda env

Run this inside your environment (ava01):

conda install -c conda-forge libstdcxx-ng


This provides a modern libstdc++.so.6 compatible with GLIBCXX_3.4.32.

⚠️ Optional Safety Check

You can confirm the supported symbols in your version of libstdc++.so.6:

strings $(g++ -print-file-name=libstdc++.so.6) | grep GLIBCXX


You're specifically missing GLIBCXX_3.4.32.

🟢 After Fix

Try running again:

python3 -m kokoro_tts


Let me know if it progresses or hits the next dependency. You're very close now.
```
