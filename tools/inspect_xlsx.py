"""Inspect structure of the supplied Excel sources."""
import sys
sys.stdout.reconfigure(encoding="utf-8")
import pandas as pd

FILES = {
    "Temperature": r"D:\Download\Temperature.xlsx",
    "Carbon": r"D:\Download\price-carbon.xlsx",
    "GLC Nominal": r"D:\Download\latest-yield-curve-data\GLC Nominal daily data current month.xlsx",
    "GLC Inflation": r"D:\Download\latest-yield-curve-data\GLC Inflation daily data current month.xlsx",
}

def clean(x):
    s = str(x)
    return s.encode("ascii", "replace").decode("ascii")

for name, path in FILES.items():
    print("\n" + "=" * 70)
    print(name, "->", path)
    try:
        xl = pd.ExcelFile(path)
        print("sheets:", xl.sheet_names)
        for sh in xl.sheet_names[:6]:
            df = xl.parse(sh, header=None, nrows=10)
            print(f"\n--- sheet '{sh}' shape-peek {df.shape} : first 10 rows x 14 cols ---")
            sub = df.iloc[:10, :14].applymap(clean)
            print(sub.to_string(max_colwidth=16))
    except Exception as e:
        print("ERROR:", clean(repr(e)))
