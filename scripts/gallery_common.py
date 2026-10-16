"""Shared bpy-safe geometry and studio setup for the Microsoft concept gallery."""

import bpy
import json
import math
from mathutils import Vector

scene = bpy.context.scene
if scene.get("blender_mcp_lab") != "disposable-test":
    raise RuntimeError("Only the isolated disposable Blender laboratory may be replaced")
bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)
bpy.data.orphans_purge(do_recursive=True)
scene["gallery_lab"] = True
scene.render.engine = "BLENDER_EEVEE"
scene.render.resolution_x = 960
scene.render.resolution_y = 720
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = "PNG"
scene.render.image_settings.color_mode = "RGBA"
scene.render.film_transparent = False
scene.view_settings.view_transform = "AgX"
scene.world.use_nodes = True
scene.world.node_tree.nodes["Background"].inputs[0].default_value = (0.025, 0.04, 0.075, 1)
scene.world.node_tree.nodes["Background"].inputs[1].default_value = 0.45


def mat(name, color, metal=0.0, rough=0.35, emission=0.0):
    item = bpy.data.materials.new(name)
    item.diffuse_color = (*color, 1)
    item.use_nodes = True
    bsdf = item.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (*color, 1)
    bsdf.inputs["Metallic"].default_value = metal
    bsdf.inputs["Roughness"].default_value = rough
    if emission:
        bsdf.inputs["Emission Color"].default_value = (*color, 1)
        bsdf.inputs["Emission Strength"].default_value = emission
    return item


navy = mat("Midnight", (0.025, 0.055, 0.11), 0.35)
blue = mat("Azure blue", (0.025, 0.30, 0.88), 0.35)
teal = mat("Fabric teal", (0.025, 0.70, 0.56), 0.3)
violet = mat("Foundry violet", (0.40, 0.14, 0.85), 0.25)
white = mat("Porcelain", (0.78, 0.87, 0.95), 0.1)
gold = mat("Amber gold", (1.0, 0.54, 0.10), 0.65)
coral = mat("Coral", (0.95, 0.20, 0.22), 0.2)
dark = mat("Dark glass", (0.009, 0.025, 0.055), 0.45, 0.2)
glow = mat("Signal light", (0.10, 0.95, 0.85), 0.1, emission=2.0)
ink = mat("Title ink", (0.70, 0.88, 1.0), emission=0.25)


def finish_object(obj, name, material):
    obj.name = name
    obj.data.materials.append(material)
    if obj.type == "MESH":
        for face in obj.data.polygons:
            face.use_smooth = True
    return obj


def box(name, pos, size, material, bevel=0.08):
    bpy.ops.mesh.primitive_cube_add(size=1, location=pos)
    obj = bpy.context.object
    obj.scale = size
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    finish_object(obj, name, material)
    if bevel:
        edge = obj.modifiers.new("Rounded edges", "BEVEL")
        edge.width = bevel
        edge.segments = 3
        obj.modifiers.new("Weighted normals", "WEIGHTED_NORMAL")
    return obj


def ball(name, pos, radius, material, scale=(1, 1, 1)):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=12, radius=radius, location=pos)
    obj = finish_object(bpy.context.object, name, material)
    obj.scale = scale
    return obj


def cylinder(name, pos, radius, depth, material, vertices=48):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth, location=pos)
    return finish_object(bpy.context.object, name, material)


def cone(name, pos, bottom, top, depth, material, vertices=6):
    bpy.ops.mesh.primitive_cone_add(vertices=vertices, radius1=bottom, radius2=top,
                                  depth=depth, location=pos)
    return finish_object(bpy.context.object, name, material)


def ring(name, pos, radius, thickness, material):
    bpy.ops.mesh.primitive_torus_add(major_radius=radius, minor_radius=thickness,
                                    major_segments=64, minor_segments=12, location=pos)
    return finish_object(bpy.context.object, name, material)


def line(name, points, radius, material):
    data = bpy.data.curves.new(name, "CURVE")
    data.dimensions = "3D"
    data.resolution_u = 12
    data.bevel_depth = radius
    data.bevel_resolution = 3
    data.use_fill_caps = True
    spline = data.splines.new("BEZIER")
    spline.bezier_points.add(len(points) - 1)
    for point, coordinate in zip(spline.bezier_points, points):
        point.co = coordinate
        point.handle_left_type = "AUTO"
        point.handle_right_type = "AUTO"
    obj = bpy.data.objects.new(name, data)
    bpy.context.collection.objects.link(obj)
    data.materials.append(material)
    return obj


def beam(name, start, end, radius, material):
    a, b = Vector(start), Vector(end)
    obj = cylinder(name, (a + b) * 0.5, radius, (b - a).length, material, 24)
    obj.rotation_euler = (b - a).to_track_quat("Z", "Y").to_euler()
    return obj


def point_at(obj, target):
    obj.rotation_euler = (Vector(target) - obj.location).to_track_quat("-Z", "Y").to_euler()


bpy.ops.object.camera_add(location=(13, -17, 15))
camera = bpy.context.object
camera.name = "Gallery camera"
camera.data.type = "ORTHO"
camera.data.ortho_scale = 17
point_at(camera, (0, 0, 1.0))
scene.camera = camera


def label(body, pos, size=0.35, material=None):
    data = bpy.data.curves.new("Label " + body, "FONT")
    data.body = body
    data.align_x = "CENTER"
    data.align_y = "CENTER"
    data.size = size
    data.extrude = 0.004
    obj = bpy.data.objects.new("Label " + body, data)
    bpy.context.collection.objects.link(obj)
    obj.location = pos
    obj.rotation_euler = camera.rotation_euler
    data.materials.append(ink if material is None else material)
    return obj


def platform(name, pos, size=(3, 2.5, 0.25), material=None):
    return box(name, pos, size, navy if material is None else material, 0.15)


def robot(name, pos, material=None, scale=1.0):
    x, y, z = pos
    color = violet if material is None else material
    box(name + " body", (x, y, z + 0.70 * scale),
        (0.66 * scale, 0.52 * scale, 0.73 * scale), color)
    box(name + " head", (x, y, z + 1.32 * scale),
        (0.84 * scale, 0.61 * scale, 0.55 * scale), white)
    box(name + " visor", (x, y - 0.32 * scale, z + 1.34 * scale),
        (0.64 * scale, 0.035 * scale, 0.26 * scale), dark, 0.04)
    for side in (-1, 1):
        ball(name + " eye", (x + side * 0.17 * scale, y - 0.35 * scale, z + 1.35 * scale),
             0.065 * scale, glow)
        box(name + " foot", (x + side * 0.20 * scale, y - 0.04 * scale, z + 0.14 * scale),
            (0.24 * scale, 0.45 * scale, 0.25 * scale), navy)
        beam(name + " arm", (x + side * 0.40 * scale, y, z + 0.95 * scale),
             (x + side * 0.55 * scale, y - 0.12 * scale, z + 0.53 * scale),
             0.095 * scale, color)
    beam(name + " antenna", (x, y, z + 1.60 * scale),
         (x, y, z + 1.85 * scale), 0.035 * scale, gold)
    ball(name + " antenna light", (x, y, z + 1.87 * scale), 0.075 * scale, glow)


def server(name, pos, material=None, height=2.2):
    x, y, z = pos
    box(name, (x, y, z + height * 0.5), (0.95, 0.75, height),
        navy if material is None else material)
    for number in range(4):
        at = z + 0.30 + number * (height - 0.45) / 4
        box(name + " blade", (x, y - 0.39, at), (0.75, 0.045, 0.22), dark, 0.02)
        ball(name + " status", (x + 0.24, y - 0.43, at), 0.04, glow)


for light_name, position, power, color, size in [
    ("Key", (1, -7, 12), 2200, (0.80, 0.91, 1.0), 8),
    ("Fill", (-7, -1, 6), 1600, (0.55, 0.75, 1.0), 7),
    ("Rim", (4, 7, 10), 2400, (0.40, 1.0, 0.83), 6),
]:
    bpy.ops.object.light_add(type="AREA", location=position)
    lamp = bpy.context.object
    lamp.name = light_name
    lamp.data.energy = power
    lamp.data.color = color
    lamp.data.shape = "DISK"
    lamp.data.size = size
    point_at(lamp, (0, 0, 1))


def gallery_finish(title, slug):
    bpy.context.view_layer.update()
    points = [obj.matrix_world @ Vector(corner) for obj in scene.objects
              if obj.type in ("MESH", "CURVE", "FONT") for corner in obj.bound_box]
    if not points:
        raise RuntimeError("Subject contains no geometry")
    minimum = Vector(tuple(min(point[k] for point in points) for k in range(3)))
    maximum = Vector(tuple(max(point[k] for point in points) for k in range(3)))
    center = (minimum + maximum) * 0.5
    camera.location = center + Vector((13, -17, 15))
    point_at(camera, center)
    bpy.context.view_layer.update()
    inverse = camera.matrix_world.inverted()
    projected = [inverse @ point for point in points]
    width = max(point.x for point in projected) - min(point.x for point in projected)
    height = max(point.y for point in projected) - min(point.y for point in projected)
    camera.data.ortho_scale = max(width / 0.86, height * (4 / 3) / 0.77)
    rotation = camera.rotation_euler.to_matrix()
    up = rotation @ Vector((0, 1, 0))
    forward = rotation @ Vector((0, 0, 1))
    label(title.upper(), center + up * (camera.data.ortho_scale * 0.325) + forward * 5,
          camera.data.ortho_scale * 0.025, white)
    label("MICROSOFT CONCEPT STUDY  /  " + slug[:2],
          center - up * (camera.data.ortho_scale * 0.333) + forward * 5,
          camera.data.ortho_scale * 0.011)
    box("Studio floor", (center.x, center.y, minimum.z - 0.30), (200, 200, 0.08), navy, 0)
    scene.name = title
    scene["gallery_subject"] = slug
    scene["external_assets"] = 0
    bpy.ops.object.select_all(action="DESELECT")
    bpy.context.view_layer.update()
    print("GALLERY_BUILD=" + json.dumps({
        "slug": slug, "objects": len(scene.objects),
        "mesh_objects": len([obj for obj in scene.objects if obj.type == "MESH"]),
        "curve_objects": len([obj for obj in scene.objects if obj.type == "CURVE"]),
        "vertices": sum(len(obj.data.vertices) for obj in scene.objects if obj.type == "MESH"),
        "camera_scale": camera.data.ortho_scale, "blender": bpy.app.version_string,
    }))
