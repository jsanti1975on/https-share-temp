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
