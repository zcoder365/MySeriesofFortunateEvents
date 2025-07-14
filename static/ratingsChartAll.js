// JavaScript for rendering the all-time ratings distribution chart
document.addEventListener('DOMContentLoaded', function() {
    // Get the canvas element for the all-time chart
    const ctx = document.getElementById('ratingsChartAll').getContext('2d');
    
    // Create the bar chart showing rating distribution
    const ratingsChartAll = new Chart(ctx, {
        type: 'bar', // Bar chart type
        data: {
            labels: window.chartLabelsAll, // Rating numbers 1-10
            datasets: [{
                label: 'Number of Entries', // Legend label
                data: window.chartDataAll, // Count of entries for each rating
                backgroundColor: [
                    '#FF6B6B', // Rating 1 - Red (poor)
                    '#FF8E53', // Rating 2 - Orange-red
                    '#FF9F40', // Rating 3 - Orange
                    '#FFB84D', // Rating 4 - Yellow-orange
                    '#FFCD56', // Rating 5 - Yellow
                    '#9FE2BF', // Rating 6 - Light green
                    '#4BC0C8', // Rating 7 - Teal
                    '#36A2EB', // Rating 8 - Blue
                    '#9966FF', // Rating 9 - Purple
                    '#4CAF50'  // Rating 10 - Green (excellent)
                ],
                borderColor: [
                    '#FF5252', '#FF7043', '#FF9800', '#FFB300', '#FFEB3B',
                    '#81C784', '#26C6DA', '#2196F3', '#7B1FA2', '#388E3C'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true, // Make chart responsive
            maintainAspectRatio: false, // Allow flexible aspect ratio
            plugins: {
                legend: {
                    display: true,
                    position: 'top'
                },
                tooltip: {
                    callbacks: {
                        // Custom tooltip to show meaningful information
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
                    beginAtZero: true, // Start y-axis from 0
                    title: {
                        display: true,
                        text: 'Number of Entries'
                    },
                    ticks: {
                        stepSize: 1 // Show whole numbers only
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Rating (1-10)'
                    }
                }
            }
        }
    });
});