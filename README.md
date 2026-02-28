# Short-Form Content Generator 🎬

A Python tool that **creates short videos with a background clip, voiceover, and subtitles**.  
You provide a script and a source video, and it generates a video with:

- Text-to-speech (TTS) audio
- Auto-generated subtitles (SRT)
- Word-for-word or karaoke-style captions
- Video segmented for short-form platforms

It’s designed for viral content generation, TikTok-style clips, or social media storytelling.

---

## Features

- **Text-to-Speech:** Uses [gTTS](https://pypi.org/project/gTTS/)
  - Supports multiple accents via TLDs (e.g., `co.au` for Australian English)
  - Configurable language (`lang` parameter)
- **Subtitle Generation:** Uses [Whisper](https://github.com/openai/whisper) to generate `.srt` files
  - Word-for-word or karaoke highlighting
  - Character limits for fast-reading subtitles
- **Video Processing:** Uses **subprocess calls to `ffmpeg`, `ffprobe` and `ffmpeg_smart_trim`**
  - Requires `ffmpeg_smart_trim` for segmentation
- **Flexible Workflow:**
  - Randomized background start time
  - Optional flushing of temporary files
  - Can handle multiple scripts in one run
  - Custom text display lengths

---

## Platform

- **Windows only** (tested on Windows 11)
- Requires `ffmpeg` and `ffmpeg_smart_trim (pypi)` installed and accessible via the command line

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/connor-koefelda/short-form-generator.git
cd short-form-generator
```

2. Install dependencies

- [gTTS](https://pypi.org/project/gTTS/)
- [Whisper](https://pypi.org/project/whisper/)
  - Whisper's 'small.en' model must be configured. Can be modified in srt.py
- [MoviePy](https://pypi.org/project/moviepy/)
- [ffmpeg-smart-trim](https://pypi.org/project/ffmpeg-smart-trim/)

## Example Usage

```python
    script_paths = ["scripts/bad_tv_shows", "scripts/embarassing_moments"]
    temp_audio_output = "temp_audio_output.mp3"
    temp_srt_output = "temp_subs.srt"
    source_video_path = "inputs/parkour_recording_trimmed.mkv"
    # video_output_path = f"outputs/{script_path[8:]}.mp4"
    tld = "com.au"
    for script in script_paths:
        generateViralVideo(script, source_video_path, f"outputs/{script[8:]}.mp4", temp_audio_output=temp_audio_output, temp_srt_output=temp_srt_output, randomize=True, karaoke=True, word_for_word=True, lang='en', tld=tld, flush=True)
```

## Notes:

- ### Scripts format:
  - Should be plaintext UTF-8 with either no extension or .txt
- ### Background video format:
  - Only tested with .mkv and .mp4
  - Should support all major video formats
- ### Resulting video format:
  - Exports videos as .mp4
