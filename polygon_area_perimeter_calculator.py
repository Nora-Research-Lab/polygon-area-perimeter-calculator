import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import io

def close_polygon(vertices):
    """If first != last, append first point to close."""
    if not np.allclose(vertices[0], vertices[-1]):
        return np.vstack([vertices, vertices[0]])
    return vertices

def shoelace_area(vertices):
    """Compute polygon area using shoelace formula. Vertices shape (N,2). Returns signed area (absolute used)."""
    x = vertices[:, 0]
    y = vertices[:, 1]
    # shift indices for cross terms
    area = 0.5 * np.abs(np.dot(x, np.roll(y, -1)) - np.dot(y, np.roll(x, -1)))
    return area

def compute_perimeter(vertices):
    """Sum of Euclidean distances between consecutive points."""
    diffs = np.diff(vertices, axis=0)
    return np.sum(np.sqrt(np.sum(diffs**2, axis=1)))

def convert_geographic_to_projected(vertices):
    """Approximate conversion of degrees to meters using simple cylindrical.
       Returns new vertices in meters and average latitude used for scaling."""
    avg_lat = np.mean(vertices[:, 1])
    lat_rad = np.radians(avg_lat)
    m_per_deg_lat = 111320.0
    m_per_deg_lon = 111320.0 * np.cos(lat_rad)
    projected = vertices.copy()
    projected[:, 0] = vertices[:, 0] * m_per_deg_lon
    projected[:, 1] = vertices[:, 1] * m_per_deg_lat
    return projected, avg_lat

def compute_centroid(vertices):
    """Centroid of polygon (sign sensitive) using formula with signed area."""
    x = vertices[:, 0]
    y = vertices[:, 1]
    # Shifted
    x_shift = np.roll(x, -1)
    y_shift = np.roll(y, -1)
    cross = x*y_shift - x_shift*y
    area = 0.5 * np.sum(cross)
    if abs(area) < 1e-15:
        return [np.mean(x), np.mean(y)]
    Cx = np.sum((x + x_shift) * cross) / (6.0 * area)
    Cy = np.sum((y + y_shift) * cross) / (6.0 * area)
    return [Cx, Cy]

def format_area(area_value, perimeter_value, area_unit, coord_system):
    """Convert area to chosen unit, determine perimeter unit, return strings."""
    # Area conversions
    to_sq_m = 1.0
    if area_unit == "square meters":
        to_sq_m = 1.0
    elif area_unit == "square kilometers":
        to_sq_m = 1e-6
    elif area_unit == "hectares":
        to_sq_m = 1e-4
    elif area_unit == "acres":
        to_sq_m = 2.47105e-4
    area_converted = area_value * to_sq_m
    area_str = f"{area_converted:.6f}"

    # Perimeter unit
    if coord_system == "Geographic (decimal degrees)":
        perimeter_unit = "degrees"
        perimeter_str = f"{perimeter_value:.6f} {perimeter_unit}"
    else:
        # Projected: assume meters, could show km if large
        if perimeter_value >= 1000:
            perimeter_str = f"{perimeter_value/1000:.6f} km"
        else:
            perimeter_str = f"{perimeter_value:.6f} m"

    unit_label = area_unit
    return area_str, perimeter_str, unit_label

def plot_polygon(vertices, centroid, coord_system, area_unit):
    """Create matplotlib figure of polygon with vertices labeled and centroid marked."""
    fig, ax = plt.subplots(figsize=(6,6))
    # Close for plotting
    x = vertices[:, 0]
    y = vertices[:, 1]
    ax.plot(x, y, 'b-', linewidth=2)
    ax.plot(x, y, 'ro', markersize=6)
    # Label vertices
    for i, (xi, yi) in enumerate(vertices):
        ax.annotate(f"V{i}", (xi, yi), textcoords="offset points", xytext=(0,10), ha='center', fontsize=8)
    # Mark centroid
    if centroid is not None:
        ax.plot(centroid[0], centroid[1], 'g*', markersize=12, label='Centroid')
        ax.legend()
    ax.set_aspect('equal')
    ax.set_title(f"Polygon (Area in {area_unit})")
    ax.grid(True, linestyle='--', alpha=0.7)
    if coord_system == "Geographic (decimal degrees)":
        ax.set_xlabel("Longitude")
        ax.set_ylabel("Latitude")
    else:
        ax.set_xlabel("X (meters)")
        ax.set_ylabel("Y (meters)")
    fig.tight_layout()
    return fig
