"""Exercise the exact VS Code stdio configuration against a running Blender UI."""

import asyncio
import base64
from datetime import timedelta
import json
import os
from pathlib import Path
import statistics
import time

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
OUT = ROOT / "output"
QUERY = (
    "import bpy, json\n"
    "state = sorted((obj.name, tuple(obj.location)) for obj in bpy.context.scene.objects)\n"
    "print('READ=' + json.dumps(state))"
)


def text_content(result) -> str:
    return "\n".join(part.text for part in result.content if part.type == "text")


def marker(text: str, prefix: str):
    for line in text.splitlines():
        if line.startswith(prefix):
            return json.loads(line[len(prefix):])
        if prefix in line and line.startswith("Code executed successfully:"):
            return json.loads(line.split(prefix, 1)[1])
    raise AssertionError(f"Missing marker {prefix}: {text[:800]}")


async def main() -> None:
    RESULTS.mkdir(exist_ok=True)
    OUT.mkdir(exist_ok=True)
    config = json.loads((ROOT / ".vscode" / "mcp.json").read_text())
    server = config["servers"]["blender-local"]
    params = StdioServerParameters(
        command=server["command"], args=server["args"],
        env={**os.environ, **server["env"]},
    )
    results = {"checks": {}, "calls": [], "configuration": ".vscode\\mcp.json"}
    with (RESULTS / "mcp-server.log").open("w", encoding="utf-8") as log:
        async with stdio_client(params, errlog=log) as (read, write):
            async with ClientSession(
                read, write, read_timeout_seconds=timedelta(seconds=180)
            ) as session:
                before = time.perf_counter()
                initialized = await session.initialize()
                results["initialize_seconds"] = time.perf_counter() - before
                results["protocol"] = initialized.protocolVersion
                results["server"] = initialized.serverInfo.model_dump()
                tools = await session.list_tools()
                names = [tool.name for tool in tools.tools]
                assert {"execute_blender_code", "get_scene_info", "look", "get_addon_status"} <= set(names)
                (RESULTS / "mcp-tools.json").write_text(
                    tools.model_dump_json(indent=2) + "\n", encoding="utf-8"
                )
                results["tool_names"] = names
                results["checks"]["initialize_and_discovery"] = True

                async def call(name, arguments=None, expected_failure=False):
                    started = time.perf_counter()
                    result = await session.call_tool(name, arguments or {})
                    elapsed = (time.perf_counter() - started) * 1000
                    text = text_content(result)
                    failed = result.isError or text.lower().startswith(
                        ("error", "failed", "rejected by safe mode")
                    )
                    results["calls"].append({
                        "tool": name, "milliseconds": elapsed,
                        "expected_failure": expected_failure,
                        "reported_failure": bool(failed),
                        "text_preview": text[:240],
                    })
                    assert failed == expected_failure, text[:3000]
                    return result, text, elapsed

                async def execute(code, expected_failure=False):
                    return await call(
                        "execute_blender_code", {"code": code},
                        expected_failure=expected_failure
                    )

                _, addon_status, _ = await call("get_addon_status")
                results["addon_status"] = addon_status
                _, consent, _ = await execute(
                    "import bpy,json\n"
                    "print('CONSENT=' + json.dumps(bpy.types.blendermcp_server.get_telemetry_consent()))"
                )
                assert marker(consent, "CONSENT=")["consent"] is False
                results["checks"]["telemetry_opt_out"] = True
                await execute(
                    "import bpy\n"
                    "assert bpy.context.scene.get('blender_mcp_lab') == 'disposable-test', "
                    "'Refusing to overwrite a scene outside the disposable lab'\n"
                    "print('DISPOSABLE_SCENE_CONFIRMED')"
                )
                _, protected_before, _ = await execute(
                    "import bpy,json\n"
                    "bpy.context.scene['blender_mcp_lab']='guard-probe'\n"
                    "print('PROTECTED='+json.dumps(len(bpy.context.scene.objects)))"
                )
                _, refused, _ = await execute(
                    (ROOT / "scripts" / "scene.py").read_text(encoding="utf-8"),
                    expected_failure=True,
                )
                assert "Refusing to replace a scene outside" in refused
                _, protected_after, _ = await execute(
                    "import bpy,json\n"
                    "bpy.context.scene['blender_mcp_lab']='disposable-test'\n"
                    "print('PROTECTED='+json.dumps(len(bpy.context.scene.objects)))"
                )
                assert marker(protected_before, "PROTECTED=") == marker(protected_after, "PROTECTED=")
                results["checks"]["foreign_scene_not_overwritten"] = True
                _, build_text, build_ms = await execute(
                    (ROOT / "scripts" / "scene.py").read_text(encoding="utf-8")
                )
                assert marker(build_text, "SCENE_BUILT=")["objects"] == 62
                results["build_roundtrip_seconds"] = build_ms / 1000
                results["checks"]["create_original_scene"] = True

                _, snapshot_text, _ = await execute(
                    (ROOT / "scripts" / "snapshot.py").read_text(encoding="utf-8")
                )
                snapshot = marker(snapshot_text, "SNAPSHOT=")
                (RESULTS / "mcp-snapshot.json").write_text(
                    json.dumps(snapshot, indent=2) + "\n", encoding="utf-8"
                )
                direct = json.loads((RESULTS / "direct-snapshot.json").read_text())
                assert snapshot == direct, "Direct and MCP scene snapshots differ"
                results["checks"]["identical_scene_snapshot"] = True
                _, info, _ = await call(
                    "get_scene_info",
                    {"query": "Tentacle", "fields": ["location", "size", "materials"], "limit": 20},
                )
                assert "Tentacle 01" in info and "Tentacle 06" in info
                results["checks"]["structured_scene_inspection"] = True

                _, edit, _ = await execute(
                    "import bpy,json\n"
                    "head=bpy.data.objects['Cat head']\n"
                    "head.location.z=3.8\n"
                    "bpy.context.view_layer.update()\n"
                    "print('EDIT='+json.dumps({'z':float(head.location.z)}))"
                )
                assert abs(marker(edit, "EDIT=")["z"] - 3.8) < 0.00001
                _, restored, _ = await execute(
                    "import bpy,json\n"
                    "bpy.data.objects['Cat head'].location.z=3.55\n"
                    "bpy.context.view_layer.update()\n"
                    "print('RESTORE='+json.dumps({'z':float(bpy.data.objects['Cat head'].location.z)}))"
                )
                assert abs(marker(restored, "RESTORE=")["z"] - 3.55) < 0.00001
                results["checks"]["edit_and_restore"] = True

                _, rejected, _ = await execute("import os\nprint(os.getcwd())", expected_failure=True)
                assert "Rejected by safe mode" in rejected
                results["checks"]["unsafe_import_blocked"] = True
                _, rejected_open, _ = await execute(
                    "open('MCP_MUST_NOT_EXIST.txt','w')", expected_failure=True
                )
                assert "Rejected by safe mode" in rejected_open
                assert not (ROOT / "MCP_MUST_NOT_EXIST.txt").exists()
                results["checks"]["raw_file_access_blocked"] = True
                _, expected_error, _ = await execute(
                    "raise ValueError('MCP_EXPECTED_ERROR')", expected_failure=True
                )
                assert "ValueError" in expected_error and "Traceback" in expected_error
                _, recovery, _ = await execute("print('RECOVERY_OK')")
                assert "RECOVERY_OK" in recovery
                results["checks"]["error_traceback_and_recovery"] = True

                _, saved, _ = await execute(
                    f"import bpy\nbpy.context.scene.render.filepath={str(OUT / 'mcp.png')!r}\n"
                    f"bpy.ops.wm.save_as_mainfile(filepath={str(OUT / 'mcp.blend')!r})\n"
                    "print('SAVE_OK')"
                )
                assert "SAVE_OK" in saved and (OUT / "mcp.blend").stat().st_size > 100000
                results["checks"]["save_blend"] = True
                _, rendered, render_ms = await execute(
                    "import bpy\nbpy.ops.render.render(write_still=True)\nprint('RENDER_OK')"
                )
                assert "RENDER_OK" in rendered and (OUT / "mcp.png").stat().st_size > 10000
                results["render_roundtrip_seconds"] = render_ms / 1000
                results["checks"]["render_png"] = True

                image_result, _, _ = await call(
                    "look", {"image": str(OUT / "mcp.png"), "max_size": 640}
                )
                images = [part for part in image_result.content if part.type == "image"]
                assert images, "MCP did not return image content"
                png = base64.b64decode(images[0].data, validate=True)
                assert png.startswith(b"\x89PNG\r\n\x1a\n")
                (OUT / "mcp-tool-image.png").write_bytes(png)
                results["checks"]["mcp_image_content"] = True

                viewport, _, _ = await call("look", {"mode": "viewport", "max_size": 640})
                viewport_images = [part for part in viewport.content if part.type == "image"]
                assert viewport_images, "MCP did not return viewport image"
                (OUT / "mcp-viewport.png").write_bytes(
                    base64.b64decode(viewport_images[0].data, validate=True)
                )
                results["checks"]["live_viewport_capture"] = True

                await execute(
                    f"import bpy\nbpy.ops.export_scene.gltf(filepath={str(OUT / 'coding-cat.glb')!r}, export_format='GLB')\n"
                    "print('EXPORT_OK')"
                )
                assert (OUT / "coding-cat.glb").read_bytes()[:4] == b"glTF"
                results["checks"]["export_glb"] = True

                reads = []
                for _ in range(20):
                    _, response, elapsed = await execute(QUERY)
                    assert len(marker(response, "READ=")) == 62
                    reads.append(elapsed)
                results["read_roundtrip_ms"] = reads
                results["read_median_ms"] = statistics.median(reads)
                results["checks"]["twenty_sequential_reads"] = True

                _, animation, _ = await execute(
                    "import bpy,json\n"
                    "scene=bpy.context.scene\n"
                    "head=bpy.data.objects['Cat head']\n"
                    "for frame,angle in [(1,0.0),(24,0.12),(48,0.0)]:\n"
                    "    head.rotation_euler.z=angle\n"
                    "    head.keyframe_insert(data_path='rotation_euler',frame=frame)\n"
                    "scene.frame_set(24)\n"
                    "assert abs(head.rotation_euler.z-0.12)<0.00001\n"
                    "scene.frame_set(1)\n"
                    "print('ANIMATION='+json.dumps({'action':head.animation_data.action.name,'frame':scene.frame_current}))"
                )
                assert marker(animation, "ANIMATION=")["frame"] == 1
                results["checks"]["keyframe_animation"] = True
                await execute(
                    "import bpy\n"
                    "bpy.context.scene.render.resolution_x=1200\n"
                    "bpy.context.scene.render.resolution_y=1200\n"
                    f"bpy.context.scene.render.filepath={str(OUT / 'coding-cat.png')!r}\n"
                    f"bpy.ops.wm.save_as_mainfile(filepath={str(OUT / 'coding-cat.blend')!r})\n"
                    "bpy.ops.render.render(write_still=True)\n"
                    "print('FINAL_OK')"
                )
                results["checks"]["final_1200px_render"] = True

    (RESULTS / "mcp.json").write_text(
        json.dumps(results, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({
        "checks_passed": len(results["checks"]), "tools": len(results["tool_names"]),
        "read_median_ms": results["read_median_ms"],
        "build_roundtrip_seconds": results["build_roundtrip_seconds"],
        "render_roundtrip_seconds": results["render_roundtrip_seconds"],
    }, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
