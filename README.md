# Z-score Heatmap Creator

Z-score Heatmap Creator is a Python tool for generating publication-ready heatmap visualizations from CSV data. This program reads CSV files containing time-series data for multiple subjects (e.g., mice), calculates z-scores, and creates high-resolution heatmap visualizations with customizable color scales, dimensions, and labels. It also supports generating separate colorbar images for publication use. Ideal for behavioral analysis, neuroscience research, and other fields requiring temporal heatmap visualization.

## Usage

```bash
python heatmap_creator_wmu.py input.csv [options]
```

### Options

*   `-o, --output`: Path to the output image file.
*   `-t, --title`: Title of the heatmap.
*   `--vmin`: Minimum value of the color scale.
*   `--vmax`: Maximum value of the color scale.
*   `--cmap`: Name of the colormap (default: 'YlOrRd').
*   `--width`: Width of the figure (default: 20).
*   `--height`: Height of the figure (default: 6).
*   `--dpi`: Resolution of the image (default: 300).
*   `--time-column`: Name of the time column (default: 'Time (s)').
*   `--mouse-prefix`: Prefix for mouse columns (default: 'Mouse').
*   `--xtick-interval`: Interval for x-axis labels (default: 500).
*   `--colorbar`: Generate a separate colorbar image.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
