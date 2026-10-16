def factory_sign(body, pos, width, size):
    panel = box("factory sign " + body, pos, (width, 0.43, 0.08), navy, 0.045)
    panel.rotation_euler = camera.rotation_euler
    outward = camera.rotation_euler.to_quaternion() @ Vector((0, 0, 0.055))
    label(body, Vector(pos) + outward, size, white)


platform("factory island foundation", (0, 0, 0), (12, 9, 0.42), navy)
box("factory inset concrete apron", (0, 0, 0.25), (11.6, 8.6, 0.14), white)
box("factory production floor", (-0.4, -1.45, 0.36), (10.8, 3.05, 0.12), dark)
box("factory front safety stripe", (-0.4, -3.03, 0.43), (10.8, 0.09, 0.035), gold)
box("factory hall foundation", (-0.7, 2.02, 0.55), (8.6, 3.0, 0.5), navy)
box("factory processing hall", (-0.7, 2.02, 1.94), (8.25, 2.75, 2.55), blue)
box("factory front porcelain fascia", (-0.7, 0.61, 2.85), (8.35, 0.12, 0.3), white)
box("factory hall lower sill", (-0.7, 0.59, 1.09), (8.35, 0.16, 0.2), navy)

# Repeated steep clerestories and sloped sheets make the sawtooth silhouette.
for tooth in range(4):
    left = -4.9 + tooth * 2.1
    roof = box("factory sawtooth sloped roof", (left + 1.05, 2.02, 3.79),
               (2.27, 3.0, 0.13), white, 0.035)
    roof.rotation_euler[1] = -math.atan2(0.82, 2.1)
    box("factory sawtooth clerestory glass", (left + 2.1, 2.02, 3.75),
        (0.075, 2.74, 0.78), dark, 0.02)
    box("factory sawtooth golden ridge", (left + 2.1, 2.02, 4.22),
        (0.11, 3.02, 0.09), gold, 0.025)
    for yy in (1.13, 2.02, 2.91):
        box("factory clerestory luminous pane", (left + 2.145, yy, 3.8),
            (0.025, 0.68, 0.43), teal, 0.015)

for x in (-4.25, -3.25, -2.25, -1.25, -0.25, 0.75, 1.75, 2.75):
    box("factory facade recessed window", (x, 0.62, 2.06), (0.78, 0.075, 1.1), dark, 0.03)
    box("factory facade window mullion", (x, 0.56, 2.06), (0.045, 0.06, 1.12), teal, 0.01)
box("factory side service door", (3.46, 2.0, 1.55), (0.06, 1.12, 1.8), navy, 0.03)
for yy in (1.62, 1.9, 2.18, 2.46):
    box("factory side door louver", (3.51, yy, 1.62), (0.04, 0.12, 1.35), white, 0.01)

box("conveyor continuous graphite belt", (-0.45, -1.43, 1.0), (10.05, 1.02, 0.17), dark)
for yy in (-2.02, -0.84):
    box("conveyor blue structural channel", (-0.45, yy, 0.91), (10.25, 0.14, 0.36), blue, 0.035)
    box("conveyor polished edge rail", (-0.45, yy, 1.15), (10.25, 0.065, 0.07), white, 0.02)
for x in (-5.15, -4.35, -3.55, -2.75, -1.95, -1.15, -0.35, 0.45, 1.25, 2.05, 2.85, 3.65, 4.45):
    beam("conveyor exposed transverse roller", (x, -1.94, 1.095), (x, -0.92, 1.095), 0.055, navy)
for x in (-4.8, -2.8, -0.8, 1.2, 3.8):
    for yy in (-1.89, -0.97):
        box("conveyor anchored support", (x, yy, 0.66), (0.18, 0.18, 0.65), navy, 0.025)

for i, x in enumerate((-4.75, -3.7, -2.75)):
    parcel = box("conveyor raw coral parcel", (x, -1.43, 1.43), (0.58, 0.63, 0.58), coral, 0.075)
    parcel.rotation_euler[2] = (-0.10, 0.13, -0.07)[i]
    box("raw parcel gold data seal", (x, -1.43, 1.731), (0.18, 0.5, 0.025), gold, 0.012)
for x in (-0.57, 0.34):
    box("station intermediate amber parcel", (x, -1.43, 1.36), (0.47, 0.57, 0.43), gold, 0.04)
for x in (2.54, 3.39, 4.25):
    box("conveyor finished teal data cube", (x, -1.43, 1.4), (0.56, 0.56, 0.56), teal, 0.055)
    box("finished cube porcelain seal", (x, -1.724, 1.4), (0.25, 0.02, 0.11), white, 0.015)

for yy in (-2.25, -0.61):
    box("factory ingest gate column", (-5.03, yy, 1.54), (0.19, 0.22, 2.2), coral)
box("factory ingest gate crosshead", (-5.03, -1.43, 2.6), (0.34, 1.9, 0.24), coral)
box("factory ingest scan strip", (-5.03, -1.43, 2.44), (0.22, 1.22, 0.06), glow, 0.015)
beam("ingest station sign bracket", (-5.03, -2.25, 2.6), (-4.93, -2.35, 2.98), 0.045, gold)
factory_sign("INGEST", (-4.93, -2.35, 3.03), 1.63, 0.26)

for xx, color, station_name in ((-1.6, violet, "transform station"), (1.48, teal, "deliver station")):
    for yy in (-2.26, -0.60):
        box(station_name + " bolted foot", (xx, yy, 0.49), (0.85, 0.48, 0.18), navy)
        box(station_name + " upright", (xx, yy, 1.55), (0.47, 0.32, 2.12), color)
        box(station_name + " front luminous indicator", (xx, yy - 0.18, 1.9),
            (0.23, 0.03, 0.5), glow, 0.025)
    box(station_name + " overhead machine housing", (xx, -1.43, 2.63), (0.86, 2.13, 0.42), color)
    box(station_name + " overhead white crown", (xx, -1.43, 2.89), (0.95, 2.22, 0.13), white, 0.04)
    box(station_name + " operator console", (xx + 0.47, -2.37, 1.27), (0.4, 0.28, 0.69), navy, 0.04)
    box(station_name + " operator screen", (xx + 0.47, -2.525, 1.43), (0.28, 0.025, 0.23), glow, 0.02)
    ball(station_name + " amber control", (xx + 0.47, -2.54, 1.12), 0.06, gold)

for xx in (-1.6, 1.48):
    beam("station sign support bracket", (xx, -2.26, 2.63), (xx, -2.65, 3.05), 0.045, gold)
factory_sign("TRANSFORM", (-1.6, -2.65, 3.1), 2.3, 0.25)
factory_sign("DELIVER", (1.48, -2.65, 3.1), 1.85, 0.26)
cone("transform station descending spindle", (-1.6, -1.43, 2.18), 0.12, 0.32, 0.48, gold, 32)
ring("transform station energy collar", (-1.6, -1.43, 2.27), 0.3, 0.07, glow)
for yy in (-1.83, -1.43, -1.03):
    box("deliver station precision scanning head", (1.48, yy, 2.31), (0.62, 0.16, 0.2), dark, 0.025)
    box("deliver station glowing scanner", (1.48, yy, 2.19), (0.46, 0.09, 0.035), glow, 0.01)

# Pipes terminate in the hall and machine crowns rather than floating.
line("factory thick violet process pipe",
     [(-2.45, 0.77, 3.07), (-2.45, 0.12, 3.45), (-2.05, -0.31, 3.48),
      (-1.6, -0.57, 3.26), (-1.6, -0.67, 2.89)], 0.17, violet)
line("factory glowing teal curved pipe",
     [(2.66, 0.75, 3.06), (2.66, 0.05, 3.58), (2.2, -0.34, 3.63),
      (1.48, -0.52, 3.32), (1.48, -0.62, 2.89)], 0.155, glow)
line("factory cooling return pipe",
     [(3.35, 2.8, 2.7), (4.15, 2.8, 2.7), (4.65, 2.72, 2.2),
      (4.65, 2.35, 1.14)], 0.15, teal)
for xx in (-2.45, 2.66):
    connector = ring("pipe wall flange", (xx, 0.57, 3.07), 0.245, 0.065, gold)
    connector.rotation_euler[0] = math.pi / 2
for xx, yy, zz in ((-1.6, -0.67, 2.98), (1.48, -0.62, 2.98)):
    ring("pipe machine flange", (xx, yy, zz), 0.23, 0.055, gold)

for yy in (0.88, 2.28):
    cylinder("factory cooling fan drum", (4.65, yy, 0.91), 0.62, 0.9, navy)
    ring("factory cooling fan rim", (4.65, yy, 1.39), 0.54, 0.07, white)
    cylinder("factory cooling fan dark well", (4.65, yy, 1.375), 0.49, 0.04, dark)
    for angle in (0, math.pi / 2, math.pi, 3 * math.pi / 2):
        blade = box("factory cooling fan blade",
                    (4.65 + math.cos(angle) * 0.245, yy + math.sin(angle) * 0.245, 1.42),
                    (0.4, 0.15, 0.055), teal, 0.04)
        blade.rotation_euler[2] = angle + 0.25
    cylinder("factory cooling fan gold hub", (4.65, yy, 1.46), 0.11, 0.12, gold)

box("delivery storage pallet", (4.35, -3.15, 0.49), (2.05, 1.3, 0.2), gold, 0.04)
for xx in (3.76, 4.36, 4.96):
    for yy in (-3.44, -2.85):
        box("delivery storage sorted teal cube", (xx, yy, 0.88), (0.52, 0.52, 0.57), teal, 0.045)
for xx in (4.06, 4.66):
    box("delivery storage second tier cube", (xx, -3.15, 1.45), (0.52, 0.52, 0.55), teal, 0.045)
factory_sign("READY / 08", (4.48, -3.98, 0.78), 1.75, 0.21)

robot("factory maintenance robot", (0.35, -3.66, 0.43), gold, 0.67)
box("factory maintenance tool case", (-0.48, -3.58, 0.68), (0.55, 0.38, 0.44), violet, 0.06)
beam("maintenance tool case handle", (-0.61, -3.58, 0.96), (-0.35, -3.58, 0.96), 0.045, navy)
for xx in (-4.8, -3.7, -2.6):
    beam("factory front safety railing post", (xx, -3.55, 0.43), (xx, -3.55, 1.1), 0.045, gold)
beam("factory front safety railing top", (-4.8, -3.55, 1.1), (-2.6, -3.55, 1.1), 0.05, gold)
beam("factory front safety railing mid", (-4.8, -3.55, 0.8), (-2.6, -3.55, 0.8), 0.035, gold)
for xx in (-4.45, -3.65, -2.85):
    arrow = box("factory ground flow chevron", (xx, -2.63, 0.445), (0.23, 0.07, 0.025), coral, 0.008)
    arrow.rotation_euler[2] = -0.6
    arrow = box("factory ground flow chevron", (xx, -2.76, 0.445), (0.23, 0.07, 0.025), coral, 0.008)
    arrow.rotation_euler[2] = 0.6
factory_sign("FLOW WORKS / 04", (-2.35, -4.12, 0.79), 3.3, 0.23)
