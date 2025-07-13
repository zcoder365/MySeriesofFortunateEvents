document.addEventListener("DOMContentLoaded", function () {
    const chartCanvas = document.getElementById('ratingsChartMonth');
    if (!chartCanvas) return;

    const ctx = chartCanvas.getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: window.chartLabelsMonth,
            datasets: [{
                label: 'Number of Entries per Rating (Month)',
                data: window.chartDataMonth,
                backgroundColor: 'rgba(226, 144, 74, 0.6)',
                borderColor: 'rgba(226, 144, 74, 1)',
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