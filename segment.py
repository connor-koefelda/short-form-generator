import subprocess
import math
import shutil
from moviepy.video.io.VideoFileClip import VideoFileClip

#NOTE: REQUIRES pypi ffmpeg_smart_trim to be installed! Also, if you're using a specific python installation this might get messed up!

TIKTOK_MAX_TIME = 3598
INSTAGRAM_MAX_TIME = 88
YOUTUBE_MAX_TIME = 178

def segmentVideo(source_video_path, tiktok=True, instagram=True, youtube=True):
    """Cuts up a video into parts to fit with popular social media max video lengths (~1.5s-2.5s short of max length).  Outputs will be in the format of outputs/{platform_name}/{platform_name}_{video_part}_{source_video_path without folders (everything after the last /)}

    Args:
        source_video_path (str): File path to video to be cut up.  Will not be deleted
        tiktok (bool, optional): should we generate tiktoks (max 60m). Defaults to True.
        instagram (bool, optional): should we generate instagram reels (max 1.5m). Defaults to True.
        youtube (bool, optional): should we generate youtube shorts (max 3m). Defaults to True.
    """

    print("Segmenting video...")
    video_timeCommand = [
        "ffprobe",
        "-i", source_video_path,
        "-show_entries", "format=duration",
        "-v", "quiet",
        "-of", "csv=p=0"
    ]
    result = subprocess.run(video_timeCommand, stdout=subprocess.PIPE, stderr = subprocess.PIPE, text=True, check=True)

    video_time = float(result.stdout.strip())

    segmentVideoForPlatform(source_video_path, video_time, "tiktok", TIKTOK_MAX_TIME)
    segmentVideoForPlatform(source_video_path, video_time, "instagram", INSTAGRAM_MAX_TIME)
    segmentVideoForPlatform(source_video_path, video_time, "youtube", YOUTUBE_MAX_TIME)

    print(f"Done segmenting {source_video_path}!")

def segmentVideoForPlatform(source_video_path, video_time, platform_name, max_time):
    print(f"Segmenting for {platform_name}...")
    try:
        name_of_file = source_video_path[source_video_path.rindex("/")+1:]
    except ValueError:
        name_of_file = source_video_path
    
    if (video_time < max_time):
        shutil.copy(source_video_path, f"outputs/{platform_name}/{platform_name}_{name_of_file}")
    else:
        videos_needed = math.ceil(video_time/max_time)
        for i in range(videos_needed):
            cropVideo(source_video_path, (max_time-2)*i, min((max_time-2)*(i+1)+2,video_time), f"outputs/{platform_name}/{platform_name}_{i}_{name_of_file}")

def cropVideo(source_video_path, start_time, end_time, output_path):
    try:
        command = [
            "python", "-m",
            "ffmpeg_smart_trim.trim", source_video_path,
            "--start_time", f"{start_time}",
            "--end_time", f"{end_time}",
            "--output", output_path
        ]

        subprocess.run(command, check=True)
    
    except subprocess.CalledProcessError as e:
        print(f"Something went wrong while trying to crop {source_video_path}")
    except FileNotFoundError:
        print(f"ffmpeg just isn't around D:.  Or maybe the file, not sure")



if (__name__ == "__main__"):
    
    source_video_path = "outputs/output.mp4"
    segmentVideo(source_video_path)