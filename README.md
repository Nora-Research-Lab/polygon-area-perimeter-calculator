![NORA logo](https://i.ibb.co/0VJCC9Gf/IMG-20260114-WA0008.jpg)
 
# Polygon Area & Perimeter Calculator
 
*For surveyors, GIS analysts, and land managers: enter a set of coordinate pairs to instantly compute the polygon's area and perimeter using the shoelace formula.*
 
[![GitHub](https://img.shields.io/badge/GitHub-Nora--Research--Lab-181717?logo=github)](https://github.com/Nora-Research-Lab) [![Hugging Face](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-NoraResearchLab-yellow)](https://huggingface.co/NoraResearchLab) [![LinkedIn](https://img.shields.io/badge/LinkedIn-NORA%20Research%20Lab-0A66C2?logo=linkedin)](https://www.linkedin.com/company/nora-research-lab) [![X](https://img.shields.io/badge/X-@noraresearchlab-000000?logo=x)](https://x.com/noraresearchlab) [![NORA Research Lab](https://img.shields.io/badge/Website-noraresearchlab.site-2ea44f)](https://noraresearchlab.site) [![NORA Earth Intelligence](https://img.shields.io/badge/Platform-noraearth.xyz-2ea44f)](https://noraearth.xyz)
 

## Overview
 
**Industry:** Surveying & Mapping
 
Inputs: (a) User provides a list of at least three coordinate pairs (X,Y) representing polygon vertices in sequence (clockwise or counterclockwise). Input can be via a text grid (each row has X and Y) or by uploading a CSV file with two columns (X,Y). (b) User selects the coordinate system: 'Projected (meters)' or 'Geographic (decimal degrees)'. (c) User selects output area unit: square meters, square kilometers, hectares, or acres. (d) Optional: a checkbox to close the polygon automatically (if first and last points don't match). Core calculation: (1) Close the polygon if not already closed by appending the first point. (2) Compute area using the shoelace formula: A = 0.5 * |Σ(x_i * y_{i+1} - x_{i+1} * y_i)|. (3) Compute perimeter as the sum of Euclidean distances between consecutive points: P = Σ sqrt((x_{i+1}-x_i)² + (y_{i+1}-y_i)²). (4) If geographic coordinates are used, convert to approximate meters using a cosine-of-latitude scaling for area (simple cylindrical projection at average latitude) and warn the user that the result is approximate. (5) Compute centroid: Cx = (Σ (x_i + x_{i+1}) * (x_i*y_{i+1} - x_{i+1}*y_i)) / (6*A), similarly for Cy. Output: (a) Numeric display of area in chosen unit, perimeter in meters/kilometers (or degrees if geographic), and centroid coordinates. (b) A Matplotlib plot showing the polygon shape with labeled vertices, centroid marked, and axes scaled equally. (c) A downloadable CSV of the vertices used (including the closing point). No AI/ML component; all deterministic geometry. Gradio UI: A 'Coordinates' Dataframe editor (or File upload for CSV), dropdown for coordinate system, dropdown for area unit, a checkbox for auto-close, a 'Calculate' button. Output area shows numeric results and a plot.
 
## Run it
 
```bash
docker build -t polygon-area-perimeter-calculator .
docker run -p 7860:7860 polygon-area-perimeter-calculator
```
 
Then open http://localhost:7860 in your browser.
 
## About
 
This tool was generated and published automatically by the **NORA Earth Intelligence**
tool factory, an autonomous pipeline maintained by **NORA Research Lab** that turns
one idea per run into a small, working geoscience tool — end to end, with an
LLM writing and Docker-testing the code, and another model generating the
banner above.
 
- Platform: [https://noraearth.xyz](https://noraearth.xyz)
- Parent lab: [https://noraresearchlab.site](https://noraresearchlab.site)
 
Built 2026-10-03.
 
---
 
### Maintainer
 
**NORA Research Lab**
[![GitHub](https://img.shields.io/badge/GitHub-Nora--Research--Lab-181717?logo=github)](https://github.com/Nora-Research-Lab) [![Hugging Face](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-NoraResearchLab-yellow)](https://huggingface.co/NoraResearchLab) [![LinkedIn](https://img.shields.io/badge/LinkedIn-NORA%20Research%20Lab-0A66C2?logo=linkedin)](https://www.linkedin.com/company/nora-research-lab) [![X](https://img.shields.io/badge/X-@noraresearchlab-000000?logo=x)](https://x.com/noraresearchlab) [![NORA Research Lab](https://img.shields.io/badge/Website-noraresearchlab.site-2ea44f)](https://noraresearchlab.site) [![NORA Earth Intelligence](https://img.shields.io/badge/Platform-noraearth.xyz-2ea44f)](https://noraearth.xyz)
