# A shared OneLake civic basin ties three different data neighborhoods together.
platform("Data city floating foundation", (0, 0, 0), (12, 9, 0.55), navy)
box("Porcelain city surface", (0, 0, 0.31), (11.65, 8.65, 0.18), white, 0.18)
box("Foundation teal reveal", (0, -4.49, -0.04), (10.8, 0.035, 0.075), glow, 0.02)
for x in (-5.35, 5.35):
    box("Foundation gold corner", (x, -4.5, 0.05), (0.33, 0.055, 0.22), gold, 0.03)

box("Front data avenue", (0, -3.25, 0.425), (11.15, 0.85, 0.045), navy, 0.15)
box("East district lane", (5.15, 0.25, 0.425), (0.65, 6.7, 0.045), navy, 0.12)
for x in range(-5, 6):
    box("Avenue lane marking", (x, -3.25, 0.455), (0.40, 0.035, 0.012), gold, 0.008)
for y in (-2, -1, 0, 1, 2, 3):
    box("East lane marking", (5.15, y, 0.455), (0.035, 0.35, 0.012), white, 0.008)

cylinder("Lake sculpted outer retaining wall", (0, -0.55, 0.50), 2.18, 0.23, navy, 96)
cylinder("Lake white promenade", (0, -0.55, 0.63), 2.09, 0.10, white, 96)
cylinder("Shared luminous teal lake", (0, -0.55, 0.70), 1.92, 0.08, teal, 96)
ring("Lake illuminated waterline", (0, -0.55, 0.75), 1.92, 0.035, glow)
for radius in (0.65, 1.11, 1.56):
    ring("Lake concentric data ripples", (0, -0.55, 0.747), radius, 0.013, glow)
cylinder("Lake central data island", (0, -0.55, 0.81), 0.48, 0.16, navy)
box("Lake shared data core", (0, -0.55, 1.13), (0.56, 0.56, 0.56), glow, 0.10)
ring("Lake core orbit", (0, -0.55, 1.50), 0.42, 0.026, gold)
label("ONE LAKE", (0, -1.72, 0.99), 0.33, navy)

platform("Ingest district plinth", (-4.0, -0.35, 0.56), (2.75, 3.65, 0.28), navy)
box("Ingest district inset", (-4, -0.35, 0.715), (2.55, 3.42, 0.045), blue, 0.12)
platform("Process district plinth", (-1.15, 2.86, 0.56), (4.25, 2.25, 0.28), navy)
box("Process district inset", (-1.15, 2.86, 0.715), (4.02, 2.02, 0.045), violet, 0.12)
platform("Analyze district plinth", (3.6, 1.15, 0.56), (2.65, 3.70, 0.28), navy)
box("Analyze district inset", (3.6, 1.15, 0.715), (2.43, 3.47, 0.045), teal, 0.12)

# Elevated pedestrian bridges carry bright, visible data conduits.
for name, start, end, accent in [
    ("Ingest", (-2.68, -0.55, 0.88), (-1.76, -0.55, 0.88), blue),
    ("Process", (-0.58, 1.18, 0.88), (-0.58, 1.94, 0.88), violet),
    ("Analyze", (1.75, 0.12, 0.88), (2.50, 0.12, 0.88), teal),
]:
    a, b = Vector(start), Vector(end)
    direction = b - a
    side = Vector((-direction.y, direction.x, 0)).normalized()
    bridge = box(name + " lake bridge deck", (a + b) / 2, (direction.length + 0.15, 0.64, 0.14), white, 0.035)
    bridge.rotation_euler.z = math.atan2(direction.y, direction.x)
    for sign in (-1, 1):
        offset = side * (sign * 0.27)
        beam(name + " bridge handrail", a + offset + Vector((0, 0, 0.28)),
             b + offset + Vector((0, 0, 0.28)), 0.026, gold)
        for p in (a, b):
            beam(name + " bridge post", p + offset, p + offset + Vector((0, 0, 0.28)), 0.022, navy)
    line(name + " glowing data stream", [a + Vector((0, 0, 0.10)), (a + b) / 2 + Vector((0, 0, 0.10)),
                                       b + Vector((0, 0, 0.10))], 0.045, glow)
    ball(name + " data packet", (a + b) / 2 + Vector((0, 0, 0.14)), 0.095, accent)

# Ingestion: a pipeline portal, receiving bins, and compact server buildings.
server("Ingest blue server tower", (-4.65, 0.68, 0.75), blue, 2.60)
server("Ingest white server tower", (-3.45, 0.68, 0.75), white, 1.95)
for x in (-4.75, -3.25):
    box("Ingest pipeline gateway pillar", (x, -1.10, 1.60), (0.22, 0.42, 1.70), white, 0.06)
box("Ingest pipeline gateway lintel", (-4, -1.10, 2.44), (1.75, 0.46, 0.27), blue, 0.07)
beam("Ingest gateway illuminated header", (-4.65, -1.35, 2.46), (-3.35, -1.35, 2.46), 0.045, glow)
box("Ingest parcel conveyor", (-4, -1.14, 0.95), (1.85, 0.75, 0.22), dark, 0.07)
for x in (-4.55, -4.0, -3.45):
    box("Ingest incoming data cube", (x, -1.14, 1.28), (0.35, 0.35, 0.40), gold, 0.035)
line("Ingest feed pipe", [(-3.2, -1.10, 1.0), (-2.87, -1.05, 1.0), (-2.85, -0.55, 0.99),
                        (-2.60, -0.55, 0.99)], 0.07, glow)

# Processing: a stepped civic compute tower with cooling halo and rooftop cores.
box("Process compute lower volume", (-1.45, 2.90, 1.45), (2.22, 1.45, 1.42), white, 0.15)
box("Process compute upper volume", (-1.62, 3.02, 2.65), (1.64, 1.20, 1.08), navy, 0.12)
box("Process compute crown", (-1.62, 3.02, 3.27), (1.87, 1.38, 0.17), violet, 0.09)
for z in (1.08, 1.46, 1.84):
    box("Process horizontal facade window", (-1.45, 2.159, z), (1.83, 0.045, 0.17), dark, 0.025)
    box("Process window signal", (-0.73, 2.126, z), (0.25, 0.025, 0.07), glow, 0.015)
for x in (-2.13, -1.62, -1.11):
    box("Process upper teal fins", (x, 2.399, 2.66), (0.12, 0.05, 0.73), teal, 0.02)
cylinder("Process rooftop spindle", (-1.62, 3.02, 3.60), 0.25, 0.52, gold)
ring("Process floating cooling halo", (-1.62, 3.02, 3.91), 0.74, 0.065, glow)
ball("Process compute nucleus", (-1.62, 3.02, 3.91), 0.27, violet)
for z in (0.95, 1.35, 1.75):
    box("Process adjacent accelerator", (0.18, 3.03, z), (0.62, 0.87, 0.28), violet, 0.06)
    box("Process accelerator strip", (0.18, 2.58, z), (0.40, 0.025, 0.055), glow, 0.01)
line("Process lake uplink", [(-0.58, 1.93, 0.99), (-0.58, 2.23, 0.99), (-0.9, 2.35, 0.99)], 0.05, glow)

# Analytics: an architectural dashboard with a genuine miniature chart.
for x in (2.86, 4.28):
    box("Analyze billboard support", (x, 2.05, 1.35), (0.17, 0.24, 1.20), gold, 0.03)
box("Analyze dashboard frame", (3.57, 2.07, 2.64), (2.20, 0.24, 1.65), white, 0.12)
box("Analyze dashboard dark display", (3.57, 1.931, 2.64), (1.96, 0.045, 1.40), dark, 0.06)
chart_label = label("LIVE INSIGHTS", (3.57, 1.894, 3.13), 0.18, white)
chart_label.rotation_euler = (math.pi / 2, 0, 0)
for i, h in enumerate((0.30, 0.46, 0.40, 0.68, 0.86)):
    box("Analyze dashboard bar", (2.89 + i * 0.31, 1.889, 2.15 + h / 2),
        (0.17, 0.035, h), teal if i < 4 else gold, 0.018)
line("Analyze dashboard trend", [(2.84, 1.855, 2.64), (3.16, 1.855, 2.82), (3.47, 1.855, 2.72),
                                (3.79, 1.855, 2.98), (4.12, 1.855, 3.00)], 0.021, glow)
box("Analyze low pavilion", (3.70, 0.30, 1.11), (1.65, 1.22, 0.73), white, 0.10)
box("Analyze pavilion glass frontage", (3.70, -0.323, 1.13), (1.37, 0.04, 0.43), dark, 0.04)
box("Analyze pavilion teal roof", (3.70, 0.30, 1.52), (1.90, 1.42, 0.14), teal, 0.07)
for x in (3.22, 3.70, 4.18):
    box("Analyze window mullion", (x, -0.35, 1.13), (0.045, 0.025, 0.45), gold, 0.008)
line("Analyze lake uplink", [(2.49, 0.12, 0.99), (2.73, 0.12, 0.99), (2.85, 0.30, 0.99)], 0.05, glow)

for text, pos, color in [
    ("INGEST", (-4.0, -2.25, 1.04), blue),
    ("PROCESS", (-1.50, 1.38, 1.28), violet),
    ("ANALYZE", (3.70, -1.12, 1.03), teal),
]:
    box(text + " wayfinding pedestal", (pos[0], pos[1], 0.68), (2.20, 0.40, 0.35), navy, 0.06)
    beam(text + " sign support", (pos[0], pos[1], 0.81), pos, 0.045, gold)
    backing = box(text + " navy wayfinding sign", Vector(pos) - camera.rotation_euler.to_matrix() @ Vector((0, 0, 0.055)),
                  (2.14, 0.46, 0.07), navy, 0.04)
    backing.rotation_euler = camera.rotation_euler
    label(text, pos, 0.34, white)
    box(text + " district color key", (pos[0], pos[1] - 0.22, 0.70), (1.85, 0.035, 0.055), color, 0.01)

for i, (x, y) in enumerate([(-5.25, 2.60), (-4.05, 3.40), (1.30, 3.53), (4.35, -2.35), (-2.45, -2.50), (1.70, -2.62)]):
    cylinder("Tree planter " + str(i), (x, y, 0.52), 0.30, 0.22, navy)
    cylinder("Tree trunk " + str(i), (x, y, 0.91), 0.062, 0.61, gold, 16)
    ball("Tree sculpted canopy " + str(i), (x, y, 1.37), 0.38, teal, (0.85, 0.85, 1.17))
    ball("Tree canopy crown " + str(i), (x + 0.12, y, 1.61), 0.25, teal)

for i, (x, y) in enumerate([(-4.9, -2.65), (-4.46, -2.65), (2.75, -2.40), (3.20, -2.40)]):
    box("Data cube delivery parcel " + str(i), (x, y, 0.67), (0.32, 0.32, 0.46), gold if i < 2 else coral, 0.035)
    box("Data cube parcel seal " + str(i), (x, y - 0.17, 0.69), (0.06, 0.018, 0.29), white, 0.01)

box("Autonomous data shuttle", (0.8, -3.27, 0.66), (0.92, 0.47, 0.36), teal, 0.14)
box("Shuttle dark canopy", (0.8, -3.27, 0.91), (0.50, 0.38, 0.22), dark, 0.08)
for x in (0.46, 1.14):
    for y in (-3.50, -3.04):
        ball("Shuttle wheel", (x, y, 0.57), 0.105, navy, (1, 0.60, 1))
for x, y in [(-5.45, -2.4), (5.42, -2.45), (5.42, 3.45)]:
    beam("City promenade lamp mast", (x, y, 0.44), (x, y, 1.58), 0.035, navy)
    ring("Promenade lamp shade", (x, y, 1.61), 0.18, 0.035, gold)
    ball("Promenade lamp light", (x, y, 1.61), 0.11, glow)
