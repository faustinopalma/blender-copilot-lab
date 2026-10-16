platform("Knowledge library foundation", (0, 0, 0), (12, 8.7, 0.42), navy)
box("Library inset floor", (0, 0, 0.26), (11.55, 8.25, 0.14), dark)
box("Front brass threshold", (0, -4.12, 0.36), (11.2, 0.045, 0.04), gold, 0.01)
for x in (-5.48, 5.48):
    box("Perimeter teal floor inlay", (x, 0, 0.35), (0.035, 7.8, 0.025), teal, 0.008)
for x in (-3.6, 0.05, 3.65):
    box("Floor division inlay", (x, -1.05, 0.35), (0.025, 5.3, 0.025), gold, 0.006)
platform("Reading area rug", (-3.35, -1.3, 0.37), (3.35, 3.05, 0.045), violet)
box("Rug inset", (-3.35, -1.3, 0.399), (3.05, 2.75, 0.018), navy, 0.08)

book_colors = [coral, gold, white, teal, violet, gold, coral, blue]
for shelf_index, sx in enumerate((-3.7, -0.15)):
    box("Archive shelf backing", (sx, 2.95, 2.7), (3.05, 0.15, 4.65), navy)
    for side in (-1, 1):
        box("Archive shelf upright", (sx + side * 1.53, 2.54, 2.7),
            (0.16, 1.0, 4.7), teal)
    for level in range(5):
        z = 0.43 + level * 1.1
        box("Archive shelf horizontal", (sx, 2.52, z), (3.13, 1.08, 0.13), navy, 0.035)
        box("Archive shelf gold lip", (sx, 1.955, z + 0.015),
            (2.94, 0.035, 0.065), gold, 0.01)
        if level < 4:
            for j in range(7):
                width = 0.25 + (j % 3) * 0.035
                height = 0.66 + ((j + level * 2 + shelf_index) % 4) * 0.075
                bx = sx - 1.19 + j * 0.39
                box("Archive shelf book spine", (bx, 2.37, z + 0.075 + height / 2),
                    (width, 0.70, height), book_colors[(j + level + shelf_index * 3) % 8], 0.025)
                if j in (1, 4):
                    box("Book gilded spine band", (bx, 2.007, z + 0.26),
                        (width * 0.77, 0.018, 0.035), gold, 0.005)
    box("Archive shelf canopy", (sx, 2.55, 5.03), (3.35, 1.15, 0.2), teal)
    box("Archive shelf catalogue plaque", (sx, 1.93, 4.97), (1.95, 0.08, 0.35), dark, 0.035)
    label("01 / SOURCES" if shelf_index == 0 else "02 / CONTEXT",
          (sx, 1.87, 4.97), 0.19, gold).rotation_euler = (math.pi / 2, 0, 0)

for x in (-4.99, -4.29):
    beam("Rolling library ladder rail", (x, 0.82, 0.39), (x, 1.91, 4.39), 0.055, gold)
for step in range(9):
    z = 0.66 + step * 0.405
    y = 0.82 + (z - 0.39) * 1.09 / 4
    beam("Library ladder rung", (-4.99, y, z), (-4.29, y, z), 0.045, white)
for x in (-4.99, -4.29):
    ball("Ladder rolling foot", (x, 0.84, 0.46), 0.1, dark)

platform("Retrieve arch landing", (0.15, -0.2, 0.44), (3.05, 2.05, 0.18), navy)
for x in (-1.12, 1.42):
    box("Retrieval arch column", (x, -0.15, 2.12), (0.3, 0.62, 3.35), violet)
    box("Retrieval arch illuminated edge", (x, -0.485, 2.12),
        (0.075, 0.035, 3.05), glow, 0.018)
    box("Retrieval arch foot", (x, -0.15, 0.69), (0.6, 0.88, 0.24), teal)
box("Retrieval arch lintel", (0.15, -0.15, 3.85), (2.84, 0.7, 0.48), violet)
box("Retrieval arch sign", (0.15, -0.53, 3.86), (2.23, 0.06, 0.34), dark, 0.03)
label("RETRIEVE", (0.15, -0.58, 3.86), 0.29, white).rotation_euler = (math.pi / 2, 0, 0)
for x in (-0.8, -0.34, 0.12, 0.58, 1.04):
    box("Retrieval scan emitter", (x, -0.15, 3.58), (0.16, 0.26, 0.065), glow, 0.025)
line("Grounded knowledge flow", [(-1.8, 1.45, 2.0), (-0.15, 0.1, 2.45),
                               (1.7, -0.5, 2.5), (2.65, -1.6, 2.25)], 0.026, glow)
for i, (x, y, z) in enumerate(((-1.65, 1.23, 1.95), (-0.86, 0.62, 2.23),
                              (0.02, 0.01, 2.53), (0.94, -0.38, 2.67),
                              (1.82, -0.88, 2.56))):
    page = box("Luminous retrieved document fragment", (x, y, z), (0.61, 0.055, 0.77),
               white if i % 2 == 0 else teal, 0.045)
    page.rotation_euler[1] = -0.13 + i * 0.065
    box("Document fragment highlighted extract", (x, y - 0.038, z + 0.16),
        (0.4, 0.02, 0.07), violet, 0.008)
    box("Document fragment text line", (x, y - 0.039, z - 0.03),
        (0.39, 0.02, 0.035), navy, 0.006)

platform("Answer assembly desk foot", (3.52, -2.08, 0.47), (3.55, 1.88, 0.22), navy)
for x in (2.26, 4.78):
    box("Answer desk pedestal", (x, -2.03, 1.03), (0.38, 1.28, 1.12), teal)
box("Answer assembly desktop", (3.52, -2.05, 1.65), (3.6, 1.85, 0.22), gold)
box("Answer desk writing surface", (3.52, -2.05, 1.78), (3.33, 1.58, 0.055), navy, 0.055)
box("Answer card violet frame", (3.36, -2.53, 2.24), (2.55, 0.13, 1.0), violet, 0.07)
box("Answer card assembled page", (3.36, -2.61, 2.26), (2.35, 0.04, 0.83), white, 0.035)
label("ANSWER", (3.36, -2.65, 2.47), 0.29, navy).rotation_euler = (math.pi / 2, 0, 0)
for n in range(2):
    box("Answer card grounded text", (3.36, -2.642, 2.22 - n * 0.13),
        (1.8 - n * 0.3, 0.018, 0.035), teal, 0.007)
for i in range(3):
    cx = 2.58 + i * 0.78
    box("Answer citation tab " + str(i + 1), (cx, -2.65, 1.85),
        (0.57, 0.08, 0.31), (teal, violet, coral)[i], 0.035)
    label("[" + str(i + 1) + "]", (cx, -2.70, 1.85), 0.23, white).rotation_euler = (math.pi / 2, 0, 0)

robot("Friendly citation librarian", (4.62, -0.46, 0.36), teal, 1.45)
beam("Librarian answer assembly arm", (4.07, -0.46, 1.73),
     (3.96, -1.3, 1.95), 0.10, gold)
ball("Librarian assembly hand", (3.96, -1.3, 1.95), 0.15, white)

cylinder("Reading lamp weighted foot", (2.08, -1.51, 1.85), 0.25, 0.09, dark)
beam("Reading lamp upright", (2.08, -1.51, 1.87), (2.08, -1.51, 2.91), 0.035, gold)
beam("Reading lamp elbow", (2.08, -1.51, 2.91), (2.57, -1.51, 3.04), 0.035, gold)
cone("Reading lamp shade", (2.57, -1.51, 2.94), 0.29, 0.12, 0.29, teal, 48)
cylinder("Reading lamp luminous diffuser", (2.57, -1.51, 2.79), 0.25, 0.025, glow)

cylinder("Reading table pedestal", (-3.25, -1.53, 0.9), 0.14, 0.95, gold)
cylinder("Reading table base", (-3.25, -1.53, 0.47), 0.53, 0.12, navy)
cylinder("Reading table round top", (-3.25, -1.53, 1.43), 0.95, 0.14, teal)
for side in (-1, 1):
    page = box("Open reference document", (-3.25 + side * 0.3, -1.53, 1.54),
               (0.57, 0.7, 0.06), white, 0.02)
    page.rotation_euler[1] = side * 0.09
beam("Open reference document binding", (-3.25, -1.85, 1.54),
     (-3.25, -1.21, 1.54), 0.025, gold)
box("Reading stool cushion", (-3.25, -2.85, 0.9), (0.85, 0.75, 0.2), coral)
for x in (-3.55, -2.95):
    beam("Reading stool legs", (x, -2.85, 0.4), (x, -2.85, 0.83), 0.055, gold)

for x, word, color in ((-3.4, "SOURCES", gold), (0.2, "GROUND", teal), (3.65, "CITED", violet)):
    box("Workflow floor plaque " + word, (x, -3.61, 0.42), (2.35, 0.66, 0.09), navy, 0.055)
    label(word, (x, -3.7, 0.55), 0.27, color)
for x in (-1.75, 1.65):
    line("Floor routing arrow", [(x - 0.25, -3.61, 0.42), (x, -3.61, 0.42),
                                (x - 0.1, -3.48, 0.42)], 0.025, glow)
