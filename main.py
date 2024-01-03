from __future__ import division

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from numpy.compat import basestring
from sklearn.cluster import KMeans
from sklearn.mixture import GaussianMixture
from sklearn.preprocessing import StandardScaler

filename = "data/asu.tsv"
df = pd.read_table(
    filename,
    skiprows=54,
    sep=";",
    header=None,
    index_col=0,
    names=["HIP", "Vmag", "Plx", "B-V", "SpType"],
    skipfooter=1,
    engine="python",
)

# Use lambda function to clean the dataframe
df_clean = df.map(lambda x: np.nan if isinstance(x, basestring) and x.isspace() else x)
df_clean = df_clean.dropna()

# Convert columns to the appropriate data types
df_clean["Vmag"] = df_clean["Vmag"].astype(float)
df_clean["Plx"] = df_clean["Plx"].astype(float)
df_clean["B-V"] = df_clean["B-V"].astype(float)

# Add a new column with the absolute magnitude
df_clean["M_V"] = df_clean["Vmag"] + 5 * np.log10(df_clean["Plx"] / 100.0)

# Check for and handle infinite values
df_clean.replace([np.inf, -np.inf], np.nan, inplace=True)
df_clean.dropna(inplace=True)

# Select the features for clustering
features = ["B-V", "M_V"]

# Extract the selected features from the DataFrame
X = df_clean[features]

# Check the summary statistics
print(df_clean.describe())

# Scale or normalize the data
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Choose the number of clusters (you may adjust this based on your needs)
num_clusters = 4

# Apply Dirichlet Process Gaussian Mixture Model
dpgmm = GaussianMixture(
    n_components=num_clusters,
    random_state=42,
    init_params="kmeans",
    max_iter=100,
    tol=1e-3,
)
df_clean["Cluster"] = dpgmm.fit_predict(X_scaled)

# Plot the clusters
fig, ax = plt.subplots(figsize=(8, 10))

for cluster in range(num_clusters):
    cluster_data = df_clean[df_clean["Cluster"] == cluster]
    ax.scatter(
        cluster_data["B-V"], cluster_data["M_V"], label=f"Cluster {cluster}", s=1
    )

ax.set_xlim(-0.5, 2.5)
ax.set_ylim(15, -15)
ax.grid()
ax.set_title("Clusters in H-R Diagram using DPGMM")

ax.title.set_fontsize(20)
ax.set_xlabel("Color index B-V")
ax.xaxis.label.set_fontsize(20)
ax.set_ylabel("Absolute magnitude")
ax.yaxis.label.set_fontsize(20)

ax.legend()
plt.show()

# Apply KMeans clustering
kmeans = KMeans(n_clusters=num_clusters, random_state=42)
df_clean["Cluster"] = kmeans.fit_predict(X_scaled)

fig, ax = plt.subplots(figsize=(8, 10))

for cluster in range(num_clusters):
    cluster_data = df_clean[df_clean["Cluster"] == cluster]
    ax.scatter(
        cluster_data["B-V"], cluster_data["M_V"], label=f"Cluster {cluster}", s=1
    )

ax.set_xlim(-0.5, 2.5)
ax.set_ylim(15, -15)
ax.grid()
ax.set_title("Clusters in H-R Diagram using KMEANS")

ax.title.set_fontsize(20)
ax.set_xlabel("Color index B-V")
ax.xaxis.label.set_fontsize(20)
ax.set_ylabel("Absolute magnitude")
ax.yaxis.label.set_fontsize(20)

ax.legend()
plt.show()
