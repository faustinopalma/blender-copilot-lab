"""Independently verify example files without modifying the live Blender instance."""

import contextlib
import hashlib
import io
import json
from pathlib import Path
import runpy

import bpy
from mathutils import Vector
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output" / "examples"
RESULTS = ROOT / "results" / "examples"
reference = json.loads((ROOT / "results" / "direct-snapshot.json").read_text())
checks = {}
expected_originals = {
    "coding-cat.blend": "15896db4ceb717c6360a26604571f41a6c7e9515b3d95026c9942d7a2b32d4a6",
    "coding-cat.png": "95212b8940c7dca133d3f429c60ebb7a187eebeb6fe6eb6a1a6856c70cb333c1",
}
for filename, expected in expected_originals.items():
    assert hashlib.sha256((ROOT / "output" / filename).read_bytes()).hexdigest() == expected
checks["original_files_unchanged"] = True

def snapshot():
    capture = io.StringIO()
    with contextlib.redirect_stdout(capture):
        runpy.run_path(str(ROOT / "scripts" / "snapshot.py"))
    return json.loads(capture.getvalue().split("SNAPSHOT=", 1)[1])


bpy.ops.wm.open_mainfile(filepath=str(OUT / "purple.blend"), use_scripts=False)
purple = snapshot()
assert purple["objects"] == reference["objects"]
expected_color = [0.38, 0.08, 0.72, 1.0]
for actual, baseline in zip(purple["materials"], reference["materials"]):
    assert actual["name"] == baseline["name"]
    assert actual["color"] == (expected_color if actual["name"] == "Lagoon accent" else baseline["color"])
shader = bpy.data.materials["Lagoon accent"].node_tree.nodes["Principled BSDF"]
assert all(abs(a - b) < 0.00001 for a, b in zip(
    shader.inputs["Base Color"].default_value, expected_color
))
assert abs(bpy.context.scene.camera.data.ortho_scale - 7.5) < 0.00001
checks["purple_only_requested_material_changed"] = True
checks["purple_geometry_unchanged"] = True

bpy.ops.wm.open_mainfile(filepath=str(OUT / "loop-framing.blend"), use_scripts=False)
loop = snapshot()
assert loop["objects"] == reference["objects"]
assert loop["materials"] == reference["materials"]
scene = bpy.context.scene
inverse = scene.camera.matrix_world.inverted()
corners = [
    inverse @ (obj.matrix_world @ Vector(corner))
    for obj in scene.objects
    if obj.type in ("MESH", "CURVE", "FONT") and not obj.hide_render
    and obj.name not in ("Studio floor", "Display plinth", "Status ring", "Plinth label")
    and not obj.name.startswith("Floating bit")
    for corner in obj.bound_box
]
scale = scene.camera.data.ortho_scale
xs, ys = [corner.x for corner in corners], [corner.y for corner in corners]
fill = max(max(xs) - min(xs), max(ys) - min(ys)) / scale
bounds = [min(xs) / scale + 0.5, max(xs) / scale + 0.5,
          min(ys) / scale + 0.5, max(ys) / scale + 0.5]
assert abs(fill - 0.78) < 0.02
assert all(0 <= value <= 1 for value in bounds)
checks["loop_target_78_percent_reached"] = True
checks["loop_character_bounds_not_clipped"] = True
checks["loop_geometry_and_materials_unchanged"] = True

images = {}
for filename in ("purple.png", "loop-01.png", "loop-02.png", "loop-03.png"):
    image = bpy.data.images.load(str(OUT / filename), check_existing=False)
    assert tuple(image.size) == (512, 512)
    values = np.asarray(image.pixels[:], dtype=np.float32).reshape(512, 512, 4)
    assert np.isfinite(values).all() and float(values[:, :, :3].std()) > 0.1
    images[filename] = values
    bpy.data.images.remove(image)
checks["four_nonblank_512px_images"] = True
assert np.array_equal(images["loop-02.png"], images["loop-03.png"])
checks["loop_final_verification_pixel_identical"] = True
assert float(np.abs(images["loop-01.png"] - images["loop-02.png"]).mean()) > 0.01
checks["loop_first_to_second_image_actually_changed"] = True
report = {
    "checks": checks, "fill_fraction": fill, "normalized_character_bounds": bounds,
    "final_ortho_scale": scale,
    "files": {
        path.name: {"bytes": path.stat().st_size,
                    "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
        for path in sorted(OUT.iterdir()) if path.suffix in (".blend", ".png")
    },
}
(RESULTS / "validation.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"checks_passed": len(checks), "fill_fraction": fill, "bounds": bounds}))
