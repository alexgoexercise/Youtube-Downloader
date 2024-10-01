import tkinter as tk
from tkinter import messagebox, filedialog
from pytube import YouTube
from tkinter.ttk import Progressbar
import os

class YouTubeDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Video & Audio Downloader")

        # Set default download folder (e.g., Downloads)
        self.default_download_folder = os.path.join(os.path.expanduser("~"), "Downloads")
        self.download_folder = self.default_download_folder

        self.setup_ui()

    def setup_ui(self):
        # Add URL entry
        tk.Label(self.root, text="YouTube URL:").pack(pady=10)
        self.url_entry = tk.Entry(self.root, width=50)
        self.url_entry.pack(pady=5)

        # Checkboxes for video and audio options
        self.video_var = tk.BooleanVar()
        self.audio_var = tk.BooleanVar()

        video_checkbox = tk.Checkbutton(self.root, text="Download Video", variable=self.video_var)
        audio_checkbox = tk.Checkbutton(self.root, text="Download Audio", variable=self.audio_var)

        video_checkbox.pack()
        audio_checkbox.pack()

        # Add download button
        download_button = tk.Button(self.root, text="Download", command=self.download_video_and_audio)
        download_button.pack(pady=20)

        # Add a button to select the folder
        folder_button = tk.Button(self.root, text="Select Download Folder", command=self.select_folder)
        folder_button.pack(pady=5)

        # Label to display selected folder
        self.folder_label = tk.Label(self.root, text=f"Selected Folder: {self.default_download_folder}")
        self.folder_label.pack(pady=5)

        # Progress bar and label for download progress
        self.progress_var = tk.DoubleVar()
        self.progress_bar = Progressbar(self.root, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(pady=10, fill='x')

        self.progress_label = tk.Label(self.root, text="Progress: 0%")
        self.progress_label.pack()

    def select_folder(self):
        """Select download folder"""
        self.download_folder = filedialog.askdirectory() or self.download_folder
        self.folder_label.config(text=f"Selected Folder: {self.download_folder}")

    def update_progress(self, stream, chunk, bytes_remaining):
        """Update the progress bar during the download"""
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage = (bytes_downloaded / total_size) * 100
        self.progress_var.set(percentage)  # Update the progress bar
        self.progress_label.config(text=f"Progress: {int(percentage)}%")

    def download_video_and_audio(self):
        """Download the selected video or audio (or both)"""
        url = self.url_entry.get()
        if not url:
            messagebox.showwarning("Input Error", "Please enter a valid URL")
            return

        if not self.video_var.get() and not self.audio_var.get():
            messagebox.showwarning("Selection Error", "Please select at least one option (Video or Audio)")
            return

        try:
            yt = YouTube(url, on_progress_callback=self.update_progress)  # Track progress
            entry_title = yt.title

            # Download video
            if self.video_var.get():
                self.progress_label.config(text="Downloading Video...")
                video_download = yt.streams.get_highest_resolution()  # Get highest resolution video
                video_download.download(output_path=self.download_folder, filename=f"{entry_title}.mp4")
                print(f"Downloaded video: {entry_title}.mp4")

            # Download audio
            if self.audio_var.get():
                self.progress_label.config(text="Downloading Audio...")
                audio_download = yt.streams.get_audio_only()  # Get audio-only stream
                audio_download.download(output_path=self.download_folder, filename=f"{entry_title}.mp3")
                print(f"Downloaded audio: {entry_title}.mp3")

            messagebox.showinfo("Success", f"Download complete for: {entry_title}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to download video/audio: {e}")

# Create the GUI window and run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeDownloaderApp(root)
    root.mainloop()
