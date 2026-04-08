import kiteconnect as kc
import pandas as pd
from src.connection import *
from src.data_pipeline import *
from src.lineral_alg import *
from src.eigen import *
from src.ortho import *


def main():
    print("running project")
    kite=initiation()
    df1=map_data()
    get_2_year_data(df1,kite)
    df2=merger_Via_Date()
    df2.to_csv("data/unprocessed_price_close.csv")
    mat=convert(df2)
    mat = mat[~np.isnan(mat).any(axis=1)]
    A=cal_return_mat(mat)
    res=linear_dependence(A)
    print(res)
    res1=vector_space_analysis(A)
    print_vector_space_report(res1)

    A = A - np.mean(A, axis=0)

    eigvals_norm, eigvecs = eigen_diagnostics(A)

    print_diagnostics(eigvals_norm,eigvecs)



    


 



if __name__ == "__main__":
    main()