# K-Means Clustering Project -- Facebook Live Dataset

## Project Overview

This project applies the **K-Means Clustering algorithm**, an
unsupervised machine learning technique, to group Facebook Live posts
based on their engagement characteristics.

The goal is to discover hidden patterns in Facebook post engagement and
create meaningful clusters of posts with similar interaction behaviour.

## Dataset

**Dataset Name:** Facebook Live Dataset (`Live.csv`)

The dataset contains information about Facebook posts, including
engagement metrics such as:

-   Number of reactions
-   Number of comments
-   Number of shares
-   Different reaction types (likes, loves, wows, hahas, sads, angrys)
-   Post type information (`status_type`)

## Objectives

-   Perform Exploratory Data Analysis (EDA) on Facebook post data.
-   Prepare engagement-based features for clustering.
-   Apply K-Means clustering to identify groups of similar posts.
-   Determine a suitable number of clusters using evaluation techniques.
-   Analyze and interpret cluster characteristics.

## Technologies Used

-   Python
-   Jupyter Notebook
-   Pandas
-   NumPy
-   Matplotlib
-   Seaborn
-   Scikit-learn

## Machine Learning Algorithm

### K-Means Clustering

K-Means is an unsupervised learning algorithm that groups data points
into K different clusters based on similarity.

The algorithm works by:

1.  Selecting K initial centroids.
2.  Assigning data points to the nearest centroid.
3.  Updating centroids based on cluster members.
4.  Repeating the process until clusters become stable.

## Data Preprocessing

The following preprocessing steps were performed:

-   Removed identifier and text-based columns:

    -   `status_id`
    -   `status_published`
    -   Redundant empty columns

-   Selected engagement features:

    -   `num_reactions`
    -   `num_comments`
    -   `num_shares`
    -   `num_likes`
    -   `num_loves`
    -   `num_wows`
    -   `num_hahas`
    -   `num_sads`
    -   `num_angrys`

-   Handled missing values using median values.

-   Applied `log1p()` transformation to reduce data skewness.

-   Standardized features using `StandardScaler`.

## Finding Optimal Number of Clusters

Two methods were used:

### 1. Elbow Method

The Elbow Method evaluates cluster compactness using inertia and helps
identify a suitable value of K.

### 2. Silhouette Score

The Silhouette Score measures how well each data point fits within its
assigned cluster.

Higher silhouette values indicate better-separated clusters.

## Model Implementation

The final K-Means model was trained using:

-   Algorithm: K-Means
-   Initialization: K-Means++
-   Random State: 42
-   Cluster labels generated for each Facebook post

## Cluster Analysis

After clustering:

-   Each post was assigned a cluster number.
-   Cluster sizes were analyzed.
-   Mean and median engagement values were calculated.
-   Clusters were interpreted based on engagement behaviour.

Example interpretations:

-   High engagement cluster: Posts receiving more reactions, comments,
    and shares.
-   Low engagement cluster: Posts receiving comparatively fewer
    interactions.

## Visualization

The project includes:

-   Distribution analysis of Facebook post types.
-   Elbow curve visualization.
-   Cluster size visualization.
-   PCA-based two-dimensional cluster visualization.
-   Post type composition analysis across clusters.

## Project Workflow

1.  Import required libraries.
2.  Load Facebook Live dataset.
3.  Perform Exploratory Data Analysis.
4.  Select relevant numerical features.
5.  Apply data transformation and scaling.
6.  Determine optimal cluster count.
7.  Train K-Means clustering model.
8.  Analyze generated clusters.
9.  Visualize results.
10. Interpret cluster behaviour.

## Conclusion

This project demonstrates how K-Means clustering can be used to analyze
Facebook post engagement patterns. By grouping posts with similar
engagement characteristics, organizations can better understand content
performance and user interaction behaviour.

## Future Improvements

-   Apply additional clustering algorithms such as DBSCAN or
    Hierarchical Clustering.
-   Include time-based engagement analysis.
-   Build a dashboard for interactive cluster exploration.
-   Develop recommendation strategies based on cluster behaviour.

## Author

Aditi Gawade

Artificial Intelligence and Data Science Engineering
