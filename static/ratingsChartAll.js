// JavaScript for rendering the all-time ratings distribution chart with proper text sizing
document.addEventListener('DOMContentLoaded', function() {
    // Get the canvas element for the all-time chart
    const ctx = document.getElementById('ratingsChartAll').getContext('2d');
    
    // Force canvas to specific pixel dimensions to prevent text compression
    const canvas = ctx.canvas;
    canvas.style.width = '100%';
    canvas.style.height = '500px';
    
    // Set actual canvas resolution higher for crisp text
    const rect = canvas.getBoundingClientRect();
    const dpr = window.devicePixelRatio || 1;
    canvas.width = rect.width * dpr;
    canvas.height = 500 * dpr;
    ctx.scale(dpr, dpr);
    
    // Create the bar chart showing rating distribution
    const ratingsChartAll = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: window.chartLabelsAll,
            datasets: [{
                label: 'Number of Entries',
                data: window.chartDataAll,
                backgroundColor: [
                    '#FF6B6B', '#FF8E53', '#FF9F40', '#FFB84D', '#FFCD56',
                    '#9FE2BF', '#4BC0C8', '#36A2EB', '#9966FF', '#4CAF50'
                ],
                borderColor: [
                    '#FF5252', '#FF7043', '#FF9800', '#FFB300', '#FFEB3B',
                    '#81C784', '#26C6DA', '#2196F3', '#7B1FA2', '#388E3C'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: false, // Disable responsive to prevent text scaling
            maintainAspectRatio: false,
            devicePixelRatio: dpr, // Use device pixel ratio for crisp text
            layout: {
                padding: {
                    top: 40,
                    bottom: 50,
                    left: 30,
                    right: 30
                }
            },
            plugins: {
                legend: {
                    display: true,
                    position: 'top',
                    labels: {
                        padding: 30,
                        font: {
                            size: 18,
                            family: '"Comic Sans MS", cursive, sans-serif'
                        },
                        usePointStyle: false,
                        boxWidth: 20,
                        boxHeight: 12
                    }
                },
                tooltip: {
                    enabled: true,
                    titleFont: {
                        size: 16,
                        family: '"Comic Sans MS", cursive, sans-serif'
                    },
                    bodyFont: {
                        size: 15,
                        family: '"Comic Sans MS", cursive, sans-serif'
                    },
                    callbacks: {
                        label: function(context) {
                            const rating = context.label;
                            const count = context.raw;
                            return `Rating ${rating}: ${count} entries`;
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
                            size: 18,
                            weight: 'bold',
                            family: '"Comic Sans MS", cursive, sans-serif'
                        },
                        padding: {
                            bottom: 20
                        }
                    },
                    ticks: {
                        stepSize: 1,
                        font: {
                            size: 16,
                            family: '"Comic Sans MS", cursive, sans-serif'
                        },
                        padding: 15,
                        color: '#333'
                    },
                    grid: {
                        drawBorder: true,
                        lineWidth: 1,
                        color: '#e0e0e0'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Rating (1-10)',
                        font: {
                            size: 18,
                            weight: 'bold',
                            family: '"Comic Sans MS", cursive, sans-serif'
                        },
                        padding: {
                            top: 20
                        }
                    },
                    ticks: {
                        font: {
                            size: 16,
                            family: '"Comic Sans MS", cursive, sans-serif'
                        },
                        padding: 15,
                        maxRotation: 0,
                        minRotation: 0,
                        color: '#333'
                    },
                    grid: {
                        drawBorder: true,
                        lineWidth: 1,
                        color: '#e0e0e0'
                    }
                }
            },
            animation: {
                duration: 1000,
                easing: 'easeOutQuart'
            }
        }
    });
    
    // Handle window resize to maintain proper dimensions
    window.addEventListener('resize', function() {
        const newRect = canvas.getBoundingClientRect();
        canvas.width = newRect.width * dpr;
        canvas.height = 500 * dpr;
        ctx.scale(dpr, dpr);
        ratingsChartAll.resize();
    });
});