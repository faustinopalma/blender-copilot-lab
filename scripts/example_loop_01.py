import bpy
import json
from mathutils import Vector

bpy.ops.wm.open_mainfile(
    filepath=r"C:\code\BlenderMCP\output\coding-cat.blend", use_scripts=False
)
scene = bpy.context.scene
assert scene.camera.data.type == "ORTHO"
print("LOOP_ORIGINAL " + json.dumps({
    "filepath": bpy.data.filepath,
    "camera": scene.camera.name,
    "ortho_scale": scene.camera.data.ortho_scale,
    "object_count": len(bpy.data.objects),
    "resolution": [scene.render.resolution_x, scene.render.resolution_y,
                   scene.render.resolution_percentage],
    "image_format": scene.render.image_settings.file_format,
}))
assert len(bpy.data.objects) == 62
assert scene.render.image_settings.file_format == "PNG"
scene.camera.data.ortho_scale = 9.0
scene.render.resolution_x = 512
scene.render.resolution_y = 512
scene.render.resolution_percentage = 100
scene.render.filepath = r"C:\code\BlenderMCP\output\examples\loop-01.png"
bpy.context.view_layer.update()
inverse = scene.camera.matrix_world.inverted()
excluded = {"Studio floor", "Display plinth", "Status ring", "Plinth label"}
points = []
character_objects = []
for obj in scene.objects:
    if (obj.type in {"MESH", "CURVE", "FONT"}
            and obj.visible_get() and not obj.hide_render
            and obj.name not in excluded
            and not obj.name.startswith("Floating bit")):
        character_objects.append(obj.name)
        for corner in obj.bound_box:
            points.append(inverse @ (obj.matrix_world @ Vector(corner)))
assert points
min_x = min(point.x for point in points)
max_x = max(point.x for point in points)
min_y = min(point.y for point in points)
max_y = max(point.y for point in points)
scale = scene.camera.data.ortho_scale
fill = max(max_x - min_x, max_y - min_y) / scale
bounds = {
    "min_x": min_x / scale + 0.5, "max_x": max_x / scale + 0.5,
    "min_y": min_y / scale + 0.5, "max_y": max_y / scale + 0.5,
}
not_clipped = all(0.0 <= value <= 1.0 for value in bounds.values())
assert not_clipped, json.dumps(bounds)
print("LOOP_METRIC " + json.dumps({
    "iteration": 1, "ortho_scale": scale, "fill_fraction": fill,
    "normalized_bounds": bounds, "tolerance_pass": abs(fill - 0.78) <= 0.02,
    "silhouette_not_clipped": not_clipped,
    "character_object_count": len(character_objects),
    "character_objects": character_objects,
    "preview": scene.render.filepath,
}))
bpy.ops.render.render(write_still=True)
