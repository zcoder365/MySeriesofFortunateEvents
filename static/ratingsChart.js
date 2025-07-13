document.addEventListener("DOMContentLoaded", function () {
    const chartCanvas = document.getElementById('ratingsChart');
    if (!chartCanvas) return; // Prevent errors if canvas is missing

    const ctx = chartCanvas.getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: window.chartLabels, // ["1", "2", ..., "10"]
            datasets: [{
                label: 'Number of Entries per Rating',
                data: window.chartData,   // [count for 1, ..., count for 10]
                backgroundColor: 'rgba(74, 144, 226, 0.6)',
                borderColor: 'rgba(74, 144, 226, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Rating'
                    }
                },
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Number of Entries'
                    },
                    ticks: {
                        stepSize: 1
                    }
                }
            }
        }
    });
});