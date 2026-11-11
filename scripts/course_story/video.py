"""Narrated video from the slides: each slide is shown with a slow push-in for its first five seconds, then holds,
while its speaker notes are read by a computer voice (Kokoro). Captions are the speaker notes as written.
Per-slide audio is cached (keyed by the words), so changing one slide only re-reads that slide.
Writes site/video/<name>.mp4 (1920x1080, H.264 + AAC) and <name>.vtt."""
from __future__ import annotations

import hashlib, json, re, shutil, subprocess, tempfile
from pathlib import Path

VOICE, SPEED = "af_bella", 0.94


def split_cue(a, b, text, most=110):
    parts, cur = [], ""
    for sent in re.split(r"(?<=[.?!])\s+", text.strip()):
        if cur and len(cur) + len(sent) + 1 > most:
            parts.append(cur)
            cur = sent
        else:
            cur = (cur + " " + sent).strip()
    parts.append(cur)
    total, t, out = sum(len(p) for p in parts), a, []
    for p in parts:
        d = (b - a) * len(p) / total
        out.append((t, t + d, p))
        t += d
    return out


def stamp(t):
    h, m = int(t // 3600), int(t % 3600 // 60)
    return f"{h:02d}:{m:02d}:{t % 60:06.3f}"


def build(kit, tts):
    import numpy as np
    import soundfile as sf
    C = kit.C
    slides = C.slides(kit)
    P = kit.site / "presentation"
    files = sorted((P / "slides").glob("*.jpg"))
    assert len(files) == len(slides), "build the slides first"
    out = kit.site / "video"
    out.mkdir(exist_ok=True)
    cache = kit.root / ".story-cache" / "audio"
    cache.mkdir(parents=True, exist_ok=True)
    k = None
    tmp = Path(tempfile.mkdtemp())
    clips, cues, t = [], [], 0.0
    for i, (img, s) in enumerate(zip(files, slides)):
        text = C.spoken(s["notes"])
        key = hashlib.sha1(f"{VOICE}|{SPEED}|{text}".encode()).hexdigest()[:16]
        wav = cache / f"{key}.wav"
        if not wav.exists():
            if k is None:
                from kokoro_onnx import Kokoro
                k = Kokoro(f"{tts}/kokoro-v1.0.onnx", f"{tts}/voices-v1.0.bin")
            a, sr = k.create(text, voice=VOICE, speed=SPEED, lang="en-us")
            idx = np.where(np.abs(a) > 0.01)[0]
            a = a[max(0, idx[0] - int(.03 * sr)): idx[-1] + int(.08 * sr)]
            a = np.concatenate([np.zeros(int(0.35 * sr)), a, np.zeros(int(0.6 * sr))]).astype(np.float32)
            sf.write(wav, a, sr)
        info = sf.info(str(wav))
        dur = info.frames / info.samplerate
        cues.append((t + 0.35, t + dur - 0.6, s["notes"]))
        t += dur
        clip = tmp / f"{i:02d}.mp4"
        # push in over the first 150 frames (5 seconds at 30 fps), then hold still so the file stays small
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-framerate", "30", "-i", str(img), "-i", str(wav),
                        "-filter_complex", f"[0:v]scale=2880:-1,zoompan=z='min(1+0.0003*on,1.045)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1920x1080:fps=30,format=yuv420p[v]",
                        "-map", "[v]", "-map", "1:a", "-c:v", "libx264", "-preset", "veryfast", "-crf", "24", "-tune", "stillimage", "-c:a", "aac", "-b:a", "96k", "-ar", "48000",
                        "-t", f"{dur:.3f}", str(clip)], check=True)
        clips.append(clip)
        print(f"{i + 1:2d} {s['key']:12s} {dur:5.1f}s", flush=True)
    lst = tmp / "list.txt"
    lst.write_text("".join(f"file '{c}'\n" for c in clips))
    mp4 = out / f"{C.VIDEO}.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", "-movflags", "+faststart", str(mp4)], check=True)
    split = [c for a, b, txt in cues for c in split_cue(a, b, txt)]
    (out / f"{C.VIDEO}.vtt").write_text("WEBVTT\n\n" + "\n".join(f"{n}\n{stamp(a)} --> {stamp(b)}\n{txt}\n" for n, (a, b, txt) in enumerate(split, 1)), encoding="utf-8")
    (out / "video.json").write_text(json.dumps({"seconds": round(t, 1), "slides": len(clips), "bytes": mp4.stat().st_size}))
    shutil.rmtree(tmp)
    print("video", round(t, 1), "s,", round(mp4.stat().st_size / 1_048_576, 1), "MB →", mp4)
