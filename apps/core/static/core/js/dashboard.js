document.addEventListener('DOMContentLoaded', function () {
  // Fungsi untuk jam realtime
  function updateClock() {
    const clockElement = document.getElementById('realtime-clock');
    if (clockElement) {
      const now = new Date();
      const timeString = now.toLocaleTimeString('id-ID', {
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        hour12: false,
      });
      clockElement.textContent = timeString;
    }
  }

  // Inisialisasi jam dan atur interval
  if (document.getElementById('realtime-clock')) {
    setInterval(updateClock, 1000);
    updateClock();
  }

  // Ambil data grafik dari elemen script dan simpan di window
  const dataElement = document.getElementById('dashboard-data');
  let dashboardChartData = null;
  if (dataElement) {
    dashboardChartData = JSON.parse(dataElement.textContent);
  }

  // Fungsi untuk inisialisasi grafik
  function initChart(canvasId, chartType, data, options = {}) {
    const canvas = document.getElementById(canvasId);
    if (canvas && dashboardChartData) {
      const chartData = dashboardChartData[data.datasetKey];
      const chartLabels = dashboardChartData[data.labelsKey];

      if (!chartLabels || !chartData) return;

      new Chart(canvas, {
        type: chartType,
        data: {
          labels: chartLabels,
          datasets: [
            {
              ...data.datasetOptions,
              data: chartData,
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          ...options,
        },
      });
    }
  }

  // Inisialisasi Grafik Distribusi Peran
  initChart(
    'peranChart',
    'doughnut',
    { // Argumen 'data'
      datasetKey: 'chart_data',
      labelsKey: 'chart_labels',
      datasetOptions: {
        label: 'Jumlah Akun',
        backgroundColor: ['#570df8', '#f000b8', '#37cdbe', '#3abff8', '#f87272'],
        hoverOffset: 4,
      },
    },
    { // Argumen 'options'
      animation: {
        duration: 1200, // Durasi animasi dalam milidetik
        easing: 'easeOutBounce', // Efek memantul saat selesai
        animateRotate: true,
        animateScale: true, // Grafik akan membesar saat muncul
      },
    }
  );
});