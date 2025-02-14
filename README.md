# YouTube Video Downloader

This Python script allows you to download YouTube videos and merge them with audio tracks using the `pytubefix` and `moviepy` libraries.  
The script downloads the desired video resolution specified by the user and the highest bitrate audio available for a given YouTube URL, combines them, and saves the final video file.

## Requirements

Before running the script, ensure you have the following libraries installed:

- [`pytubefix`](https://pypi.org/project/pytubefix/)
- [`moviepy`](https://pypi.org/project/moviepy/)
- `os`
- `re`
- `argparse`
- `getpass`

If you don't have them, you can easily install the required libraries using pip and the `requirements.txt` file:

```
pip install -r requirements.txt
```
## Overview

The script performs the following steps:

1. **Function Definition**:
    - `parse_arguments() -> str`: it parses the required arguments
    - `download_path() -> str`: it autodetermines and returns the download path where the file will be saved
    - `sanitize_filename(filename: str) -> str`: it takes a filename as input and performs the following:
        - removes the unwanted characters from the given filename using `re`
        - outputs the new filename without the unwanted characters
    - `download_stream(stream: object, output_path=download_path()) -> str`: it takes a stream object and the file saving path as input and downloads the video and audio in the given path
    
    - `download_and_merge(url: str, quality: str)`: it takes a YouTube video URL and the video quality as input and performs the following:
        - creates a `YouTube` object with the provided URL and sets a progress callback
        - checks if the file already exists
        - filters and selects specified resolution video stream and the highest bitrate audio stream
        - calls the `download_stream` function to download the video and audio
        - renames the downloaded files to temporary names for further processing
        - loads the video and audio clips using `moviepy`
        - combines the audio with the video clip
        - writes the final merged video file with the title of the YouTube video
        - cleans up by removing the temporary files

2. **Main Execution Block**:
    - prompts the user to provide the desired video quality and the YouTube video URL.
    - calls the `download_and_merge` function with the provided video quality and URL.

## How To Use

This program is quite simply to use, all you have to do is just launch the `downloader.py` file.  
To do so you can simply type:

```
python3 downloader.py --quality <desired video quality> --url <youtube video url>
```

## Note

To comply with YouTube's download policy, the script will require two tokens (poToken) during its initial execution.  
In order to obtain these tokens you can follow [this guide](https://pytubefix.readthedocs.io/en/latest/user/po_token.html#manually-acquiring-a-po-token-from-a-browser-for-use-when-logged-out) provided by the developer of the `pytubefix` library.

## Conclusion

With this YouTube Video Downloader, you have the power to take your favorite videos offline and enjoy them anytime, anywhere **without ADS**.  
Whether you're curating a personal collection of cat videos or compiling the ultimate playlist of motivational speeches, this script is your trusty sidekick.  
Remember, the code is open for modification! Feel free to tweak it, enhance it, or even turn it into a full-fledged video editing suite.  
Just keep in mind: **with great power comes great responsibility**.  
So, while you’re free to modify the code, please don’t use it to create a 10-hour loop of your neighbor’s karaoke night—unless, of course, you’re planning to win a "Best Neighbor" award!

Happy coding!



~*That's it. That's all there is.*~
