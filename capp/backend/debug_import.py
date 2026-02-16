import sys
import traceback
import os

# Add current directory to sys.path
sys.path.append(os.getcwd())

print(f"Attempting to import main from {os.getcwd()}...")

try:
    import main
    print("Successfully imported main.")
except Exception:
    traceback.print_exc()
