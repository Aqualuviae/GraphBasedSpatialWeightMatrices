
# Graph-Based Spatial Weight Matrices (GBSWM) Project

## Project Overview

This project implements a graph-based spatial weight matrix (SWM) approach to improve the accuracy of spatial econometric models in urban studies. Using shortest path algorithms on urban street networks, the graph-based SWM aims to capture spatial interactions more effectively compared to traditional distance-based SWMs. The methodology and implementation are detailed in the paper "Optimizing Spatial Weight Matrices in Spatial Econometrics: A Graph-Theoretic Approach Based on Shortest Path Algorithms" by Y. Song and A. Cibin (2024), which is included in the project directory.

## Project Structure

```plaintext
GraphBasedSpatialWeightMatrices/
├── data/ (External Link)
│   └── [Google Drive Data Folder](https://drive.google.com/drive/folders/1ps9J-7VWHT5K7ePWXEboW1x9wvuQdGb2?usp=sharing)
├── notebooks/
│   └── Graph-Based Spatial Weight Matrices.ipynb
├── output/
│   ├── Complaint_Correlation_Matrix.png
│   ├── Flowcharts.png
│   ├── NYC_Community_District_and_Road_Network_Map.png
│   ├── Shooting_Correlation_Matrix.png
│   ├── Summons_Correlation_Matrix.png
│   ├── Weighted_Network_Graph_1.png
│   └── Weighted_Network_Graph_2.png
├── scripts/
│   ├── __init__.py
│   ├── main.py
│   ├── data_loading.py
│   ├── spatial_weights.py
│   └── utils.py
├── requirements.txt
├── README.md
└── Song_Y_Cibin_A_2024_Optimizing_Spatial_Weight_Matrices.pdf
```

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/Aqualuviae/GraphBasedSpatialWeightMatrices.git
   cd GraphBasedSpatialWeightMatrices
   ```

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

To run the project, execute the `main.py` script:

   ```bash
   python scripts/main.py
   ```

This script performs the following steps:
1. Loads and aligns spatial data from the provided data files (downloaded separately from the Google Drive link).
2. Generates a graph-based spatial weight matrix (GBSWM) based on the specified method.
3. Saves the output results, including figures and matrices, in the `output/` directory.

## Data Sources

The data required for this project is available for download from the following link:
- **[Google Drive Data Folder](https://drive.google.com/drive/folders/1ps9J-7VWHT5K7ePWXEboW1x9wvuQdGb2?usp=sharing)**

Download the contents and place them in a local `data/` folder at the root of this project.

## Results

Output files are saved in the `output/` directory and include:
- **Correlation Matrices**: Visual correlation matrices for different incident types, such as complaints, shootings, and summonses.
- **Network Graphs**: Visualizations of the generated weighted network graphs, which illustrate spatial relationships.

## Reference

- **Song, Y., & Cibin, A.** (2024). *Optimizing Spatial Weight Matrices in Spatial Econometrics: A Graph-Theoretic Approach Based on Shortest Path Algorithms*. International Review for Spatial Planning and Sustainable Development.
