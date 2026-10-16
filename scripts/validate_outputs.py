"""Reopen saved files in a separate Blender process and compare actual pixels."""

import contextlib
import hashlib
import io
import json
from pathlib import Path
import runpy
import struct

import bpy
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output"
RESULTS = ROOT / "results"
results = {"checks": {}, "files": {}}
reference = json.loads((RESULTS / "direct-snapshot.json").read_text())
for route in ("direct", "mcp"):
    bpy.ops.wm.open_mainfile(filepath=str(OUT / f"{route}.blend"), use_scripts=False)
    capture = io.StringIO()
    with contextlib.redirect_stdout(capture):
        runpy.run_path(str(ROOT / "scripts" / "snapshot.py"))
    actual = json.loads(capture.getvalue().split("SNAPSHOT=", 1)[1])
    assert actual == reference, f"Persisted {route} scene differs from reference"
    results["checks"][f"reopen_{route}_blend"] = True

pixels = []
for filename, expected in (("direct.png", 640), ("mcp.png", 640), ("coding-cat.png", 1200)):
    image = bpy.data.images.load(str(OUT / filename), check_existing=False)
    assert tuple(image.size) == (expected, expected)
    data = np.asarray(image.pixels[:], dtype=np.float32).reshape(expected, expected, 4)
    assert np.isfinite(data).all()
    deviation = float(data[:, :, :3].std())
    assert deviation > 0.10, f"Blank or nearly uniform image: {filename}"
    results["checks"][f"nonblank_{filename}"] = True
    results[filename] = {"width": expected, "height": expected, "rgb_stddev": deviation}
    if expected == 640:
        pixels.append(data[:, :, :3])
    bpy.data.images.remove(image)
error = np.abs(pixels[0] - pixels[1])
results["pixel_comparison"] = {
    "mean_absolute_error": float(error.mean()),
    "max_absolute_error": float(error.max()),
    "mean_error_limit": 0.01,
    "normalized_channels": "0..1",
}
assert results["pixel_comparison"]["mean_absolute_error"] < 0.01
results["checks"]["matching_api_mcp_render"] = True

blob = (OUT / "coding-cat.glb").read_bytes()
magic, version, total = struct.unpack_from("<III", blob)
assert magic == 0x46546C67 and version == 2 and total == len(blob)
length, kind = struct.unpack_from("<II", blob, 12)
assert kind == 0x4E4F534A
gltf = json.loads(blob[20:20 + length])
names = {node["name"] for node in gltf["nodes"] if "mesh" in node}
assert {f"Tentacle {number:02}" for number in range(1, 7)} <= names
assert {"Cat head", "Cat torso", "Display plinth", "Terminal glyph", "Plinth label"} <= names
results["checks"]["glb_geometry_including_curves_and_text"] = True
results["glb_meshes"] = len(gltf["meshes"])

bpy.ops.wm.open_mainfile(filepath=str(OUT / "coding-cat.blend"), use_scripts=False)
scene = bpy.context.scene
assert scene.get("blender_mcp_lab") == "disposable-test"
assert (scene.render.resolution_x, scene.render.resolution_y) == (1200, 1200)
assert len(scene.objects) == 62
head = bpy.data.objects["Cat head"]
assert head.animation_data.action is not None
scene.frame_set(24)
assert abs(head.rotation_euler.z - 0.12) < 0.00001
scene.frame_set(1)
assert abs(head.rotation_euler.z) < 0.00001
results["checks"]["reopen_final_scene_and_animation"] = True
assert not scene.animation_data or not scene.animation_data.drivers
assert all(not obj.animation_data or not obj.animation_data.drivers for obj in scene.objects)
assert len(bpy.data.texts) == 0, "Unexpected embedded Python text"
results["checks"]["no_embedded_scripts_or_object_drivers"] = True

for path in sorted(OUT.iterdir()):
    if path.suffix in (".blend", ".png", ".glb"):
        results["files"][path.name] = {
            "bytes": path.stat().st_size,
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        }
(RESULTS / "validation.json").write_text(
    json.dumps(results, indent=2) + "\n", encoding="utf-8"
)
print("OUTPUT_VALIDATION_PASS=" + json.dumps(results), flush=True)
