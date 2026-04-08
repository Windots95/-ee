import ctypes
from ctypes import wintypes
import random
import time
import sys
import os
import threading

# Windows API Setup
user32 = ctypes.windll.user32
gdi32 = ctypes.windll.gdi32
kernel32 = ctypes.windll.kernel32
mci = ctypes.windll.winmm 

# Path to your Downloads folder
DOWNLOADS_PATH = os.path.join(os.path.expanduser("~"), "Downloads")

# Mapping your uploaded files exactly as named in your Downloads
SOUND_FILES = {
    1: "salinewin.exe-1-made-with-Voicemod.mp3",
    2: "salinewin.exe-2-made-with-Voicemod.mp3",
    3: "salinewin.exe-3-made-with-Voicemod.mp3",
    4: "salinewin.exe-4-made-with-Voicemod.mp3",
    6: "salinewin.exe-6-(this-is-fire,-trust-me!!)-made-with-Voicemod.mp3",
    7: "salinewin.exe-7-made-with-Voicemod.mp3",
    8: "salinewin.exe-8-made-with-Voicemod.mp3",
    9: "salinewin.exe-9-(fire-warning)-made-with-Voicemod.mp3"
}

def stop_all_audio():
    """Stops any currently playing glitch audio to prevent overlapping loops."""
    for i in SOUND_FILES:
        mci.mciSendStringW(f"close glitch_{i}", None, 0, 0)

def play_mp3_loop(index):
    """Starts playing an MP3 from Downloads in a continuous loop."""
    stop_all_audio()
    if index in SOUND_FILES:
        file_path = os.path.join(DOWNLOADS_PATH, SOUND_FILES[index])
        if os.path.exists(file_path):
            alias = f"glitch_{index}"
            # Open the file and play with the 'repeat' flag
            mci.mciSendStringW(f"open \"{file_path}\" type mpegvideo alias {alias}", None, 0, 0)
            mci.mciSendStringW(f"play {alias} repeat", None, 0, 0)

def show_message(title, text):
    return user32.MessageBoxW(0, text, title, 4 | 48)

def minimize_console():
    hWnd = kernel32.GetConsoleWindow()
    if hWnd:
        user32.ShowWindow(hWnd, 6)

def system_glitch_overload():
    # --- SAFETY CHECKPOINTS ---
    if show_message("System Execution", "You have executed this program. If you want to continue, press YES on your keyboard. If you press NO, the program will not start.") != 6: 
        sys.exit()

    if show_message("FINAL WARNING", "This will give you flashing lights and effects. If you still want to continue, click YES. If you don't click NO.") != 6:
        sys.exit()

    minimize_console()
    sw, sh = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    
    # REQUIRED: First stage is locked to Stage 0
    current_stage = 0
    
    # UPDATED: 30 seconds per stage as requested
    STAGE_TIME_LIMIT = 30 
    start_time = time.time()
    
    # Start the first loop (Sound #1 for Stage 0)
    play_mp3_loop(1)

    print(f"!!! SYSTEM OVERLOAD: STAGE {current_stage} STARTING !!!")
    print(f"Time limit per stage set to 30 seconds.")

    try:
        while True:
            now = time.time()
            
            # Switch stages and update the looping sound after 30 SECONDS
            if now - start_time > STAGE_TIME_LIMIT:
                # Randomize the next stage
                current_stage = random.choice([0, 1, 2, 3, 7, 10, 14, 15, 17])
                start_time = now
                
                # Assign sounds to the selected stage
                if current_stage == 0: play_mp3_loop(1)
                elif current_stage == 1: play_mp3_loop(2)
                elif current_stage == 2: play_mp3_loop(3)
                elif current_stage == 3: play_mp3_loop(4)
                elif current_stage == 7: play_mp3_loop(8)
                elif current_stage == 10: play_mp3_loop(6)
                elif current_stage == 14: play_mp3_loop(7)
                elif current_stage == 17: play_mp3_loop(9)
                else: play_mp3_loop(2) # Fallback
                
                print(f"!!! 30 SECONDS ELAPSED: SWITCHING TO STAGE {current_stage} !!!")

            hdc = user32.GetDC(0)

            # --- VISUAL ENGINE (Pixelated & Rotational Effects) ---
            if current_stage == 0: # Jitter
                gdi32.BitBlt(hdc, random.randint(-5, 5), random.randint(-5, 5), sw, sh, hdc, 0, 0, 0xCC0020)
            
            elif current_stage == 1: # Pixel Melt
                x, y = random.randint(0, sw), random.randint(0, sh)
                gdi32.BitBlt(hdc, x+random.randint(-15, 15), y+random.randint(-15, 15), 300, 300, hdc, x, y, 0xCC0020)
            
            elif current_stage == 2: # 8-Bit Noise
                brush = gdi32.CreateSolidBrush(random.randint(0, 0xFFFFFF))
                rect = wintypes.RECT(random.randint(0, sw), random.randint(0, sh), random.randint(0, sw), random.randint(0, sh))
                user32.FillRect(hdc, ctypes.byref(rect), brush)
                gdi32.DeleteObject(brush)

            elif current_stage == 3: # Classic Spin
                pts = (wintypes.POINT * 3)(wintypes.POINT(30, 0), wintypes.POINT(sw, 30), wintypes.POINT(0, sh-30))
                gdi32.PlgBlt(hdc, ctypes.byref(pts), hdc, 0, 0, sw, sh, 0, 0, 0)

            elif current_stage == 7: # Block Shift
                pw, ph = 400, 400
                gdi32.BitBlt(hdc, random.randint(0, sw), random.randint(0, sh), pw, ph, hdc, random.randint(0, sw), random.randint(0, sh), 0xCC0020)

            elif current_stage == 10: # Pixel Rotation
                size = 500
                rx, ry = random.randint(0, sw-size), random.randint(0, sh-size)
                pts = (wintypes.POINT * 3)(wintypes.POINT(rx+size, ry), wintypes.POINT(rx+size, ry+size), wintypes.POINT(rx, ry))
                gdi32.PlgBlt(hdc, ctypes.byref(pts), hdc, rx, ry, size, size, 0, 0, 0)

            elif current_stage == 14: # Screen Flip
                gdi32.StretchBlt(hdc, 0, sh, sw, -sh, hdc, 0, 0, sw, sh, 0xCC0020)

            elif current_stage == 15: # Mosaic Spread
                x, y = random.randint(0, sw), random.randint(0, sh)
                for i in range(5):
                    gdi32.BitBlt(hdc, x + (i*50), y, 50, 50, hdc, x, y, 0xCC0020)

            elif current_stage == 17: # Zoom Glitch
                gdi32.StretchBlt(hdc, -50, -50, sw+100, sh+100, hdc, 0, 0, sw, sh, 0xCC0020)

            user32.ReleaseDC(0, hdc)
            time.sleep(0.05) 

    except KeyboardInterrupt:
        stop_all_audio()
        user32.InvalidateRect(0, None, True)
        sys.exit()

if __name__ == "__main__":
    system_glitch_overload()