document.addEventListener('DOMContentLoaded', function() {
    const levelUpBtn = document.getElementById('level-up-btn');
    const activityButtonsContainer = document.getElementById('activity-buttons');
    const returnBtn = document.getElementById('return-btn');
    
    const ctx = document.getElementById('statsChart').getContext('2d');
    const statsChart = new Chart(ctx, {
        type: 'radar',
        data: {
            labels: ['HP', 'Attack', 'Defense', 'Sp. Attack', 'Sp. Defense', 'Speed'],
            datasets: [{
                label: 'Character Stats',
                data: [
                    parseInt(document.getElementById('hp-value').textContent), 
                    parseInt(document.getElementById('atk-value').textContent), 
                    parseInt(document.getElementById('def-value').textContent), 
                    parseInt(document.getElementById('spa-value').textContent), 
                    parseInt(document.getElementById('spd-value').textContent), 
                    parseInt(document.getElementById('spe-value').textContent)
                ],
                backgroundColor: 'rgba(255, 165, 0, 0.2)',
                borderColor: 'orange',
                pointBackgroundColor: 'orange',
                pointBorderColor: '#fff',
                pointHoverBackgroundColor: '#fff',
                pointHoverBorderColor: 'orange'
            }]
        },
        options: {
            elements: {
                line: {
                    borderWidth: 3
                }
            },
            scales: {
                r: {
                    angleLines: {
                        display: true
                    },
                    suggestedMin: 0,
                    suggestedMax: 20
                }
            }
        }
    });
    
    function toggleActivityButtons() {
        if (activityButtonsContainer.classList.contains('visible')) {
            activityButtonsContainer.classList.remove('visible');
            
            setTimeout(() => {
                levelUpBtn.classList.remove('collapsed');
            }, 300);
        } else {
            levelUpBtn.classList.add('collapsed');
            
            setTimeout(() => {
                activityButtonsContainer.classList.add('visible');
            }, 300);
        }
    }
    
    levelUpBtn.addEventListener('click', toggleActivityButtons);
    returnBtn.addEventListener('click', toggleActivityButtons);
    
    document.getElementById('github-btn').addEventListener('click', function(e) {
        e.preventDefault();
        
        console.log('GitHub button clicked, redirecting...');
        
        window.location.href = '/github';
    });
    
    document.getElementById('leetcode-btn').addEventListener('click', function(e) {
        e.preventDefault();
        
        console.log('LeetCode button clicked, redirecting...');
        
        window.location.href = '/leetcode';
    });
    
    document.getElementById('pomodoro-btn').addEventListener('click', function(e) {
        e.preventDefault();
        
        console.log('Pomodoro button clicked, redirecting...');
        
        window.location.href = '/pomodoro';
    });
    
    try {
        const hpValue = parseInt(document.getElementById('hp-value').textContent) || 20;
        const atkValue = parseInt(document.getElementById('atk-value').textContent) || 5;
        const defValue = parseInt(document.getElementById('def-value').textContent) || 5;
        const spaValue = parseInt(document.getElementById('spa-value').textContent) || 5;
        const spdValue = parseInt(document.getElementById('spd-value').textContent) || 5;
        const speValue = parseInt(document.getElementById('spe-value').textContent) || 5;
        
        statsChart.data.datasets[0].data = [
            hpValue,
            atkValue,
            defValue,
            spaValue,
            spdValue,
            speValue
        ];
        
        statsChart.update();
    } catch (error) {
        console.error("Error initializing or updating chart:", error);
    }
});
