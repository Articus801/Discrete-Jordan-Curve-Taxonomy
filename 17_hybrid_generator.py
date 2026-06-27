import numpy as np
import scipy.ndimage as ndimage

def initiate_koch_segment(p1, p2, depth):
    """Recursively generates a single Koch curve segment between two points."""
    if depth == 0:
        return [p1, p2]

    p1 = np.array(p1)
    p2 = np.array(p2)

    # Calculate the internal dividing points of the Koch generation step
    v = p2 - p1
    a = p1 + v / 3.0
    c = p1 + 2.0 * v / 3.0

    # Find the apex (b) of the equilateral triangle via a 60-degree rotation
    cos60, sin60 = np.cos(np.pi / 3), np.sin(np.pi / 3)
    rotation_matrix = np.array([[cos60, -sin60], [sin60, cos60]])
    b = a + np.dot(rotation_matrix, v / 3.0)

    # Recursively build the 4 sub-segments
    seg1 = initiate_koch_segment(p1, a, depth - 1)
    seg2 = initiate_koch_segment(a, b, depth - 1)
    seg3 = initiate_koch_segment(b, c, depth - 1)
    seg4 = initiate_koch_segment(c, p2, depth - 1)

    return seg1[:-1] + seg2[:-1] + seg3[:-1] + seg4

def generate_hybrid_jordan_curve(fractal_depth=4, smooth_sigma=4.0):
    """
    Constructs a closed, simple Jordan curve.
    Sides 1, 2, 3: A smooth/flat open square box baseline.
    Side 4: A Koch fractal segment closing the loop.
    Saves and returns both the sharp pure fractal loop and the rounded variant loop.
    """
    # 1. Define the baseline smooth sides of the box
    # Corners: (0,1) -> (0,0) -> (1,0) -> (1,1)
    side1 = np.array([[0.0, y] for y in np.linspace(1.0, 0.0, 100, endpoint=False)])
    side2 = np.array([[x, 0.0] for x in np.linspace(0.0, 1.0, 100, endpoint=False)])
    side3 = np.array([[1.0, y] for y in np.linspace(0.0, 1.0, 100, endpoint=False)])

    box_base = np.vstack([side1, side2, side3])

    # 2. Generate the fractal patch for Side 4 (from (1,1) back to (0,1))
    fractal_pts = initiate_koch_segment([1.0, 1.0], [0.0, 1.0], depth=fractal_depth)
    fractal_pts = np.array(fractal_pts)

    # Pure Sharp Hybrid Loop (Close the loop by making start and end match)
    sharp_loop = np.vstack([box_base, fractal_pts[:-1]])
    sharp_loop = np.vstack([sharp_loop, sharp_loop[0]])

    # 3. Create the Rounded Variant
    # Apply a 1D Gaussian filter to the fractal coordinates to regularise them
    smoothed_fractal = np.copy(fractal_pts)
    smoothed_fractal[:, 0] = ndimage.gaussian_filter1d(fractal_pts[:, 0], sigma=smooth_sigma, mode='wrap')
    smoothed_fractal[:, 1] = ndimage.gaussian_filter1d(fractal_pts[:, 1], sigma=smooth_sigma, mode='wrap')

    rounded_loop = np.vstack([box_base, smoothed_fractal[:-1]])
    rounded_loop = np.vstack([rounded_loop, rounded_loop[0]])

    # Save arrays to disk to establish clear handovers between modules
    np.save('17_sharp_curve.npy', sharp_loop)
    np.save('17_rounded_curve.npy', rounded_loop)

    return sharp_loop, rounded_loop

if __name__ == "__main__":
    sharp, rounded = generate_hybrid_jordan_curve(fractal_depth=4, smooth_sigma=4.0)
    print(f"[17_hybrid_generator] Success.")
    print(f" -> Sharp Curve Matrix shape: {sharp.shape}")
    print(f" -> Rounded Curve Matrix shape: {rounded.shape}")
    print(" Saved configurations to disk as '17_sharp_curve.npy' and '17_rounded_curve.npy'.")
