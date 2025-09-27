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
