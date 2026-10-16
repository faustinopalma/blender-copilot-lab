"""Load the pinned addon only in this disposable Blender instance."""

import importlib.util
import json
import os
from pathlib import Path
import sys

import bpy

sys.path.insert(0, str(Path(__file__).resolve().parent))
from local_network import install_guard

install_guard()
ROOT = Path(__file__).resolve().parents[1]
os.environ["BLENDERMCP_NO_UPDATE_CHECK"] = "1"
os.environ["BLENDER_MCP_DISABLE_TELEMETRY"] = "1"
saved_scene = ROOT / "output" / "coding-cat.blend"
if saved_scene.exists():
    bpy.ops.wm.open_mainfile(filepath=str(saved_scene), use_scripts=False)

spec = importlib.util.spec_from_file_location(
    "blender_mcp_test_addon", ROOT / "vendor" / "mcp-for-blender" / "addon.py"
)
if spec is None or spec.loader is None:
    raise RuntimeError("Cannot load pinned Blender addon")
addon = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = addon
spec.loader.exec_module(addon)
addon.register()
scene = bpy.context.scene
scene["blender_mcp_lab"] = "disposable-test"
scene.blendermcp_auto_start_server = False
scene.blendermcp_port = 9876
if bpy.app.timers.is_registered(addon._blendermcp_ensure_server_running):
    bpy.app.timers.unregister(addon._blendermcp_ensure_server_running)
server = addon.BlenderMCPServer(host="127.0.0.1", port=9876)
bpy.types.blendermcp_server = server
server.start()
if not server.running:
    raise RuntimeError("Blender bridge failed to start on 127.0.0.1:9876")
scene.blendermcp_server_running = True
bpy.context.preferences.filepaths.save_version = 0
ready = {
    "pid": os.getpid(), "host": server.host, "port": server.port,
    "version": bpy.app.version_string, "addon_protocol": addon.ADDON_PROTOCOL_VERSION,
    "telemetry_consent": server.get_telemetry_consent(),
    "updates_disabled": True,
}
(ROOT / "results").mkdir(exist_ok=True)
(ROOT / "results" / "blender-ready.json").write_text(
    json.dumps(ready, indent=2) + "\n", encoding="utf-8"
)
print("BLENDER_READY=" + json.dumps(ready), flush=True)
