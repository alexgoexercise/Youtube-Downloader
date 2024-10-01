import tkinter as tk
from tkinter import messagebox, filedialog
from pytube import YouTube
from tkinter.ttk import Progressbar
import os

# Set default download folder (e.g., Desktop)
default_download_folder = os.path.join(os.path.expanduser("~"), "Downloads")
download_folder = default_download_folder  # Initialize with the default folder

def select_folder():
    global download_folder
    download_folder = filedialog.askdirectory()  # Open a dialog to select a folder
    if download_folder:
        folder_label.config(text=f"Selected Folder: {download_folder}")  # Update the label to show selected folder

def update_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage = (bytes_downloaded / total_size) * 100
    progress_var.set(percentage)  # Update the progress bar
    progress_label.config(text=f"Progress: {int(percentage)}%")

def download_video_and_audio():
    global download_folder
    url = url_entry.get()
    if not url:
        messagebox.showwarning("Input Error", "Please enter a valid URL")
        return

    if not video_var.get() and not audio_var.get():
        messagebox.showwarning("Selection Error", "Please select at least one option (Video or Audio)")
        return

    try:
        yt = YouTube(url, on_progress_callback=update_progress)  # Track progress

        entry_title = yt.title

        # Download video
        if video_var.get():
            video_download = yt.streams.get_highest_resolution()  # Get highest resolution video
            progress_label.config(text="Downloading Video...")
            video_download.download(output_path=download_folder, filename=f"{entry_title}.mp4")
            print(f"Downloaded video: {entry_title}.mp4")

        # Download audio
        if audio_var.get():
            audio_download = yt.streams.get_audio_only()  # Get audio-only stream
            progress_label.config(text="Downloading Audio...")
            audio_download.download(output_path=download_folder, filename=f"{entry_title}.mp3")
            print(f"Downloaded audio: {entry_title}.mp3")

        messagebox.showinfo("Success", f"Download complete for: {entry_title}")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to download video/audio: {e}")

# Create the GUI window
root = tk.Tk()
root.title("YouTube Video & Audio Downloader")

# Add URL entry
tk.Label(root, text="YouTube URL:").pack(pady=10)
url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)

# Checkboxes for video and audio options
video_var = tk.BooleanVar()
audio_var = tk.BooleanVar()

video_checkbox = tk.Checkbutton(root, text="Download Video", variable=video_var)
audio_checkbox = tk.Checkbutton(root, text="Download Audio", variable=audio_var)

video_checkbox.pack()
audio_checkbox.pack()

# Add download button
download_button = tk.Button(root, text="Download", command=download_video_and_audio)
download_button.pack(pady=20)

# Add a button to select the folder
folder_button = tk.Button(root, text="Select Download Folder", command=select_folder)
folder_button.pack(pady=5)

# Label to display selected folder (initialize with the default download folder)
folder_label = tk.Label(root, text=f"Selected Folder: {default_download_folder}")
folder_label.pack(pady=5)

# Progress bar and label for download progress
progress_var = tk.DoubleVar()
progress_bar = Progressbar(root, variable=progress_var, maximum=100)
progress_bar.pack(pady=10, fill='x')

progress_label = tk.Label(root, text="Progress: 0%")
progress_label.pack()

# Run the GUI loop
root.mainloop()

