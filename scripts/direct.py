"""Run with Blender --background --factory-startup --python direct.py."""

import contextlib
import io
import json
from pathlib import Path
import runpy
import time

import bpy

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output"
OUT.mkdir(exist_ok=True)
(ROOT / "results").mkdir(exist_ok=True)
started = time.perf_counter()
bpy.context.scene["blender_mcp_lab"] = "disposable-test"
runpy.run_path(str(ROOT / "scripts" / "scene.py"))
built = time.perf_counter()
capture = io.StringIO()
with contextlib.redirect_stdout(capture):
    runpy.run_path(str(ROOT / "scripts" / "snapshot.py"))
snapshot = json.loads(capture.getvalue().split("SNAPSHOT=", 1)[1])
(ROOT / "results" / "direct-snapshot.json").write_text(
    json.dumps(snapshot, indent=2) + "\n", encoding="utf-8"
)
bpy.context.scene.render.filepath = str(OUT / "direct.png")
bpy.context.preferences.filepaths.save_version = 0
bpy.ops.wm.save_as_mainfile(filepath=str(OUT / "direct.blend"))
render_started = time.perf_counter()
bpy.ops.render.render(write_still=True)
render_seconds = time.perf_counter() - render_started
head = bpy.data.objects["Cat head"]
original = head.location.z
head.location.z += 0.25
bpy.context.view_layer.update()
assert abs(head.location.z - original - 0.25) < 0.00001
head.location.z = original
bpy.context.view_layer.update()
assert abs(head.location.z - original) < 0.00001
read_times = []
for _ in range(20):
    before = time.perf_counter()
    state = sorted((obj.name, tuple(obj.location)) for obj in bpy.context.scene.objects)
    assert len(state) == len(snapshot["objects"])
    read_times.append((time.perf_counter() - before) * 1000)
result = {
    "build_seconds": built - started,
    "render_seconds": render_seconds,
    "read_in_process_ms": read_times,
    "edit_restore_pass": True,
    "objects": len(snapshot["objects"]),
    "blender": bpy.app.version_string,
}
(ROOT / "results" / "direct.json").write_text(
    json.dumps(result, indent=2) + "\n", encoding="utf-8"
)
print("DIRECT_PASS=" + json.dumps(result), flush=True)
