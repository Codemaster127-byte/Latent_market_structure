import numpy as np

def convert(df):
    df = df.drop(df.columns[0], axis=1)
    nat= df.to_numpy(dtype=np.float64,copy=True)

    np.set_printoptions(threshold=np.inf)
    print(nat)
    return nat

def cal_return_mat(mat):
    log_ret_mat=np.diff(np.log(mat),axis=0)
    return(log_ret_mat)


def rref(A, tol=None):
    M = A.astype(float).copy()
    m, n = M.shape
    
    if tol is None:
        tol = np.max(np.abs(M)) * max(m, n) * np.finfo(float).eps * 1e4

    pivot_cols = []
    row = 0

    for col in range(n):
        if row >= m:
            break
        best = np.argmax(np.abs(M[row:, col])) + row
        if abs(M[best, col]) < tol:
            continue
        M[[row, best]] = M[[best, row]]
        M[row] /= M[row, col]
        for r in range(m):
            if r != row and abs(M[r, col]) > tol:
                M[r] -= M[r, col] * M[row]
        pivot_cols.append(col)
        row += 1
    print(M)
    return M, pivot_cols, len(pivot_cols)


def linear_dependence(A):
    A_demeaned = A - A.mean(axis=0)  # remove per-asset drift
    R, pivot_cols, rank = rref(A_demeaned)
    
    all_cols = list(range(A.shape[1]))
    dependent_cols = [c for c in all_cols if c not in pivot_cols]
    
    return {
        "rank": rank,
        "pivot_cols": pivot_cols,       # independent assets
        "dependent_cols": dependent_cols # redundant assets
    }


def vector_space_analysis(A, tol=1e-10):

    rank = np.linalg.matrix_rank(A, tol=tol)

    U, S, Vt = np.linalg.svd(A)

    column_basis = U[:, :rank]


    row_basis = Vt[:rank, :]


    null_basis = Vt[rank:, :].T

    nullity = A.shape[1] - rank

    return {
        "rank": rank,
        "nullity": nullity,
        "column_basis": column_basis,
        "row_basis": row_basis,
        "null_basis": null_basis
    }

def print_vector_space_report(result):
    rank = result["rank"]
    nullity = result["nullity"]

    print("\n--- Vector Space Analysis ---")
    print(f"Rank: {rank}")
    print(f"Nullity: {nullity}")

    if nullity == 0:
        print("\nNull Space: Trivial (only zero vector)")
        print("→ No exact linear dependencies between stocks")

    print("\nColumn Space:")
    print(f"Dimension = {rank}")
    print("Number of independent stock behaviors")

    print("\nRow Space:")
    print(f"Dimension = {rank}")
    print("Independent temporal patterns")

    print("\n--- Interpretation ---")
    if nullity == 0:
        print("System is full rank → No exact redundancy")
    
    return