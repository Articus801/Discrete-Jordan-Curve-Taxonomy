# Let's write a complete script that simulates your Central Chord Radial Transform,
# builds the midpoint sets, and implements the square hunter loop.

import numpy as np

def generate_circle(n=300):
    t = np.linspace(0, 2*np.pi, n, endpoint=False)
    return np.column_stack((np.cos(t), np.sin(t)))

def generate_ellipse(n=300, a=1.4, b=0.7, deg=45):
    t = np.linspace(0, 2*np.pi, n, endpoint=False)
    x = a * np.cos(t)
    y = b * np.sin(t)
    rad = np.radians(deg)
    c, s = np.cos(rad), np.sin(rad)
    return np.column_stack((x*c - y*s, x*s + y*c))

def generate_bumpy(n=300):
    t = np.linspace(0, 2*np.pi, n, endpoint=False)
    r = 1.0 + 0.15 * np.sin(3*t) + 0.08 * np.cos(5*t)
    return np.column_stack((r*np.cos(t), r*np.sin(t)))

def analyze_curve(curve):
    midpoints = []
    chords = [] # storing (x, y, length, midpoint)

    for x in curve:
        # Find y by casting ray through center (0,0) -> closest to -x
        dists = np.hypot(curve[:,0] + x[0], curve[:,1] + x[1])
        y = curve[np.argmin(dists)]

        midpoint = (x + y) / 2.0
        length = np.hypot(x[0]-y[0], x[1]-y[1])

        midpoints.append(midpoint)
        chords.append({'x': x, 'y': y, 'midpoint': midpoint, 'length': length})

    return np.array(midpoints), chords

def hunt_squares(chords, tol_len=0.03, tol_mid=0.03):
    # Hunt for squares: Two chords with similar lengths, perpendicular, sharing the same midpoint
    squares_found = []
    n = len(chords)
    for i in range(n):
        c1 = chords[i]
        v1 = c1['x'] - c1['y']
        for j in range(i+1, n):
            c2 = chords[j]
            # Check length similarity
            if abs(c1['length'] - c2['length']) > tol_len:
                continue
            # Check midpoint similarity
            if np.hypot(c1['midpoint'][0] - c2['midpoint'][0], c1['midpoint'][1] - c2['midpoint'][1]) > tol_mid:
                continue
            # Check perpendicularity (dot product close to 0)
            v2 = c2['x'] - c2['y']
            dot = np.dot(v1, v2) / (c1['length'] * c2['length'])
            if abs(dot) < 0.1: # close to perpendicular
                squares_found.append((c1, c2))
                if len(squares_found) >= 1: # just find the first clear one
                    return squares_found
    return squares_found

# Run analysis
m_circle, c_circle = analyze_curve(generate_circle())
m_ellipse, c_ellipse = analyze_curve(generate_ellipse())
m_bumpy, c_bumpy = analyze_curve(generate_bumpy())

sq_circle = hunt_squares(c_circle)
sq_ellipse = hunt_squares(c_ellipse)
sq_bumpy = hunt_squares(c_bumpy)

print(f"Circle Midpoints Mean Variance: {np.var(m_circle):.6f}")
print(f"Ellipse Midpoints Mean Variance: {np.var(m_ellipse):.6f}")
print(f"Squares found in bumpy curve: {len(sq_bumpy)}")
