const CreditAnalytics = (() => {
    'use strict';

    const chartDefaults = {
        fontFamily: "'JetBrains Mono', monospace",
        color: '#94a3b8',
        gridColor: 'rgba(255, 255, 255, 0.05)'
    };

    const createGradient = (ctx, colorStart, colorEnd) => {
        const gradient = ctx.createLinearGradient(0, 0, 0, 400);
        gradient.addColorStop(0, colorStart);
        gradient.addColorStop(1, colorEnd);
        return gradient;
    };

    return {
        initRadar: (id, metrics, isSuccess) => {
            const canvas = document.getElementById(id);
            if (!canvas) return;
            const ctx = canvas.getContext('2d');
            const accent = isSuccess ? '#10b981' : '#e11d48';

            return new Chart(ctx, {
                type: 'radar',
                data: {
                    labels: ['LIQUIDITY', 'TENURE', 'HISTORY', 'DTI', 'STABILITY'],
                    datasets: [{
                        data: metrics,
                        backgroundColor: accent + '15',
                        borderColor: accent,
                        borderWidth: 3,
                        pointBackgroundColor: accent,
                        pointBorderColor: '#fff',
                        pointHoverRadius: 8,
                        fill: true
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        r: {
                            angleLines: { color: chartDefaults.gridColor },
                            grid: { color: chartDefaults.gridColor },
                            pointLabels: {
                                color: chartDefaults.color,
                                font: { family: chartDefaults.fontFamily, size: 11, weight: 'bold' }
                            },
                            ticks: { display: false },
                            suggestedMin: 0,
                            suggestedMax: 100
                        }
                    },
                    plugins: { legend: { display: false } },
                    animation: { duration: 2500, easing: 'easeOutQuart' }
                }
            });
        },

        initAmortization: (id, p, i, isSuccess) => {
            const canvas = document.getElementById(id);
            if (!canvas) return;
            const ctx = canvas.getContext('2d');
            
            return new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: ['PRINCIPAL CAPITAL', 'ESTIMATED INTEREST'],
                    datasets: [{
                        data: [p, i],
                        backgroundColor: [createGradient(ctx, '#3b82f6', '#1d4ed8'), isSuccess ? '#10b981' : '#e11d48'],
                        borderWidth: 0,
                        hoverOffset: 20
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    cutout: '85%',
                    plugins: {
                        legend: {
                            position: 'bottom',
                            labels: {
                                color: chartDefaults.color,
                                font: { family: chartDefaults.fontFamily, size: 10 },
                                padding: 20
                            }
                        }
                    },
                    animation: { animateRotate: true, animateScale: true, duration: 2000 }
                }
            });
        }
    };
})();