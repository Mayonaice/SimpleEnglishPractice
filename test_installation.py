import sys
import importlib.util
import tkinter
import platform
import os
import ctypes

def check_module_exists(module_name, package_name=None):
    """Memeriksa apakah modul dapat diimpor."""
    try:
        if package_name:
            # Coba impor paket terlebih dahulu
            importlib.import_module(package_name)
        importlib.import_module(module_name)
        return True
    except ImportError:
        return False

def print_status(module_name, exists):
    """Menampilkan status modul dengan warna."""
    status = "OK" if exists else "TIDAK TERINSTAL"
    color = "32" if exists else "31"  # 32 untuk hijau, 31 untuk merah
    print(f"[{colored(status, color)}] {module_name}")

def colored(text, color_code):
    """Memberikan warna pada teks di konsol."""
    return f"\033[{color_code}m{text}\033[0m"

def main():
    print("\n===== VERIFIKASI INSTALASI APLIKASI ENGLISH PRACTICE =====\n")
    
    # Tampilkan informasi sistem
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    arch = platform.architecture()[0]
    print(f"Python version: {sys.version}")
    print(f"Python {python_version} - {arch}")
    print(f"Platform: {platform.system()} {platform.release()}")
    print("\n")
    
    # Daftar modul yang diperlukan (modul_name, package_name)
    required_modules = [
        ("tkinter", None),
        ("customtkinter", None),
        ("PIL", "Pillow"),
        ("speech_recognition", "SpeechRecognition"),
        ("pyaudio", "PyAudio"),
        ("language_tool_python", None),
        ("json", None),
        ("threading", None),
        ("difflib", None),
        ("datetime", None)
    ]
    
    # Check setiap modul
    all_ok = True
    missing_modules = []
    missing_packages = []
    
    for module_name, package_name in required_modules:
        exists = check_module_exists(module_name, package_name)
        print_status(module_name, exists)
        if not exists:
            all_ok = False
            missing_modules.append(module_name)
            if package_name:
                missing_packages.append(package_name)
            else:
                missing_packages.append(module_name)
    
    print("\n")
    
    # Test mikrofon jika PyAudio terinstal dan platform adalah Windows
    pyaudio_installed = "pyaudio" not in missing_modules
    if pyaudio_installed and platform.system() == 'Windows':
        print("Checking microphone access...")
        try:
            import speech_recognition as sr
            r = sr.Recognizer()
            with sr.Microphone() as source:
                print("Mikrofon terdeteksi dan dapat diakses.")
                print("Mendengarkan 1 detik untuk menyesuaikan kebisingan...")
                r.adjust_for_ambient_noise(source, duration=1)
                print("Mikrofon berfungsi dengan baik.")
        except Exception as e:
            print(f"Error saat mengakses mikrofon: {e}")
            all_ok = False
    
    print("\n===== HASIL VERIFIKASI =====\n")
    
    if all_ok:
        print(colored("Semua komponen yang diperlukan terinstal dengan benar!", "32"))
        print("Anda dapat menjalankan aplikasi dengan perintah:")
        print(colored("py english_practice_app.py", "36"))  # Cyan
    else:
        print(colored("Beberapa komponen belum terinstal!", "31"))
        
        if "pyaudio" in missing_modules:
            print("\nUntuk menginstal PyAudio di Windows:")
            print("1. Unduh file wheel PyAudio yang sesuai dengan versi Python Anda dari:")
            print(colored("https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio", "36"))
            print(f"2. Cari file untuk Python {python_version} dan {arch}")
            print("   Contoh: PyAudio‑0.2.11‑cp39‑cp39‑win_amd64.whl untuk Python 3.9 64-bit")
            print("3. Instal dengan perintah:")
            print(colored("py -m pip install C:\\path\\to\\downloaded\\PyAudio-x.x.x-cpxx-cpxx-win_xxxx.whl", "36"))
            
            # Hapus PyAudio dari daftar missing packages
            if "PyAudio" in missing_packages:
                missing_packages.remove("PyAudio")
        
        if missing_packages:
            other_missing = [p for p in missing_packages if p.lower() != "pyaudio"]
            if other_missing:
                print("\nUntuk menginstal modul lain yang belum terinstal:")
                print(colored(f"py -m pip install {' '.join(other_missing)}", "36"))

if __name__ == "__main__":
    # Check if running in a terminal that supports ANSI colors
    if platform.system() == 'Windows':
        try:
            # Enable ANSI colors on Windows
            os.system('')
            # Alternative method for Windows 10+
            kernel32 = ctypes.windll.kernel32
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
        except:
            pass
    
    main() 