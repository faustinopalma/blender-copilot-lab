bronze_metal = mat("Bronze / warm brushed copper", (0.56, 0.23, 0.085), .82, .28)
silver_metal = mat("Silver / satin platinum", (.57, .72, .83), .85, .23)
gold_metal = mat("Gold / polished champagne", (.95, .61, .17), .82, .18)
bronze_inset = mat("Bronze / raw landing surface", (.13, .065, .043), .48, .40)
silver_inset = mat("Silver / clean slate surface", (.10, .20, .26), .58, .30)
gold_inset = mat("Gold / curated surface", (.13, .115, .055), .50, .23)
crystal_mat = mat("Gold / information jade", (.08, .81, .64), .60, .13)

platform("Medallion architecture exhibition plinth", (0, .15, .06), (12.0, 7.0, .40), dark)
box("Plinth bronze front inlay", (-3.9, -3.32, .28), (3.3, .035, .035), bronze_metal, .01)
box("Plinth silver front inlay", (0, -3.32, .28), (3.3, .035, .035), silver_metal, .01)
box("Plinth gold front inlay", (3.9, -3.32, .28), (3.3, .035, .035), gold_metal, .01)
for x in (-5.65, 5.65):
    for y in (-2.95, 3.25):
        cylinder("Plinth recessed fastener", (x, y, .274), .07, .018, silver_metal, 24)
label("ONE LAKE   /   THREE LEVELS OF TRUST", (0, -2.85, .39), .22, white)

terraces = [
    ("bronze", -3.9, -.25, 1.05, bronze_metal, bronze_inset, "BRONZE / RAW", "LAND  /  RETAIN", "01"),
    ("silver", 0, .20, 2.00, silver_metal, silver_inset, "SILVER / CLEAN", "VALIDATE  /  CONFORM", "02"),
    ("gold", 3.9, .65, 2.95, gold_metal, gold_inset, "GOLD / READY", "CURATE  /  SERVE", "03"),
]
for name, x, y, top, metal, inset, heading, subtitle, number in terraces:
    cylinder(name + " circular foundation", (x, y, .37), 1.84, .20, navy, 96)
    cylinder(name + " rising drum", (x, y, (.46 + top - .20) / 2), 1.63, top - .66, dark, 96)
    cylinder(name + " metallic crown", (x, y, top - .13), 1.82, .26, metal, 96)
    cylinder(name + " inset working terrace", (x, y, top + .018), 1.60, .045, inset, 96)
    ring(name + " luminous perimeter", (x, y, top + .035), 1.73, .028, metal)
    ring(name + " drum lower band", (x, y, .49), 1.65, .045, metal)
    ring(name + " drum upper band", (x, y, top - .29), 1.64, .033, metal)
    for i in range(5):
        angle = -math.pi / 2 + (i - 2) * .20
        px, py = x + 1.644 * math.cos(angle), y + 1.644 * math.sin(angle)
        beam(name + " front status slit", (px, py, top - .44), (px, py, top - .32), .025, glow)
    for dx in (-.85, .85):
        beam(name + " label bracket", (x + dx, y - 1.25, top - .12),
             (x + dx, y - 2.0, top - .05), .035, metal)
    text = label(heading, (x, y - 2.02, top + .09), .29, white)
    normal = text.rotation_euler.to_matrix() @ Vector((0, 0, 1))
    panel = box(name + " floating legend plaque", Vector(text.location) - normal * .055,
                (3.02, .75, .09), navy, .07)
    panel.rotation_euler = text.rotation_euler
    label(subtitle, Vector(text.location) + text.rotation_euler.to_matrix() @ Vector((0, -.23, .015)),
          .115, metal)
    label(number, (x - .95, y + 1.10, top + .17), .34, metal)

raw_fragments = [
    (-1.0, -.35, .26, .38, .32, -.25), (-.40, -.72, .19, .40, .28, .40),
    (.30, -.63, .31, .35, .43, -.50), (.88, -.18, .20, .33, .27, .22),
    (-1.02, .32, .28, .30, .42, .55), (-.48, .05, .39, .46, .50, -.18),
    (.18, .14, .22, .30, .31, .75), (.82, .47, .33, .37, .46, -.62),
    (-.44, .75, .20, .36, .26, .33), (.22, .85, .29, .32, .42, -.31),
    (-.70, -.33, .10, .21, .13, .70), (.45, -.15, .12, .25, .18, -.45),
    (-.05, .47, .13, .24, .16, .15), (1.08, .13, .12, .22, .15, .65),
]
for i, (dx, dy, h, sx, sy, turn) in enumerate(raw_fragments):
    fragment = box("bronze uneven raw data fragment %02d" % i,
                   (-3.9 + dx, -.25 + dy, 1.09 + h / 2), (sx, sy, h),
                   (bronze_metal, coral, blue, silver_metal)[i % 4], .035)
    fragment.rotation_euler = (.06 * (i % 3), -.05 * (i % 2), turn)
    if i < 8:
        stripe = box("bronze fragment unparsed field", (-3.9 + dx, -.25 + dy, 1.10 + h),
                     (sx * .65, .035, .018), white, .005)
        stripe.rotation_euler.z = turn

for row in range(3):
    for col in range(3):
        x, y = (col - 1) * .66, .2 + (row - 1) * .64
        box("silver clean ordered data cube %d %d" % (row, col),
            (x, y, 2.30), (.48, .46, .50), silver_metal, .045)
        box("silver cube validated field", (x, y - .238, 2.34), (.30, .022, .075), glow, .01)
        box("silver cube white top", (x, y, 2.56), (.38, .36, .025), white, .025)
for step in (-1.0, -.34, .34, 1.0):
    beam("silver alignment grid longitudinal", (step, -.82, 2.054), (step, 1.22, 2.054), .009, teal)
    beam("silver alignment grid transverse", (-1.02, .2 + step, 2.054), (1.02, .2 + step, 2.054), .009, teal)

for i, (dx, dy, h, radius) in enumerate([(-.73, .55, 1.16, .32), (-.05, .87, .80, .26), (.59, .74, 1.03, .29)]):
    x, y = 3.9 + dx, .65 + dy
    cylinder("gold crystal socket", (x, y, 3.06), radius + .09, .14, gold_metal, 48)
    lower = cone("gold polished information crystal lower %d" % i, (x, y, 3.20),
                 radius * .60, radius, .20, crystal_mat, 6)
    tip = cone("gold polished information crystal tip %d" % i, (x, y, 3.30 + h / 2),
               radius, 0, h, crystal_mat, 6)
    for crystal in (lower, tip):
        for face in crystal.data.polygons:
            face.use_smooth = False

box("gold miniature chart tray", (4.03, .07, 3.05), (2.11, .89, .13), dark, .06)
for i, h in enumerate((.36, .62, .91, 1.22)):
    x, y = 3.28 + i * .49, .07
    box("gold ready information chart bar %d" % i, (x, y, 3.12 + h / 2),
        (.29, .36, h), (teal, silver_metal, gold_metal, gold_metal)[i], .035)
    box("gold chart bar polished cap %d" % i, (x, y, 3.135 + h),
        (.30, .37, .035), white, .02)
beam("gold chart horizontal axis", (3.02, -.17, 3.13), (5.02, -.17, 3.13), .022, silver_metal)
for i in range(4):
    beam("gold chart axis tick", (3.28 + i * .49, -.17, 3.13),
         (3.28 + i * .49, -.26, 3.13), .013, silver_metal)

for index in range(2):
    left, right = terraces[index], terraces[index + 1]
    a = Vector((left[1] + 1.26, left[2] - .54, left[3] + .08))
    b = Vector((right[1] - 1.26, right[2] - .54, right[3] + .08))
    delta = b - a
    side = Vector((-delta.y, delta.x, 0)).normalized()
    deck = box("bridge %d ascending conveyor deck" % index, (a + b) / 2,
               (delta.length, .65, .13), navy, .035)
    deck.rotation_euler = (0, -math.atan2(delta.z, math.hypot(delta.x, delta.y)),
                          math.atan2(delta.y, delta.x))
    for sign in (-1, 1):
        beam("bridge %d luminous guide rail" % index, a + side * sign * .34 + Vector((0, 0, .11)),
             b + side * sign * .34 + Vector((0, 0, .11)), .034, glow)
    for i in range(8):
        p = a.lerp(b, (i + .5) / 8) + Vector((0, 0, .082))
        beam("bridge %d conveyor transverse roller" % index, p - side * .28, p + side * .28,
             .028, silver_metal)
    direction = delta.normalized()
    for i in range(3):
        p = a.lerp(b, .23 + i * .27) + Vector((0, 0, .23))
        for sign in (-1, 1):
            beam("bridge %d forward luminous chevron" % index, p - direction * .16 + side * sign * .12,
                 p + direction * .10, .026, glow)
        ball("bridge %d flowing data particle" % index, p + Vector((0, 0, .17)), .055, glow)
    middle = a.lerp(b, .5)
    beam("bridge %d structural diagonal" % index, (middle.x - .25, middle.y, .30),
         middle - Vector((0, 0, .13)), .065, left[4])
    beam("bridge %d structural brace" % index, (middle.x + .25, middle.y, .30),
         middle - Vector((0, 0, .13)), .065, right[4])
