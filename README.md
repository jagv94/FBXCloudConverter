# 🛠️ 3D Conversion Tool with CloudCompare

A lightweight, GUI-based utility to convert photogrammetry or laser-scanned 3D models into `.fbx` format using [CloudCompare](https://www.danielgm.net/cc/). Designed for simplicity, automation, and extendability.

---

## 📆 Features

* 🎨 Convert a wide range of 3D formats to **binary FBX**
* 🔄 Apply transformation matrices (defaults to identity)
* 📁 Move output files to a chosen destination
* ❓ Handle existing file conflicts with interactive GUI options
* 🌎 Cross-compatible with common 3D formats: `.las`, `.obj`, `.ply`, etc.
* ⚡ Fast execution with real-time output monitoring

---

## 📂 Project Structure

```
ProjectRoot/
├── convert.py
└── Tools/
    └── CloudCompare/
        └── CloudCompare.exe
```

Make sure `CloudCompare.exe` is located at `Tools/CloudCompare/` relative to the script.

---

## 💻 Requirements

* Python 3.x
* No external dependencies (uses only Python standard library):

  * `os`, `sys`, `shutil`, `subprocess`, `tempfile`, `tkinter`, `threading`

---

## 🚀 How to Use

1. Run `convert.py`
2. Select a supported 3D model file
3. Choose a destination folder for the output
4. Monitor the CloudCompare process in the popup window
5. Resolve file conflicts if prompted (overwrite, move, delete, or keep)

---

## ⚙️ How It Works

### Main Workflow:

* **`apply_transformation(input_file)`**

  * Creates a temporary identity matrix file
  * Executes CloudCompare in silent mode
  * Applies the matrix and exports as `.fbx`

* **`move_generated_files(input_file, destination_folder)`**

  * Moves `.fbx` and `.fbm` to the selected folder
  * Handles overwriting or relocating conflicts via GUI

* **`select_alternative_action(file_path)`**

  * Prompts the user with action options if output already exists

### Example CloudCompare Command:

```bash
CloudCompare.exe -SILENT -AUTO_SAVE OFF -M_EXPORT_FMT FBX -FBX \
  -EXPORT_FMT FBX_binary -O -GLOBAL_SHIFT AUTO <input_file> \
  -APPLY_TRANS -APPLY_TO_GLOBAL FORCE <matrix_file> \
  -NO_TIMESTAMP -SAVE_MESHES
```

---

## 🔄 Possible Improvements

* Batch processing for multiple files
* Custom transformation matrix input
* Support for additional export formats (`.glb`, `.stl`, etc.)
* GUI enhancements (progress bar, status indicators)
* Packaging into a standalone `.exe` via PyInstaller
* Localization support (English, Spanish, Japanese, etc.)

---

## 👨‍💻 Maintainer Notes

This tool was created to simplify the mesh conversion workflow for VR and photogrammetry projects. It is meant to be easily extensible for other developers in similar pipelines or educational environments.

Forks are welcome!

---
