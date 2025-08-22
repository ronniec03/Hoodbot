import os
import sys
import winshell
from win32com.client import Dispatch

# Paths
project_dir = r"C:\Users\Justin\Documents\CompanionAI"
script_path = os.path.join(project_dir, "src", "carmen_core.py")
shortcut_path = os.path.join(os.path.expanduser("~"), "Desktop", "Carmen.lnk")

def create_shortcut():
    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(shortcut_path)
    shortcut.Targetpath = sys.executable  # Python exe
    shortcut.Arguments = f'"{script_path}"'
    shortcut.WorkingDirectory = project_dir
    shortcut.IconLocation = sys.executable  # Python icon, can replace with custom .ico
    shortcut.save()
    print(f"✅ Shortcut created on Desktop: {shortcut_path}")

if __name__ == "__main__":
    create_shortcut()
