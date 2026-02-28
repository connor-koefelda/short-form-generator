import subprocess
from srt import formatTimestamp
import random
#crop video
#add audio to video
#add srt subs to video

def createVideo(source_video_path, audio_path, srt_path, video_output_path, randomize=False):
    """Crops a source video and adds subtitles and audio.

    Args:
        source_video_path (str): File path to background video.
        audio_path (str): File path to audio.
        srt_path (str): File path to srt (subtitles).
        video_output_path (str): File path to desired output.  Recommended to end in .mp4.
        randomize (bool, optional): If True, starts background video at a random (viable) time. Defaults to False.
    """
    print("Combining audio, video, and subtitles (srt)...")
    doEverything(source_video_path,audio_path,srt_path, video_output_path, randomize=randomize)
    print(f"Success!  Hopefully...   Worth double checking.  Should be {video_output_path}")

def doEverything(source_video_path, audio_path, srt_path, video_output_path, randomize=False):
    try:
        if (randomize): #Make the source video start at a random (viable) time
            videoTimeCommand = [
                "ffprobe",
                "-i", source_video_path,
                "-show_entries", "format=duration",
                "-v", "quiet",
                "-of", "csv=p=0"
            ]
            result = subprocess.run(videoTimeCommand, stdout=subprocess.PIPE, stderr = subprocess.PIPE, text=True, check=True)

            videoTime = result.stdout.strip()

            audioTimeCommand = [
                "ffprobe",
                "-i", audio_path,
                "-show_entries", "format=duration",
                "-v", "quiet",
                "-of", "csv=p=0"
            ]

            result = subprocess.run(audioTimeCommand, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)

            audioTime = result.stdout.strip()
            
            startRange = float(videoTime)-float(audioTime)
            startTime = formatTimestamp(random.uniform(0,startRange))
            startTime = f"{startTime[:8]}.{startTime[9:]}"
        else:
            startTime = "00:00:00.000"
        
        #add srt subtitles to source video
        command = [
            "ffmpeg",
            "-y",
            "-ss", startTime,
            "-i", source_video_path,
            "-i", audio_path,
            "-ss", "0",
            "-vf", f"subtitles={srt_path}:force_style='Alignment=6,MarginV=140,FontName=Comic Sans MS Bold,Shadow=2,Fontsize=24'",
            "-ss", "0",
            "-map", "0:v:0",
            "-map", "1:a:0",
            "-c:v", "libx264",
            "-c:a", "copy",               # Copy audio without re-encoding
            "-shortest",
            video_output_path
            ]

            
        subprocess.run(command, check=True)

    except subprocess.CalledProcessError as e:
        print(f" Something went wrong while cutting the video: {e}")
    except FileNotFoundError:
        print("FFmpeg isn't around D:")

#Uses the srt file to find the duration of the audio
#Deprecated, use ffprobe above now
def getAudioDuration(srt_path):
    srt = open(srt_path, "r")
    lines = [line for line in srt]
    last_stamps = lines[len(lines)-3] #00:03:24,040 --> 00:03:25,960
    last_stamp = last_stamps[len(last_stamps) - len("00:00:00,000")-1:] #00:03:25,960
    print("LAST STAMP: " + last_stamp)
    duration = f"{last_stamp[:8]}.{last_stamp[9:-2]}" #00:03:25.960
    print("THE DURATION" + duration)
    return duration


    
if (__name__ == "__main__"):
    source_video_path = "verticaltrimmed.mp4"
    audio_path = "test_audio.mp3"
    srt_path = "sub.srt"
    video_output_path = "output.mp4"
    createVideo(source_video_path, audio_path, srt_path, video_output_path, randomize=True)