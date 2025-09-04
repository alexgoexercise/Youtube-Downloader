import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import yt_dlp
import os
import threading
from pathlib import Path
import re

class URLInputBox:
    """Individual URL input box with remove button"""
    def __init__(self, parent, index, on_remove):
        self.frame = ttk.Frame(parent)
        self.index = index
        self.on_remove = on_remove
        
        # URL entry
        self.url_entry = ttk.Entry(self.frame, width=60)
        self.url_entry.pack(side='left', fill='x', expand=True, padx=(0, 5))
        
        # Remove button (only show if not the first box)
        if index > 0:
            self.remove_btn = ttk.Button(self.frame, text="✕", width=3, 
                                       command=self.remove_box)
            self.remove_btn.pack(side='right')
        
        # URL validation indicator
        self.status_label = ttk.Label(self.frame, text="", font=('Arial', 8))
        self.status_label.pack(side='right', padx=(0, 5))
        
        # Bind URL validation
        self.url_entry.bind('<KeyRelease>', self.validate_url)
    
    def validate_url(self, event=None):
        """Validate YouTube URL and update status"""
        url = self.url_entry.get().strip()
        if not url:
            self.status_label.config(text="", foreground="black")
        elif self.is_valid_youtube_url(url):
            self.status_label.config(text="✓", foreground="green")
        else:
            self.status_label.config(text="✗", foreground="red")
    
    def is_valid_youtube_url(self, url):
        """Check if the URL is a valid YouTube URL"""
        youtube_patterns = [
            r'https?://(?:www\.)?youtube\.com/watch\?v=[\w-]+',
            r'https?://(?:www\.)?youtu\.be/[\w-]+',
            r'https?://(?:www\.)?youtube\.com/playlist\?list=[\w-]+',
            r'https?://(?:www\.)?youtube\.com/channel/[\w-]+',
            r'https?://(?:www\.)?youtube\.com/c/[\w-]+',
            r'https?://(?:www\.)?youtube\.com/user/[\w-]+'
        ]
        
        for pattern in youtube_patterns:
            if re.match(pattern, url):
                return True
        return False
    
    def get_url(self):
        """Get the URL from this input box"""
        return self.url_entry.get().strip()
    
    def remove_box(self):
        """Remove this URL input box"""
        self.frame.destroy()
        self.on_remove(self.index)
    
    def pack(self, **kwargs):
        """Pack the frame"""
        self.frame.pack(**kwargs)
    
    def pack_forget(self):
        """Unpack the frame"""
        self.frame.pack_forget()

class YouTubeDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Video & Audio Downloader")
        self.root.geometry("750x650")
        
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
        
        # URL input boxes management
        self.url_boxes = []
        self.next_box_id = 0
        
        # Batch download tracking
        self.total_urls = 0
        self.completed_urls = 0
        self.current_url_index = 0
        
        self.setup_ui()

    def setup_ui(self):
        # Main frame with scrollbar
        main_canvas = tk.Canvas(self.root)
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=main_canvas.yview)
        scrollable_frame = ttk.Frame(main_canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all"))
        )
        
        main_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        main_canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack scrollbar and canvas
        scrollbar.pack(side="right", fill="y")
        main_canvas.pack(side="left", fill="both", expand=True)
        
        # Main frame
        main_frame = ttk.Frame(scrollable_frame, padding="10")
        main_frame.pack(fill='both', expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="YouTube Video & Audio Downloader", 
                               font=('Arial', 16, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # URL entry frame
        url_frame = ttk.LabelFrame(main_frame, text="YouTube URLs", padding="10")
        url_frame.pack(fill='x', pady=(0, 10))
        
        # Instructions
        instructions = ttk.Label(url_frame, 
                                text="Add multiple YouTube URLs below. Each box represents one URL to download.",
                                font=('Arial', 9), foreground='gray')
        instructions.pack(anchor='w', pady=(0, 10))
        
        # URL boxes container
        self.url_boxes_frame = ttk.Frame(url_frame)
        self.url_boxes_frame.pack(fill='x', pady=(0, 10))
        
        # Add URL button frame
        add_button_frame = ttk.Frame(url_frame)
        add_button_frame.pack(fill='x')
        
        # Add URL button
        add_url_btn = ttk.Button(add_button_frame, text="+ Add Another URL", 
                                command=self.add_url_box)
        add_url_btn.pack(side='left')
        
        # URL count label
        self.url_count_label = ttk.Label(add_button_frame, text="URLs: 1", font=('Arial', 9))
        self.url_count_label.pack(side='right')
        
        # Add first URL box (after creating url_count_label)
        self.add_url_box()
        
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
        self.download_button = ttk.Button(button_frame, text="Download All URLs", 
                                         command=self.start_download)
        self.download_button.pack(side='left', padx=(0, 10))
        
        # Refresh button
        self.refresh_button = ttk.Button(button_frame, text="Clear All", 
                                       command=self.refresh_app)
        self.refresh_button.pack(side='left')
        
        # Status text
        self.status_text = tk.Text(main_frame, height=6, width=80, wrap='word')
        self.status_text.pack(fill='both', expand=True, pady=(10, 0))
        
        # Scrollbar for status text
        status_scrollbar = ttk.Scrollbar(main_frame, orient='vertical', command=self.status_text.yview)
        status_scrollbar.pack(side='right', fill='y')
        self.status_text.configure(yscrollcommand=status_scrollbar.set)

    def add_url_box(self):
        """Add a new URL input box"""
        box = URLInputBox(self.url_boxes_frame, self.next_box_id, self.remove_url_box)
        box.pack(fill='x', pady=2)
        self.url_boxes.append(box)
        self.next_box_id += 1
        self.update_url_count()
        
        # Focus on the new box
        box.url_entry.focus()

    def remove_url_box(self, index):
        """Remove a URL input box"""
        # Find and remove the box
        for i, box in enumerate(self.url_boxes):
            if box.index == index:
                self.url_boxes.pop(i)
                break
        
        # Reindex remaining boxes
        for i, box in enumerate(self.url_boxes):
            box.index = i
        
        self.next_box_id -= 1
        self.update_url_count()

    def update_url_count(self):
        """Update the URL count display"""
        count = len(self.url_boxes)
        self.url_count_label.config(text=f"URLs: {count}")

    def get_urls_from_boxes(self):
        """Extract URLs from all input boxes"""
        urls = []
        for box in self.url_boxes:
            url = box.get_url()
            if url and box.is_valid_youtube_url(url):
                urls.append(url)
        return urls

    def select_folder(self):
        """Select download folder"""
        folder = filedialog.askdirectory(initialdir=self.download_folder)
        if folder:
            self.download_folder = folder
            self.folder_label.config(text=f"Folder: {self.download_folder}")

    def refresh_app(self):
        """Refresh the application state for new downloads"""
        # Clear all URL boxes except the first one
        while len(self.url_boxes) > 1:
            self.url_boxes[-1].remove_box()
        
        # Clear the first box
        if self.url_boxes:
            self.url_boxes[0].url_entry.delete(0, 'end')
        
        # Reset progress
        self.progress_var.set(0)
        self.progress_label.config(text="Ready to download")
        
        # Clear status text
        self.status_text.delete(1.0, 'end')
        
        # Re-enable download button
        self.download_button.config(state='normal')
        
        # Reset batch tracking
        self.total_urls = 0
        self.completed_urls = 0
        self.current_url_index = 0
        
        # Update URL count
        self.update_url_count()
        
        # Log refresh message
        self.log_message("🔄 Application refreshed - ready for new downloads")
        
        # Focus on first URL box
        if self.url_boxes:
            self.url_boxes[0].url_entry.focus()

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
                    # Calculate overall progress including batch progress
                    file_progress = (downloaded / total) * 100
                    batch_progress = (self.completed_urls / self.total_urls) * 100 if self.total_urls > 0 else 0
                    overall_progress = (batch_progress + (file_progress / self.total_urls)) if self.total_urls > 0 else file_progress
                    
                    self.progress_var.set(overall_progress)
                    self.progress_label.config(text=f"URL {self.current_url_index}/{self.total_urls} - Downloading: {file_progress:.1f}%")
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
        """Start the batch download process"""
        urls = self.get_urls_from_boxes()
        
        if not urls:
            messagebox.showwarning("Input Error", "Please enter at least one valid YouTube URL")
            return
        
        if not self.video_var.get() and not self.audio_var.get():
            messagebox.showwarning("Selection Error", "Please select at least one option (Video or Audio)")
            return
        
        # Initialize batch tracking
        self.total_urls = len(urls)
        self.completed_urls = 0
        self.current_url_index = 0
        
        # Disable download button during download
        self.download_button.config(state='disabled')
        self.progress_var.set(0)
        self.progress_label.config(text="Starting batch download...")
        self.status_text.delete(1.0, 'end')
        
        self.log_message(f"🚀 Starting batch download of {self.total_urls} URL(s)")
        
        # Start download in separate thread
        download_thread = threading.Thread(target=self.batch_download, args=(urls,))
        download_thread.daemon = True
        download_thread.start()

    def batch_download(self, urls):
        """Download multiple URLs in batch"""
        try:
            total_success_count = 0
            failed_urls = []
            
            for i, url in enumerate(urls):
                self.current_url_index = i + 1
                self.log_message(f"\n📥 Processing URL {self.current_url_index}/{self.total_urls}: {url}")
                
                url_success_count = 0
                
                # Download video
                if self.video_var.get():
                    if self.download_with_yt_dlp(url, 'video'):
                        url_success_count += 1
                
                # Download audio
                if self.audio_var.get():
                    if self.download_with_yt_dlp(url, 'audio'):
                        url_success_count += 1
                
                if url_success_count > 0:
                    total_success_count += url_success_count
                    self.completed_urls += 1
                    self.log_message(f"✅ URL {self.current_url_index} completed successfully")
                else:
                    failed_urls.append(url)
                    self.log_message(f"❌ URL {self.current_url_index} failed")
                
                # Update overall progress
                overall_progress = (self.completed_urls / self.total_urls) * 100
                self.progress_var.set(overall_progress)
            
            # Show completion message
            if total_success_count > 0:
                self.progress_label.config(text="Batch download completed!")
                self.log_message(f"\n🎉 Batch download completed!")
                self.log_message(f"✅ Successfully downloaded {total_success_count} file(s) from {self.completed_urls} URL(s)")
                
                if failed_urls:
                    self.log_message(f"❌ Failed URLs: {len(failed_urls)}")
                    for failed_url in failed_urls:
                        self.log_message(f"   - {failed_url}")
                
                messagebox.showinfo("Success", f"Batch download completed!\n{total_success_count} file(s) downloaded from {self.completed_urls} URL(s)")
            else:
                self.progress_label.config(text="Batch download failed!")
                self.log_message(f"\n❌ Batch download failed! No files were downloaded.")
                messagebox.showerror("Error", "Failed to download any files. Check the log for details.")
                
        except Exception as e:
            self.log_message(f"❌ Unexpected error during batch download: {str(e)}")
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