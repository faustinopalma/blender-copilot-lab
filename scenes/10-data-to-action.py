bronze = mat("Fabric bronze tier", (0.48, 0.23, 0.10), metal=0.65)
silver = mat("Fabric silver tier", (0.53, 0.67, 0.76), metal=0.75)

# One continuous exhibit deck ties the three distinct disciplines together.
platform("Data to action exhibition plinth", (0, 0, 0), (12.2, 7.0, 0.42), navy)
box("Exhibition porcelain reveal", (0, 0, 0.23), (12.0, 6.8, 0.10), white)
platform("Exhibition inset deck", (0, 0, 0.34), (11.8, 6.6, 0.16), dark)
for x, zone, color, number in [
    (-4, "fabric", teal, "01"), (0, "foundry", violet, "02"),
    (4, "azure", blue, "03"),
]:
    platform(zone + " colored island", (x, 0.10, 0.49), (3.65, 5.50, 0.22), color)
    platform(zone + " inset work surface", (x, 0.10, 0.62), (3.45, 5.30, 0.10), navy)
    box(zone + " front label rail", (x, -2.76, 0.56), (3.5, 0.25, 0.23), color)
    label(zone.upper(), (x, -2.94, 0.99), 0.30, white)
    label({"fabric": "PREPARE", "foundry": "REASON", "azure": "DELIVER"}[zone],
          (x, -3.03, 0.65), 0.18, ink)
    cylinder(zone + " stage index medallion", (x - 1.38, -2.18, 0.73), 0.22, 0.10, color)
    label(number, (x - 1.38, -2.25, 0.89), 0.15, white)
    for y in (-0.8, 0.0, 0.8, 1.6):
        box(zone + " peripheral deck marker", (x + 1.55, y, 0.69),
            (0.06, 0.23, 0.025), color, 0.01)

# Fabric: a literal data lake, fed by a compact ingestion rack.
cylinder("fabric lake retaining vessel", (-4.0, 0.93, 0.78), 1.36, 0.23, teal)
cylinder("fabric dark liquid data lake", (-4.0, 0.93, 0.91), 1.25, 0.07, dark)
for radius in (0.55, 0.88, 1.19):
    ring("fabric concentric lake signal", (-4.0, 0.93, 0.96), radius, 0.023, glow)
for i in range(6):
    angle = i * math.tau / 6
    x, y = -4.0 + 0.87 * math.cos(angle), 0.93 + 0.87 * math.sin(angle)
    record = box("fabric floating source record", (x, y, 1.06), (0.32, 0.25, 0.10), teal, 0.035)
    record.rotation_euler.z = angle
    box("fabric record bright header", (x, y, 1.12), (0.18, 0.06, 0.015), white, 0.01)
cylinder("fabric lake catalog hub", (-4.0, 0.93, 1.02), 0.28, 0.16, white)
box("fabric catalog crystal", (-4.0, 0.93, 1.25), (0.30, 0.30, 0.30), glow, 0.035)
server("fabric ingestion rack", (-5.15, 2.02, 0.68), teal, height=1.85)
line("fabric ingestion feed", [(-5.15, 1.65, 1.0), (-5.0, 1.2, 1.08),
                              (-4.7, 1.12, 1.04)], 0.035, glow)
label("ONELAKE", (-4.05, 0.37, 1.40), 0.19, white)
for i, (tier, material) in enumerate([("BRONZE", bronze), ("SILVER", silver), ("GOLD", gold)]):
    x, top = -5.05 + i * 1.02, 0.94 + i * 0.28
    box("fabric " + tier.lower() + " refinement step",
        (x, -0.77, (0.67 + top) / 2), (0.93, 1.06, top - 0.67), material)
    for layer in range(3):
        cylinder("fabric " + tier.lower() + " refined database wafer",
                 (x, -0.72, top + 0.075 + layer * 0.13), 0.29, 0.10, material)
    ring("fabric " + tier.lower() + " wafer rim", (x, -0.72, top + 0.38), 0.25, 0.018, glow)
    label(tier, (x, -1.27, top + 0.13), 0.135, white)
for i in range(2):
    beam("fabric refinement transition", (-4.64 + i * 1.02, -0.76, 1.12 + i * 0.28),
         (-4.44 + i * 1.02, -0.76, 1.29 + i * 0.28), 0.035, glow)

# Foundry: a small agent at its workbench, surrounded by grounded knowledge.
cylinder("foundry agent turntable", (0, 0.28, 0.76), 1.12, 0.18, violet)
ring("foundry turntable illuminated perimeter", (0, 0.28, 0.87), 1.04, 0.045, glow)
cylinder("foundry turntable top", (0, 0.28, 0.88), 0.94, 0.06, dark)
robot("foundry reasoning agent", (0, 0.12, 0.93), violet, scale=1.12)
for x in (-1.35, 1.35):
    box("foundry knowledge gantry foot", (x, 1.27, 0.78), (0.33, 0.58, 0.22), violet)
    beam("foundry knowledge gantry upright", (x, 1.27, 0.86), (x, 1.27, 3.11), 0.065, silver)
halo = ring("foundry knowledge halo outer frame", (0, 1.28, 2.33), 1.39, 0.085, violet)
halo.rotation_euler.x = math.pi / 2
halo = ring("foundry knowledge halo luminous inner rim", (0, 1.20, 2.33), 1.26, 0.025, glow)
halo.rotation_euler.x = math.pi / 2
for i, (x, z) in enumerate([(-0.90, 2.29), (0, 3.13), (0.94, 2.39)]):
    box("foundry grounded knowledge card frame", (x, 1.01, z), (0.71, 0.15, 0.91), white, 0.055)
    box("foundry knowledge card face", (x, 0.922, z), (0.62, 0.035, 0.79), dark, 0.025)
    box("foundry knowledge card heading", (x - 0.06, 0.894, z + 0.24),
        (0.36, 0.022, 0.07), violet, 0.01)
    for row in range(3):
        box("foundry knowledge card evidence row", (x - 0.03, 0.892, z + 0.07 - row * 0.14),
            (0.43 - row * 0.06, 0.024, 0.035), teal if row == 2 else silver, 0.01)
box("foundry agent workbench top", (0, -0.98, 1.25), (2.65, 0.63, 0.16), white)
for x in (-1.06, 1.06):
    box("foundry workbench support", (x, -0.98, 0.94), (0.13, 0.46, 0.47), violet, 0.035)
box("foundry workbench task pad", (-0.58, -1.0, 1.35), (0.63, 0.39, 0.05), dark, 0.03)
for i in range(3):
    box("foundry workbench task token", (-0.78 + i * 0.20, -1.0, 1.40),
        (0.12, 0.20, 0.05), teal if i < 2 else gold, 0.02)
cylinder("foundry tool receptacle", (0.92, -0.97, 1.44), 0.14, 0.22, violet)
for offset in (-0.06, 0.06):
    beam("foundry precision stylus", (0.92 + offset, -0.97, 1.48),
         (0.96 + offset, -0.97, 1.80), 0.022, gold)
label("GROUNDED AGENT", (0, 1.12, 3.96), 0.21, white)

# Azure: an open application pavilion with a live dashboard and user kiosk.
for x in (2.55, 5.42):
    for y in (-0.36, 2.10):
        box("azure pavilion column shoe", (x, y, 0.76), (0.31, 0.31, 0.18), blue)
        box("azure pavilion porcelain column", (x, y, 2.14), (0.12, 0.12, 2.68), white, 0.035)
platform("azure pavilion rear canopy lintel", (3.99, 2.10, 3.56), (3.30, 0.48, 0.20), white)
box("azure pavilion blue rear roof fascia", (3.99, 2.10, 3.70), (3.25, 0.43, 0.13), blue)
for x in (2.55, 5.42):
    box("azure pavilion open roof side beam", (x, 0.87, 3.56), (0.18, 2.95, 0.20), white)
box("azure pavilion front roof lintel", (3.99, -0.48, 3.56), (3.30, 0.18, 0.20), blue)
box("azure pavilion front luminous soffit", (3.99, -0.48, 3.44), (2.85, 0.07, 0.04), glow, 0.015)
label("APP SERVICE", (4.02, -0.65, 3.76), 0.20, white)
box("azure dashboard suspension", (3.98, 1.76, 3.12), (0.15, 0.15, 0.65), silver, 0.03)
box("azure application screen porcelain frame", (3.98, 1.64, 2.44), (2.55, 0.22, 1.76), white)
box("azure application large dashboard screen", (3.98, 1.508, 2.44), (2.36, 0.05, 1.56), dark, 0.04)
label("ACTION READY", (3.92, 1.28, 3.02), 0.16, white)
for i, h in enumerate((0.25, 0.43, 0.64, 0.90)):
    box("azure dashboard rising delivery bar", (3.26 + i * 0.38, 1.466, 2.06 + h / 2),
        (0.21, 0.026, h), teal if i < 3 else blue, 0.025)
line("azure dashboard success graph", [(3.12, 1.414, 2.27), (3.59, 1.414, 2.45),
                                     (4.03, 1.414, 2.37), (4.64, 1.414, 2.90)], 0.025, gold)
for x, z in [(3.12, 2.27), (3.59, 2.45), (4.03, 2.37), (4.64, 2.90)]:
    ball("azure dashboard graph event", (x, 1.405, z), 0.055, gold)
box("azure user terminal foot", (4.50, -0.85, 0.76), (0.78, 0.64, 0.17), blue)
box("azure user terminal pedestal", (4.50, -0.75, 1.15), (0.29, 0.34, 0.67), white)
terminal = box("azure user terminal angled console", (4.50, -0.86, 1.61),
               (0.95, 0.66, 0.14), blue)
terminal.rotation_euler.x = math.radians(18)
terminal = box("azure user terminal touch glass", (4.50, -0.89, 1.70),
               (0.78, 0.49, 0.035), dark, 0.025)
terminal.rotation_euler.x = math.radians(18)
for i in range(3):
    box("azure terminal touch tile", (4.27 + i * 0.23, -0.96, 1.71),
        (0.15, 0.13, 0.035), glow if i == 2 else blue, 0.02)
for x in (3.36, 3.63):
    box("azure app user shoe", (x, -0.94, 0.75), (0.19, 0.36, 0.14), dark, 0.04)
    beam("azure app user leg", (x, -0.87, 0.80), (x, -0.85, 1.12), 0.07, navy)
cone("azure app user jacket", (3.50, -0.85, 1.34), 0.23, 0.28, 0.53, coral, vertices=32)
ball("azure app user head", (3.50, -0.85, 1.88), 0.20, white)
beam("azure app user reaching arm", (3.72, -0.85, 1.52), (4.15, -0.95, 1.67), 0.07, coral)
ball("azure app user hand", (4.15, -0.95, 1.67), 0.08, white)
beam("azure app user resting arm", (3.29, -0.85, 1.51), (3.21, -0.96, 1.18), 0.07, coral)

# The physical signal stays unobstructed at the front of every station.
route = [(-4.48, 0.53, 1.00), (-5.42, -0.10, 0.83),
         (-5.35, -1.78, 0.79), (-3.2, -1.93, 0.79),
         (-1.65, -1.93, 0.79), (0, -1.93, 0.79), (1.75, -1.93, 0.79),
         (3.50, -1.93, 0.79), (5.13, -1.63, 0.79), (5.17, 0.12, 0.86),
         (4.75, 0.53, 1.02)]
line("impulse continuous dark guide channel", route, 0.135, dark)
line("impulse continuous glowing data route", [(x, y, z + 0.14) for x, y, z in route], 0.057, glow)
for i in range(10):
    x = -4.75 + i * 0.95
    packet = box("impulse physical data packet", (x, -1.94, 0.93),
                 (0.22, 0.22, 0.22), gold if i in (2, 5, 8) else white, 0.035)
    packet.rotation_euler = (0, math.pi / 4, math.pi / 4)
for x in (-2.0, 2.0):
    box("impulse bridge support", (x, -1.93, 0.60), (0.40, 0.42, 0.24), silver, 0.04)
    for dx in (-0.13, 0.13):
        box("impulse bridge guide light", (x + dx, -1.93, 0.74),
            (0.035, 0.35, 0.04), glow, 0.01)
for x in (-3.30, 0.12, 3.50):
    arrow = cone("impulse forward direction arrow", (x, -1.94, 0.98),
                 0.16, 0, 0.31, teal, vertices=3)
    arrow.rotation_euler.y = math.pi / 2
label("DATA", (-2.03, -0.83, 1.17), 0.17, teal)
label("DECISIONS", (1.98, -0.89, 1.26), 0.16, gold)
