<template>
<div data-page="dashboard" class="admin-layout">
    <!-- Loading Screen -->
    <div id="loading-screen" class="loading-screen">
        <div class="loading-spinner">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
        </div>
    </div>

    <!-- Main Wrapper -->
    <div class="admin-wrapper" id="admin-wrapper">
        
        <!-- Main Content -->
        <main class="admin-main">
            <div class="container-fluid p-1 p-lg-5">
                <!-- Page Header -->
                <div class="d-flex justify-content-between align-items-center mb-4">
                    <div>
                        <h1 class="h3 mb-0">Dashboard</h1>
                        <p class="text-muted mb-0">Welcome back! Here's what's happening.</p>
                    </div>
                   
                </div>

                <!-- Stats Cards with Alpine.js -->
                <div class="row g-4 mb-4">
                    <div class="col-xl-3 col-lg-6" x-data="statsCounter(12426, 5)">
                        <div class="card stats-card">
                            <div class="card-body">
                                <div class="d-flex align-items-center">
                                    <div class="flex-shrink-0">
                                        <div class="stats-icon bg-primary bg-opacity-10 text-primary">
                                            <i class="bi bi-people"></i>
                                        </div>
                                    </div>
                                    <div class="flex-grow-1 ms-3">
                                        <h6 class="mb-0 text-muted">Total Users</h6>
                                        <h3 class="mb-0" x-text="value.toLocaleString()" data-stat-value>12,426</h3>
                                        <small class="text-success">
                                            <i class="bi bi-arrow-up"></i> +12.5%
                                        </small>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="col-xl-3 col-lg-6">
                        <div class="card stats-card">
                            <div class="card-body">
                                <div class="d-flex align-items-center">
                                    <div class="flex-shrink-0">
                                        <div class="stats-icon bg-success bg-opacity-10 text-success">
                                            <i class="bi bi-graph-up"></i>
                                        </div>
                                    </div>
                                    <div class="flex-grow-1 ms-3">
                                        <h6 class="mb-0 text-muted">Revenue</h6>
                                        <h3 class="mb-0">$54,320</h3>
                                        <small class="text-success">
                                            <i class="bi bi-arrow-up"></i> +8.2%
                                        </small>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="col-xl-3 col-lg-6">
                        <div class="card stats-card">
                            <div class="card-body">
                                <div class="d-flex align-items-center">
                                    <div class="flex-shrink-0">
                                        <div class="stats-icon bg-warning bg-opacity-10 text-warning">
                                            <i class="bi bi-bag-check"></i>
                                        </div>
                                    </div>
                                    <div class="flex-grow-1 ms-3">
                                        <h6 class="mb-0 text-muted">Orders</h6>
                                        <h3 class="mb-0">1,852</h3>
                                        <small class="text-danger">
                                            <i class="bi bi-arrow-down"></i> -2.1%
                                        </small>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="col-xl-3 col-lg-6">
                        <div class="card stats-card">
                            <div class="card-body">
                                <div class="d-flex align-items-center">
                                    <div class="flex-shrink-0">
                                        <div class="stats-icon bg-info bg-opacity-10 text-info">
                                            <i class="bi bi-clock-history"></i>
                                        </div>
                                    </div>
                                    <div class="flex-grow-1 ms-3">
                                        <h6 class="mb-0 text-muted">Avg. Response</h6>
                                        <h3 class="mb-0">2.3s</h3>
                                        <small class="text-success">
                                            <i class="bi bi-arrow-up"></i> +5.4%
                                        </small>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Chart Section -->
                <div class="row g-4 mb-4">
                    <div class="col-lg-8">
                        <div class="card">
                            <div class="card-header d-flex justify-content-between align-items-center">
                                <h5 class="card-title mb-0">Revenue Overview</h5>
                                <div class="btn-group btn-group-sm" role="group">
                                    <button type="button" class="btn btn-outline-primary active" data-chart-period="7d">7D</button>
                                    <button type="button" class="btn btn-outline-primary" data-chart-period="30d">30D</button>
                                    <button type="button" class="btn btn-outline-primary" data-chart-period="90d">90D</button>
                                    <button type="button" class="btn btn-outline-primary" data-chart-period="1y">1Y</button>
                                </div>
                            </div>
                            <div class="card-body">
                                <canvas id="revenueChart" height="250"></canvas>
                            </div>
                        </div>
                    </div>

                    <div class="col-lg-4">
                        <div class="card">
                            <div class="card-header">
                                <h5 class="card-title mb-0">Recent Activity</h5>
                            </div>
                            <div class="card-body">
                                <div class="activity-feed">
                                    <div class="activity-item">
                                        <div class="activity-icon bg-primary bg-opacity-10 text-primary">
                                            <i class="bi bi-person-plus"></i>
                                        </div>
                                        <div class="activity-content">
                                            <p class="mb-1">New user registered</p>
                                            <small class="text-muted">2 minutes ago</small>
                                        </div>
                                    </div>
                                    <div class="activity-item">
                                        <div class="activity-icon bg-success bg-opacity-10 text-success">
                                            <i class="bi bi-bag-check"></i>
                                        </div>
                                        <div class="activity-content">
                                            <p class="mb-1">Order #1234 completed</p>
                                            <small class="text-muted">5 minutes ago</small>
                                        </div>
                                    </div>
                                    <div class="activity-item">
                                        <div class="activity-icon bg-warning bg-opacity-10 text-warning">
                                            <i class="bi bi-exclamation-triangle"></i>
                                        </div>
                                        <div class="activity-content">
                                            <p class="mb-1">Server maintenance scheduled</p>
                                            <small class="text-muted">1 hour ago</small>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Additional Charts Row -->
                <div class="row g-4 mb-4">
                    <div class="col-lg-6">
                        <div class="card">
                            <div class="card-header">
                                <h5 class="card-title mb-0">User Growth (Last 7 Days)</h5>
                            </div>
                            <div class="card-body">
                                <canvas id="userGrowthChart" height="200"></canvas>
                            </div>
                        </div>
                    </div>

                    <div class="col-lg-6">
                        <div class="card">
                            <div class="card-header">
                                <h5 class="card-title mb-0">Order Status Distribution</h5>
                            </div>
                            <div class="card-body">
                                <canvas id="orderStatusChart" height="200"></canvas>
                            </div>
                        </div>
                    </div>
                </div>

            </div>
        </main>
    </div> <!-- /.admin-wrapper -->



</div>
</template>

<script setup>
import { onMounted } from 'vue';
import Chart from 'chart.js/auto';

// Función para inicializar los gráficos
const initCharts = () => {
  // Gráfico de Revenue Overview
  const revenueCtx = document.getElementById('revenueChart');
  if (revenueCtx) {
    new Chart(revenueCtx, {
      type: 'line',
      data: {
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'],
        datasets: [{
          label: 'Revenue (USD)',
          data: [5000, 8000, 12000, 9000, 15000, 18000, 20000],
          borderColor: '#4e73df',
          backgroundColor: 'rgba(78, 115, 223, 0.05)',
          tension: 0.3,
          fill: true
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'top',
          }
        }
      }
    });
  }

  // Gráfico de User Growth
  const userGrowthCtx = document.getElementById('userGrowthChart');
  if (userGrowthCtx) {
    new Chart(userGrowthCtx, {
      type: 'bar',
      data: {
        labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
        datasets: [{
          label: 'New Users',
          data: [45, 78, 56, 89, 76, 65, 91],
          backgroundColor: 'rgba(40, 167, 69, 0.5)',
          borderColor: '#28a745',
          borderWidth: 1
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'top',
          }
        }
      }
    });
  }

  // Gráfico de Order Status
  const orderStatusCtx = document.getElementById('orderStatusChart');
  if (orderStatusCtx) {
    new Chart(orderStatusCtx, {
      type: 'doughnut',
      data: {
        labels: ['Completed', 'Processing', 'Cancelled', 'Pending'],
        datasets: [{
          data: [65, 15, 10, 10],
          backgroundColor: [
            '#28a745',
            '#17a2b8',
            '#dc3545',
            '#ffc107'
          ],
          borderWidth: 1
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'right',
          }
        }
      }
    });
  }
};

onMounted(() => {
  // Ocultar pantalla de carga cuando todo esté listo
  const hideLoadingScreen = () => {
    const loadingScreen = document.getElementById('loading-screen');
    if (loadingScreen) {
      loadingScreen.style.display = 'none';
    }
  };

  // Inicializar gráficos
  initCharts();

  // Manejar el sidebar toggle
  const toggleButton = document.querySelector('[data-sidebar-toggle]');
  const wrapper = document.getElementById('admin-wrapper');

  if (toggleButton && wrapper) {
    // Set initial state from localStorage
    const isCollapsed = localStorage.getItem('sidebar-collapsed') === 'true';
    if (isCollapsed) {
      wrapper.classList.add('sidebar-collapsed');
      toggleButton.classList.add('is-active');
    }

    // Attach click listener
    toggleButton.addEventListener('click', () => {
      const isCurrentlyCollapsed = wrapper.classList.contains('sidebar-collapsed');
      
      if (isCurrentlyCollapsed) {
        wrapper.classList.remove('sidebar-collapsed');
        toggleButton.classList.remove('is-active');
        localStorage.setItem('sidebar-collapsed', 'false');
      } else {
        wrapper.classList.add('sidebar-collapsed');
        toggleButton.classList.add('is-active');
        localStorage.setItem('sidebar-collapsed', 'true');
      }
    });
  }

  // Ocultar pantalla de carga después de un pequeño retraso para asegurar que todo esté cargado
  setTimeout(hideLoadingScreen, 500);
});
</script>

<style scoped>
/* Estilos para los gráficos */
.card-body canvas {
  width: 100% !important;
  height: auto !important;
  min-height: 200px;
}

/* Estilos para el loading screen */
.loading-screen {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(255, 255, 255, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
  transition: opacity 0.5s ease-out;
}

.loading-screen.hidden {
  opacity: 0;
  pointer-events: none;
}

.loading-spinner {
  text-align: center;
}

/* Asegurar que los tooltips de Bootstrap funcionen */
[data-bs-toggle="tooltip"] {
  cursor: pointer;
}
</style>