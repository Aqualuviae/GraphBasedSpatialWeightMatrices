import numpy as np

def save_matrix(matrix, file_path):
    """Save matrix to CSV."""
    np.savetxt(file_path, matrix, delimiter=",")

def load_matrix(file_path):
    """Load matrix from CSV."""
    return np.loadtxt(file_path, delimiter=",")
