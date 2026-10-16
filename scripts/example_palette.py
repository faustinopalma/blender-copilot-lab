import bpy
import json

ORIGINAL = r"C:\code\BlenderMCP\output\coding-cat.blend"
BLEND_OUTPUT = r"C:\code\BlenderMCP\output\examples\purple.blend"
IMAGE_OUTPUT = r"C:\code\BlenderMCP\output\examples\purple.png"
PURPLE = (0.38, 0.08, 0.72, 1.0)


def scene_signature():
    return (
        tuple((obj.name, obj.type, obj.data.name if obj.data else None,
               tuple(tuple(row) for row in obj.matrix_world))
              for obj in bpy.data.objects),
        tuple((mesh.name, tuple(tuple(v.co) for v in mesh.vertices),
               tuple(tuple(e.vertices) for e in mesh.edges),
               tuple(tuple(p.vertices) for p in mesh.polygons))
              for mesh in bpy.data.meshes),
        tuple((curve.name, tuple(
            (spline.type, spline.use_cyclic_u,
             tuple(tuple(p.co) for p in spline.points),
             tuple((tuple(p.co), tuple(p.handle_left), tuple(p.handle_right))
                   for p in spline.bezier_points))
            for spline in curve.splines)) for curve in bpy.data.curves),
        tuple((camera.name, camera.type, camera.lens, camera.ortho_scale,
               camera.shift_x, camera.shift_y, camera.clip_start, camera.clip_end)
              for camera in bpy.data.cameras),
        tuple((light.name, light.type, light.energy, tuple(light.color))
              for light in bpy.data.lights),
        bpy.context.scene.camera.name if bpy.context.scene.camera else None,
    )


bpy.ops.wm.open_mainfile(filepath=ORIGINAL, use_scripts=False)
before_signature = scene_signature()
material = bpy.data.materials["Lagoon accent"]
node = material.node_tree.nodes["Principled BSDF"]
rgba_before = tuple(node.inputs["Base Color"].default_value)
diffuse_before = tuple(material.diffuse_color)
tentacles_before = sorted(obj.name for obj in bpy.data.objects
                          if obj.type == "CURVE" and obj.name.startswith("Tentacle "))
assert len(bpy.data.objects) == 62
assert len(tentacles_before) == 6
result = {
    "object_count": 62,
    "tentacle_curve_count": 6,
    "tentacle_names": tentacles_before,
    "rgba_before": rgba_before,
    "diffuse_rgba_before": diffuse_before,
}
try:
    node.inputs["Base Color"].default_value = PURPLE
    material.diffuse_color = PURPLE
    scene = bpy.context.scene
    scene.render.resolution_x = 512
    scene.render.resolution_y = 512
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.filepath = IMAGE_OUTPUT
    assert scene_signature() == before_signature
    result["rgba_after"] = tuple(node.inputs["Base Color"].default_value)
    result["diffuse_rgba_after"] = tuple(material.diffuse_color)
    assert all(abs(actual - expected) < 1e-6
               for actual, expected in zip(result["rgba_after"], PURPLE))
    assert result["rgba_after"] == result["diffuse_rgba_after"]
    assert len(bpy.data.objects) == 62
    assert sorted(obj.name for obj in bpy.data.objects
                  if obj.type == "CURVE" and obj.name.startswith("Tentacle ")) == tentacles_before
    bpy.ops.wm.save_as_mainfile(filepath=BLEND_OUTPUT, check_existing=False)
    bpy.ops.render.render(write_still=True)
    assert scene_signature() == before_signature
    result["geometry_camera_lights_unchanged"] = True
    preview_image = bpy.data.images.load(filepath=IMAGE_OUTPUT, check_existing=False)
    result["image_size"] = tuple(preview_image.size)
    assert result["image_size"] == (512, 512)
finally:
    bpy.ops.wm.open_mainfile(filepath=ORIGINAL, use_scripts=False)
    restored_material = bpy.data.materials["Lagoon accent"]
    restored_rgba = tuple(restored_material.node_tree.nodes["Principled BSDF"]
                          .inputs["Base Color"].default_value)
    assert restored_rgba == rgba_before
    assert tuple(restored_material.diffuse_color) == diffuse_before
    assert scene_signature() == before_signature
    assert len(bpy.data.objects) == 62
    result["rgba_restored"] = restored_rgba
    result["scene_restored"] = True
print("PALETTE_RESULT " + json.dumps(result, sort_keys=True))
