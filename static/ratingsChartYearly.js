// JavaScript for rendering the yearly review chart with proper text sizing
document.addEventListener('DOMContentLoaded', function() {
    // Get the canvas element for the yearly chart
    const ctx = document.getElementById('ratingsChartYearly').getContext('2d');
    
    // Force canvas to specific pixel dimensions to prevent text compression
    const canvas = ctx.canvas;
    canvas.style.width = '100%';
    canvas.style.height = '400px';
    
    // Set actual canvas resolution higher for crisp text
    const rect = canvas.getBoundingClientRect();
    const dpr = window.devicePixelRatio || 1;
    canvas.width = rect.width * dpr;
    canvas.height = 400 * dpr;
    ctx.scale(dpr, dpr);
    
    // Create the line chart showing yearly trend
    const ratingsChartYearly = new Chart(ctx, {
        type: 'line',
        data: {
            labels: window.chartLabelsYearly, // Month names
            datasets: [{
                label: 'Average Rating by Month',
                data: window.chartDataYearly, // Monthly averages
                borderColor: '#4CAF50',
                backgroundColor: 'rgba(76, 175, 80, 0.1)',
                borderWidth: 4,
                pointBackgroundColor: '#4CAF50',
                pointBorderColor: '#2E7D32',
                pointBorderWidth: 3,
                pointRadius: 8,
                pointHoverRadius: 12,
                fill: true,
                tension: 0.4 // Smooth curves
            }, {
                label: 'Entry Count by Month',
                data: window.chartCountsYearly, // Monthly entry counts
                type: 'bar',
                backgroundColor: 'rgba(255, 193, 7, 0.6)',
                borderColor: '#FFC107',
                borderWidth: 2,
                yAxisID: 'y1' // Use secondary y-axis
            }]
        },
        options: {
            responsive: false, // Disable responsive to prevent text scaling
            maintainAspectRatio: false,
            devicePixelRatio: dpr, // Use device pixel ratio for crisp text
            layout: {
                padding: {
                    top: 30,
                    bottom: 40,
                    left: 30,
                    right: 30
                }
            },
            plugins: {
                legend: {
                    display: true,
                    position: 'top',
                    labels: {
                        padding: 25,
                        font: {
                            size: 16,
                            family: '"Comic Sans MS", cursive, sans-serif'
                        },
                        usePointStyle: true,
                        boxWidth: 15,
                        boxHeight: 15
                    }
                },
                tooltip: {
                    enabled: true,
                    titleFont: {
                        size: 16,
                        family: '"Comic Sans MS", cursive, sans-serif'
                    },
                    bodyFont: {
                        size: 14,
                        family: '"Comic Sans MS", cursive, sans-serif'
                    },
                    callbacks: {
                        label: function(context) {
                            if (context.datasetIndex === 0) {
                                return `Average Rating: ${context.raw.toFixed(2)}`;
                            } else {
                                return `Entries: ${context.raw}`;
                            }
                        },
                        afterLabel: function(context) {
                            if (context.datasetIndex === 0 && context.raw > 0) {
                                const count = window.chartCountsYearly[context.dataIndex];
                                return `Based on ${count} entries`;
                            }
                            return '';
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 10, // Rating scale 1-10
                    title: {
                        display: true,
                        text: 'Average Rating',
                        font: {
                            size: 16,
                            weight: 'bold',
                            family: '"Comic Sans MS", cursive, sans-serif'
                        },
                        color: '#4CAF50',
                        padding: {
                            bottom: 15
                        }
                    },
                    ticks: {
                        stepSize: 1,
                        font: {
                            size: 14,
                            family: '"Comic Sans MS", cursive, sans-serif'
                        },
                        padding: 10,
                        color: '#333'
                    },
                    grid: {
                        drawBorder: true,
                        lineWidth: 1,
                        color: '#e0e0e0'
                    }
                },
                y1: {
                    type: 'linear',
                    display: true,
                    position: 'right',
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Number of Entries',
                        font: {
                            size: 16,
                            weight: 'bold',
                            family: '"Comic Sans MS", cursive, sans-serif'
                        },
                        color: '#FFC107',
                        padding: {
                            bottom: 15
                        }
                    },
                    ticks: {
                        font: {
                            size: 14,
                            family: '"Comic Sans MS", cursive, sans-serif'
                        },
                        padding: 10,
                        color: '#333'
                    },
                    grid: {
                        drawOnChartArea: false, // Don't draw grid lines for secondary axis
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Month',
                        font: {
                            size: 16,
                            weight: 'bold',
                            family: '"Comic Sans MS", cursive, sans-serif'
                        },
                        padding: {
                            top: 15
                        }
                    },
                    ticks: {
                        font: {
                            size: 14,
                            family: '"Comic Sans MS", cursive, sans-serif'
                        },
                        padding: 10,
                        maxRotation: 45,
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
                duration: 1500,
                easing: 'easeOutQuart'
            }
        }
    });
    
    // Handle window resize to maintain proper dimensions
    window.addEventListener('resize', function() {
        const newRect = canvas.getBoundingClientRect();
        canvas.width = newRect.width * dpr;
        canvas.height = 400 * dpr;
        ctx.scale(dpr, dpr);
        ratingsChartYearly.resize();
    });
});