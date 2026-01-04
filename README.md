
# TempoPitch Music Player 🎚️🎵  
A lightweight desktop music player built with **PySide6** that supports **real-time tempo and pitch adjustment during playback**.

- **Tempo**: 0.5× → 2.0×  
- **Pitch**: -12 → +12 semitones  
- **Key Lock** (independent tempo/pitch)  
- **Tape Mode** (tempo changes pitch together)

This repo includes a Windows-friendly layout with a bundled SoundTouch DLL and a one-click launcher.

---

## What’s in this repo

- **`TempoPitch_Music_Player.py`** — main application
- **`RUN_Player.bat`** — Windows launcher
- **`SoundTouchDLL/`**  
  - **`SoundTouchDLL_x64.dll`** — SoundTouch DSP library (used for high-quality realtime tempo/pitch)

> The player is configured to load SoundTouch from:  
> `./SoundTouchDLL/SoundTouchDLL_x64.dll`

---

## Features

### Playback
- Play / Pause / Stop
- Seek bar + time display (duration via `ffprobe`)
- Next / Previous track
- Volume slider + mute
- Auto-advance (best-effort)

### Playlist
- Add audio files (multi-select)
- Add folders (recursive scan)
- Drag & drop files/folders into the playlist
- Reorder tracks by dragging

### Tempo & Pitch (during playback)
- Tempo slider with live updates
- Pitch slider (semitones) with live updates
- **Key Lock**: change tempo without changing pitch
- **Tape Mode**: classic “speed changes pitch” behavior
- Reset button

---

## Requirements

### Windows (recommended setup)
- Python 3.10+ recommended
- FFmpeg installed and available on PATH (`ffmpeg` + `ffprobe`)

### Python packages
Install:
```bash
pip install PySide6 numpy sounddevice
````

### FFmpeg

Verify in a new terminal:

```bat
ffmpeg -version
ffprobe -version
```

If those commands aren’t found, install FFmpeg and add it to PATH.

---

## Run (Windows)

### Option A — One-click launcher (recommended)

Double-click:

* **`RUN_Player.bat`**

### Option B — Run from terminal

```bat
python TempoPitch_Music_Player.py
```

---

## SoundTouch DSP (bundled)

This repo includes the SoundTouch DLL and the app is **hardcoded** to load it from:

```
./SoundTouchDLL/SoundTouchDLL_x64.dll
```

If you get a SoundTouch load error:

* Confirm the DLL exists at that exact path relative to the `.py` file
* Confirm you’re running **64-bit Python** (required for the x64 DLL)

You can check Python architecture:

```bat
python -c "import platform; print(platform.architecture())"
```

---

## Supported File Types

FFmpeg determines what formats are playable. Commonly:

* mp3, wav, flac, ogg, m4a/aac, etc.

If FFmpeg can decode it, the player can likely play it.

---

## Controls & Shortcuts

* **Space**: Play / Pause toggle
* **Ctrl+O**: Open Files…
* **Ctrl+L**: Open Folder…
* **Ctrl+Left / Ctrl+Right**: Seek ±10s

---

## Troubleshooting

### “ffmpeg not found in PATH”

Install FFmpeg and ensure `ffmpeg` and `ffprobe` work in Command Prompt:

```bat
ffmpeg -version
ffprobe -version
```

### App launches but there’s no audio / sounddevice errors

`sounddevice` uses PortAudio. Make sure:

* Your default output device is working
* You aren’t running inside an environment that blocks audio device access

### SoundTouch DLL load issues

Most common causes:

* Running **32-bit Python** with a 64-bit DLL
* DLL moved/renamed or the folder structure changed

Fix:

* Install 64-bit Python
* Keep `SoundTouchDLL/SoundTouchDLL_x64.dll` in place

### Audio quality artifacts at extreme settings

Try more moderate ranges:

* Tempo: ~0.75×–1.5×
* Pitch: within ±6 semitones

---

## Architecture (high level)

**Decode Thread**

* Runs `ffmpeg` to decode audio into float32 PCM
* Sends chunks into DSP (SoundTouch)
* Pushes processed audio into a ring buffer

**DSP**

* SoundTouch (realtime tempo/pitch/rate)

**Audio Output**

* `sounddevice` OutputStream callback pulls from ring buffer
* GUI updates position/buffer status periodically

---

## Roadmap / Ideas

* Better metadata (artist/album/artwork)
* Repeat/shuffle modes
* Playlists saved to disk (M3U/M3U8)
* Output device selector
* Packaging: PyInstaller builds for Windows
