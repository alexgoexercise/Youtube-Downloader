import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import yt_dlp
import os
import threading
from pathlib import Path

class YouTubeDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Video & Audio Downloader")
        self.root.geometry("650x550")
        
        # Set default download folder
        self.default_download_folder = os.path.join(os.path.expanduser("~"), "Downloads")
        self.download_folder = self.default_download_folder
        
        # Download options
        self.download_options = {
            'video': {
                'format': 'best[height<=1080]',
                'ext': 'mp4'
            },
            'audio': {
                'format': 'bestaudio[ext=m4a]/bestaudio',
                'ext': 'mp3'
            }
        }
        
        self.setup_ui()

    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill='both', expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="YouTube Video & Audio Downloader", 
                               font=('Arial', 16, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # URL entry frame
        url_frame = ttk.LabelFrame(main_frame, text="Video URL", padding="10")
        url_frame.pack(fill='x', pady=(0, 10))
        
        ttk.Label(url_frame, text="YouTube URL:").pack(anchor='w')
        self.url_entry = ttk.Entry(url_frame, width=60)
        self.url_entry.pack(fill='x', pady=(5, 0))
        
        # Download options frame
        options_frame = ttk.LabelFrame(main_frame, text="Download Options", padding="10")
        options_frame.pack(fill='x', pady=(0, 10))
        
        # Checkboxes for video and audio options
        self.video_var = tk.BooleanVar(value=True)
        self.audio_var = tk.BooleanVar()
        
        video_checkbox = ttk.Checkbutton(options_frame, text="Download Video (MP4)", 
                                       variable=self.video_var)
        audio_checkbox = ttk.Checkbutton(options_frame, text="Download Audio", 
                                       variable=self.audio_var)
        
        video_checkbox.pack(anchor='w', pady=2)
        audio_checkbox.pack(anchor='w', pady=2)
        
        # Quality and format selection
        quality_frame = ttk.Frame(options_frame)
        quality_frame.pack(fill='x', pady=(10, 0))
        
        # Video quality selection
        video_quality_frame = ttk.Frame(quality_frame)
        video_quality_frame.pack(fill='x', pady=(0, 5))
        
        ttk.Label(video_quality_frame, text="Video Quality:").pack(side='left')
        self.quality_var = tk.StringVar(value="1080p")
        quality_combo = ttk.Combobox(video_quality_frame, textvariable=self.quality_var, 
                                   values=["720p", "1080p", "1440p", "2160p"], 
                                   state="readonly", width=10)
        quality_combo.pack(side='left', padx=(5, 0))
        
        # Audio format selection
        audio_format_frame = ttk.Frame(quality_frame)
        audio_format_frame.pack(fill='x', pady=(5, 0))
        
        ttk.Label(audio_format_frame, text="Audio Format:").pack(side='left')
        self.audio_format_var = tk.StringVar(value="MP3")
        audio_format_combo = ttk.Combobox(audio_format_frame, textvariable=self.audio_format_var, 
                                        values=["MP3", "M4A", "WAV", "OPUS", "AAC"], 
                                        state="readonly", width=10)
        audio_format_combo.pack(side='left', padx=(5, 0))
        
        # Folder selection frame
        folder_frame = ttk.LabelFrame(main_frame, text="Download Location", padding="10")
        folder_frame.pack(fill='x', pady=(0, 10))
        
        folder_button = ttk.Button(folder_frame, text="Select Download Folder", 
                                  command=self.select_folder)
        folder_button.pack(side='left')
        
        self.folder_label = ttk.Label(folder_frame, text=f"Folder: {self.default_download_folder}")
        self.folder_label.pack(side='left', padx=(10, 0), fill='x', expand=True)
        
        # Progress frame
        progress_frame = ttk.LabelFrame(main_frame, text="Download Progress", padding="10")
        progress_frame.pack(fill='x', pady=(0, 10))
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, 
                                          maximum=100, length=400)
        self.progress_bar.pack(fill='x', pady=(0, 5))
        
        self.progress_label = ttk.Label(progress_frame, text="Ready to download")
        self.progress_label.pack()
        
        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=10)
        
        # Download button
        self.download_button = ttk.Button(button_frame, text="Download", 
                                         command=self.start_download, style='Accent.TButton')
        self.download_button.pack(side='left', padx=(0, 10))
        
        # Refresh button
        self.refresh_button = ttk.Button(button_frame, text="Refresh", 
                                       command=self.refresh_app)
        self.refresh_button.pack(side='left')
        
        # Status text
        self.status_text = tk.Text(main_frame, height=6, width=60, wrap='word')
        self.status_text.pack(fill='both', expand=True, pady=(10, 0))
        
        # Scrollbar for status text
        scrollbar = ttk.Scrollbar(main_frame, orient='vertical', command=self.status_text.yview)
        scrollbar.pack(side='right', fill='y')
        self.status_text.configure(yscrollcommand=scrollbar.set)

    def select_folder(self):
        """Select download folder"""
        folder = filedialog.askdirectory(initialdir=self.download_folder)
        if folder:
            self.download_folder = folder
            self.folder_label.config(text=f"Folder: {self.download_folder}")

    def refresh_app(self):
        """Refresh the application state for new downloads"""
        # Clear URL entry
        self.url_entry.delete(0, 'end')
        
        # Reset progress
        self.progress_var.set(0)
        self.progress_label.config(text="Ready to download")
        
        # Clear status text
        self.status_text.delete(1.0, 'end')
        
        # Re-enable download button
        self.download_button.config(state='normal')
        
        # Log refresh message
        self.log_message("🔄 Application refreshed - ready for new download")
        
        # Focus on URL entry for convenience
        self.url_entry.focus()

    def log_message(self, message):
        """Add message to status text"""
        self.status_text.insert('end', f"{message}\n")
        self.status_text.see('end')
        self.root.update_idletasks()

    def progress_hook(self, d):
        """Progress callback for yt-dlp"""
        if d['status'] == 'downloading':
            try:
                total = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
                downloaded = d.get('downloaded_bytes', 0)
                if total > 0:
                    percentage = (downloaded / total) * 100
                    self.progress_var.set(percentage)
                    self.progress_label.config(text=f"Downloading: {percentage:.1f}%")
            except:
                pass
        elif d['status'] == 'finished':
            self.progress_label.config(text="Processing...")
            self.log_message(f"Downloaded: {d['filename']}")

    def get_ydl_opts(self, download_type):
        """Get yt-dlp options based on download type"""
        if download_type == 'video':
            quality = self.quality_var.get()
            height = quality.replace('p', '')
            format_str = f'best[height<={height}]/best'
        else:  # audio
            audio_format = self.audio_format_var.get().lower()
            if audio_format == 'mp3':
                format_str = 'bestaudio[ext=m4a]/bestaudio'
                postprocessors = [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }]
            elif audio_format == 'm4a':
                format_str = 'bestaudio[ext=m4a]/bestaudio'
                postprocessors = []
            elif audio_format == 'wav':
                format_str = 'bestaudio[ext=m4a]/bestaudio'
                postprocessors = [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'wav',
                }]
            elif audio_format == 'opus':
                format_str = 'bestaudio[ext=opus]/bestaudio'
                postprocessors = []
            elif audio_format == 'aac':
                format_str = 'bestaudio[ext=m4a]/bestaudio'
                postprocessors = [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'aac',
                }]
            else:
                format_str = 'bestaudio[ext=m4a]/bestaudio'
                postprocessors = []
        
        opts = {
            'format': format_str,
            'outtmpl': os.path.join(self.download_folder, '%(title)s.%(ext)s'),
            'progress_hooks': [self.progress_hook],
            'ignoreerrors': False,
            'no_warnings': False,
            'quiet': False,
        }
        
        if download_type == 'audio' and 'postprocessors' in locals():
            opts['postprocessors'] = postprocessors
        
        return opts

    def download_with_yt_dlp(self, url, download_type):
        """Download using yt-dlp"""
        try:
            ydl_opts = self.get_ydl_opts(download_type)
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Get video info first
                info = ydl.extract_info(url, download=False)
                title = info.get('title', 'Unknown')
                
                self.log_message(f"Starting {download_type} download: {title}")
                
                # Download the video/audio
                ydl.download([url])
                
                self.log_message(f"✅ {download_type.title()} download completed!")
                return True
                
        except Exception as e:
            self.log_message(f"❌ Error downloading {download_type}: {str(e)}")
            return False

    def start_download(self):
        """Start the download process in a separate thread"""
        url = self.url_entry.get().strip()
        
        if not url:
            messagebox.showwarning("Input Error", "Please enter a valid YouTube URL")
            return
        
        if not self.video_var.get() and not self.audio_var.get():
            messagebox.showwarning("Selection Error", "Please select at least one option (Video or Audio)")
            return
        
        # Disable download button during download
        self.download_button.config(state='disabled')
        self.progress_var.set(0)
        self.progress_label.config(text="Starting download...")
        self.status_text.delete(1.0, 'end')
        
        # Start download in separate thread
        download_thread = threading.Thread(target=self.download_video_and_audio, args=(url,))
        download_thread.daemon = True
        download_thread.start()

    def download_video_and_audio(self, url):
        """Download the selected video or audio (or both)"""
        try:
            success_count = 0
            
            # Download video
            if self.video_var.get():
                if self.download_with_yt_dlp(url, 'video'):
                    success_count += 1
            
            # Download audio
            if self.audio_var.get():
                if self.download_with_yt_dlp(url, 'audio'):
                    success_count += 1
            
            # Show completion message
            if success_count > 0:
                self.progress_label.config(text="Download completed!")
                self.log_message(f"🎉 Successfully downloaded {success_count} file(s)!")
                messagebox.showinfo("Success", f"Download completed! {success_count} file(s) downloaded.")
            else:
                self.progress_label.config(text="Download failed!")
                messagebox.showerror("Error", "Failed to download any files. Check the log for details.")
                
        except Exception as e:
            self.log_message(f"❌ Unexpected error: {str(e)}")
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")
        finally:
            # Re-enable download button
            self.download_button.config(state='normal')

def main():
    root = tk.Tk()
    app = YouTubeDownloaderApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
