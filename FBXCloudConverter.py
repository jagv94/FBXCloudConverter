import os
import subprocess
import sys
import tempfile
import shutil
import tkinter as tk
import threading
from tkinter import filedialog, messagebox, scrolledtext

# Determine the base directory where the script or executable is located
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Define the path to the CloudCompare executable (assumed to be bundled in Tools/CloudCompare/)
CLOUDCOMPARE_PATH = os.path.join(BASE_DIR, "Tools", "CloudCompare", "CloudCompare.exe")

def apply_transformation(input_file):
    """
    Applies a transformation to the input 3D file using CloudCompare,
    exporting the result as FBX. A temporary identity matrix is used for this purpose.
    The process is visualized in a GUI with real-time logging.
    """
    if not os.path.exists(CLOUDCOMPARE_PATH):
        messagebox.showerror("Error", f"CloudCompare not found at {CLOUDCOMPARE_PATH}")
        return

    # Create a temporary identity matrix file for transformation
    with tempfile.NamedTemporaryFile(delete=False, mode="w", suffix=".txt") as temp_matrix:
        temp_matrix.write("\n".join([
            "1.0 0.0 0.0 0.0",
            "0.0 1.0 0.0 0.0",
            "0.0 0.0 1.0 0.0",
            "0.0 0.0 0.0 1.0"
        ]))
        matrix_file = temp_matrix.name

    # Prepare CloudCompare command-line arguments
    command = [
        CLOUDCOMPARE_PATH, '-SILENT', '-AUTO_SAVE', 'OFF',
        '-M_EXPORT_FMT', 'FBX', '-FBX', '-EXPORT_FMT', 'FBX_binary', '-O',
        '-GLOBAL_SHIFT', 'AUTO', input_file, '-APPLY_TRANS',
        '-APPLY_TO_GLOBAL', 'FORCE', matrix_file, '-NO_TIMESTAMP',
        '-SAVE_MESHES'
    ]

    def execute():
        # Execute the command in a subprocess, capturing its output
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

        # Stream CloudCompare output in real-time to the GUI
        for line in process.stdout:
            progress_text.insert(tk.END, line)
            progress_text.see(tk.END)  # Auto-scroll
            root.update_idletasks()   # Ensure GUI remains responsive

        process.stdout.close()
        process.wait()

        # Notify the user on completion
        root.after(0, lambda: messagebox.showinfo("Process Completed", "CloudCompare has finished."))
        root.after(0, root.quit)

        # Clean up temporary matrix file
        os.remove(matrix_file)

    # Create a simple GUI window to display the processing output
    root = tk.Tk()
    root.title("Conversion Progress")

    progress_text = scrolledtext.ScrolledText(root, width=80, height=20)
    progress_text.pack(padx=10, pady=10)

    threading.Thread(target=execute, daemon=True).start()
    root.mainloop()

def select_alternative_action(file_path):
    """
    Displays a dialog to ask the user what to do when the destination file already exists.
    Options: move to another location, delete, or keep the existing file.
    """
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    action = None

    def set_action(value):
        nonlocal action
        action = value
        window.quit()
        window.destroy()

    window = tk.Toplevel()
    window.title("File Already Exists")
    window.geometry("400x200")
    tk.Label(window, text=f"The file '{file_path}' already exists.\nWhat would you like to do?", pady=10).pack()

    tk.Button(window, text="Move to another location", command=lambda: set_action("mover")).pack(pady=5)
    tk.Button(window, text="Delete the generated file", command=lambda: set_action("eliminar")).pack(pady=5)
    tk.Button(window, text="Keep it in current location", command=lambda: set_action("mantener")).pack(pady=5)

    window.mainloop()
    
    return action

def move_generated_files(input_file, destination_folder):
    """
    Moves the generated FBX and FBM files from the source to the user-selected destination.
    Handles conflicts if the destination file already exists.
    """
    source_folder = os.path.dirname(input_file)
    file_name = os.path.splitext(os.path.basename(input_file))[0]

    transformed_fbx = f"{file_name}_TRANSFORMED.fbx"
    transformed_fbm = f"{file_name}_TRANSFORMED.fbm"

    fbx_path = os.path.join(source_folder, transformed_fbx)
    destination_fbx = os.path.join(destination_folder, transformed_fbx)

    fbm_path = os.path.join(source_folder, transformed_fbm)
    destination_fbm = os.path.join(destination_folder, transformed_fbm)

    # If source and destination folders are the same, skip moving
    if os.path.normpath(source_folder) == os.path.normpath(destination_folder):
        messagebox.showinfo("Same Destination", "Files are already in the selected location.")
        return

    # Handle conflicts if the file already exists in the destination
    while os.path.exists(destination_fbx):
        overwrite = messagebox.askyesno("File Exists", f"The file '{destination_fbx}' already exists. Overwrite it?")
        if overwrite:
            os.remove(destination_fbx)
            break
        else:
            action = select_alternative_action(destination_fbx)
            if action == "mover":
                new_folder = filedialog.askdirectory(title="Select New Destination")
                if new_folder:
                    destination_fbx = os.path.join(new_folder, transformed_fbx)
                    destination_fbm = os.path.join(new_folder, transformed_fbm)

                    if os.path.normpath(new_folder) == os.path.normpath(source_folder):
                        messagebox.showinfo("Same Destination", "Files are already in the selected location.")
                        return
            elif action == "eliminar":
                os.remove(fbx_path)
                return
            elif action == "mantener":
                return

    # Move FBX and FBM files if they exist and are not already in the target location
    if os.path.exists(fbx_path) and os.path.normpath(fbx_path) != os.path.normpath(destination_fbx):
        shutil.move(fbx_path, destination_fbx)
    
    if os.path.exists(fbm_path) and os.path.normpath(fbm_path) != os.path.normpath(destination_fbm):
        shutil.move(fbm_path, destination_fbm)

if __name__ == "__main__":
    # Ask the user to select an input 3D file
    input_file = filedialog.askopenfilename(
        title="Select a file",
        filetypes=[("Supported files", "*.las *.laz *.e57 *.xyz *.ply *.pts *.obj *.stl *.glb *.gltf *.dxf"), ("All files", "*.*")]
    )
    if not input_file:
        messagebox.showerror("Error", "No file was selected.")
        sys.exit()

    # Ask for a destination folder for the processed files
    destination_folder = filedialog.askdirectory(title="Select Destination Folder")
    if not destination_folder:
        messagebox.showerror("Error", "No destination folder was selected.")
        sys.exit()

    messagebox.showinfo("Start", f"Selected file: {input_file}\nDestination: {destination_folder}")

    # Run the transformation and move the output
    try:
        apply_transformation(input_file)
        move_generated_files(input_file, destination_folder)
        messagebox.showinfo("Finished", "Files have been processed successfully.")
    except Exception as e:
        messagebox.showerror("Error", str(e))