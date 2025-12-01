# analyze.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm

# ----------------------------
# 1. Read the cleaned World Happiness Report data
# ----------------------------
FILE = "preprocess_world_happiness.csv"   #
df = pd.read_csv(FILE)

print("Loaded dataset shape:", df.shape)
print(df.head())

# ----------------------------
# 2. Calculate the overall correlation coefficient (Pearson)
# ----------------------------
corr = df["ladder score"].corr(df["perceptions of corruption"])
print("\n📌 Pearson Correlation (Happiness vs Perceived Corruption):", corr)

# ----------------------------
# 3. Plot Scatter Plot + Regression Line
# ----------------------------
plt.figure(figsize=(8,6))
sns.regplot(
    data=df,
    x="perceptions of corruption",
    y="ladder score",
    scatter_kws={"alpha":0.5},
    line_kws={"color": "red"}
)
plt.title("Happiness vs Perceived Corruption (2015–2024)")
plt.xlabel("Perceptions of Corruption (Higher = More Corruption)")
plt.ylabel("Ladder Score (Happiness)")
plt.tight_layout()
plt.savefig("scatter_regression.png", dpi=300)
plt.show()
print("📊 Saved: scatter_regression.png")

# ----------------------------
# 4. Linear Regression (OLS)
# ----------------------------
X = df["perceptions of corruption"]
Y = df["ladder score"]

# Add constant term (intercept)
X = sm.add_constant(X)

model = sm.OLS(Y, X).fit()
print("\n OLS Regression Summary:\n")
print(model.summary())

# Save regression summary to a text file (for reporting)
with open("regression_summary.txt", "w") as f:
    f.write(model.summary().as_text())
print(" Saved: regression_summary.txt")

print("\n Analysis Completed.")
