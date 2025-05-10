import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk
import speech_recognition as sr
import threading
import re
import time
import os
import json
from datetime import datetime
from tkinter import messagebox
from difflib import SequenceMatcher

# Set tema aplikasi
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class EnglishPracticeApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Konfigurasi window
        self.title("English Speaking Practice")
        self.geometry("900x700")
        self.minsize(800, 600)
        
        # Inisialisasi recognizer
        self.recognizer = sr.Recognizer()
        
        # Variable untuk menyimpan status rekaman
        self.recording = False
        self.recording_thread = None
        
        # Variable untuk menyimpan kalimat dan hasil
        self.sentence = ""
        self.spoken_text = ""
        self.accuracy = 0.0
        self.history = self.load_history()
        
        # Membuat folder untuk menyimpan history jika belum ada
        if not os.path.exists("data"):
            os.makedirs("data")
        
        # Membuat UI
        self.create_widgets()
        
        # Membuat tab untuk fitur tambahan
        self.create_tabs()
    
    def create_widgets(self):
        # Frame utama
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Judul aplikasi
        self.title_label = ctk.CTkLabel(
            self.main_frame, 
            text="English Speaking Practice", 
            font=ctk.CTkFont(size=28, weight="bold")
        )
        self.title_label.pack(pady=(0, 20))
        
        # Tabs untuk berbagai fitur
        self.tabview = ctk.CTkTabview(self.main_frame)
        self.tabview.pack(fill=tk.BOTH, expand=True)
        
        # Tab utama
        self.tab_practice = self.tabview.add("Latihan")
        self.tab_history = self.tabview.add("Riwayat")
        self.tab_settings = self.tabview.add("Pengaturan")
        
        # Set default tab
        self.tabview.set("Latihan")
        
        # Setup tab latihan
        self.setup_practice_tab()
        
        # Setup tab riwayat
        self.setup_history_tab()
        
        # Setup tab pengaturan
        self.setup_settings_tab()
    
    def setup_practice_tab(self):
        # Frame untuk input kalimat
        self.input_frame = ctk.CTkFrame(self.tab_practice)
        self.input_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.input_label = ctk.CTkLabel(
            self.input_frame, 
            text="Masukkan kalimat yang ingin Anda latih:", 
            font=ctk.CTkFont(size=16)
        )
        self.input_label.pack(anchor="w", pady=(10, 5))
        
        self.sentence_entry = ctk.CTkTextbox(
            self.input_frame, 
            height=80,
            font=ctk.CTkFont(size=14)
        )
        self.sentence_entry.pack(fill=tk.X, pady=5)
        
        self.sample_sentences_frame = ctk.CTkFrame(self.input_frame)
        self.sample_sentences_frame.pack(fill=tk.X, pady=5)
        
        self.sample_label = ctk.CTkLabel(
            self.sample_sentences_frame,
            text="Atau pilih contoh kalimat:",
            font=ctk.CTkFont(size=14)
        )
        self.sample_label.pack(anchor="w", pady=5)
        
        self.sample_sentences = [
            "The quick brown fox jumps over the lazy dog.",
            "How are you doing today?",
            "Could you please tell me where the nearest restaurant is?",
            "I need to improve my English pronunciation.",
            "What's the weather like today?"
        ]
        
        self.sample_buttons_frame = ctk.CTkFrame(self.sample_sentences_frame)
        self.sample_buttons_frame.pack(fill=tk.X, pady=5)
        
        for i, sentence in enumerate(self.sample_sentences):
            btn = ctk.CTkButton(
                self.sample_buttons_frame,
                text=f"Kalimat {i+1}",
                command=lambda s=sentence: self.use_sample_sentence(s),
                width=100
            )
            btn.pack(side=tk.LEFT, padx=5)
        
        # Frame untuk rekaman
        self.record_frame = ctk.CTkFrame(self.tab_practice)
        self.record_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.record_label = ctk.CTkLabel(
            self.record_frame, 
            text="Tekan tombol untuk merekam ucapan Anda:", 
            font=ctk.CTkFont(size=16)
        )
        self.record_label.pack(anchor="w", pady=(10, 5))
        
        self.button_frame = ctk.CTkFrame(self.record_frame)
        self.button_frame.pack(fill=tk.X, pady=5)
        
        self.record_button = ctk.CTkButton(
            self.button_frame,
            text="Mulai Merekam",
            font=ctk.CTkFont(size=14),
            command=self.toggle_recording,
            fg_color="#4CAF50",
            hover_color="#45a049",
            width=200
        )
        self.record_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.clear_button = ctk.CTkButton(
            self.button_frame,
            text="Bersihkan",
            font=ctk.CTkFont(size=14),
            command=self.clear_results,
            fg_color="#FF9800",
            hover_color="#F57C00",
            width=150
        )
        self.clear_button.pack(side=tk.LEFT)
        
        self.status_label = ctk.CTkLabel(
            self.record_frame,
            text="Status: Siap",
            font=ctk.CTkFont(size=14)
        )
        self.status_label.pack(pady=(5, 10))
        
        # Frame untuk hasil
        self.result_frame = ctk.CTkFrame(self.tab_practice)
        self.result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.result_label = ctk.CTkLabel(
            self.result_frame, 
            text="Hasil Latihan:", 
            font=ctk.CTkFont(size=16)
        )
        self.result_label.pack(anchor="w", pady=(10, 5))
        
        self.comparison_frame = ctk.CTkFrame(self.result_frame)
        self.comparison_frame.pack(fill=tk.X, pady=5)
        
        self.original_label = ctk.CTkLabel(
            self.comparison_frame,
            text="Kalimat Asli:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.original_label.pack(anchor="w", padx=10, pady=(10, 5))
        
        self.original_text = ctk.CTkLabel(
            self.comparison_frame,
            text="-",
            font=ctk.CTkFont(size=14),
            wraplength=700
        )
        self.original_text.pack(anchor="w", padx=10, pady=5)
        
        self.spoken_label = ctk.CTkLabel(
            self.comparison_frame,
            text="Kalimat Anda:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.spoken_label.pack(anchor="w", padx=10, pady=(10, 5))
        
        self.spoken_text_label = ctk.CTkLabel(
            self.comparison_frame,
            text="-",
            font=ctk.CTkFont(size=14),
            wraplength=700
        )
        self.spoken_text_label.pack(anchor="w", padx=10, pady=5)
        
        self.accuracy_frame = ctk.CTkFrame(self.result_frame)
        self.accuracy_frame.pack(fill=tk.X, pady=10)
        
        self.accuracy_label = ctk.CTkLabel(
            self.accuracy_frame,
            text="Akurasi Pengucapan:",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.accuracy_label.pack(anchor="w", padx=10, pady=(10, 5))
        
        self.progress_bar = ctk.CTkProgressBar(
            self.accuracy_frame,
            orientation="horizontal",
            mode="determinate"
        )
        self.progress_bar.pack(fill=tk.X, padx=10, pady=5)
        self.progress_bar.set(0)
        
        self.accuracy_value = ctk.CTkLabel(
            self.accuracy_frame,
            text="0%",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.accuracy_value.pack(pady=5)
        
        self.feedback_label = ctk.CTkLabel(
            self.result_frame,
            text="Koreksi dan Saran:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.feedback_label.pack(anchor="w", padx=10, pady=(10, 5))
        
        self.feedback_text = ctk.CTkLabel(
            self.result_frame,
            text="-",
            font=ctk.CTkFont(size=14),
            wraplength=700
        )
        self.feedback_text.pack(anchor="w", padx=10, pady=5)
    
    def setup_history_tab(self):
        # Frame untuk history
        self.history_frame = ctk.CTkFrame(self.tab_history)
        self.history_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.history_label = ctk.CTkLabel(
            self.history_frame,
            text="Riwayat Latihan:",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        self.history_label.pack(pady=(10, 20))
        
        # Scrollable frame untuk history items
        self.history_scrollable = ctk.CTkScrollableFrame(
            self.history_frame,
            width=700,
            height=400
        )
        self.history_scrollable.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Display history items
        self.display_history()
        
        # Button untuk menghapus history
        self.clear_history_button = ctk.CTkButton(
            self.history_frame,
            text="Hapus Semua Riwayat",
            command=self.clear_history,
            fg_color="#F44336",
            hover_color="#D32F2F"
        )
        self.clear_history_button.pack(pady=10)
    
    def setup_settings_tab(self):
        # Frame untuk settings
        self.settings_frame = ctk.CTkFrame(self.tab_settings)
        self.settings_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.settings_label = ctk.CTkLabel(
            self.settings_frame,
            text="Pengaturan:",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        self.settings_label.pack(pady=(10, 20))
        
        # Appearance mode settings
        self.appearance_frame = ctk.CTkFrame(self.settings_frame)
        self.appearance_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.appearance_label = ctk.CTkLabel(
            self.appearance_frame,
            text="Tema Aplikasi:",
            font=ctk.CTkFont(size=16)
        )
        self.appearance_label.pack(anchor="w", padx=10, pady=5)
        
        self.appearance_option = ctk.CTkOptionMenu(
            self.appearance_frame,
            values=["System", "Light", "Dark"],
            command=self.change_appearance_mode
        )
        self.appearance_option.pack(padx=10, pady=5)
        self.appearance_option.set("System")
        
        # About section
        self.about_frame = ctk.CTkFrame(self.settings_frame)
        self.about_frame.pack(fill=tk.X, padx=10, pady=20)
        
        self.about_label = ctk.CTkLabel(
            self.about_frame,
            text="Tentang Aplikasi:",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.about_label.pack(anchor="w", padx=10, pady=5)
        
        self.about_text = ctk.CTkLabel(
            self.about_frame,
            text="English Speaking Practice adalah aplikasi untuk berlatih pengucapan bahasa Inggris. "
                 "Aplikasi ini membantu meningkatkan kemampuan berbicara dengan memberikan umpan balik instan.",
            font=ctk.CTkFont(size=14),
            wraplength=700,
            justify="left"
        )
        self.about_text.pack(anchor="w", padx=10, pady=5)
        
        self.version_label = ctk.CTkLabel(
            self.about_frame,
            text="Versi: 1.0.0",
            font=ctk.CTkFont(size=14)
        )
        self.version_label.pack(anchor="w", padx=10, pady=5)
    
    def create_tabs(self):
        pass  # Already implemented in create_widgets
    
    def use_sample_sentence(self, sentence):
        self.sentence_entry.delete("1.0", tk.END)
        self.sentence_entry.insert("1.0", sentence)
    
    def toggle_recording(self):
        if not self.recording:
            self.sentence = self.sentence_entry.get("1.0", tk.END).strip()
            if not self.sentence:
                self.status_label.configure(text="Status: Silakan masukkan kalimat terlebih dahulu")
                return
                
            self.original_text.configure(text=self.sentence)
            self.recording = True
            self.record_button.configure(text="Berhenti Merekam", fg_color="#F44336", hover_color="#D32F2F")
            self.status_label.configure(text="Status: Merekam...")
            
            # Memulai rekaman dalam thread terpisah
            self.recording_thread = threading.Thread(target=self.record_audio)
            self.recording_thread.daemon = True
            self.recording_thread.start()
        else:
            self.recording = False
            self.record_button.configure(text="Mulai Merekam", fg_color="#4CAF50", hover_color="#45a049")
            self.status_label.configure(text="Status: Memproses...")
    
    def record_audio(self):
        try:
            with sr.Microphone() as source:
                self.status_label.configure(text="Status: Merekam... (bicara sekarang)")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                
                self.status_label.configure(text="Status: Memproses...")
                
                # Gunakan Google Speech Recognition untuk mengenali audio
                self.spoken_text = self.recognizer.recognize_google(audio, language="en-US")
                
                # Update tampilan
                self.spoken_text_label.configure(text=self.spoken_text)
                
                # Hitung akurasi
                self.accuracy = self.calculate_similarity(self.spoken_text, self.sentence)
                
                # Update tampilan akurasi
                self.progress_bar.set(self.accuracy / 100)
                self.accuracy_value.configure(text=f"{self.accuracy:.1f}%")
                
                # Generate feedback
                feedback = self.generate_feedback(self.sentence, self.spoken_text)
                self.feedback_text.configure(text=feedback)
                
                # Simpan ke history
                self.save_to_history()
                
                # Reset status
                self.status_label.configure(text="Status: Siap")
                self.recording = False
                self.record_button.configure(text="Mulai Merekam", fg_color="#4CAF50", hover_color="#45a049")
                
        except sr.WaitTimeoutError:
            self.status_label.configure(text="Status: Waktu habis, tidak ada suara terdeteksi")
            messagebox.showwarning("Peringatan", "Tidak ada suara terdeteksi!")
            self.recording = False
            self.record_button.configure(text="Mulai Merekam", fg_color="#4CAF50", hover_color="#45a049")
            
        except sr.UnknownValueError:
            self.status_label.configure(text="Status: Ucapan tidak dapat dikenali")
            messagebox.showwarning("Peringatan", "Ucapan tidak dapat dikenali!")
            self.recording = False
            self.record_button.configure(text="Mulai Merekam", fg_color="#4CAF50", hover_color="#45a049")
            
        except sr.RequestError as e:
            self.status_label.configure(text="Status: Error saat memproses")
            messagebox.showerror("Error", f"Error pada layanan Google Speech Recognition: {e}")
            self.recording = False
            self.record_button.configure(text="Mulai Merekam", fg_color="#4CAF50", hover_color="#45a049")
            
        except Exception as e:
            self.status_label.configure(text="Status: Error")
            messagebox.showerror("Error", f"Error saat merekam: {e}")
            self.recording = False
            self.record_button.configure(text="Mulai Merekam", fg_color="#4CAF50", hover_color="#45a049")
    
    def calculate_similarity(self, text1, text2):
        # Gunakan SequenceMatcher untuk menghitung kemiripan teks
        matcher = SequenceMatcher(None, text1.lower(), text2.lower())
        similarity = matcher.ratio() * 100
        return similarity
    
    def generate_feedback(self, original, spoken):
        # Fungsi sederhana untuk mengenali perbedaan kata dan memberikan saran
        original_words = original.lower().split()
        spoken_words = spoken.lower().split()
        
        # Jika spoken sama persis dengan original
        if original.lower() == spoken.lower():
            return "Pengucapan sempurna! Tidak ada koreksi yang diperlukan."
        
        # Jika panjang sangat berbeda
        if abs(len(original_words) - len(spoken_words)) > 3:
            return "Kalimat yang diucapkan terlalu berbeda dari kalimat asli. Coba lagi dengan lebih hati-hati."
        
        # Cari kata yang berbeda
        feedback_parts = []
        
        # Gunakan difflib sequence matcher untuk menemukan operasi yang diperlukan
        s = SequenceMatcher(None, original_words, spoken_words)
        for tag, i1, i2, j1, j2 in s.get_opcodes():
            if tag == 'replace':
                for i, word in enumerate(original_words[i1:i2]):
                    if i + i1 < len(original_words) and i + j1 < len(spoken_words):
                        feedback_parts.append(f"'{spoken_words[i+j1]}' seharusnya '{original_words[i+i1]}'")
            elif tag == 'delete':
                for word in original_words[i1:i2]:
                    feedback_parts.append(f"Kata '{word}' tidak terdeteksi")
            elif tag == 'insert':
                for word in spoken_words[j1:j2]:
                    feedback_parts.append(f"Kata '{word}' tidak ada pada kalimat asli")
        
        if not feedback_parts:
            # Jika tidak ada perbedaan spesifik yang terdeteksi tapi nilainya < 100%
            return "Ada perbedaan pada pengucapan. Perhatikan intonasi dan pengucapan setiap kata."
        
        # Batasi jumlah feedback untuk menghindari terlalu banyak teks
        if len(feedback_parts) > 3:
            feedback_parts = feedback_parts[:3]
            feedback_parts.append("... dan perbedaan lainnya.")
            
        return "Koreksi: " + "; ".join(feedback_parts)
    
    def clear_results(self):
        self.sentence_entry.delete("1.0", tk.END)
        self.original_text.configure(text="-")
        self.spoken_text_label.configure(text="-")
        self.progress_bar.set(0)
        self.accuracy_value.configure(text="0%")
        self.feedback_text.configure(text="-")
        self.status_label.configure(text="Status: Siap")
    
    def load_history(self):
        try:
            if os.path.exists("data/history.json"):
                with open("data/history.json", "r") as file:
                    return json.load(file)
            return []
        except Exception:
            return []
    
    def save_history(self):
        try:
            with open("data/history.json", "w") as file:
                json.dump(self.history, file)
        except Exception as e:
            print(f"Error saving history: {e}")
    
    def save_to_history(self):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = {
            "timestamp": timestamp,
            "original": self.sentence,
            "spoken": self.spoken_text,
            "accuracy": self.accuracy
        }
        self.history.append(entry)
        self.save_history()
    
    def display_history(self):
        # Clear existing widgets
        for widget in self.history_scrollable.winfo_children():
            widget.destroy()
        
        # Sort history by date (newest first)
        sorted_history = sorted(self.history, key=lambda x: x["timestamp"], reverse=True)
        
        if not sorted_history:
            no_data_label = ctk.CTkLabel(
                self.history_scrollable,
                text="Belum ada riwayat latihan.",
                font=ctk.CTkFont(size=14)
            )
            no_data_label.pack(pady=20)
            return
        
        # Add history items
        for i, entry in enumerate(sorted_history):
            item_frame = ctk.CTkFrame(self.history_scrollable)
            item_frame.pack(fill=tk.X, pady=5)
            
            header_frame = ctk.CTkFrame(item_frame)
            header_frame.pack(fill=tk.X)
            
            date_label = ctk.CTkLabel(
                header_frame,
                text=f"Tanggal: {entry['timestamp']}",
                font=ctk.CTkFont(size=12)
            )
            date_label.pack(side=tk.LEFT, padx=10, pady=5)
            
            accuracy_label = ctk.CTkLabel(
                header_frame,
                text=f"Akurasi: {entry['accuracy']:.1f}%",
                font=ctk.CTkFont(size=12, weight="bold")
            )
            accuracy_label.pack(side=tk.RIGHT, padx=10, pady=5)
            
            content_frame = ctk.CTkFrame(item_frame)
            content_frame.pack(fill=tk.X, padx=5, pady=5)
            
            original_label = ctk.CTkLabel(
                content_frame,
                text=f"Kalimat Asli: {entry['original']}",
                font=ctk.CTkFont(size=12),
                wraplength=650,
                justify="left"
            )
            original_label.pack(anchor="w", padx=10, pady=2)
            
            spoken_label = ctk.CTkLabel(
                content_frame,
                text=f"Kalimat Anda: {entry['spoken']}",
                font=ctk.CTkFont(size=12),
                wraplength=650,
                justify="left"
            )
            spoken_label.pack(anchor="w", padx=10, pady=2)
            
    def clear_history(self):
        self.history = []
        self.save_history()
        self.display_history()
    
    def change_appearance_mode(self, new_appearance_mode):
        ctk.set_appearance_mode(new_appearance_mode)

# Menjalankan aplikasi
if __name__ == "__main__":
    app = EnglishPracticeApp()
    app.mainloop() 