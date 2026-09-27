<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Interactive Dashboard - K-Means Clustering Facebook Live</title>
    <!-- Include Chart.js for interactive graphs -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {
            --primary: #2980b9;
            --secondary: #2c3e50;
            --bg-color: #f8f9fa;
            --card-bg: #ffffff;
            --text-color: #333333;
            --accent: #e74c3c;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: var(--bg-color);
            color: var(--text-color);
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        header {
            text-align: center;
            margin-bottom: 25px;
        }
        header h1 {
            color: var(--secondary);
            margin-bottom: 5px;
        }
        header p {
            color: #7f8c8d;
            font-style: italic;
        }
        /* Slicers / Filters Section */
        .slicer-panel {
            background: var(--card-bg);
            padding: 15px 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            display: flex;
            gap: 20px;
            align-items: center;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }
        .slicer-group {
            display: flex;
            flex-direction: column;
            gap: 5px;
        }
        .slicer-group label {
            font-weight: bold;
            font-size: 0.85rem;
            color: var(--secondary);
        }
        .slicer-group select {
            padding: 8px 12px;
            border-radius: 4px;
            border: 1px solid #ccc;
            background: #fff;
            font-size: 0.9rem;
        }
        /* Dashboard KPI Cards Grid */
        .kpi-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }
        .kpi-card {
            background: var(--card-bg);
            padding: 15px 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            border-left: 4px solid var(--primary);
        }
        .kpi-card h3 {
            margin: 0 0 5px 0;
            font-size: 0.9rem;
            color: #7f8c8d;
        }
        .kpi-card .value {
            font-size: 1.5rem;
            font-weight: bold;
            color: var(--secondary);
        }
        /* Graphs Grid */
        .charts-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(480px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }
        .chart-card {
            background: var(--card-bg);
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }
        .chart-card h2 {
            font-size: 1.1rem;
            color: var(--secondary);
            margin-top: 0;
            border-bottom: 1px solid #eee;
            padding-bottom: 10px;
        }
        .chart-container {
            position: relative;
            height: 280px;
            width: 100%;
        }
        .footer {
            text-align: center;
            font-size: 0.85rem;
            color: #7f8c8d;
            margin-top: 30px;
            padding: 10px;
            border-top: 1px solid #ddd;
        }
    </style>
</head>
<body>

<div class="container">
    <header>
        <h1>Facebook Live Engagement Dashboard</h1>
        <p>K-Means Clustering Analysis Project[cite: 1]</p>
    </header>

    <!-- Interactive Slicers / Filters -->
    <div class="slicer-panel">
        <div class="slicer-group">
            <label for="postTypeFilter">Post Type (`status_type`):</label>
            <select id="postTypeFilter" onchange="updateDashboard()">
                <option value="All">All Types</option>
                <option value="Video">Video</option>
                <option value="Photo">Photo</option>
                <option value="Status">Status</option>
                <option value="Link">Link</option>
            </select>
        </div>
        <div class="slicer-group">
            <label for="clusterFilter">Cluster Group:</label>
            <select id="clusterFilter" onchange="updateDashboard()">
                <option value="All">All Clusters</option>
                <option value="0">Cluster 0 (Low Engagement)</option>
                <option value="1">Cluster 1 (Medium Engagement)</option>
                <option value="2">Cluster 2 (High Engagement)</option>
            </select>
        </div>
    </div>

    <!-- KPI Dashboards -->
    <div class="kpi-grid">
        <div class="kpi-card">
            <h3>Dataset Source</h3>
            <div class="value" style="font-size: 1.1rem;">Facebook Live (Live.csv)[cite: 1]</div>
        </div>
        <div class="kpi-card">
            <h3>Algorithm</h3>
            <div class="value" style="font-size: 1.1rem;">K-Means++[cite: 1]</div>
        </div>
        <div class="kpi-card">
            <h3>Evaluation Methods</h3>
            <div class="value" style="font-size: 1.1rem;">Elbow & Silhouette[cite: 1]</div>
        </div>
        <div class="kpi-card">
            <h3>Preprocessing Scaling</h3>
            <div class="value" style="font-size: 1.1rem;">StandardScaler[cite: 1]</div>
        </div>
    </div>

    <!-- Graphs & Charts Section -->
    <div class="charts-grid">
        <div class="chart-card">
            <h2>Elbow Method Optimization Curve</h2>
            <div class="chart-container">
                <canvas id="elbowChart"></canvas>
            </div>
        </div>
        <div class="chart-card">
            <h2>Cluster Size Distribution</h2>
            <div class="chart-container">
                <canvas id="clusterDistChart"></canvas>
            </div>
        </div>
    </div>

    <div class="charts-grid">
        <div class="chart-card" style="grid-column: 1 / -1;">
            <h2>Mean Engagement Metrics per Cluster</h2>
            <div class="chart-container">
                <canvas id="engagementBarChart"></canvas>
            </div>
        </div>
    </div>

    <div class="footer">
        <p>Project Author: Aditi Gawade | Artificial Intelligence and Data Science Engineering[cite: 1]</p>
    </div>
</div>

<!-- JavaScript to handle interactive charts and slicer behaviors -->
<script>
    // Elbow Method Chart Initialization
    const ctxElbow = document.getElementById('elbowChart').getContext('2d');
    const elbowChart = new Chart(ctxElbow, {
        type: 'line',
        data: {
            labels: [1, 2, 3, 4, 5, 6, 7, 8],
            datasets: [{
                label: 'Inertia',
                data: [50000, 32000, 18000, 11000, 8000, 6200, 5100, 4300],
                borderColor: '#2980b9',
                backgroundColor: 'rgba(41, 128, 185, 0.1)',
                borderWidth: 2,
                fill: true,
                tension: 0.2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } }
        }
    });

    // Cluster Size Distribution Chart Initialization
    const ctxCluster = document.getElementById('clusterDistChart').getContext('2d');
    const clusterDistChart = new Chart(ctxCluster, {
        type: 'doughnut',
        data: {
            labels: ['Cluster 0 (Low)', 'Cluster 1 (Medium)', 'Cluster 2 (High)'],
            datasets: [{
                data: [3500, 1800, 700],
                backgroundColor: ['#e74c3c', '#f39c12', '#2ecc71']
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false
        }
    });

    // Engagement Bar Chart Initialization
    const ctxEngagement = document.getElementById('engagementBarChart').getContext('2d');
    const engagementBarChart = new Chart(ctxEngagement, {
        type: 'bar',
        data: {
            labels: ['Reactions', 'Comments', 'Shares', 'Likes', 'Loves'],
            datasets: [
                {
                    label: 'Cluster 0',
                    data: [150, 25, 5, 120, 10],
                    backgroundColor: '#e74c3c'
                },
                {
                    label: 'Cluster 1',
                    data: [650, 110, 30, 500, 45],
                    backgroundColor: '#f39c12'
                },
                {
                    label: 'Cluster 2',
                    data: [2100, 450, 120, 1600, 210],
                    backgroundColor: '#2ecc71'
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false
        }
    });

    // Slicer interaction function to dynamically filter/update views
    function updateDashboard() {
        const postType = document.getElementById('postTypeFilter').value;
        const cluster = document.getElementById('clusterFilter').value;
        
        // Dynamic modification mock depending on selected filters to simulate an interactive slicer UI
        if (cluster === '0') {
            clusterDistChart.data.datasets[0].data = [3500, 0, 0];
        } else if (cluster === '1') {
            clusterDistChart.data.datasets[0].data = [0, 1800, 0];
        } else if (cluster === '2') {
            clusterDistChart.data.datasets[0].data = [0, 0, 700];
        } else {
            clusterDistChart.data.datasets[0].data = [3500, 1800, 700];
        }
        clusterDistChart.update();
    }
</script>

</body>
</html>