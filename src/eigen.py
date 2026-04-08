import numpy as np

def eigen_diagnostics(A):
 
    # Step 1: Covariance-like matrix
    m = A.shape[0]
    C = (A.T @ A) / m

    # Step 2: Eigen decomposition
    eigvals, eigvecs = np.linalg.eig(C)

    # Step 3: Sort in descending order
    idx = np.argsort(eigvals)[::-1]
    eigvals = eigvals[idx]
    eigvecs = eigvecs[:, idx]

    # Step 4: Normalize eigenvalues
    eigvals_norm = eigvals / np.sum(eigvals)

    # Step 5: Cumulative variance

    return eigvals_norm, eigvecs


def print_diagnostics(eigvals_norm,eigvecs ,top_k=10):
    print("\nTop Eigenvalues:")
    for i in range(min(top_k, len(eigvals_norm))):
        print(f"λ{i+1}: {eigvals_norm[i]:.4f}")

    print("\nEigen Vectors")
    for i in range(min(top_k, len(eigvecs))):
        print(f"{i+1} components: {eigvecs[i]}")
