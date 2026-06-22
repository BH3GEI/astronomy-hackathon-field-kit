#!/usr/bin/env python3
"""
NASA Exoplanet Archive 数据探索脚本
从notebook转换而来，用于直接运行
"""

import pandas as pd
import matplotlib
matplotlib.use('Agg')  # 非交互式后端
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from astroquery.nasa_exoplanet_archive import NasaExoplanetArchive
import os

# 创建输出目录
os.makedirs('../data', exist_ok=True)
os.makedirs('../figures', exist_ok=True)

# 设置图表风格
sns.set_theme(style="whitegrid")
print("=" * 50)
print("NASA Exoplanet Archive 数据探索")
print("=" * 50)

# ============================================================
# 1. 数据获取
# ============================================================
print("\n[1/8] 正在查询NASA Exoplanet Archive...")

query_columns = """
    pl_name, hostname, discoverymethod, disc_year, disc_facility,
    pl_orbper, pl_rade, pl_bmasse, pl_eqt,
    st_teff, st_rad, st_mass, st_logg,
    sy_dist, sy_vmag, sy_kmag
"""

try:
    table = NasaExoplanetArchive.query_criteria(
        table="pscomppars",
        select=query_columns
    )
    df = table.to_pandas()
    print(f"✓ 查询完成! 共获取 {len(df)} 条记录")
except Exception as e:
    print(f"✗ 查询失败: {e}")
    print("尝试使用备用方法...")
    # 备用方法：直接下载CSV
    import urllib.request
    url = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=select+pl_name,hostname,discoverymethod,disc_year,disc_facility,pl_orbper,pl_rade,pl_bmasse,pl_eqt,st_teff,st_rad,st_mass,st_logg,sy_dist,sy_vmag,sy_kmag+from+pscomppars&format=csv"
    df = pd.read_csv(url)
    print(f"✓ 备用方法成功! 共获取 {len(df)} 条记录")

# ============================================================
# 2. 基本统计
# ============================================================
print("\n[2/8] 数据集概览:")
print(f"  确认行星总数: {len(df)}")
print(f"  独特恒星系统: {df['hostname'].nunique()}")
print(f"  发现年份范围: {df['disc_year'].min():.0f} - {df['disc_year'].max():.0f}")
print(f"  缺失值统计:")
for col in df.columns:
    missing = df[col].isnull().sum()
    if missing > 0:
        print(f"    {col}: {missing} ({missing/len(df)*100:.1f}%)")

# ============================================================
# 3. 发现方法分析
# ============================================================
print("\n[3/8] 发现方法分析:")
method_counts = df['discoverymethod'].value_counts()
print(method_counts)

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# 饼图
axes[0].pie(method_counts.values, labels=method_counts.index, autopct='%1.1f%%', startangle=90)
axes[0].set_title('Distribution of Discovery Methods', fontsize=14)

# 柱状图
method_counts.plot(kind='bar', ax=axes[1], color=sns.color_palette("viridis", len(method_counts)))
axes[1].set_title('Number of Planets by Discovery Method', fontsize=14)
axes[1].set_xlabel('Discovery Method')
axes[1].set_ylabel('Count')
axes[1].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig('../figures/01_discovery_methods.png', dpi=150, bbox_inches='tight')
plt.close()
print("✓ 图表已保存: figures/01_discovery_methods.png")

# ============================================================
# 4. 发现时间趋势
# ============================================================
print("\n[4/8] 发现时间趋势分析...")
yearly_counts = df.groupby('disc_year').size().reset_index(name='count')
yearly_method = df.groupby(['disc_year', 'discoverymethod']).size().unstack(fill_value=0)

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# 总发现趋势
axes[0].plot(yearly_counts['disc_year'], yearly_counts['count'], 'b-o', linewidth=2)
axes[0].fill_between(yearly_counts['disc_year'], yearly_counts['count'], alpha=0.3)
axes[0].set_title('Exoplanet Discoveries by Year', fontsize=14)
axes[0].set_xlabel('Year')
axes[0].set_ylabel('Number of Discoveries')
axes[0].grid(True, alpha=0.3)

# 按方法堆叠
yearly_method.plot(kind='area', stacked=True, ax=axes[1], alpha=0.7)
axes[1].set_title('Discoveries by Method Over Time', fontsize=14)
axes[1].set_xlabel('Year')
axes[1].set_ylabel('Count')
axes[1].legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)

plt.tight_layout()
plt.savefig('../figures/02_discovery_trends.png', dpi=150, bbox_inches='tight')
plt.close()
print("✓ 图表已保存: figures/02_discovery_trends.png")

peak_year = yearly_counts.loc[yearly_counts['count'].idxmax()]
print(f"  发现高峰年份: {peak_year['disc_year']:.0f}年 ({peak_year['count']}颗行星)")

# ============================================================
# 5. 行星参数分布
# ============================================================
print("\n[5/8] 行星参数分布分析...")
df_clean = df.dropna(subset=['pl_rade', 'pl_eqt']).copy()
print(f"  有效数据: {len(df_clean)} 条记录")

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# 1. 行星半径分布
axes[0, 0].hist(df_clean['pl_rade'].clip(0, 20), bins=50, color='steelblue', edgecolor='black')
axes[0, 0].set_title('Planet Radius Distribution', fontsize=14)
axes[0, 0].set_xlabel('Radius (Earth Radii)')
axes[0, 0].set_ylabel('Count')
axes[0, 0].axvline(x=1, color='red', linestyle='--', label='Earth')
axes[0, 0].axvline(x=11.2, color='orange', linestyle='--', label='Jupiter')
axes[0, 0].legend()

# 2. 平衡温度分布
axes[0, 1].hist(df_clean['pl_eqt'].clip(0, 3000), bins=50, color='coral', edgecolor='black')
axes[0, 1].set_title('Planet Equilibrium Temperature Distribution', fontsize=14)
axes[0, 1].set_xlabel('Temperature (K)')
axes[0, 1].set_ylabel('Count')
axes[0, 1].axvline(x=255, color='blue', linestyle='--', label='Earth (255K)')
axes[0, 1].legend()

# 3. 轨道周期分布 (对数坐标)
df_period = df.dropna(subset=['pl_orbper'])
axes[1, 0].hist(np.log10(df_period['pl_orbper'].clip(0.1, 10000)), bins=50, color='green', edgecolor='black')
axes[1, 0].set_title('Orbital Period Distribution (log scale)', fontsize=14)
axes[1, 0].set_xlabel('log10(Period / days)')
axes[1, 0].set_ylabel('Count')

# 4. 距离分布
df_dist = df.dropna(subset=['sy_dist'])
axes[1, 1].hist(df_dist['sy_dist'].clip(0, 1000), bins=50, color='purple', edgecolor='black')
axes[1, 1].set_title('Distance Distribution', fontsize=14)
axes[1, 1].set_xlabel('Distance (parsecs)')
axes[1, 1].set_ylabel('Count')

plt.tight_layout()
plt.savefig('../figures/03_parameter_distributions.png', dpi=150, bbox_inches='tight')
plt.close()
print("✓ 图表已保存: figures/03_parameter_distributions.png")

# ============================================================
# 6. 宜居带行星筛选
# ============================================================
print("\n[6/8] 宜居带行星筛选...")
habitable = df_clean[
    (df_clean['pl_eqt'] >= 200) &
    (df_clean['pl_eqt'] <= 300) &
    (df_clean['pl_rade'] >= 0.5) &
    (df_clean['pl_rade'] <= 2.0)
].copy()

print(f"  宜居带候选行星: {len(habitable)} 颗")
if len(habitable) > 0:
    print("\n  Top 10 最近的宜居带候选:")
    habitable_sorted = habitable.sort_values('sy_dist')
    for idx, row in habitable_sorted.head(10).iterrows():
        print(f"    {row['pl_name']}: 半径={row['pl_rade']:.2f}R⊕, 温度={row['pl_eqt']:.0f}K, 距离={row['sy_dist']:.1f}pc")

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# 半径 vs 温度散点图
scatter = axes[0].scatter(
    df_clean['pl_eqt'],
    df_clean['pl_rade'],
    c=np.log10(df_clean['sy_dist'].clip(1, 10000)),
    cmap='viridis',
    alpha=0.5,
    s=10
)
axes[0].axhspan(0.5, 2.0, alpha=0.2, color='green', label='Habitable Radius Range')
axes[0].axvspan(200, 300, alpha=0.2, color='blue', label='Habitable Temp Range')
axes[0].set_xlabel('Equilibrium Temperature (K)', fontsize=12)
axes[0].set_ylabel('Planet Radius (Earth Radii)', fontsize=12)
axes[0].set_title('Planet Radius vs Temperature', fontsize=14)
axes[0].set_xlim(0, 3000)
axes[0].set_ylim(0, 20)
axes[0].legend(loc='upper right')
plt.colorbar(scatter, ax=axes[0], label='log10(Distance/pc)')

# 宜居带行星按距离排序
if len(habitable) > 0:
    habitable_near = habitable.sort_values('sy_dist').head(20)
    axes[1].barh(range(len(habitable_near)), habitable_near['sy_dist'], color='teal')
    axes[1].set_yticks(range(len(habitable_near)))
    axes[1].set_yticklabels(habitable_near['pl_name'], fontsize=9)
    axes[1].set_xlabel('Distance (parsecs)', fontsize=12)
    axes[1].set_title('Nearest Habitable Zone Candidates', fontsize=14)
    axes[1].invert_yaxis()

plt.tight_layout()
plt.savefig('../figures/04_habitable_zone.png', dpi=150, bbox_inches='tight')
plt.close()
print("✓ 图表已保存: figures/04_habitable_zone.png")

# ============================================================
# 7. 恒星参数分析 (简化赫罗图)
# ============================================================
print("\n[7/8] 恒星参数分析...")
df_stars = df.dropna(subset=['st_teff', 'st_rad']).copy()
print(f"  有恒星参数的记录: {len(df_stars)} 条")

fig, ax = plt.subplots(figsize=(10, 8))

# 计算光度代理 (R^2 * T^4)
df_stars['luminosity_proxy'] = (df_stars['st_rad'] ** 2) * ((df_stars['st_teff'] / 5778) ** 4)

scatter = ax.scatter(
    df_stars['st_teff'],
    np.log10(df_stars['luminosity_proxy'].clip(1e-4, 1e6)),
    c=df_stars['st_teff'],
    cmap='RdYlBu_r',
    alpha=0.5,
    s=20
)

# 标记太阳
ax.scatter(5778, 0, color='yellow', s=200, marker='*', edgecolors='black', linewidth=2, label='Sun', zorder=5)

ax.set_xlabel('Stellar Effective Temperature (K)', fontsize=12)
ax.set_ylabel('log10(Luminosity / L_sun)', fontsize=12)
ax.set_title('Simplified Hertzsprung-Russell Diagram\n(Host Stars of Exoplanets)', fontsize=14)
ax.invert_xaxis()  # HR图惯例：高温在左
ax.legend()
plt.colorbar(scatter, label='Temperature (K)')
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('../figures/05_hr_diagram.png', dpi=150, bbox_inches='tight')
plt.close()
print("✓ 图表已保存: figures/05_hr_diagram.png")

# ============================================================
# 8. 多行星系统分析
# ============================================================
print("\n[8/8] 多行星系统分析...")
planets_per_star = df.groupby('hostname').size().reset_index(name='planet_count')
system_counts = planets_per_star['planet_count'].value_counts().sort_index()

print("  多行星系统统计:")
for count, num_systems in system_counts.items():
    print(f"    {count}颗行星的系统: {num_systems}个")

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# 行星数量分布
axes[0].bar(system_counts.index, system_counts.values, color='teal', edgecolor='black')
axes[0].set_xlabel('Number of Planets per System', fontsize=12)
axes[0].set_ylabel('Number of Systems', fontsize=12)
axes[0].set_title('Planets per Star System', fontsize=14)
axes[0].set_xticks(range(1, max(system_counts.index)+1))

# 找到行星最多的系统
top_systems = planets_per_star.nlargest(10, 'planet_count')
axes[1].barh(range(len(top_systems)), top_systems['planet_count'], color='coral')
axes[1].set_yticks(range(len(top_systems)))
axes[1].set_yticklabels(top_systems['hostname'], fontsize=10)
axes[1].set_xlabel('Number of Planets', fontsize=12)
axes[1].set_title('Top 10 Multi-Planet Systems', fontsize=14)
axes[1].invert_yaxis()

plt.tight_layout()
plt.savefig('../figures/06_multi_planet_systems.png', dpi=150, bbox_inches='tight')
plt.close()
print("✓ 图表已保存: figures/06_multi_planet_systems.png")

# ============================================================
# 9. 数据导出
# ============================================================
print("\n" + "=" * 50)
print("数据导出:")
output_path = "../data/exoplanets_processed.csv"
df.to_csv(output_path, index=False)
print(f"✓ 全部数据已导出: {output_path} ({len(df)} 条)")

habitable_path = "../data/habitable_candidates.csv"
habitable.to_csv(habitable_path, index=False)
print(f"✓ 宜居带候选已导出: {habitable_path} ({len(habitable)} 条)")

# ============================================================
# 10. 数据摘要
# ============================================================
print("\n" + "=" * 50)
print("数据集摘要 (可用于Agent上下文):")
summary = {
    "total_planets": len(df),
    "unique_systems": df['hostname'].nunique(),
    "year_range": f"{df['disc_year'].min():.0f}-{df['disc_year'].max():.0f}",
    "habitable_candidates": len(habitable),
    "discovery_methods": df['discoverymethod'].nunique(),
    "top_method": df['discoverymethod'].mode()[0],
}
if len(habitable) > 0:
    summary["nearest_habitable"] = habitable.sort_values('sy_dist').iloc[0]['pl_name']

for k, v in summary.items():
    print(f"  {k}: {v}")

print("\n" + "=" * 50)
print("探索完成!")
print("=" * 50)
