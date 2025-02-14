from pytubefix import YouTube  # import the YouTube class from the pytubefix library for downloading YouTube videos
from pytubefix.cli import on_progress  # import the on_progress callback to track download progress
from moviepy import VideoFileClip, AudioFileClip, CompositeAudioClip  # import the necessary tools for video editing
import os  # import the os module for file operations like renaming and deleting files
import re  # import the re module for regular expression operations
import argparse  # import the argparse module for command-line argument parsing
import getpass  # import the getpass module to safely get the current user's username

def parse_arguments() -> str:
    parser = argparse.ArgumentParser(description="YouTube Video Downloader") # create a parser for command-line arguments

    parser.add_argument('--quality', required=True, help="specify the quality of the video (e.g. 720p, 1080p, 2160p)")
    parser.add_argument('--url', required=True, help="specify the URL of the video")

    args = parser.parse_args() # parse the arguments from the command-line

    return args

def download_path() -> str:
    operating_system = os.name # determine the operating system

    if operating_system == 'nt': # Windows OS
        path = fr'C:\Users\{getpass.getuser()}\Downloads'
    elif operating_system == 'posix': # Unix-like OS
        path = fr'\home\{getpass.getuser()}\Downloads'
        if not os.path.exists(path=path):
            os.makedirs(path)
    return path

def sanitize_filename(filename: str) -> str:
    return re.sub(r'[<>:"/\\|?*]', '', filename)  # remove characters that are not allowed in filenames

def download_stream(stream: object, output_path=download_path()) -> str:
    try:
        return stream.download(output_path=output_path)  # download the desired stream and save it in the specified path
    except Exception as e:
        print(f"failed to download: {e}")  # if download not successful print the relative error
        return None

def download_and_merge(quality: str, url: str):
    try:
        # create a YouTube object with the provided URL and set the progress callback
        yt = YouTube(url, on_progress_callback=on_progress, use_po_token=True)

        # rename and sanitize the filename
        final_filename = f"{sanitize_filename(yt.title)}.mp4"

        # get the download path
        result_path = download_path()

        # check if the file already exists
        if os.path.exists(fr'{result_path}\{final_filename}'):
            print(f"{final_filename} already exist")
            return

        # filter for the provided resolution video stream
        video_stream = yt.streams.filter(only_video=True, file_extension='mp4', resolution=quality).first()
        if not video_stream:
            print(f"no video stream found for quality {quality}")
            return

        # filter for the highest bitrate audio stream available
        audio_stream = yt.streams.filter(only_audio=True, file_extension='mp4').order_by('abr').desc().first()
        if not audio_stream:
            print("no audio stream found")
            return

        # download the video and audio streams using the download_stream() function
        print(f"downloading {final_filename}")
        video_filename = download_stream(video_stream)
        audio_filename = download_stream(audio_stream)

        if not video_filename or not audio_filename:
            print("failed to download streams")
            return
        
        print(result_path)

        # temporary filenames for the downloaded video and audio
        video_tmp = fr'{result_path}\temp_video.mp4'
        audio_tmp = fr'{result_path}\temp_audio.mp4'

        # rename the downloaded files to temporary names for processing
        os.rename(video_filename, video_tmp)
        os.rename(audio_filename, audio_tmp)

        # load the video and audio clips using moviepy
        with VideoFileClip(video_tmp) as video_clip, AudioFileClip(audio_tmp) as audio_clip:
            # combine the audio with the video clip
            video_clip.audio = CompositeAudioClip([audio_clip])  # set the audio of the video clip

            # write the final video file with the combined audio
            video_clip.write_videofile(fr'{result_path}\{final_filename}')

        # remove the temporary files after processing
        os.remove(video_tmp)
        os.remove(audio_tmp)

    except Exception as e:
        print(f"error: {e}")

if __name__ == "__main__":
    args = parse_arguments() # parse command-line arguments
    download_and_merge(args.quality, args.url)  # call the download_and_merge function with the provided video quality and URL