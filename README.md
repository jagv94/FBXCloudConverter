# FBXCloudConverter — point clouds and photogrammetry to FBX with CloudCompare

Small Python tool with a Tkinter interface that converts a 3D file (point cloud or mesh) to **binary FBX** by running [CloudCompare](https://www.cloudcompare.org/) in silent mode. It is the first step of the pipeline that feeds [NaniteConverter](https://github.com/jagv94/NaniteConverter) (FBX → Nanite Static Mesh in Unreal Engine 5.4).

Built during my university internship (January–May 2025) at the Faculty of Earth Sciences, University of Barcelona, for a VR viewer of photogrammetry models. **It was developed with substantial AI assistance** to meet the internship deadlines; the goals, decisions, integration and testing are mine.

## What it does

1. Asks for an input file. The dialog offers `.las`, `.laz`, `.e57`, `.xyz`, `.ply`, `.pts`, `.obj`, `.stl`, `.glb`, `.gltf` and `.dxf` (what can actually be opened depends on CloudCompare and its plugins).
2. Asks for a destination folder.
3. Runs CloudCompare headless with an identity transformation matrix and automatic global shift, and exports a binary FBX. A window shows CloudCompare's output in real time.
4. Moves `<name>_TRANSFORMED.fbx` and, if it exists, the texture folder `<name>_TRANSFORMED.fbm` to the destination. If a file with the same name already exists, it asks whether to overwrite it, move the new one to another folder, delete the new one or leave it where it was generated (next to the input file).

The `_TRANSFORMED` suffix is the one NaniteConverter expects.

CloudCompare command used:

```bat
CloudCompare.exe -SILENT -AUTO_SAVE OFF -M_EXPORT_FMT FBX -FBX -EXPORT_FMT FBX_binary -O -GLOBAL_SHIFT AUTO <input_file> -APPLY_TRANS -APPLY_TO_GLOBAL FORCE <identity_matrix.txt> -NO_TIMESTAMP -SAVE_MESHES
```

## Requirements

- Windows (the script calls `Tools\CloudCompare\CloudCompare.exe`).
- Python 3.6 or later with Tkinter (included in the standard python.org installer for Windows). No external Python packages.
- CloudCompare in `Tools/CloudCompare/`. The repository includes a copy of CloudCompare 2.13.2; see [Third-party software](#third-party-software).

```
FBXCloudConverter/
├── FBXCloudConverter.py
├── FBXCloudConverter.bat
└── Tools/
    └── CloudCompare/
        └── CloudCompare.exe
```

## Usage

Double-click `FBXCloudConverter.bat`, or run:

```bat
python FBXCloudConverter.py
```

Then follow the dialogs: input file → destination folder → wait for "Process Completed" → resolve conflicts if asked.

## Limitations

- One file per run (no batch mode).
- The transformation is always the identity matrix; there is no option for a custom matrix yet.
- Windows only; minimal error handling.

## Third-party software

`Tools/CloudCompare/` contains an unmodified binary copy of **CloudCompare 2.13.2**, distributed under the **GNU General Public License v2**. Its license is included in [`Tools/CloudCompare/license.txt`](Tools/CloudCompare/license.txt), and the official source code of that exact version is available at <https://github.com/CloudCompare/CloudCompare/tree/v2.13.2>.

**CloudCompare is not covered by the MIT license of this repository.**

If that link is ever unavailable, contact me through the repository and I will provide the corresponding source.

## License

The MIT license ([LICENSE](LICENSE)) covers only my own code: `FBXCloudConverter.py` and `FBXCloudConverter.bat`. Everything under `Tools/CloudCompare/` keeps its own license (GPL v2).

## Author

Jose Adrián Guerra Viudez — [jagv94.github.io](https://jagv94.github.io)
Internship project for the Faculty of Earth Sciences, University of Barcelona (2025).
