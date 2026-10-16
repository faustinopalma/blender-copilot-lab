islands = {
    "compute": (-3.05, -2.0, 2.55),
    "storage": (2.75, -2.0, 2.12),
    "network": (3.0, 2.35, 2.95),
    "AI": (-2.95, 2.55, 3.42),
}


def rocky_island(name, x, y, z):
    rock = cone(name + " floating basalt heart", (x, y, z - .93),
                .23, 1.53, 1.65, navy, vertices=7)
    rock.rotation_euler.z = .18
    rock.data.materials.append(blue)
    rock.data.materials.append(dark)
    for face in rock.data.polygons:
        face.use_smooth = False
        face.material_index = 1 if face.index % 4 == 0 else (2 if face.index % 3 == 0 else 0)
    for j, (dx, dy, depth) in enumerate([(-.77, -.27, 1.1),
                                        (.68, .37, .95), (.1, .85, .8)]):
        shard = cone(name + " fractured rock " + str(j),
                     (x + dx, y + dy, z - .6), .08, .65, depth, navy, vertices=5)
        shard.rotation_euler = (.12 * (j - 1), .15, j * .7)
        for face in shard.data.polygons:
            face.use_smooth = False
    cylinder(name + " porcelain island rim", (x, y, z - .05),
             1.55, .2, white, vertices=8)
    cylinder(name + " blue service terrace", (x, y, z + .075),
             1.43, .1, blue, vertices=8)
    ring(name + " luminous perimeter", (x, y, z + .14), 1.4, .028, glow)
    sign_position = Vector((x + .65, y - 1.57, z + .22))
    sign = box(name + " floating identification plaque", sign_position,
               (1.85, .46, .08), navy, .055)
    sign.rotation_euler = camera.rotation_euler
    sign_front = camera.rotation_euler.to_matrix() @ Vector((0, 0, .06))
    label(name.upper(), sign_position + sign_front, .28, white)


for name, (x, y, z) in islands.items():
    rocky_island(name, x, y, z)


def suspension_bridge(name, first, second):
    a = Vector(first)
    b = Vector(second)
    axis = b - a
    horizontal = Vector((axis.x, axis.y, 0)).normalized()
    side = Vector((-horizontal.y, horizontal.x, 0))
    a += horizontal * 1.32 + Vector((0, 0, .18))
    b -= horizontal * 1.32 - Vector((0, 0, .18))
    heading = math.atan2(horizontal.y, horizontal.x)

    def deck(t):
        return a.lerp(b, t) - Vector((0, 0, .16 * math.sin(math.pi * t)))

    span = (b - a).length
    for j in range(7):
        p = deck((j + .5) / 7)
        plank = box(name + " bridge porcelain tread " + str(j), p,
                    (span / 7 * .94, .72, .11), white, .025)
        plank.rotation_euler.y = -math.atan2(b.z - a.z, span)
        plank.rotation_euler.z = heading
    for sign in (-1, 1):
        offset = side * .42 * sign
        for t in (0, 1):
            foot = deck(t) + offset
            beam(name + " bridge blue suspension pylon", foot,
                 foot + Vector((0, 0, .9)), .052, blue)
        cable_points = []
        for t in (0, .25, .5, .75, 1):
            p = deck(t) + offset
            cable_points.append(p + Vector((0, 0, .9 - .48 * math.sin(math.pi * t))))
        line(name + " bridge luminous suspension cable", cable_points, .027, glow)
        for t in (.28, .72):
            foot = deck(t) + offset
            beam(name + " bridge vertical hanger", foot,
                 foot + Vector((0, 0, .9 - .48 * math.sin(math.pi * t))),
                 .018, white)
    for j, t in enumerate((.33, .7)):
        packet = box(name + " bridge travelling packet " + str(j),
                     deck(t) + Vector((0, 0, .24)), (.22, .22, .22),
                     gold if j == 0 else glow, .035)
        packet.rotation_euler.z = heading + .35


for name, first, second in [
    ("compute storage", "compute", "storage"),
    ("storage network", "storage", "network"),
    ("network AI", "network", "AI"),
    ("AI compute", "AI", "compute"),
]:
    suspension_bridge(name, islands[first], islands[second])

x, y, z = islands["compute"]
for j, (dx, dy, height) in enumerate([(-.59, -.31, 1.53),
                                      (.59, -.31, 1.85), (0, .64, 2.12)]):
    server("compute server tower " + str(j), (x + dx, y + dy, z + .14),
           white, height=height)
    box("compute azure roof light", (x + dx, y + dy, z + height + .17),
        (.7, .53, .07), blue, .025)
for dx in (-.94, .94):
    box("compute terrace status marker", (x + dx, y - .91, z + .23),
        (.14, .25, .13), glow, .03)

x, y, z = islands["storage"]
for j, (dx, dy, height) in enumerate([(-.69, .18, 1.23),
                                     (.47, .43, 1.52), (.26, -.66, 1.03)]):
    base = z + .14
    cylinder("storage cylindrical data tank " + str(j),
             (x + dx, y + dy, base + height / 2), .43, height, white)
    cylinder("storage tank azure lid", (x + dx, y + dy, base + height),
             .45, .09, blue)
    for level in (.16, height - .14):
        ring("storage tank luminous data band", (x + dx, y + dy, base + level),
             .435, .025, glow)
    box("storage tank readout", (x + dx, y + dy - .433, base + height * .55),
        (.3, .035, .25), navy, .025)
    box("storage tank status light", (x + dx, y + dy - .457, base + height * .55),
        (.17, .026, .05), glow, .01)
for dx in (-.65, .51):
    line("storage connected data conduit", [
        (x + dx, y + .19, z + .3), (x + dx, y + .87, z + .3),
        (x + .05, y + .95, z + .3)], .045, gold)

x, y, z = islands["network"]
cylinder("network transmission mast footing", (x, y, z + .25), .62, .23, navy)
beam("network tapered transmission mast", (x, y, z + .35),
     (x, y, z + 2.35), .09, white)
for level in (.65, 1.45):
    ring("network mast blue collar", (x, y, z + level), .18, .065, blue)
ball("network mast signal beacon", (x, y, z + 2.38), .14, glow)
for j, radius in enumerate((.43, .71, .99)):
    points = [(x + radius * math.cos(t), y,
               z + 1.52 + radius * math.sin(t))
              for t in [math.pi * k / 12 for k in range(13)]]
    line("network transmission signal arc " + str(j), points, .037,
         glow if j < 2 else blue)
for angle in (0, 2.094, 4.189):
    beam("network mast stabilizer", (x, y, z + 1.05),
         (x + .9 * math.cos(angle), y + .9 * math.sin(angle), z + .19),
         .035, gold)
label("UPLINK", (x, y - .75, z + .72), .18, white)

x, y, z = islands["AI"]
cylinder("AI neural crystal cradle", (x, y, z + .25), .7, .23, navy, vertices=8)
ring("AI crystal violet induction ring", (x, y, z + .4), .58, .04, violet)
for name, center, bottom, top, depth in [
    ("AI upper neural crystal", z + 1.54, .61, 0, 1.55),
    ("AI lower neural crystal", z + .63, .1, .61, .28),
]:
    crystal = cone(name, (x, y, center), bottom, top, depth, violet, vertices=6)
    crystal.rotation_euler.z = .32
    crystal.data.materials.append(white)
    crystal.data.materials.append(blue)
    for face in crystal.data.polygons:
        face.use_smooth = False
        face.material_index = 2 if face.index % 3 == 0 else 0
orbit = []
for j in range(17):
    t = j * math.tau / 16
    orbit.append((x + .9 * math.cos(t), y + .65 * math.sin(t),
                  z + 1.15 + .25 * math.cos(t)))
line("AI neural orbit", orbit, .018, glow)
for j in range(3):
    ball("AI neural satellite node", orbit[j * 5], .095, gold)
label("NEURAL CORE", (x, y - .76, z + .63), .16, white)

for j, (cx, cy, cz, radius) in enumerate([
    (-3.45, -2.15, .44, .62), (2.85, -2.13, .16, .62),
    (3.48, 2.65, .88, .6), (-3.36, 2.72, 1.3, .62),
    (-.08, .13, .25, .7),
]):
    for k, (dx, dy, dz, s) in enumerate([
        (-.54, .08, -.04, .8), (0, 0, .16, 1), (.55, -.06, -.08, .76)
    ]):
        ball("cloud cluster " + str(j) + " puff " + str(k),
             (cx + dx, cy + dy, cz + dz), radius * s,
             white, scale=(1.25, .9, .66))
