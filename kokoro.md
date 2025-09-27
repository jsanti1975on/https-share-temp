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
