import gradio as gr
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from polygon_area_perimeter_calculator import (
    close_polygon,
    shoelace_area,
    compute_perimeter,
    convert_geographic_to_projected,
    compute_centroid,
    format_area,
    plot_polygon
)

def process_input(coords_df, csv_file, coord_system, area_unit, auto_close):
    # Get vertices from either dataframe or csv file
    vertices = None
    if csv_file is not None:
        try:
            df = pd.read_csv(csv_file.name)
            if df.shape[1] < 2:
                return "CSV file must have at least two columns (X, Y).", None, None
            vertices = df.iloc[:, :2].values.astype(float)
        except Exception as e:
            return f"Error reading CSV: {str(e)}", None, None
    elif coords_df is not None and len(coords_df) > 0:
        # Filter out rows with missing values
        valid = coords_df.dropna()
        if len(valid) < 3:
            return "Please provide at least 3 valid coordinate pairs.", None, None
        vertices = valid.iloc[:, :2].values.astype(float)
    else:
        return "Please provide coordinates via grid or CSV.", None, None

    if len(vertices) < 3:
        return "Need at least 3 points.", None, None

    # Auto-close if checkbox checked or first != last
    if auto_close or not np.allclose(vertices[0], vertices[-1]):
        vertices = close_polygon(vertices)

    # Compute area in input units (degrees or meters)
    area_input, perimeter_input = shoelace_area(vertices), compute_perimeter(vertices)
    centroid_input = compute_centroid(vertices)

    # If geographic, convert area/perimeter to approximate meters
    approx_warning = ""
    if coord_system == "Geographic (decimal degrees)":
        # Convert to metres using simple cylindrical at average latitude
        avg_lat = np.mean(vertices[:, 1])
        scale = np.cos(np.radians(avg_lat))
        # Adjust area: degrees^2 -> m^2 (rough: 1 deg lat = 111320 m, 1 deg lon = 111320*cos(lat) m)
        m_per_deg_lat = 111320.0
        m_per_deg_lon = 111320.0 * scale
        area_m2_raw = area_input * (m_per_deg_lat * m_per_deg_lon)  # degrees^2 to m^2
        perimeter_m_raw = perimeter_input * np.sqrt(m_per_deg_lat**2 + m_per_deg_lon**2)  # rough
        # Recompute centroid as we store original
        centroid_out = list(centroid_input)  # keep in degrees
        area_used = area_m2_raw
        perimeter_used = perimeter_m_raw
        approx_warning = " (approximate – geographic coordinates converted using cylindrical projection at average latitude)"
    else:
        area_used = area_input
        perimeter_used = perimeter_input
        centroid_out = list(centroid_input)  # already in meters

    # Format area output
    area_str, perimeter_str, unit_label = format_area(area_used, perimeter_used, area_unit, coord_system)

    # Build result text
    result_text = f"Area: {area_str} {unit_label}\n"
    result_text += f"Perimeter: {perimeter_str}\n"
    result_text += f"Centroid: ({centroid_out[0]:.6f}, {centroid_out[1]:.6f})\n"
    if approx_warning:
        result_text += approx_warning

    # Generate plot
    fig = plot_polygon(vertices, centroid_out, coord_system, area_unit)

    # Prepare CSV for download: vertices used (including closing point)
    df_out = pd.DataFrame(vertices, columns=['X', 'Y'])
    csv_path = "/tmp/polygon_vertices.csv"
    df_out.to_csv(csv_path, index=False)

    return result_text, fig, csv_path

# Gradio UI
with gr.Blocks(title="Polygon Area & Perimeter Calculator") as demo:
    gr.Markdown("## Polygon Area & Perimeter Calculator")
    with gr.Row():
        with gr.Column():
            coords_input = gr.Dataframe(
                headers=["X", "Y"],
                datatype="number",
                row_count=5,
                col_count=2,
                label="Coordinates (X, Y) - one per row",
                interactive=True
            )
            csv_input = gr.File(label="Or upload CSV (X,Y columns)")
            coord_system = gr.Dropdown(
                choices=["Projected (meters)", "Geographic (decimal degrees)"],
                value="Projected (meters)",
                label="Coordinate System"
            )
            area_unit = gr.Dropdown(
                choices=["square meters", "square kilometers", "hectares", "acres"],
                value="square meters",
                label="Output Area Unit"
            )
            auto_close = gr.Checkbox(label="Auto-close polygon (if first and last points differ)", value=True)
            calc_btn = gr.Button("Calculate")
        with gr.Column():
            output_text = gr.Textbox(label="Results", lines=5)
            output_plot = gr.Plot(label="Polygon Plot")
            output_csv = gr.File(label="Download Vertices CSV")

    calc_btn.click(
        fn=process_input,
        inputs=[coords_input, csv_input, coord_system, area_unit, auto_close],
        outputs=[output_text, output_plot, output_csv]
    )

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
