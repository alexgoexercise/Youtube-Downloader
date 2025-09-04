# YouTube Video & Audio Downloader

A modern, reliable YouTube downloader application with a user-friendly GUI interface.

## Features

- ✅ **Reliable Downloads**: Uses `yt-dlp` (actively maintained fork of youtube-dl)
- ✅ **Video Downloads**: Download videos in various qualities (720p, 1080p, 1440p, 2160p)
- ✅ **Audio Downloads**: Download audio in multiple formats (MP3, M4A, WAV, OPUS, AAC)
- ✅ **Modern UI**: Clean, intuitive interface with progress tracking
- ✅ **Threaded Downloads**: Non-blocking downloads with real-time progress
- ✅ **Error Handling**: Comprehensive error reporting and logging
- ✅ **Custom Folders**: Choose your download location
- ✅ **Status Logging**: Real-time download status and error messages
- ✅ **Format Selection**: Choose specific video quality and audio format
- ✅ **Refresh Function**: Reset app state for new downloads

## Installation

### Prerequisites
- Python 3.7 or higher
- Windows, macOS, or Linux

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run the Application

**Method 1: Direct Python Execution**
```bash
python youtube_video_downloader.py
```

**Method 2: Using the Executable**
- Navigate to the `dist` folder
- Run `youtube_video_downloader.exe`

## How to Use

1. **Enter YouTube URL**: Paste any YouTube video URL into the input field
2. **Select Download Type**: 
   - Check "Download Video (MP4)" for video files
   - Check "Download Audio" for audio files
   - You can download both simultaneously
3. **Choose Quality & Format**: 
   - Select your preferred video quality (720p, 1080p, etc.)
   - Select your preferred audio format (MP3, M4A, WAV, OPUS, AAC)
4. **Set Download Folder**: Click "Select Download Folder" to choose where files are saved
5. **Start Download**: Click "Download" and monitor progress in real-time
6. **Refresh for New Downloads**: Click "Refresh" to clear the form and prepare for the next download

## Technical Details

### Why yt-dlp?
The app was updated from `pytube` to `yt-dlp` because:
- **Active Maintenance**: yt-dlp is actively maintained and updated regularly
- **Better Compatibility**: Handles YouTube's frequent API changes
- **More Features**: Supports more formats and quality options
- **Reliability**: More stable and reliable downloads

### Key Improvements
- **Threaded Downloads**: Downloads run in background threads, keeping UI responsive
- **Better Error Handling**: Comprehensive error reporting with detailed logs
- **Progress Tracking**: Real-time download progress with percentage display
- **Modern UI**: Improved interface with better organization and styling
- **Quality Selection**: Choose specific video quality instead of just "highest available"
- **Audio Format Options**: Support for multiple audio formats (MP3, M4A, WAV, OPUS, AAC)
- **Refresh Functionality**: Easy reset for consecutive downloads

## Troubleshooting

### Common Issues

1. **"No module named 'yt_dlp'"**
   - Solution: Run `pip install yt-dlp`

2. **Download fails with "Video unavailable"**
   - Solution: Check if the video is available in your region
   - Try a different video URL

3. **Slow download speeds**
   - This is normal for large files
   - Check your internet connection

4. **Audio conversion issues**
   - The app automatically handles audio conversion
   - Ensure you have sufficient disk space

### Getting Help
- Check the status log in the application for detailed error messages
- Ensure your YouTube URL is valid and the video is publicly available
- Try downloading a different video to test if the issue is specific to one URL

## Building the Executable

To create a standalone executable:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --icon=resources/youtube_icon.ico youtube_video_downloader.py
```

The executable will be created in the `dist` folder.

## License

This project is open source and available under the MIT License.