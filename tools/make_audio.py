"""Record every phrase with the Piper voice "Serena" into audio/<key>.m4a (macOS, needs afconvert).

Usage:
  node tools/export_phrases.js index.html phrases.json
  python tools/make_audio.py phrases.json it_IT-serena-high.onnx audio [espeak-data-dir]

Only phrases without an existing file are recorded. If Piper cannot find its espeak data
(it fails on very long paths), pass a short path or symlink to piper/espeak-ng-data.
"""
import json, os, subprocess, sys, tempfile, wave
from piper import PiperVoice, SynthesisConfig

phrases, model, outdir = sys.argv[1:4]
kw = {"espeak_data_dir": sys.argv[4]} if len(sys.argv) > 4 else {}
voice = PiperVoice.load(model, **kw)
cfg = SynthesisConfig(length_scale=1.12)
os.makedirs(outdir, exist_ok=True)
tmp = tempfile.mkdtemp()
for key, text in json.load(open(phrases)).items():
    out = os.path.join(outdir, key + ".m4a")
    if os.path.exists(out):
        continue
    spoken = text.replace("—", ",").replace("…", ".").replace("TV", "tivù")
    wav = os.path.join(tmp, key + ".wav")
    with wave.open(wav, "wb") as wf:
        voice.synthesize_wav(spoken, wf, syn_config=cfg)
    subprocess.run(["afconvert", "-f", "m4af", "-d", "aac", "-b", "48000", wav, out], check=True)
    os.remove(wav)
