import numpy as np

def eigen_diagnostics(A):
 
    m = A.shape[0]
    C = (A.T @ A) / m

    eigvals, eigvecs = np.linalg.eig(C)

    idx = np.argsort(eigvals)[::-1]
    eigvals = eigvals[idx]
    eigvecs = eigvecs[:, idx]

    eigvals_norm = eigvals / np.sum(eigvals)

    return eigvals_norm, eigvecs


def print_diagnostics(eigvals_norm,eigvecs ,top_k=10):
    print("\nTop Eigenvalues:")
    for i in range(min(top_k, len(eigvals_norm))):
        print(f"λ{i+1}: {eigvals_norm[i]:.4f}")

    print("\nEigen Vectors")
    for i in range(min(top_k, len(eigvecs))):
        print(f"{i+1} components: {eigvecs[:,i]}")
