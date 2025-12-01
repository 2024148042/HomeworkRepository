import pandas as pd
import glob
import os

# 1️⃣ 设置数据路径
path = "/Users/qin/Downloads/archive"  
files = glob.glob(os.path.join(path, "world_happiness_*.csv"))

# 2️⃣ 读取并合并所有年度文件
df_list = []
for f in sorted(files):
    temp = pd.read_csv(f, sep=None, engine='python', on_bad_lines='skip')
    temp["Year"] = int(os.path.basename(f).split("_")[-1].split(".")[0])  
    df_list.append(temp)
df = pd.concat(df_list, ignore_index=True)
print(sorted(list(df.columns))[:30])


# 3️⃣ 标准化列名（全面适配2015–2024）
df.columns = df.columns.str.strip().str.lower()

rename_map = {
    # 幸福分数（避免重复）
    "happiness score": "ladder score",
    "happiness.score": "ladder score",
    "score": "ladder score",
    "life ladder": "ladder score",

    # 国家与地区
    "country": "country",
    "country or region": "country",
    "region": "regional indicator",
    "regional indicator": "regional indicator",

    # GDP / 经济
    "economy (gdp per capita)": "gdp per capita",
    "economy..gdp.per.capita.": "gdp per capita",
    "logged gdp per capita": "gdp per capita",
    "gdp per capita": "gdp per capita",

    # 健康与预期寿命
    "health (life expectancy)": "healthy life expectancy",
    "health..life.expectancy.": "healthy life expectancy",
    "healthy life expectancy": "healthy life expectancy",

    # 自由与社会支持
    "freedom": "freedom to make life choices",
    "freedom to make life choices": "freedom to make life choices",
    "social support": "social support",

    # 慷慨与腐败感知
    "generosity": "generosity",
    "trust (government corruption)": "perceptions of corruption",
    "perceptions of corruption": "perceptions of corruption",
    "corruption": "perceptions of corruption",
    "perceived corruption": "perceptions of corruption",
}
df.rename(columns=rename_map, inplace=True)

# 🚫 删除重复列
df = df.loc[:, ~df.columns.duplicated()]


# 4️⃣ 保留主要列（部分年份缺少某些列时自动忽略）
keep_cols = []
for c in [
    "country", "year", "ladder score", "gdp per capita", "social support",
    "healthy life expectancy", "freedom to make life choices",
    "generosity", "perceptions of corruption"
]:
    if c in df.columns:
        keep_cols.append(c)
df = df[keep_cols].copy()


# 5️⃣ 删除缺失值和重复行
df = df.dropna(subset=["ladder score", "perceptions of corruption"])
df = df.drop_duplicates(subset=["country", "year"])

# 6️⃣ 类型转换
df["year"] = df["year"].astype(int)

# 7️⃣ 保存清洗结果
output_path = os.path.join(path, "world_happiness_cleaned.csv")
df.to_csv(output_path, index=False)

print("✅ Cleaned dataset saved to:", output_path)
print("📊 Rows:", len(df))
print("📄 Columns:", list(df.columns))

