import bpy
import json
import math

scene = bpy.context.scene
objects = []


def by_name(item):
    return item.name


for obj in sorted(scene.objects, key=by_name):
    assert all(math.isfinite(value) for value in obj.location)
    objects.append({
        "name": obj.name,
        "type": obj.type,
        "location": [round(float(v), 5) for v in obj.location],
        "rotation": [round(float(v), 5) for v in obj.rotation_euler],
        "scale": [round(float(v), 5) for v in obj.scale],
        "dimensions": [round(float(v), 5) for v in obj.dimensions],
        "materials": [slot.material.name for slot in obj.material_slots if slot.material],
        "vertices": len(obj.data.vertices) if obj.type == "MESH" else None,
        "faces": len(obj.data.polygons) if obj.type == "MESH" else None,
    })
tentacles = [obj for obj in scene.objects
             if obj.name.startswith("Tentacle ") and obj.type == "CURVE"]
assert len(tentacles) == 6, "Expected six original tentacles"
assert bpy.data.objects.get("Cat head") is not None
assert scene.camera is not None
assert scene["original_design"] is True
assert scene["external_assets"] == 0
material_names = {slot.material.name for obj in scene.objects
                  for slot in obj.material_slots if slot.material}
print("SNAPSHOT=" + json.dumps({
    "objects": objects,
    "materials": [{
        "name": mat.name,
        "color": [round(float(v), 5) for v in mat.diffuse_color],
    } for mat in sorted(bpy.data.materials, key=by_name) if mat.name in material_names],
    "engine": scene.render.engine,
    "resolution": [scene.render.resolution_x, scene.render.resolution_y],
    "camera": scene.camera.name,
}, sort_keys=True))
