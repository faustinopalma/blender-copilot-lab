outline = [(-4.5, -4.2), (4.5, -4.2), (5.8, -2.9), (5.8, 2.9),
           (4.5, 4.2), (-4.5, 4.2), (-5.8, 2.9), (-5.8, -2.9)]


def octagonal_slab(name, z, depth, factor, material):
    points = [(x * factor, y * factor, z + dz)
              for dz in (-depth / 2, depth / 2) for x, y in outline]
    faces = [tuple(reversed(range(8))), tuple(range(8, 16))]
    faces += [(i, (i + 1) % 8, (i + 1) % 8 + 8, i + 8) for i in range(8)]
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(points, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    finish_object(obj, name, material)
    edge = obj.modifiers.new("Machined edge", "BEVEL")
    edge.width = 0.06
    edge.segments = 3
    obj.modifiers.new("Weighted normals", "WEIGHTED_NORMAL")
    return obj


octagonal_slab("Citadel octagonal foundation", 0.0, 0.46, 1.035, navy)
octagonal_slab("Citadel silver reveal", 0.24, 0.10, 1.015, white)
octagonal_slab("Cyan circuit floor", 0.34, 0.16, 1.0, dark)

for i, a in enumerate(outline):
    b = outline[(i + 1) % 8]
    beam("Perimeter cyan inlay %02d" % i,
         (a[0] * 0.97, a[1] * 0.97, 0.435),
         (b[0] * 0.97, b[1] * 0.97, 0.435), 0.025, glow)

# Low, broken ramparts keep both identity apertures visible.
for i, a in enumerate(outline):
    b = outline[(i + 1) % 8]
    for j in range(2):
        if i == 0 and j == 0:
            continue
        t = (j + 0.5) / 2
        x = (a[0] + (b[0] - a[0]) * t) * 0.92
        y = (a[1] + (b[1] - a[1]) * t) * 0.92
        length = math.hypot(b[0] - a[0], b[1] - a[1]) * 0.43
        angle = math.atan2(b[1] - a[1], b[0] - a[0])
        height = 0.56 if y < 0 else 0.84
        body = box("Segmented wall %02d %d" % (i, j),
                   (x, y, 0.43 + height / 2), (length, 0.29, height), navy)
        body.rotation_euler.z = angle
        cap = box("Wall porcelain coping %02d %d" % (i, j),
                  (x, y, 0.46 + height), (length + 0.06, 0.39, 0.12), white, 0.04)
        cap.rotation_euler.z = angle
        signal = box("Wall teal status %02d %d" % (i, j),
                     (x, y, 0.58 + height), (length * 0.69, 0.09, 0.035), teal, 0.01)
        signal.rotation_euler.z = angle

for i, (x, y) in enumerate([(-5.15, -2.6), (5.12, -2.6),
                            (-4.35, 3.45), (4.7, 3.1)]):
    cylinder("Watch sensor pedestal %d" % i, (x, y, 0.58), 0.24, 0.30, navy, 8)
    beam("Watch sensor mast %d" % i, (x, y, 0.68), (x, y, 1.78), 0.07, white)
    ball("Watch sensor housing %d" % i, (x, y, 1.86), 0.25, navy, (1.15, 0.85, 0.8))
    ball("Watch sensor cyan lens %d" % i, (x, y - 0.18, 1.86),
         0.12, glow, (1, 0.35, 1))
    ring("Watch sensor halo %d" % i, (x, y, 1.68), 0.27, 0.026, gold)

circuits = [
    [(-4.9, -1.4, .45), (-4.0, -1.4, .45), (-3.6, -.9, .45), (-3.6, 1.9, .45)],
    [(-4.6, 2.7, .45), (-2.3, 2.7, .45), (-1.8, 2.2, .45), (-1.8, 1.2, .45)],
    [(-4.8, .0, .45), (-4.3, .0, .45), (-4.0, .5, .45), (-4.0, 1.7, .45)],
    [(-1.4, -3.3, .45), (-.2, -3.3, .45), (.3, -2.8, .45), (2.5, -2.8, .45)],
    [(4.8, -1.9, .45), (3.9, -1.9, .45), (3.3, -1.2, .45), (2.5, -1.2, .45)],
    [(4.8, .0, .45), (4.3, .0, .45), (4.0, .5, .45), (4.0, 1.1, .45)],
]
for i, points in enumerate(circuits):
    line("Cyan floor circuit %d" % i, points, 0.022, teal)
    for j, p in enumerate((points[0], points[-1])):
        cylinder("Circuit terminal %d %d" % (i, j), p, 0.075, 0.024, glow, 12)

route = [(-2.85, -4.15, .47), (-2.85, -2.45, .47), (-2.6, -1.55, .47),
         (-.55, -.8, .47), (-.55, .25, .47), (.1, .85, .47), (2.35, .85, .47)]
line("Identity route dark walkway", route, 0.34, navy)
line("Identity route gold authorization spine", [(x, y, .82) for x, y, z in route],
     0.035, gold)
for offset in (-.28, .28):
    line("Checkpoint linked cyan path edge",
         [(x + offset, y, .76) for x, y, z in route], .024, glow)

for i, (x, y) in enumerate([(-2.85, -3.55), (-2.7, -1.6), (-.55, -.8),
                            (-.25, .65), (1.0, .85)]):
    angle = 0 if i < 3 else -math.pi / 2
    for side in (-1, 1):
        start = Vector((side * .16, -.12, 0))
        end = Vector((0, .10, 0))
        c, s = math.cos(angle), math.sin(angle)
        a = (x + c * start.x - s * start.y, y + s * start.x + c * start.y, .84)
        b = (x + c * end.x - s * end.y, y + s * end.x + c * end.y, .84)
        beam("Authorized path chevron %d" % i, a, b, .027, gold)

for index, (x, y, color, title) in enumerate([
        (-2.85, -2.45, blue, "VERIFY"),
        (-.55, .25, teal, "LEAST PRIVILEGE")], 1):
    for side in (-1, 1):
        sx = x + side * 1.00
        box("Checkpoint %d grounded shoe" % index, (sx, y, .57), (.52, .78, .30), navy)
        box("Identity checkpoint %d armored jamb" % index,
            (sx, y, 1.80), (.34, .47, 2.28), white)
        box("Checkpoint %d colored inset" % index,
            (sx, y - .245, 1.82), (.19, .025, 1.92), color, .025)
        box("Checkpoint %d illuminated aperture" % index,
            (x + side * .78, y, 1.82), (.055, .30, 2.18), glow, .018)
        box("Identity checkpoint %d reader" % index,
            (sx, y - .32, 1.48), (.28, .15, .43), navy, .035)
        ball("Identity checkpoint accepted indicator %d" % index,
             (sx, y - .415, 1.48), .070, glow, (1, .25, 1))
    box("Checkpoint %d lintel" % index, (x, y, 3.05), (2.48, .62, .48), color)
    box("Checkpoint %d nameplate" % index, (x, y - .33, 3.05),
        (2.24, .065, .36), navy, .025)
    gate_title = label(title, (x, y - .44, 3.10), .27 if index == 1 else .205, white)
    gate_title.rotation_euler = (math.pi / 2, 0, 0)
    identity_label = label("IDENTITY / 0%d" % index, (x, y - .42, 2.69), .13, gold)
    identity_label.rotation_euler = (math.pi / 2, 0, 0)
    cylinder("Identity gold token %d" % index, (x, y, 1.73), .31, .09, gold, 48).rotation_euler.x = math.pi / 2
    ring("Identity token cyan authorization %d" % index,
         (x, y - .058, 1.73), .22, .026, glow).rotation_euler.x = math.pi / 2
    token_label = label("0%d" % index, (x, y - .13, 1.75), .20, dark)
    token_label.rotation_euler = (math.pi / 2, 0, 0)

vx, vy = 2.4, 1.95
cylinder("Vault octagonal foundation", (vx, vy, .67), 1.72, .47, navy, 8)
cylinder("Vault gold perimeter reveal", (vx, vy, .94), 1.58, .09, gold, 8)
cylinder("Vault tier porcelain deck", (vx, vy, 1.045), 1.49, .15, white, 8)
cylinder("Secure vault tower", (vx, vy, 2.39), 1.34, 2.62, blue, 8)
for i in range(8):
    theta = math.pi / 8 + i * math.pi / 4
    x, y = vx + 1.24 * math.cos(theta), vy + 1.24 * math.sin(theta)
    box("Vault vertical armor rib %d" % i, (x, y, 2.39),
        (.12, .12, 2.62), white, .04)
cylinder("Vault chamber dark sill", (vx, vy, 3.78), 1.44, .17, navy, 8)
ring("Vault chamber cyan sill", (vx, vy, 3.90), 1.31, .042, glow)
for i in range(6):
    theta = i * math.pi / 3
    x, y = vx + 1.13 * math.cos(theta), vy + 1.13 * math.sin(theta)
    beam("Vault open crystal chamber post %d" % i, (x, y, 3.86),
         (x, y, 5.10), .065, gold)
for i, (dx, dy, height) in enumerate([(-.48, -.44, .64), (.05, -.40, .84), (.50, -.44, .58)]):
    cylinder("Vault key crystal socket %d" % i, (vx + dx, vy + dy, 3.99),
             .22, .16, navy, 8)
    cone("Vault key crystal %d" % i, (vx + dx, vy + dy, 4.07 + height / 2),
         .24, 0, height, violet if i != 1 else glow, 5)
cylinder("Vault crown floating canopy", (vx, vy, 5.13), 1.24, .19, navy, 8)
cone("Vault crown tapered porcelain", (vx, vy, 5.32), 1.23, .90, .22, white, 8)
ring("Vault crown cyan seal", (vx, vy, 5.47), .88, .045, glow)


def shield_plate(name, x, y, z, factor, material):
    contour = [(-.74, .65), (.74, .65), (.64, -.10), (.41, -.58),
               (0, -.87), (-.41, -.58), (-.64, -.10)]
    vertices = [(x + a * factor, y + depth, z + b * factor)
                for depth in (0, .10) for a, b in contour]
    faces = [tuple(reversed(range(7))), tuple(range(7, 14))]
    faces += [(i, (i + 1) % 7, (i + 1) % 7 + 7, i + 7) for i in range(7)]
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(vertices, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    finish_object(obj, name, material)
    bevel = obj.modifiers.new("Shield beveled border", "BEVEL")
    bevel.width = .035
    bevel.segments = 3
    obj.modifiers.new("Weighted shield normals", "WEIGHTED_NORMAL")


box("Vault reinforced portal", (vx, .69, 2.16), (1.64, .17, 1.86), navy, .15)
shield_plate("Vault original gold shield", vx, .53, 2.64, 1.0, gold)
shield_plate("Vault original porcelain shield field", vx, .405, 2.64, .82, white)
cylinder("Vault shield keyhole circle", (vx, .375, 2.75), .16, .035, dark, 48).rotation_euler.x = math.pi / 2
keyhole = box("Vault shield keyhole stem", (vx, .37, 2.49), (.17, .04, .37), dark, .025)
box("Vault access cyan threshold", (vx, .52, 1.23), (1.17, .16, .08), glow, .025)
vault_label = label("VAULT", (vx, .19, 1.55), .32, white)
vault_label.rotation_euler = (math.pi / 2, 0, 0)

robot("Identity visitor robot", (-3.53, -3.55, .44), white, .62)
box("Visitor credential", (-3.53, -3.76, .94), (.25, .04, .22), gold, .025)

platform("Security telemetry console base", (-3.4, 1.65, .54), (1.7, 1.20, .22), navy)
box("Security telemetry console support", (-3.4, 1.74, .98), (.86, .56, .72), white)
box("Security telemetry console screen", (-3.4, 1.39, 1.44), (1.32, .14, .82), navy)
for i in range(3):
    box("Security telemetry status row %d" % i, (-3.56, 1.305, 1.22 + i * .20),
        (.70 - i * .12, .035, .045), glow, .01)
policy_label = label("POLICY ENGINE", (-3.4, 1.18, 2.02), .20, white)
policy_label.rotation_euler = (math.pi / 2, 0, 0)
