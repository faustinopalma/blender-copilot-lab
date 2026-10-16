# One shared reservoir, fed by three distinct floating data sources.
water = mat("Lake water - luminous jade", (0.015, 0.58, 0.49), metal=.38, rough=.19)
rock = mat("Island slate facets", (0.045, 0.115, 0.19), metal=.22, rough=.58)
rock_light = mat("Island mineral facets", (0.065, 0.22, 0.29), metal=.3, rough=.46)
foam = mat("Water pearl foam", (0.43, 1.0, .89), rough=.23, emission=.35)
timber = mat("Dock warm brasswood", (.55, .30, .10), metal=.2, rough=.46)


def faceted(name, pos, bottom, top, depth, material, vertices=9):
    obj = cone(name, pos, bottom, top, depth, material, vertices)
    for face in obj.data.polygons:
        face.use_smooth = False
    return obj


faceted("lake floating faceted bedrock", (0, 0, 1.15), .65, 3.18, 2.25, rock, 11)
faceted("lake shoreline escarpment", (0, 0, 2.17), 3.18, 3.03, .43, rock_light, 11)
cylinder("lake recessed dark basin", (0, 0, 2.36), 3.02, .15, navy, 96)
cylinder("lake shared teal water", (0, 0, 2.445), 2.87, .095, water, 96)
ring("lake gold shoreline inlay", (0, 0, 2.43), 2.96, .035, gold)
ring("lake fine waterline", (0, 0, 2.50), 2.84, .021, foam)

for i, (angle, height) in enumerate([(-135, 1.05), (-75, .75), (15, 1.1), (125, .65)]):
    a = math.radians(angle)
    faceted("lake hanging mineral shard %02d" % i,
            (2.0 * math.cos(a), 2.0 * math.sin(a), height),
            .08, .52, .85, rock_light, 5)

# Plank-built docks touch the reservoir; the two consumers share the same water.
for dock_name, x, y, sx, sy in [
    ("warehouse dock", -1.95, -.55, 1.38, 2.10),
    ("analytics dock", 1.94, .15, 1.20, 2.00),
]:
    box(dock_name + " dark frame", (x, y, 2.57), (sx + .12, sy + .12, .16), navy)
    for j in range(10):
        box(dock_name + " plank %02d" % j, (x, y - sy / 2 + .105 + j * sy / 10, 2.67),
            (sx, sy / 10 - .026, .08), timber, .015)
    for side in (-1, 1):
        for end in (-1, 1):
            px, py = x + side * sx * .43, y + end * sy * .44
            cylinder(dock_name + " mooring post", (px, py, 2.68), .067, .53, navy, 16)
            cylinder(dock_name + " post cap", (px, py, 2.96), .079, .055, gold, 16)

box("warehouse porcelain walls", (-1.95, -.22, 3.08), (1.12, 1.04, .78), white)
box("warehouse navy roof", (-1.95, -.22, 3.51), (1.28, 1.19, .13), navy)
box("warehouse gold roof ridge", (-1.95, -.22, 3.59), (.95, .08, .06), gold, .02)
box("warehouse loading doorway", (-1.95, -.756, 2.99), (.48, .035, .55), dark, .025)
for z in (2.82, 2.96, 3.10):
    box("warehouse roller door slat", (-1.95, -.784, z), (.42, .018, .023), teal, .005)
for x in (-2.35, -1.55):
    box("warehouse illuminated front window", (x, -.76, 3.22), (.19, .035, .22), blue, .02)
box("warehouse landing parcel", (-2.29, -1.25, 2.84), (.28, .26, .27), gold, .025)
box("warehouse parcel strap", (-2.29, -1.39, 2.84), (.047, .014, .25), white, .005)
warehouse_label = label("WAREHOUSE", (-1.95, -.87, 3.50), .16, white)
warehouse_label.location += Vector((13, -17, 15)).normalized() * .8

box("analytics glass pavilion", (1.94, .43, 3.14), (.94, .98, .87), blue)
box("analytics floating white canopy", (1.94, .43, 3.64), (1.15, 1.17, .13), white)
box("analytics front display", (1.94, -.08, 3.18), (.75, .035, .61), dark, .025)
for j, height in enumerate((.16, .28, .40, .32)):
    box("analytics glowing chart bar %d" % j, (1.68 + j * .17, -.108, 2.97 + height / 2),
        (.095, .018, height), glow if j != 2 else gold, .012)
for x in (1.52, 2.36):
    box("analytics white mullion", (x, -.09, 3.16), (.045, .05, .84), white, .012)
analytics_label = label("ANALYTICS", (1.94, -.20, 3.66), .16, navy)
analytics_label.location += Vector((13, -17, 15)).normalized() * .8

# Each elevated island has its own visual source icon and labelled inlet.
sources = [
    ("FILES", (-4.35, 1.0, 3.55), blue),
    ("TABLES", (-1.05, 3.95, 4.23), teal),
    ("EVENTS", (3.85, 2.60, 3.75), violet),
]
for name, (x, y, z), color in sources:
    faceted("source " + name + " suspended rock", (x, y, z - .68), .19, 1.12, 1.24, rock, 7)
    faceted("source " + name + " upper shelf", (x, y, z - .10), 1.12, 1.03, .22, rock_light, 7)
    cylinder("source " + name + " intake pool", (x, y, z + .035), .90, .08, color, 64)
    ring("source " + name + " gold rim", (x, y, z + .08), .98, .035, gold)
    cylinder("source " + name + " icon plinth", (x, y + .12, z + .16), .56, .18, navy, 48)
    source_label = label(name, (x, y - .43, z + 1.48), .31, white)
    source_label.location += Vector((13, -17, 15)).normalized() * .8

x, y, z = sources[0][1]
for i in range(3):
    box("source FILES stacked document %d" % i, (x - .10 + i * .07, y + .10, z + .32 + i * .13),
        (.61, .69, .085), white, .025)
box("source FILES file tab", (x + .20, y + .38, z + .62), (.18, .18, .055), gold, .012)
for j in range(3):
    box("source FILES blue document line", (x + .035, y - .08 + j * .14, z + .63),
        (.37, .035, .018), blue, .008)

x, y, z = sources[1][1]
for j in range(3):
    cylinder("source TABLES database tier", (x, y + .10, z + .32 + j * .18),
             .40, .145, white, 48)
    ring("source TABLES tier teal seam", (x, y + .10, z + .40 + j * .18), .38, .025, teal)
for j in range(3):
    ball("source TABLES status light", (x + .16 * (j - 1), y - .29, z + .65), .035, gold)

x, y, z = sources[2][1]
cylinder("source EVENTS transmitter base", (x, y + .10, z + .30), .33, .16, white)
beam("source EVENTS antenna", (x, y + .10, z + .36), (x, y + .10, z + .91), .055, gold)
ball("source EVENTS pulse beacon", (x, y + .10, z + .95), .13, glow)
for r in (.32, .51):
    line("source EVENTS broadcast arc",
         [(x + r * math.cos(a), y + .10, z + .90 + r * math.sin(a))
          for a in [math.radians(v) for v in range(15, 170, 25)]], .025, white)

# Broad three-strand streams preserve a clear continuous connection to the lake.
paths = [
    [(-3.94, .48, 3.61), (-3.35, .25, 3.53), (-2.81, .28, 3.07), (-2.35, .48, 2.52)],
    [(-1.02, 3.30, 4.29), (-.94, 2.84, 4.12), (-.72, 2.37, 3.25), (-.48, 1.90, 2.52)],
    [(3.36, 2.06, 3.81), (2.92, 1.78, 3.70), (2.44, 1.47, 3.00), (1.88, 1.25, 2.52)],
]
for i, points in enumerate(paths):
    for j in (-1, 0, 1):
        line("stream %d flowing ribbon %d" % (i, j),
             [(x + j * .095, y, z) for x, y, z in points], .092,
             foam if j == -1 else (blue if i == 0 else teal))
    end = points[-1]
    for r in (.21, .35):
        ripple = ring("stream %d arrival ripple" % i, (end[0], end[1], 2.505), r, .016, foam)
        ripple.scale.y = .63
    for j in range(2):
        p = points[j + 1]
        cube = box("stream %d floating data cube %d" % (i, j),
                   (p[0] + .05, p[1], p[2] + .23), (.20, .20, .20), white if j else gold, .025)
        cube.rotation_euler = (.18, .24, .40)

# Falls spill over the forward shoreline, leaving the rock silhouette visible.
for side, angle in enumerate((-140, -28)):
    a = math.radians(angle)
    px, py = 2.82 * math.cos(a), 2.82 * math.sin(a)
    for j in range(3):
        dx = (j - 1) * .11
        line("lake waterfall ribbon %d %d" % (side, j),
             [(px + dx, py, 2.50), (px + dx, py - .20, 2.29),
              (px + dx * 1.2, py - .27, 1.48), (px + dx * 1.4, py - .37, .60)],
             .055 if j != 1 else .075, foam if j == 0 else teal)
    for j in range(3):
        ball("lake waterfall suspended spray", (px + (j - 1) * .19, py - .37, .43 + j * .08),
             .065, foam, (1, 1, 1.6))

# Tiny harbour launch, with its bow wake and glazed cabin.
ball("lake boat navy hull", (.28, -1.18, 2.60), 1, navy, (.29, .65, .16))
ball("lake boat gold gunwale", (.28, -1.18, 2.68), 1, gold, (.27, .60, .075))
box("lake boat white deck", (.28, -1.18, 2.73), (.38, .76, .08), white, .06)
box("lake boat coral cabin", (.28, -1.04, 2.89), (.33, .33, .27), coral, .06)
box("lake boat blue windscreen", (.28, -1.22, 2.93), (.26, .02, .12), blue, .018)
box("lake boat cabin roof", (.28, -1.04, 3.04), (.39, .40, .06), white, .035)
beam("lake boat radio mast", (.28, -.96, 3.07), (.28, -.96, 3.35), .017, gold)
for side in (-1, 1):
    line("lake boat spreading wake",
         [(.28 + side * .14, -.58, 2.51), (.28 + side * .32, -.33, 2.51),
          (.28 + side * .49, -.13, 2.51)], .017, foam)

for i, (x, y, radius) in enumerate([(-.65, -.65, .31), (.85, .62, .32), (-.75, .92, .22),
                                  (1.00, -1.95, .23), (-.70, -2.06, .20)]):
    line("lake gentle wave %d" % i,
         [(x + radius * math.cos(a), y + radius * .46 * math.sin(a), 2.505)
          for a in [math.radians(v) for v in range(20, 160, 25)]], .018, foam)

for cluster, (x, y) in enumerate([(-2.50, 1.03), (-2.66, -.15), (2.60, -.65)]):
    for j in range(3):
        px, py = x + (j - 1) * .11, y + (j % 2) * .12
        h = .38 + .11 * (j % 2)
        beam("lake reed %d stem" % cluster, (px, py, 2.45), (px + .04, py, 2.45 + h), .018, gold)
        ball("lake reed %d seed head" % cluster, (px + .04, py, 2.51 + h),
             .045, timber, (.65, .65, 2.1))

for j, (x, y, z) in enumerate([(-.80, .1, 2.76), (1.00, 1.25, 2.82), (-3.65, .50, 2.76)]):
    obj = box("lake free floating data cube %d" % j, (x, y, z), (.22, .22, .22), teal, .03)
    obj.rotation_euler = (.2, .4, .35)

lake_label = label("ONE LAKE", (.05, -2.91, 1.69), .55, white)
lake_label.location += Vector((13, -17, 15)).normalized() * 1.5
lake_subtitle = label("SHARED DATA  /  ONE COPY", (.05, -2.96, 1.25), .15, foam)
lake_subtitle.location += Vector((13, -17, 15)).normalized() * 1.5
