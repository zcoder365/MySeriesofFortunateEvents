// JavaScript for rendering the yearly review bar chart with proper text sizing
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
    
    // Create the bar chart showing yearly monthly averages
    const ratingsChartYearly = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: window.chartLabelsYearly, // Month names
            datasets: [{
                label: 'Average Rating by Month',
                data: window.chartDataYearly, // Monthly averages
                backgroundColor: [
                    '#FF6B6B', // January - Red
                    '#FF8E53', // February - Orange-red  
                    '#FF9F40', // March - Orange
                    '#FFB84D', // April - Yellow-orange
                    '#FFCD56', // May - Yellow
                    '#9FE2BF', // June - Light green
                    '#4BC0C8', // July - Teal
                    '#36A2EB', // August - Blue
                    '#9966FF', // September - Purple
                    '#4CAF50', // October - Green
                    '#FF7043', // November - Deep orange
                    '#795548'  // December - Brown
                ],
                borderColor: [
                    '#FF5252', '#FF7043', '#FF9800', '#FFB300', '#FFEB3B',
                    '#81C784', '#26C6DA', '#2196F3', '#7B1FA2', '#388E3C',
                    '#FF5722', '#5D4037'
                ],
                borderWidth: 2
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
                        size: 14,
                        family: '"Comic Sans MS", cursive, sans-serif'
                    },
                    callbacks: {
                        label: function(context) {
                            const month = context.label;
                            const avgRating = context.raw;
                            const entryCount = window.chartCountsYearly[context.dataIndex];
                            
                            if (avgRating === 0) {
                                return `${month}: No entries`;
                            }
                            return `${month}: ${avgRating.toFixed(2)} avg (${entryCount} entries)`;
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
                        color: '#333',
                        callback: function(value) {
                            return value.toFixed(1);
                        }
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
                        maxRotation: 0, // Keep month names horizontal
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
                duration: 1200,
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