"""Execute exactly one gallery source through MCP and record host phase timings."""

import argparse
import asyncio
from datetime import datetime, timedelta, timezone
import hashlib
import json
import os
from pathlib import Path
import time

from blender_mcp.safe_mode import validate_code
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

ROOT = Path(__file__).resolve().parents[1]


def utc():
    return datetime.now(timezone.utc).isoformat()


async def run(slug, title):
    source_file = ROOT / "scenes" / f"{slug}.py"
    common = (ROOT / "scripts" / "gallery_common.py").read_text(encoding="utf-8")
    subject = source_file.read_text(encoding="utf-8")
    code = common + "\n" + subject + "\n" + f"gallery_finish({title!r}, {slug!r})\n"
    validate_code(code)
    output = ROOT / "output" / "gallery"
    results = ROOT / "results" / "gallery"
    output.mkdir(parents=True, exist_ok=True)
    results.mkdir(parents=True, exist_ok=True)
    manifest_file = results / f"{slug}.json"
    manifest = json.loads(manifest_file.read_text()) if manifest_file.exists() else {
        "slug": slug, "title": title, "attempts": [],
    }
    attempt = {"started_at_utc": utc(), "source_sha256": hashlib.sha256(subject.encode()).hexdigest(),
               "common_sha256": hashlib.sha256(common.encode()).hexdigest(),
               "source_lines": len(subject.splitlines()), "phases_seconds": {}}
    manifest["attempts"].append(attempt)
    start = time.perf_counter()
    config = json.loads((ROOT / ".vscode" / "mcp.json").read_text())["servers"]["blender-local"]
    params = StdioServerParameters(command=config["command"], args=config["args"],
                                   env={**os.environ, **config["env"]})

    def persist():
        manifest_file.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    persist()
    try:
        with (results / f"{slug}.log").open("a", encoding="utf-8") as log:
            async with stdio_client(params, errlog=log) as (read, write):
                async with ClientSession(
                    read, write, read_timeout_seconds=timedelta(seconds=180)
                ) as client:
                    await client.initialize()
                    attempt["phases_seconds"]["initialize"] = time.perf_counter() - start

                    async def execute(phase, script):
                        before = time.perf_counter()
                        result = await client.call_tool("execute_blender_code", {"code": script})
                        elapsed = time.perf_counter() - before
                        attempt["phases_seconds"][phase] = elapsed
                        text = "\n".join(part.text for part in result.content if part.type == "text")
                        if result.isError or text.lower().startswith(("error", "failed", "rejected")):
                            raise RuntimeError(f"{phase}: {text[:4000]}")
                        persist()
                        return text

                    text = await execute("build", code)
                    if "GALLERY_BUILD=" not in text:
                        raise RuntimeError("Build did not report its verification marker")
                    attempt["scene"] = json.loads(text.split("GALLERY_BUILD=", 1)[1].strip())
                    attempt["phases_seconds"]["preview_render"] = 0.0
                    await execute(
                        "preview_render",
                        "import bpy\nbpy.context.scene.render.resolution_x=640\n"
                        "bpy.context.scene.render.resolution_y=480\n"
                        f"bpy.context.scene.render.filepath={str(output / (slug + '-preview.png'))!r}\n"
                        "bpy.ops.render.render(write_still=True)\nprint('PREVIEW_OK')"
                    )
                    await execute(
                        "final_render",
                        "import bpy\nbpy.context.scene.render.resolution_x=960\n"
                        "bpy.context.scene.render.resolution_y=720\n"
                        f"bpy.context.scene.render.filepath={str(output / (slug + '.png'))!r}\n"
                        "bpy.ops.render.render(write_still=True)\nprint('FINAL_OK')"
                    )
                    await execute(
                        "save",
                        "import bpy\n"
                        f"bpy.ops.wm.save_as_mainfile(filepath={str(output / (slug + '.blend'))!r})\n"
                        "print('SAVE_OK')"
                    )
        for suffix in (".png", "-preview.png", ".blend"):
            path = output / (slug + suffix)
            if path.stat().st_size < 1000:
                raise RuntimeError(f"Missing or empty output: {path.name}")
        attempt["status"] = "success"
    except (Exception, BaseExceptionGroup) as error:
        attempt["status"] = "failed"
        attempt["error"] = str(error)
        raise
    finally:
        attempt["ended_at_utc"] = utc()
        attempt["total_seconds"] = time.perf_counter() - start
        persist()
    print(json.dumps({"slug": slug, "attempt": len(manifest["attempts"]),
                      "seconds": attempt["total_seconds"],
                      "phases": attempt["phases_seconds"], "scene": attempt["scene"]}))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("slug")
    parser.add_argument("--title", required=True)
    arguments = parser.parse_args()
    if not arguments.slug or any(char not in "abcdefghijklmnopqrstuvwxyz0123456789-" for char in arguments.slug):
        parser.error("Use a lowercase kebab-case slug")
    asyncio.run(run(arguments.slug, arguments.title))
