# =============================================================================
# Intellectual Property Notice
# -----------------------------------------------------------------------------
# This project and its source code are the exclusive intellectual property of
# Saleh Ali. All rights reserved.
#
# Unauthorized modification, reproduction, redistribution, reverse engineering,
# or creation of derivative works is strictly prohibited without prior written
# approval from Saleh Ali.
#
# For full license and disclaimer details, please refer to the LICENSE.md and
# DISCLAIMER.md files in the project root.
# =============================================================================

import subprocess
import time
import sys
import os

def start_api():
    print("[*] Starting Argus Pro API...")
    return subprocess.Popen([sys.executable, "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8000"])

def start_gui():
    print("[*] Starting Argus Pro GUI...")
    return subprocess.Popen([sys.executable, "gui/main_window.py"])

if __name__ == "__main__":
    # Add current directory to PYTHONPATH for all subprocesses
    os.environ["PYTHONPATH"] = os.getcwd() + os.pathsep + os.environ.get("PYTHONPATH", "")
    
    # Ensure database is initialized
    print("[*] Initializing Database...")
    subprocess.run([sys.executable, "scripts/init_db.py"])
    
    api_proc = start_api()
    time.sleep(2) # Wait for API to start
    
    gui_proc = start_gui()
    
    try:
        while True:
            time.sleep(1)
            if api_proc.poll() is not None:
                print("[!] API process died. Exiting.")
                break
            if gui_proc.poll() is not None:
                print("[*] GUI closed. Shutting down API.")
                api_proc.terminate()
                break
    except KeyboardInterrupt:
        api_proc.terminate()
        gui_proc.terminate()
    
    print("[*] Argus Pro stopped.")
