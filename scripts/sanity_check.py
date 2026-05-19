"""Confirma que tudo está funcionando."""
import sys
import pandas as pd
import numpy as np
import sklearn

print(f"Python:       {sys.version.split()[0]}")
print(f"pandas:       {pd.__version__}")
print(f"numpy:        {np.__version__}")
print(f"scikit-learn: {sklearn.__version__}")

df = pd.DataFrame({"cidade": ["Cabo Frio", "Niterói", "Rio"],
                   "preco_m2": [8500, 9200, 12000]})
print("\nPrimeiro DataFrame do ImobIA:")
print(df)
print(f"\nPreço médio: R$ {df['preco_m2'].mean():.2f}/m²")
