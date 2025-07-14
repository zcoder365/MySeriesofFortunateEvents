// JavaScript for rendering the monthly ratings chart
document.addEventListener('DOMContentLoaded', function() {
    const ctx = document.getElementById('ratingsChartMonth').getContext('2d');
    
    const ratingsChartMonth = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: window.chartLabelsMonth,
            datasets: [{
                label: 'Number of Entries per Rating (Month)',
                data: window.chartDataMonth,
                backgroundColor: '#FFB84D',
                borderColor: '#FF9800',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false, // Key for preventing text compression
            layout: {
                padding: {
                    top: 20,
                    bottom: 20,
                    left: 10,
                    right: 10
                }
            },
            plugins: {
                legend: {
                    display: true,
                    position: 'top',
                    labels: {
                        padding: 20,
                        font: {
                            size: 14
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Number of Entries',
                        font: {
                            size: 14,
                            weight: 'bold'
                        }
                    },
                    ticks: {
                        stepSize: 1,
                        font: {
                            size: 12
                        },
                        padding: 8
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Rating (1-10)',
                        font: {
                            size: 14,
                            weight: 'bold'
                        }
                    },
                    ticks: {
                        font: {
                            size: 12
                        },
                        padding: 8,
                        maxRotation: 0,
                        minRotation: 0
                    }
                }
            }
        }
    });
});