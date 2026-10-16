"""Independently reopen gallery scenes, verify outputs, and export browser GLBs."""

import hashlib
import json
import math
from pathlib import Path
import struct
import time

import bpy
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output" / "gallery"
RESULTS = ROOT / "results" / "gallery"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def fingerprint(path):
    return {"bytes": path.stat().st_size, "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def inspect_glb(path):
    raw = path.read_bytes()
    magic, version, length = struct.unpack_from("<4sII", raw)
    require((magic, version, length) == (b"glTF", 2, len(raw)), "Invalid GLB container")
    chunk_length, chunk_type = struct.unpack_from("<II", raw, 12)
    require(chunk_type == 0x4E4F534A, "Missing GLB JSON chunk")
    document = json.loads(raw[20:20 + chunk_length])
    require(document["asset"]["version"] == "2.0", "Not glTF 2.0")
    require(not document.get("animations"), "Expected static export")
    require(all("uri" not in item for kind in ("buffers", "images") for item in document.get(kind, [])),
            "GLB must be self-contained")
    require("KHR_draco_mesh_compression" not in document.get("extensionsRequired", []),
            "No remote decoder should be needed")
    triangles = sum(
        document["accessors"][primitive["indices"]]["count"] // 3
        for mesh in document["meshes"] for primitive in mesh["primitives"]
    )
    return {"meshes": len(document["meshes"]), "nodes": len(document["nodes"]),
            "materials": len(document.get("materials", [])), "triangles": triangles}


def main():
    subjects = json.loads((ROOT / "scenes" / "subjects.json").read_text())
    require(len(subjects) == 10, "Expected ten subjects")
    originals = {
        "coding-cat.blend": "15896db4ceb717c6360a26604571f41a6c7e9515b3d95026c9942d7a2b32d4a6",
        "coding-cat.png": "95212b8940c7dca133d3f429c60ebb7a187eebeb6fe6eb6a1a6856c70cb333c1",
    }
    for name, expected in originals.items():
        require(fingerprint(ROOT / "output" / name)["sha256"] == expected, f"Original changed: {name}")
    report, web = [], []
    for subject in subjects:
        started = time.perf_counter()
        slug = subject["slug"]
        blend = OUT / f"{slug}.blend"
        before = fingerprint(blend)
        manifest = json.loads((RESULTS / f"{slug}.json").read_text())
        final = manifest["attempts"][-1]
        require(final["status"] == "success", f"{slug}: final attempt failed")
        source_text = (ROOT / "scenes" / f"{slug}.py").read_text(encoding="utf-8")
        require(hashlib.sha256(source_text.encode("utf-8")).hexdigest() == final["source_sha256"],
                f"{slug}: source changed after final build")
        bpy.ops.wm.open_mainfile(filepath=str(blend), use_scripts=False)
        scene = bpy.context.scene
        require(scene.get("gallery_subject") == slug, f"{slug}: wrong scene marker")
        require(scene.get("external_assets") == 0, f"{slug}: unexpected external assets")
        require(scene.get("blender_mcp_lab") == "disposable-test", f"{slug}: missing lab marker")
        require(scene.camera is not None and scene.camera.type == "CAMERA", f"{slug}: missing camera")
        require((scene.render.resolution_x, scene.render.resolution_y, scene.render.resolution_percentage)
                == (960, 720, 100), f"{slug}: wrong saved resolution")
        require(len(scene.objects) == final["scene"]["objects"] >= 80, f"{slug}: object count mismatch")
        names = " ".join(obj.name.lower() for obj in scene.objects)
        for fragment in subject["required_name_fragments"]:
            require(fragment in names, f"{slug}: missing expected {fragment} geometry")
        for obj in scene.objects:
            require(all(math.isfinite(value) for row in obj.matrix_world for value in row),
                    f"{slug}: nonfinite transform on {obj.name}")
        require(not bpy.data.texts, f"{slug}: unexpected embedded scripts")
        ids = list(bpy.data.objects) + list(bpy.data.materials) + list(bpy.data.scenes)
        for block in ids:
            require(not block.animation_data or not block.animation_data.drivers,
                    f"{slug}: unexpected animation drivers")
        images = {}
        for suffix, dimensions in (("-preview.png", (640, 480)), (".png", (960, 720))):
            path = OUT / f"{slug}{suffix}"
            image = bpy.data.images.load(str(path), check_existing=False)
            require(tuple(image.size) == dimensions, f"{slug}: wrong PNG dimensions")
            pixels = np.asarray(image.pixels[:], dtype=np.float32).reshape(-1, 4)[:, :3]
            require(np.isfinite(pixels).all() and float(pixels.std()) > 0.08,
                    f"{slug}: blank or nonfinite PNG")
            images[path.name] = {**fingerprint(path), "rgb_std": float(pixels.std())}
            bpy.data.images.remove(image)
        original_count = len(scene.objects)
        bpy.ops.object.select_all(action="DESELECT")
        floor_names = {"Studio floor"}
        excluded = [
            obj for obj in scene.objects
            if obj.name in floor_names or (
                obj.type == "FONT" and (
                    obj.data.body == subject["title"].upper()
                    or obj.data.body.startswith("MICROSOFT CONCEPT STUDY")
                )
            )
        ]
        require(len(excluded) == 3, f"{slug}: expected studio floor, title and footer")
        geometry = [obj for obj in scene.objects if obj.type in {"MESH", "CURVE", "FONT"}
                    and not obj.hide_render and obj not in excluded]
        fonts = sum(obj.type == "FONT" for obj in geometry)
        curves = sum(obj.type == "CURVE" for obj in geometry)
        for obj in geometry:
            obj.hide_set(False)
            obj.select_set(True)
        bpy.context.view_layer.objects.active = geometry[0]
        bpy.ops.object.convert(target="MESH")
        require(all(obj.type == "MESH" for obj in bpy.context.selected_objects),
                f"{slug}: text or curve conversion failed")
        export_started = time.perf_counter()
        glb = OUT / f"{slug}.glb"
        bpy.ops.export_scene.gltf(
            filepath=str(glb), export_format="GLB", use_selection=True,
            export_apply=True, export_animations=False, export_cameras=False, export_lights=False,
            export_extras=False, export_draco_mesh_compression_enable=False,
        )
        export_seconds = time.perf_counter() - export_started
        gltf = inspect_glb(glb)
        require(gltf["meshes"] >= 80, f"{slug}: missing export geometry")
        require(before == fingerprint(blend), f"{slug}: validation changed saved scene")
        row = {
            "slug": slug, "objects": original_count,
            "converted_font_objects": fonts, "converted_curve_objects": curves,
            "exported_mesh_objects": len(geometry), "excluded_studio_objects": [obj.name for obj in excluded],
            "blend": before, "images": images, "glb": {**fingerprint(glb), **gltf},
            "export_seconds": export_seconds, "verification_and_export_seconds": time.perf_counter() - started,
        }
        report.append(row)
        web.append({**subject, "objects": original_count, "exported_meshes": len(geometry), "glb_bytes": glb.stat().st_size})
        print("GALLERY_VERIFIED=" + json.dumps(row))
    require(len(report) == 10, "Incomplete gallery")
    (RESULTS / "validation.json").write_text(json.dumps({
        "blender": bpy.app.version_string, "subjects_verified": len(report),
        "original_files_unchanged": True, "subjects": report,
    }, indent=2) + "\n", encoding="utf-8")
    (ROOT / "web" / "gallery.json").write_text(json.dumps(web, indent=2) + "\n", encoding="utf-8")
    print("GALLERY_VALIDATION_COMPLETE=10")


if __name__ == "__main__":
    main()
