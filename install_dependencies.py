import os
import subprocess
import sys

# List of dependencies to install
dependencies = [
    "pandas",
    "unidecode",
    "numpy",
    "keyboard",
    "plotly",
    "scikit-learn"
]

def install_dependencies():
    # Iterate over each dependency and install using pip
    for package in dependencies:
        print(f"Installing {package}...")
        try:
            process = subprocess.Popen(
                [sys.executable, "-m", "pip", "install", package],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True  # Ensure output is in text format
            )
            
            # Display output and errors in real-time
            for line in process.stdout:
                print(line, end='')
            for line in process.stderr:
                print(line, end='')
            
            process.wait()  # Wait for the process to finish
            
            if process.returncode == 0:
                print(f"Successfully installed {package}.\n")
            else:
                print(f"Failed to install {package}. Please try installing it manually.\n")

        except Exception as e:
            print(f"An error occurred while installing {package}: {e}\n")

if __name__ == "__main__":
    print("Starting dependency installation process...\n")
    install_dependencies()
    print("\nAll dependencies have been processed.")
