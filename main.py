from tts import generateTTS
from srt import mp3_to_srt
from combine import createVideo
from segment import segmentVideo
import os

def generateViralVideo(script_path, source_video_path, video_output_path, temp_audio_output="temp_audio_output.mp3", temp_srt_output="temp_subs.srt", randomize=False, karaoke=True, word_for_word=True, max_chars=8, lang='en', tld='co.au', flush=True):
    """Creates a video or series of videos with footage in the background and subtitles in the foreground.

    Args:
        script_path (str): Path to script file.  Script should be a utf-8 text file, preferably without an extension.  This is what will generate the audio.
        source_video_path (str): Path to source video file.  This is what will be playing in the background.
        video_output_path (str): Path to desired output.  This is where the video will be saved.
        temp_audio_output (str, optional): Any file path that isn't being used, should end in .mp3. Defaults to "temp_audio_output.mp3", will be deleted if flush=True.
        temp_srt_output (str, optional): Any file path that isn't being used, should end in .srt. Defaults to "temp_subs.srt", will be deleted if flush=True.
        randomize (bool, optional): If True, the background video will start at a random (viable) time.  If False, the background video will start at the beginning. Defaults to False.
        karaoke (bool, optional): If karaoke=True and word_for_word=False, the subtitled word being spoken will show in yellow. Defaults to True.
        word_for_word (bool, optional): If True, subtitles will only display {max_chars} characters at a time.  Defaults to True.
        max_chars (int, optional): Maximum number of characters for a subtitle to display at a time if word_for_word=True, must be positive.  Defaults to 8.
        lang (str, optional): Language for TTS, only specific languages supported. Defaults to 'en'.
        tld (str, optional): Regional accent for TTS based on domain, only specific domains supported. Defaults to 'com'.
        flush (bool, optional): If True, deletes all temp files (temp_audio_output and temp_srt_output) when finished. Defaults to True.
    """
    checkExistence([script_path, source_video_path])
    script = readFileAsString(script_path)
    generateTTS(script, temp_audio_output, lang=lang, tld=tld)
    mp3_to_srt(temp_audio_output, temp_srt_output, karaoke=karaoke, word_for_word=word_for_word, max_chars=max_chars)
    createVideo(source_video_path, temp_audio_output, temp_srt_output, video_output_path, randomize=randomize)
    if (flush):
       flushTempFiles([temp_audio_output, temp_srt_output])
    segmentVideo(video_output_path)
    

#Checks if all of the files in path_list exist, raising an error if any are missing
def checkExistence(path_list):
    for path in path_list:
        if not os.path.exists(path):
            raise FileNotFoundError(f"Error: The file '{path}' does not exist.  Generation halted.")

#returns the contents of a text file as a strings
def readFileAsString(text_file_path):

    with open(text_file_path, 'r', encoding='utf-8') as file:
        file_content = file.read()

    return file_content

#Deletes all files in path_list
def flushTempFiles(path_list):
    for path in path_list:
        try:
            os.remove(path)
        except (...):
            print(f"Odd, {path} couldn't be deleted or wasn't found...")

if (__name__ == "__main__"):
    script_paths = ["scripts/bad_tv_shows", "scripts/embarassing_moments"]
    temp_audio_output = "temp_audio_output.mp3"
    temp_srt_output = "temp_subs.srt"
    source_video_path = "inputs/parkour_recording_trimmed.mkv"
    # video_output_path = f"outputs/{script_path[8:]}.mp4"
    tld = "com.au"
    for script in script_paths:
        generateViralVideo(script, source_video_path, f"outputs/{script[8:]}.mp4", temp_audio_output=temp_audio_output, temp_srt_output=temp_srt_output, randomize=True, karaoke=True, word_for_word=True, lang='en', tld=tld, flush=True)

