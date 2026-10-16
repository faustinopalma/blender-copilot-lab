platform("Team coordination island", (0, 0, 0.17), (11.5, 8.1, 0.38), navy)
box("Island luminous reveal", (0, 0, 0.37), (11.15, 7.76, 0.07), teal, 0.12)
platform("Inset porcelain deck", (0, 0, 0.47), (10.98, 7.59, 0.16), white)
box("Front navy fascia", (0, -3.96, 0.20), (8.7, 0.10, 0.26), dark, 0.03)
deck_caption = label("HUMAN INTENT  /  SHARED INTELLIGENCE",
                     (0, -3.38, 0.565), 0.22, navy)
deck_caption.rotation_euler = (0, 0, 0)
for x in (-5.05, 5.05):
    for y in (-3.25, 3.25):
        cylinder("Deck titanium fastener", (x, y, 0.565), 0.09, 0.025, navy, 24)
        box("Fastener slot", (x, y, 0.583), (0.10, 0.025, 0.012), gold, 0.003)

# The three stations form a triangle around the shared task.
stations = [
    ("research", (-3.05, 0.95), teal, "01 / RESEARCHER"),
    ("build", (-2.82, -2.05), blue, "02 / BUILDER"),
    ("review", (3.10, -0.70), gold, "03 / REVIEWER"),
]
for name, (x, y), color, title in stations:
    cylinder(name + " raised workstation pad", (x, y, 0.63), 1.10, 0.17, navy)
    ring(name + " pad illuminated rim", (x, y, 0.72), 1.01, 0.037, color)
    cylinder(name + " pad inset", (x, y, 0.725), 0.90, 0.035, dark)
    robot(name + " specialist robot", (x, y, 0.75), color, 1.03)
    box(name + " chest identification", (x, y - 0.281, 1.53),
        (0.34, 0.035, 0.22), white, 0.025)
    chest_number = label(str(stations.index((name, (x, y), color, title)) + 1),
                         (x, y - 0.33, 1.54), 0.15, navy)
    chest_number.rotation_euler = (math.pi / 2, 0, 0)
    box(name + " nameplate plinth", (x, y - 0.86, 0.83),
        (2.15, 0.25, 0.32), navy, 0.045)
    station_caption = label(title, (x, y - 1.025, 0.85), 0.185, color)
    station_caption.rotation_euler = (math.pi / 2, 0, 0)
    line(name + " floor service cable",
         [(x + 0.45, y + 0.45, 0.58),
          (x * 0.70, y + 0.65, 0.59),
          (x * 0.42, y * 0.5, 0.59)], 0.045, navy)

# Researcher's optical sensors and orderly floating document stack.
for x in (-3.25, -2.90):
    lens = ring("research optical sensor rim", (x, 0.58, 2.14), 0.125, 0.023, teal)
    lens.rotation_euler[0] = math.pi / 2
beam("research spectacle bridge", (-3.13, 0.58, 2.14),
     (-3.02, 0.58, 2.14), 0.018, teal)
box("research shoulder satchel", (-3.50, 1.02, 1.50), (0.23, 0.52, 0.52), dark)
for index in range(3):
    x = -4.27 + index * 0.18
    y = 0.44 + index * 0.16
    z = 1.72 + index * 0.26
    box("research document card", (x, y, z), (0.68, 0.055, 0.86), white, 0.045)
    box("research card teal header", (x, y - 0.036, z + 0.26),
        (0.48, 0.014, 0.09), teal, 0.01)
    for row in range(3):
        box("research document text rule", (x - 0.04, y - 0.036, z + 0.08 - row * 0.14),
            (0.39 - row * 0.06, 0.014, 0.025), navy, 0.005)
beam("research card projector stem", (-4.1, 0.75, 0.57),
     (-4.1, 0.75, 1.23), 0.05, teal)
cylinder("research document projector", (-4.1, 0.75, 0.68), 0.26, 0.20, navy)

# Builder: helmet, open-ended wrench, and a compact tool tray.
ball("build cobalt safety helmet", (-2.82, -2.05, 2.44), 0.48,
     blue, (1.05, 0.83, 0.48))
box("build helmet brim", (-2.82, -2.14, 2.40), (1.04, 0.81, 0.085), blue, 0.045)
box("build helmet amber stripe", (-2.82, -2.05, 2.64),
    (0.10, 0.52, 0.035), gold, 0.01)
beam("build wrench handle", (-1.99, -2.18, 1.30),
     (-1.70, -2.18, 2.02), 0.085, white)
ball("build wrench grip", (-1.98, -2.18, 1.32), 0.12, blue)
beam("build wrench left jaw", (-1.70, -2.18, 2.00),
     (-1.87, -2.18, 2.22), 0.085, white)
beam("build wrench right jaw", (-1.70, -2.18, 2.00),
     (-1.45, -2.18, 2.08), 0.085, white)
beam("build wrench left tip", (-1.87, -2.18, 2.22),
     (-1.82, -2.18, 2.40), 0.085, white)
beam("build wrench right tip", (-1.45, -2.18, 2.08),
     (-1.31, -2.18, 2.23), 0.085, white)
box("build toolbox", (-4.35, -2.05, 0.84), (0.90, 0.66, 0.49), blue)
box("build toolbox lid", (-4.35, -2.05, 1.10), (0.97, 0.72, 0.10), navy, 0.035)
line("build toolbox handle", [(-4.59, -2.05, 1.16), (-4.59, -2.05, 1.36),
     (-4.11, -2.05, 1.36), (-4.11, -2.05, 1.16)], 0.045, gold)
for x in (-4.60, -4.10):
    box("build toolbox clasp", (x, -2.40, 1.00), (0.11, 0.035, 0.18), gold, 0.015)

# Reviewer's shield is a real five-sided solid with an inset check mark.
shield_points = [(-0.43, 0.43), (0.43, 0.43), (0.39, -0.10),
                 (0.0, -0.57), (-0.39, -0.10)]
verts = [(4.02 + x, y, 1.83 + z) for y in (-1.16, -1.00)
         for x, z in shield_points]
faces = [(4, 3, 2, 1, 0), (5, 6, 7, 8, 9)]
faces += [(i, (i + 1) % 5, (i + 1) % 5 + 5, i + 5) for i in range(5)]
mesh = bpy.data.meshes.new("review shield solid geometry")
mesh.from_pydata(verts, [], faces)
mesh.update()
shield = bpy.data.objects.new("review approval shield", mesh)
bpy.context.collection.objects.link(shield)
shield.data.materials.append(navy)
line("review shield gold perimeter",
     [(4.02 + x, -1.185, 1.83 + z) for x, z in shield_points + [shield_points[0]]],
     0.038, gold)
line("review shield approval check", [(3.78, -1.22, 1.86), (3.96, -1.22, 1.66),
     (4.29, -1.22, 2.05)], 0.065, glow)
box("review shoulder epaulette", (3.55, -0.70, 1.85), (0.24, 0.58, 0.13), white)
for x in (2.98, 3.10, 3.22):
    ball("review merit badge", (x, -0.984, 1.64), 0.043, gold)
box("review completed task docket", (4.62, -0.38, 0.93), (0.52, 0.70, 0.65), navy)
for z in (0.76, 0.96, 1.16):
    box("review accepted task tab", (4.62, -0.745, z), (0.36, 0.03, 0.09), gold, 0.015)

# Low round table and open holographic crown keep the collaborators visible.
cylinder("Collaboration table foot", (0, 0, 0.64), 1.09, 0.18, navy)
cylinder("Collaboration fluted pedestal", (0, 0, 1.02), 0.67, 0.62, navy)
for angle in range(0, 360, 60):
    a = math.radians(angle)
    box("Pedestal luminous flute", (0.66 * math.cos(a), 0.66 * math.sin(a), 1.02),
        (0.07, 0.07, 0.42), teal, 0.02)
cylinder("Collaboration circular table", (0, 0, 1.40), 1.88, 0.22, navy)
cylinder("Holographic dark tabletop", (0, 0, 1.525), 1.77, 0.04, dark)
ring("Table cyan outer light", (0, 0, 1.55), 1.80, 0.035, glow)
ring("Table inner violet circuit", (0, 0, 1.56), 1.24, 0.022, violet)
ring("Crystal projection target", (0, 0, 1.56), 0.69, 0.025, teal)
cylinder("Shared task crystal emitter", (0, 0, 1.63), 0.42, 0.17, navy, 6)
ring("Shared task crystal emitter light", (0, 0, 1.73), 0.39, 0.035, gold)
cone("Shared central task crystal lower facets", (0, 0, 2.04),
     0.05, 0.44, 0.56, violet, 6)
cone("Shared central task crystal upper facets", (0, 0, 2.60),
     0.44, 0.0, 0.56, teal, 6)
ring("Task crystal orbit", (0, 0, 2.31), 0.66, 0.021, glow)
for a in (0, 2.094, 4.189):
    ball("Shared task orbit datum", (0.66 * math.cos(a), 0.66 * math.sin(a), 2.31),
         0.07, gold)
label("SHARED TASK", (0, -0.90, 1.84), 0.235, white)
label("SYNC / 03", (0, -1.50, 1.65), 0.17, glow)

# Handoffs use luminous, continuous routes and tangible arrowheads.
routes = [
    ("research to build handoff", [(-2.64, 0.33, 1.60), (-2.10, -0.25, 1.85),
      (-1.88, -0.98, 1.75), (-2.20, -1.45, 1.56)], teal),
    ("build to review handoff", [(-1.84, -2.35, 1.25), (-0.95, -2.65, 1.19),
      (0.65, -2.61, 1.19), (2.34, -1.55, 1.37)], blue),
    ("review to research handoff", [(2.76, 0.04, 1.62), (1.87, 1.42, 1.85),
      (0.0, 1.90, 1.86), (-2.26, 1.40, 1.67)], gold),
]
for name, points, color in routes:
    line(name + " dark cable sheath", points, 0.064, navy)
    raised = [(x, y, z + 0.08) for x, y, z in points]
    line(name + " luminous transfer path", raised, 0.031, color)
    start, end = Vector(raised[-2]), Vector(raised[-1])
    arrow = cone(name + " direction arrow", end, 0.13, 0, 0.31, color, 12)
    arrow.rotation_euler = (end - start).to_track_quat("Z", "Y").to_euler()
    ball(name + " transfer packet", raised[1], 0.10, glow)

# Backdrop: a compact command console, not a second competing focal point.
for x in (-4.76, 4.76):
    box("Backdrop console structural tower", (x, 2.94, 2.19), (0.42, 0.65, 3.28), navy)
    box("Backdrop console illuminated edge", (x, 2.59, 2.30),
        (0.075, 0.03, 2.60), teal, 0.02)
    cylinder("Backdrop tower foundation", (x, 2.94, 0.64), 0.42, 0.18, navy)
box("Backdrop console lintel", (0, 2.94, 3.88), (9.95, 0.66, 0.32), navy)
box("Backdrop console amber cap", (0, 2.60, 3.91), (8.65, 0.025, 0.045), gold, 0.01)
box("Team orchestration display housing", (0.30, 2.97, 2.83),
    (4.88, 0.24, 1.55), navy)
box("Team orchestration display glass", (0.30, 2.83, 2.83),
    (4.55, 0.035, 1.27), dark, 0.045)
console_heading = label("TEAM / ONLINE", (0.30, 2.69, 3.18), 0.30, glow)
console_heading.rotation_euler = (math.pi / 2, 0, 0)
console_workflow = label("PLAN   >   BUILD   >   VERIFY",
                         (0.30, 2.61, 2.73), 0.205, white)
console_workflow.rotation_euler = (math.pi / 2, 0, 0)
for index, color in enumerate((teal, blue, gold)):
    x = -1.18 + index * 1.47
    box("Console phase completed bar", (x, 2.79, 2.40), (1.15, 0.025, 0.08), color, 0.02)
    ball("Console phase heartbeat", (x + 0.48, 2.77, 2.55), 0.045, glow)
box("Backdrop control desk", (2.10, 2.42, 1.13), (2.55, 0.95, 0.23), navy)
for x in (1.18, 3.02):
    box("Console desk support", (x, 2.64, 0.84), (0.15, 0.33, 0.56), navy)
for index in range(5):
    box("Console touch key", (1.30 + index * 0.34, 2.25, 1.267),
        (0.23, 0.27, 0.028), teal if index < 3 else gold, 0.025)
line("Console protected floor trunk", [(2.8, 2.68, 0.58), (3.9, 2.5, 0.59),
     (4.2, 1.2, 0.59), (3.8, 0.0, 0.59)], 0.055, navy)
