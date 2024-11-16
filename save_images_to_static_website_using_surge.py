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

print(f"Files found: {files}")  # Debugging print

# Separate files into PNG and HTML pairs
file_pairs = {}
for file in files:
    name, ext = os.path.splitext(file)
    if ext.lower() == ".png":
        if name not in file_pairs:
            file_pairs[name] = {"png": file}
        else:
            file_pairs[name]["png"] = file
    elif ext.lower() == ".html":
        if name not in file_pairs:
            file_pairs[name] = {"html": file}
        else:
            file_pairs[name]["html"] = file

print(f"File pairs before filtering: {file_pairs}")  # Debugging print

# Filter out incomplete pairs (missing either png or html)
filtered_file_pairs = {name: pair for name, pair in file_pairs.items() if "png" in pair and "html" in pair}
print(f"Filtered file pairs: {filtered_file_pairs}")  # Debugging print

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
    index_file.write("    <style>\n")
    index_file.write("        body { font-family: Arial, sans-serif; }\n")
    index_file.write("        .gallery { display: flex; flex-wrap: wrap; gap: 20px; justify-content: center; }\n")
    index_file.write("        .gallery-item { flex: 1 1 calc(50% - 20px); max-width: calc(50% - 20px); box-sizing: border-box; }\n")
    index_file.write("        .gallery-item img { width: 100%; height: auto; }\n")
    index_file.write("        @media (max-width: 600px) {\n")
    index_file.write("            .gallery-item { flex: 1 1 100%; max-width: 100%; }\n")
    index_file.write("        }\n")
    index_file.write("    </style>\n")
    index_file.write("</head>\n")
    index_file.write("<body>\n")
    index_file.write("    <h1>Graficos interativos</h1>\n")
    index_file.write("    <div class='gallery'>\n")

    # Add image thumbnails with links to corresponding HTML files
    for name, pair in filtered_file_pairs.items():
        png_file = pair["png"]
        html_file = pair["html"]
        png_url = f"{base_url}/{png_file}"
        html_url = f"{base_url}/{html_file}"
        print(f"Adding to index: PNG - {png_file}, HTML - {html_file}")  # Debugging print
        index_file.write(f"        <div class='gallery-item'><a href='{html_url}' target={name}><img src='{png_url}' alt='{name}'></a></div>\n")

    # Close the HTML structure
    index_file.write("    </div>\n")
    index_file.write("</body>\n")
    index_file.write("</html>\n")

print(f"{index_filename} has been created with linked images.")
create_surgeignore(images_folder, EXTENSIONS)
run_surge(images_folder, DOMAIN)
