amber = mat("Forge molten amber", (1.0, 0.30, 0.025), metal=0.25, emission=2.6)
plasma = mat("Forge violet plasma", (0.53, 0.12, 1.0), emission=2.0)
steel = mat("Workshop brushed titanium", (0.20, 0.27, 0.37), metal=0.75, rough=0.28)

platform("forge workshop foundation", (0, 0, 0), (12, 9, 0.42), navy)
box("forge foundation amber reveal", (0, -4.46, 0.04), (10.9, 0.035, 0.07), amber, 0.01)
for x in (-5.25, 5.25):
    for y in (-3.7, 3.7):
        cylinder("forge foundation corner rivet", (x, y, 0.24), 0.1, 0.055, gold, 16)
for x in (-4.5, -1.5, 1.5, 4.5):
    for y in (-2.9, 0.0, 2.9):
        box("forge inset floor panel", (x, y, 0.23), (2.9, 2.79, 0.035), steel, 0.025)
for x in (-5.75, 5.75):
    box("forge safety side curb", (x, 0.7, 0.34), (0.16, 7.0, 0.22), violet, 0.04)

# The assembly island has a warm inner well and concentric service rails.
cylinder("forge circular assembly plinth", (0, 0.35, 0.43), 1.8, 0.4, navy, 64)
cylinder("forge amber energy well", (0, 0.35, 0.66), 1.42, 0.09, amber, 64)
cylinder("forge raised robot mounting plate", (0, 0.35, 0.75), 1.11, 0.16, steel, 64)
ring("forge outer violet induction ring", (0, 0.35, 0.67), 1.66, 0.075, plasma)
ring("forge gold containment ring", (0, 0.35, 0.80), 1.22, 0.055, gold)
for index in range(8):
    a = index * math.tau / 8
    x, y = 1.59 * math.cos(a), 0.35 + 1.59 * math.sin(a)
    clamp = box("forge radial containment clamp", (x, y, 0.74), (0.3, 0.22, 0.17), gold, 0.03)
    clamp.rotation_euler.z = a

robot("forge central agent", (0, 0.35, 0.84), violet, 1.38)
box("forge agent amber chest socket", (0, -0.027, 1.83), (0.39, 0.06, 0.34), gold, 0.045)
box("forge agent luminous installed core", (0, -0.065, 1.83), (0.22, 0.035, 0.2), amber, 0.025)
label("AGENT / 07", (0, -1.24, 0.95), 0.21, white)

# An open arch makes the central silhouette legible without enclosing the set.
for side in (-1, 1):
    x = side * 2.3
    box("forge gantry anchor", (x, 1.65, 0.52), (0.68, 0.74, 0.55), navy)
    box("forge gantry upright", (x, 1.65, 1.12), (0.28, 0.38, 1.1), steel, 0.05)
    box("forge gantry upright amber stripe", (x, 1.44, 1.15), (0.1, 0.035, 0.75), amber, 0.015)
arc_points = [(2.3 * math.cos(a), 1.65, 1.55 + 2.8 * math.sin(a))
              for a in [math.pi * i / 16 for i in range(17)]]
line("forge overhead articulated gantry arc", arc_points, 0.18, violet)
line("forge overhead amber power rail", [(p[0], p[1] - 0.16, p[2]) for p in arc_points], 0.04, amber)
box("forge overhead crown", (0, 1.65, 4.34), (1.05, 0.59, 0.34), navy)
label("AGENT FORGE", (0, 1.24, 4.42), 0.24, white)
beam("forge suspended assembly nozzle", (0, 1.65, 4.15), (0, 1.15, 3.72), 0.1, steel)
cone("forge precision assembly emitter", (0, 1.15, 3.64), 0.18, 0.11, 0.28, gold, 12)

for side in (-1, 1):
    x = side * 2.42
    cylinder("forge robot arm pedestal", (x, -0.25, 0.52), 0.37, 0.52, navy)
    ball("forge robotic shoulder", (x, -0.25, 0.91), 0.25, gold)
    elbow = (side * 2.05, -0.12, 2.20)
    wrist = (side * 0.98, -0.15, 2.33)
    beam("forge articulated robotic upper arm", (x, -0.25, 0.91), elbow, 0.15, violet)
    ball("forge robotic elbow bearing", elbow, 0.23, steel)
    beam("forge articulated robotic forearm", elbow, wrist, 0.12, white)
    ball("forge robotic wrist bearing", wrist, 0.17, gold)
    for dy in (-0.14, 0.14):
        beam("forge precision gripper finger", (wrist[0], wrist[1] + dy, wrist[2]),
             (side * 0.72, wrist[1] + dy, 2.17), 0.047, steel)
    line("forge robotic arm power cable",
         [(x, -0.13, 0.9), (side * 2.31, 0.05, 1.75), elbow, (side * 1.2, -0.02, 2.4)],
         0.038, amber)

# MODEL: cartridge supply, with a short tiled belt leading into the island.
platform("model supply station foot", (-4.2, 0.1, 0.43), (2.25, 2.1, 0.34), violet)
box("model cartridge cabinet", (-4.2, 0.4, 1.14), (1.8, 1.25, 1.14), navy)
box("model station worktop", (-4.2, 0.35, 1.76), (2.0, 1.47, 0.14), steel)
for x in (-4.69, -4.2, -3.71):
    box("model cartridge dark cradle", (x, 0.52, 1.88), (0.37, 0.7, 0.1), dark, 0.025)
    box("model violet cartridge", (x, 0.54, 2.13), (0.28, 0.55, 0.47), violet, 0.045)
    box("model cartridge amber key", (x, 0.245, 2.14), (0.12, 0.025, 0.22), amber, 0.015)
box("model station header plaque", (-4.2, -0.17, 2.62), (1.9, 0.13, 0.48), navy)
label("MODEL", (-4.2, -0.29, 2.66), 0.31, white)
label("01 / SELECT", (-4.2, -0.58, 1.09), 0.18, gold)
for x in (-4.63, -4.2, -3.77):
    box("model cabinet vent", (x, -0.25, 1.3), (0.28, 0.035, 0.07), steel, 0.01)
box("model module conveyor bed", (-2.95, -1.18, 0.57), (2.7, 0.75, 0.26), navy)
for i in range(7):
    box("model conveyor moving tile", (-4.08 + 0.37 * i, -1.18, 0.75), (0.31, 0.67, 0.11), steel, 0.02)
for x in (-3.73, -2.64):
    box("model in transit cartridge", (x, -1.18, 0.96), (0.43, 0.48, 0.32), violet, 0.045)
    box("model in transit luminous key", (x, -1.43, 0.96), (0.2, 0.02, 0.11), amber, 0.01)

# KNOWLEDGE: a library of physical memory folios at the rear-left.
platform("knowledge memory library base", (-3.45, 3.03, 0.43), (2.5, 1.62, 0.34), navy)
for x in (-4.52, -2.38):
    box("knowledge shelf side upright", (x, 3.15, 1.72), (0.13, 1.2, 2.25), violet, 0.035)
for z in (0.77, 1.77, 2.77):
    box("knowledge memory library shelf", (-3.45, 3.15, z), (2.26, 1.2, 0.12), steel, 0.03)
for level in range(2):
    for i in range(5):
        x = -4.21 + 0.38 * i
        z = 1.22 + level
        box("knowledge encoded memory folio", (x, 3.13, z), (0.25, 0.72, 0.72),
            teal if i % 2 == 0 else violet, 0.025)
        box("knowledge folio gold spine", (x, 2.755, z), (0.13, 0.025, 0.47), gold, 0.01)
box("knowledge library header", (-3.45, 3.15, 3.19), (2.65, 0.24, 0.53), navy)
label("KNOWLEDGE", (-3.45, 2.91, 3.28), 0.27, white)
line("knowledge memory delivery conduit",
     [(-2.35, 3.15, 1.0), (-1.8, 2.8, 0.55), (-0.8, 2.0, 0.55)], 0.07, glow)
box("knowledge memory delivery module", (-1.28, 2.4, 0.72), (0.5, 0.5, 0.28), teal, 0.05)

# TOOLS: a pegboard, distinct implements, and golden skill blocks.
platform("tool supply station base", (4.1, 1.64, 0.44), (2.65, 2.27, 0.36), violet)
box("tool workstation cabinet", (4.1, 1.6, 1.0), (2.2, 1.6, 0.84), navy)
box("tool brushed steel worktop", (4.1, 1.6, 1.48), (2.4, 1.8, 0.15), steel)
box("tool rack pegboard", (4.1, 2.35, 2.39), (2.3, 0.16, 1.67), dark)
for x in (3.34, 3.83, 4.32, 4.81):
    for z in (1.91, 2.41, 2.91):
        ball("tool rack mounting peg", (x, 2.24, z), 0.035, steel)
for x, material in ((3.40, gold), (4.1, coral), (4.80, teal)):
    beam("tool rack implement handle", (x, 2.14, 1.99), (x, 2.14, 2.66), 0.065, material)
    if material == gold:
        head = ring("tool rack socket wrench head", (x, 2.14, 2.76), 0.13, 0.045, steel)
        head.rotation_euler.x = math.pi / 2
    else:
        box("tool rack precision implement head", (x, 2.14, 2.75), (0.32, 0.17, 0.17), steel, 0.035)
box("tool station label plaque", (4.1, 2.25, 3.43), (2.3, 0.21, 0.48), navy)
label("TOOLS", (4.1, 2.0, 3.49), 0.31, white)
label("02 / EQUIP", (4.1, 0.69, 1.07), 0.18, gold)
for x in (3.58, 4.34):
    box("tool skill module", (x, 1.34, 1.75), (0.55, 0.55, 0.39), gold, 0.06)
    box("tool skill module slot", (x, 1.05, 1.75), (0.25, 0.02, 0.12), dark, 0.01)
box("tool skill conveyor bed", (3.35, -0.53, 0.56), (2.6, 0.75, 0.26), navy)
for i in range(7):
    box("tool skill conveyor tile", (2.24 + i * 0.37, -0.53, 0.75), (0.31, 0.67, 0.11), steel, 0.02)
box("tool skill module approaching forge", (2.61, -0.53, 0.99), (0.46, 0.48, 0.36), gold, 0.055)

# A completed agent is staged on the departure pad, separate from assembly.
platform("forge departure pad", (3.4, -2.7, 0.36), (2.45, 2.1, 0.21), navy)
ring("forge departure illuminated halo", (3.4, -2.7, 0.5), 0.82, 0.045, glow)
robot("forge finished departure agent", (3.4, -2.7, 0.51), teal, 0.74)
label("READY", (3.4, -3.75, 0.71), 0.24, glow)
for x in (1.64, 2.14, 2.64):
    arrow = box("forge departure path chevron", (x, -3.68, 0.29), (0.21, 0.21, 0.025), gold, 0.015)
    arrow.rotation_euler.z = math.pi / 4
box("forge front identification plaque", (-1.8, -3.57, 0.40), (3.9, 0.72, 0.16), dark)
label("BUILD  /  EQUIP  /  RELEASE", (-1.8, -3.72, 0.65), 0.23, white)

# Billboard lettering must clear its solid backing across the whole text width.
for obj in scene.objects:
    if obj.type == "FONT":
        obj.location += Vector((13, -17, 15)).normalized() * 0.95
