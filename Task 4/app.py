import os
import numpy as np
import pandas as pd
from flask import Flask, render_template_string, request
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

app = Flask(__name__)

# Inline HTML/Bootstrap Dashboard Template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Facebook Live Clustering Dashboard</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body { background-color: #f8f9fa; }
        .card { border: none; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
        .sidebar { background: white; min-height: 100vh; border-right: 1px solid #dee2e6; }
    </style>
</head>
<body>

<div class="container-fluid">
    <div class="row">
        <!-- Sidebar Controls -->
        <div class="col-md-3 p-4 sidebar">
            <h3 class="fw-bold text-primary mb-4">FB Analytics</h3>
            <p class="text-muted small">Unsupervised K-Means clustering dashboard for Facebook Live engagement data.</p>
            <hr>
            
            <form method="POST" action="/">
                <div class="mb-3">
                    <label for="n_clusters" class="form-label fw-semibold">Number of Clusters (k): <span id="kVal">{{ n_clusters }}</span></label>
                    <input type="range" class="form-range" min="2" max="6" id="n_clusters" name="n_clusters" value="{{ n_clusters }}" oninput="document.getElementById('kVal').innerText = this.value">
                </div>

                <div class="mb-4">
                    <label for="status_type" class="form-label fw-semibold">Filter Status Type:</label>
                    <select class="form-select" id="status_type" name="status_type">
                        {% for st in status_types %}
                            <option value="{{ st }}" {% if st == selected_status %}selected{% endif %}>{{ st }}</option>
                        {% endfor %}
                    </select>
                </div>

                <button type="submit" class="btn btn-primary w-100 py-2 shadow-sm">Apply Filters</button>
            </form>
        </div>

        <!-- Main Dashboard Content -->
        <div class="col-md-9 p-4">
            <div class="d-flex justify-content-between align-items-center mb-4">
                <h2 class="fw-bold text-dark">Clustering & Engagement Dashboard</h2>
                <span class="badge bg-success px-3 py-2 fs-6">Model Active</span>
            </div>

            <!-- KPI Metric Cards -->
            <div class="row g-3 mb-4">
                <div class="col-md-3">
                    <div class="card p-3 bg-white border-start border-primary border-4">
                        <h6 class="text-muted">Total Posts</h6>
                        <h3 class="fw-bold mb-0">{{ total_posts }}</h3>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card p-3 bg-white border-start border-success border-4">
                        <h6 class="text-muted">Avg Reactions</h6>
                        <h3 class="fw-bold mb-0">{{ avg_reactions }}</h3>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card p-3 bg-white border-start border-warning border-4">
                        <h6 class="text-muted">Avg Comments</h6>
                        <h3 class="fw-bold mb-0">{{ avg_comments }}</h3>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card p-3 bg-white border-start border-danger border-4">
                        <h6 class="text-muted">Avg Shares</h6>
                        <h3 class="fw-bold mb-0">{{ avg_shares }}</h3>
                    </div>
                </div>
            </div>

            <!-- Charts Section -->
            <div class="row g-4">
                <div class="col-md-6">
                    <div class="card p-4">
                        <h5 class="fw-bold mb-3">Cluster Distribution</h5>
                        <canvas id="barChart" height="200"></canvas>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="card p-4">
                        <h5 class="fw-bold mb-3">PCA Cluster Separation (2D)</h5>
                        <canvas id="scatterChart" height="200"></canvas>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<!-- Chart Scripts -->
<script>
    const barCtx = document.getElementById('barChart').getContext('2d');
    new Chart(barCtx, {
        type: 'bar',
        data: {
            labels: {{ cluster_labels | safe }},
            datasets: [{
                label: 'Number of Posts per Cluster',
                data: {{ cluster_values | safe }},
                backgroundColor: 'rgba(54, 162, 235, 0.7)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1,
                borderRadius: 5
            }]
        },
        options: { responsive: true, scales: { y: { beginAtZero: true } } }
    });

    const scatterCtx = document.getElementById('scatterChart').getContext('2d');
    const scatterDatasets = {{ scatter_data | safe }};
    const colors = ['#ff6384', '#36a2eb', '#cc65fe', '#ffce56', '#4bc0c0', '#9966ff'];
    
    scatterDatasets.forEach((ds, index) => {
        ds.backgroundColor = colors[index % colors.length];
        ds.pointRadius = 4;
    });

    new Chart(scatterCtx, {
        type: 'scatter',
        data: { datasets: scatterDatasets },
        options: {
            responsive: true,
            plugins: { legend: { position: 'top' } },
            scales: {
                x: { title: { display: true, text: 'PCA Component 1' } },
                y: { title: { display: true, text: 'PCA Component 2' } }
            }
        }
    });
</script>

</body>
</html>
"""

def load_and_process_data(n_clusters=3):
    df = pd.read_csv("Live (1).csv")
    drop_cols = ["status_id", "status_published", "Column1", "Column2", "Column3", "Column4"]
    data = df.drop(columns=[col for col in drop_cols if col in df.columns], errors='ignore')
    
    features = [
        "num_reactions", "num_comments", "num_shares",
        "num_likes", "num_loves", "num_wows",
        "num_hahas", "num_sads", "num_angrys"
    ]
    
    X_raw = data[features].copy()
    X_log = np.log1p(X_raw)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_log)
    
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    clusters = kmeans.fit_predict(X_scaled)
    data['Cluster'] = clusters
    
    pca = PCA(n_components=2, random_state=42)
    pca_coords = pca.fit_transform(X_scaled)
    data['PCA1'] = pca_coords[:, 0]
    data['PCA2'] = pca_coords[:, 1]
    
    return data

@app.route('/', methods=['GET', 'POST'])
def index():
    n_clusters = int(request.form.get('n_clusters', 3))
    selected_status = request.form.get('status_type', 'All')
    
    data = load_and_process_data(n_clusters=n_clusters)
    
    if selected_status != 'All':
        filtered_data = data[data['status_type'] == selected_status]
    else:
        filtered_data = data
        
    total_posts = int(len(filtered_data))
    avg_reactions = float(filtered_data['num_reactions'].mean())
    avg_comments = float(filtered_data['num_comments'].mean())
    avg_shares = float(filtered_data['num_shares'].mean())
    
    cluster_counts = filtered_data['Cluster'].value_counts().sort_index().to_dict()
    cluster_labels = [f"Cluster {k}" for k in cluster_counts.keys()]
    cluster_values = list(cluster_counts.values())
    
    scatter_data = []
    for cluster_id in range(n_clusters):
        cluster_subset = filtered_data[filtered_data['Cluster'] == cluster_id]
        points = [{"x": float(row['PCA1']), "y": float(row['PCA2'])} for _, row in cluster_subset.iterrows()]
        scatter_data.append({
            "label": f"Cluster {cluster_id}",
            "data": points
        })

    status_types = ['All'] + list(data['status_type'].unique())

    return render_template_string(
        HTML_TEMPLATE,
        total_posts=total_posts,
        avg_reactions=round(avg_reactions, 2),
        avg_comments=round(avg_comments, 2),
        avg_shares=round(avg_shares, 2),
        cluster_labels=cluster_labels,
        cluster_values=cluster_values,
        scatter_data=scatter_data,
        status_types=status_types,
        selected_status=selected_status,
        n_clusters=n_clusters
    )

if __name__ == '__main__':
    app.run(debug=True)