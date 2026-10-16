import bpy
import json
from mathutils import Vector

scene = bpy.context.scene
assert scene.camera.data.type == "ORTHO"
assert len(bpy.data.objects) == 62
bpy.context.view_layer.update()
inverse = scene.camera.matrix_world.inverted()
excluded = {"Studio floor", "Display plinth", "Status ring", "Plinth label"}
points = []
for obj in scene.objects:
    if (obj.type in {"MESH", "CURVE", "FONT"}
            and obj.visible_get() and not obj.hide_render
            and obj.name not in excluded
            and not obj.name.startswith("Floating bit")):
        for corner in obj.bound_box:
            points.append(inverse @ (obj.matrix_world @ Vector(corner)))
assert points
min_x = min(point.x for point in points)
max_x = max(point.x for point in points)
min_y = min(point.y for point in points)
max_y = max(point.y for point in points)
previous_scale = scene.camera.data.ortho_scale
previous_fill = max(max_x - min_x, max_y - min_y) / previous_scale
if abs(previous_fill - 0.78) > 0.02:
    scene.camera.data.ortho_scale = previous_scale * previous_fill / 0.78
scene.render.resolution_x = 512
scene.render.resolution_y = 512
scene.render.resolution_percentage = 100
scene.render.filepath = r"C:\code\BlenderMCP\output\examples\loop-03.png"
bpy.context.view_layer.update()
scale = scene.camera.data.ortho_scale
fill = max(max_x - min_x, max_y - min_y) / scale
bounds = {
    "min_x": min_x / scale + 0.5, "max_x": max_x / scale + 0.5,
    "min_y": min_y / scale + 0.5, "max_y": max_y / scale + 0.5,
}
not_clipped = all(0.0 <= value <= 1.0 for value in bounds.values())
assert not_clipped, json.dumps(bounds)
print("LOOP_METRIC " + json.dumps({
    "iteration": 3, "previous_ortho_scale": previous_scale,
    "previous_fill_fraction": previous_fill,
    "ortho_scale": scale, "fill_fraction": fill,
    "normalized_bounds": bounds, "tolerance_pass": abs(fill - 0.78) <= 0.02,
    "silhouette_not_clipped": not_clipped, "preview": scene.render.filepath,
}))
bpy.ops.render.render(write_still=True)
bpy.ops.wm.save_as_mainfile(
    filepath=r"C:\code\BlenderMCP\output\examples\loop-framing.blend",
    check_existing=False, copy=True,
)
