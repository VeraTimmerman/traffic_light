import math
import matplotlib.pyplot as plt

# =====================
# Gegevens
# =====================
center = (150.0, 100.0)
radius = 5.0  # diameter 10 cm

# =====================
# Hex grid functies
# =====================
def hex_to_cart(q, r, a):
    x = a * (q + r / 2.0)
    y = a * (math.sqrt(3) / 2.0 * r)
    return x, y

def hex_ring(radius):
    coords = []
    q = -radius
    r = 0
    for i in range(radius):
        coords.append((q, r))
        q += 1
        r -= 1
    for i in range(radius):
        coords.append((q, r))
        r -= 1
    for i in range(radius):
        coords.append((q, r))
        q -= 1
    for i in range(radius):
        coords.append((q, r))
        q -= 1
        r += 1
    for i in range(radius):
        coords.append((q, r))
        r += 1
    for i in range(radius):
        coords.append((q, r))
        q += 1
    return coords

# =====================
# Pitch bepalen
# =====================
pitch = radius / 4.0  # zodat ring 4 net buiten valt

# =====================
# Punten genereren
# =====================
hex_coords = [(0, 0)]
for ring in range(1, 4):
    hex_coords += hex_ring(ring)

points = []
for q, r in hex_coords:
    x, y = hex_to_cart(q, r, pitch)
    dist = math.hypot(x, y)
    if dist <= radius:
        ring = max(abs(q), abs(r), abs(q + r))
        points.append((ring, q, r, x, y, dist))

points.sort(key=lambda p: (p[0], p[5]))

base = [p for p in points if p[0] <= 2]
ring3 = [p for p in points if p[0] == 3]

step = max(1, len(ring3) // 6)
ring3_selected = ring3[::step][:6]

selected = base + ring3_selected

points_abs = []
for ring, q, r, x, y, _ in selected:
    label = "M" if ring == 0 else f"R{ring}"
    points_abs.append((label, (center[0] + x, center[1] + y)))

# =====================
# Plot
# =====================
fig, ax = plt.subplots(figsize=(7, 7))

circle = plt.Circle(center, radius, fill=False, linewidth=2)
ax.add_patch(circle)

for label, (x, y) in points_abs:
    ax.scatter(x, y, zorder=3)
    dx = x - center[0]
    dy = y - center[1]
    ax.text(
        x, y,
        f"{label}\n({dx:.3f}, {dy:.3f})",
        fontsize=8,
        ha='left',
        va='bottom'
    )

ax.scatter(center[0], center[1], s=60)
ax.text(center[0], center[1], "M", fontsize=10, ha='right', va='top')

# Aantal punten in de plot weergeven
ax.text(
    0.02, 0.98,
    f"Aantal punten: {len(points_abs)}",
    transform=ax.transAxes,
    fontsize=12,
    va='top',
    ha='left',
    bbox=dict(boxstyle="round", fc="white", ec="black")
)

ax.set_aspect('equal')
ax.set_xlabel("X (cm)")
ax.set_ylabel("Y (cm)")
ax.set_title("Cirkel (Ø 10 cm) met hexagonaal raster (25 punten)")
ax.grid(True)

# Laat Matplotlib zelf de limieten bepalen
ax.autoscale()

plt.show()
