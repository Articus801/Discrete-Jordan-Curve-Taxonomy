import numpy as np
import matplotlib.pyplot as plt

def generate_bumpy_bezier(n=400):
    """Generates our standard bumpy shape family."""
    t = np.linspace(0, 2*np.pi, n, endpoint=False)
    r = 1.0 + 0.18 * np.sin(3*t) + 0.08 * np.cos(5*t)
    return np.column_stack((r*np.cos(t), r*np.sin(t)))

def analyze_curve_ccrt(curve):
    """Executes the CCRT tracking engine."""
    midpoints = []
    chords = []
    for x in curve:
        # Find opposing boundary intersection passing through the frame center
        dists = np.linalg.norm(curve + x, axis=1)
        y = curve[np.argmin(dists)]

        midpoint = (x + y) / 2.0
        length = np.linalg.norm(x - y)

        midpoints.append(midpoint)
        chords.append({'x': x, 'y': y, 'midpoint': midpoint, 'length': length})
    return np.array(midpoints), chords

if __name__ == "__main__":
    print("Generating geometric visual files...")

    # 1. Gather our discrete point sets
    curve = generate_bumpy_bezier(n=400)
    midpoints, chords = analyze_curve_ccrt(curve)

    # 2. Initialize dual-panel plot space
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 6))

    # --- LEFT PANEL: THE COMPLETE WORKSPACE ---
    ax1.plot(curve[:, 0], curve[:, 1], 'b-', lw=2.5, label='Jordan Curve ($\gamma$)')
    ax1.scatter(midpoints[:, 0], midpoints[:, 1], color='red', s=8, zorder=3, label='Midpoint Cloud')

    # Render a sparse subset of chords to avoid visual clutter
    for i in range(0, len(chords), 15):
        c = chords[i]
        ax1.plot([c['x'][0], c['y'][0]], [c['x'][1], c['y'][1]], color='gray', alpha=0.15, lw=1)

    ax1.set_title("Central Chord Radial Transform", fontsize=12, fontweight='bold')
    ax1.set_aspect('equal')
    ax1.grid(True, linestyle=':', alpha=0.6)
    ax1.legend(loc='upper right')

    # --- RIGHT PANEL: THE MIDPOINT STRAWS ALIGNMENT ---
    # Draw the internal 'straw vectors' originating from the coordinate frame center
    for i in range(0, len(midpoints), 2):
        ax2.plot([0, midpoints[i, 0]], [0, midpoints[i, 1]], color='crimson', alpha=0.3, lw=1.2)

    ax2.scatter(midpoints[:, 0], midpoints[:, 1], color='darkred', s=4, zorder=3)
    ax2.axhline(0, color='black', lw=0.5, linestyle='--')
    ax2.axvline(0, color='black', lw=0.5, linestyle='--')

    ax2.set_title("Isolated Midpoint Straw Spectrum", fontsize=12, fontweight='bold')
    ax2.set_aspect('equal')
    ax2.grid(True, linestyle=':', alpha=0.6)

    plt.tight_layout()

    # Save a high-resolution file to your directory
    output_filename = "jordan_curve_straws_analysis.png"
    plt.savefig(output_filename, dpi=300)
    print(f"Success! Visual chart exported cleanly as: {output_filename}")
    plt.show()
