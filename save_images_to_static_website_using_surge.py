import os
import subprocess

# CONFIGURATION
EXTENSIONS = ['.html', '.htm', '.png']
DOMAIN = "mdt-cienciadedados.surge.sh"
SUBFOLDER = "images"

def create_surgeignore(images_folder, EXTENSIONS):
    # Define the path for the .surgeignore file
    surgeignore_path = os.path.join(images_folder, ".surgeignore")
    
    # Open the file in write mode
    with open(surgeignore_path, "w", encoding="utf-8") as f:
        # Write the first line as '*'
        f.write("*\n")
        
        # Write one line for each extension in EXTENSIONS, formatted like "!*.extension"
        for extension in EXTENSIONS:
            f.write(f"!*{extension}\n")

    print(f".surgeignore file created at {surgeignore_path}")

def run_surge(images_folder, domain):
    try:
        surge_path = r"surge.cmd"
        print(f"Command: {[surge_path, images_folder, domain]}")
        subprocess.run(
            [surge_path, images_folder, domain],
            check=True,
            text=True,
        )
        print("Surge program executed successfully.")
    except FileNotFoundError:
        print("Error: 'surge' command not found. Ensure it is installed and the path is correct.")
    except subprocess.CalledProcessError as e:
        print("Error while executing the surge program:")
        print("Return Code:", e.returncode)

# Get list of files with supported extensions, excluding index.html
base_url = f"https://{DOMAIN}"
current_folder = os.getcwd()
images_folder = os.path.join(current_folder, SUBFOLDER)
files = [
    f for f in os.listdir(images_folder)
    if os.path.isfile(os.path.join(images_folder, f))
    and os.path.splitext(f)[1].lower() in EXTENSIONS
    and f != "index.html"
]
# Create or overwrite index.html
index_filename = os.path.join(images_folder, "index.html")
with open(index_filename, "w", encoding="utf-8") as index_file:
    # Start the HTML structure
    index_file.write("<!DOCTYPE html>\n")
    index_file.write("<html lang='en'>\n")
    index_file.write("<head>\n")
    index_file.write("    <meta charset='UTF-8'>\n")
    index_file.write("    <meta name='viewport' content='width=device-width, initial-scale=1.0'>\n")
    index_file.write("    <title>MDT - Ciencia de Dados</title>\n")
    index_file.write("</head>\n")
    index_file.write("<body>\n")
    index_file.write("    <h1>Graficos interativos</h1>\n")
    index_file.write("    <ul>\n")

    # Add links to files
    for file in files:
        file_url = f"{base_url}/{file}"
        index_file.write(f"        <li><a href='{file_url}' target={file}>{file}</a><br></li>\n")

    # Close the HTML structure
    index_file.write("    </ul>\n")
    index_file.write("</body>\n")
    index_file.write("</html>\n")

print(f"{index_filename} has been created with links to {len(files)} files.")
create_surgeignore(images_folder, EXTENSIONS)
run_surge(images_folder, DOMAIN)
