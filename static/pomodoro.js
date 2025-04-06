document.addEventListener('DOMContentLoaded', function() {
    const minutesDisplay = document.getElementById('minutes');
    const secondsDisplay = document.getElementById('seconds');
    const progressBar = document.getElementById('progress-bar');
    const startBtn = document.getElementById('start-btn');
    const pauseBtn = document.getElementById('pause-btn');
    const resetBtn = document.getElementById('reset-btn');
    const modeButtons = document.querySelectorAll('.mode-btn');
    const sessionCount = document.getElementById('session-count');
    const targetSessions = document.getElementById('target-sessions');
    const sessionIcons = document.getElementById('session-icons');
    const completionMessage = document.getElementById('completion-message');
    const completedCount = document.getElementById('completed-count');
    const claimRewardBtn = document.getElementById('claim-reward-btn');
    const statSelectionModal = document.getElementById('stat-selection-modal');
    const statOptionButtons = document.querySelectorAll('.stat-option-btn');
    
    let timer;
    let minutes = 1;  
    let seconds = 0;
    let totalSeconds = minutes * 60;
    let remainingSeconds = totalSeconds;
    let isRunning = false;
    let sessionsCompleted = 0;
    let selectedStats = [];
    const targetSessionCount = 4;
    
    function initSessionIcons() {
        sessionIcons.innerHTML = '';
        for (let i = 0; i < targetSessionCount; i++) {
            const icon = document.createElement('div');
            icon.className = 'session-icon';
            icon.innerHTML = '<i class="fas fa-check"></i>';
            sessionIcons.appendChild(icon);
        }
        sessionCount.textContent = sessionsCompleted;
        targetSessions.textContent = targetSessionCount;
    }
    
    function updateDisplay() {
        minutesDisplay.textContent = String(minutes).padStart(2, '0');
        secondsDisplay.textContent = String(seconds).padStart(2, '0');
        
        const progress = (remainingSeconds / totalSeconds);
        progressBar.style.transform = `scaleX(${progress})`;
    }
    
    function setTimerMode(mode) {
        clearInterval(timer);
        isRunning = false;
        startBtn.disabled = false;
        pauseBtn.disabled = true;
        
        minutes = mode;
        seconds = 0;
        totalSeconds = minutes * 60;
        remainingSeconds = totalSeconds;
        
        updateDisplay();
    }
    
    function startTimer() {
        if (isRunning) return;
        
        isRunning = true;
        startBtn.disabled = true;
        pauseBtn.disabled = false;
        
        timer = setInterval(function() {
            remainingSeconds--;
            
            minutes = Math.floor(remainingSeconds / 60);
            seconds = remainingSeconds % 60;
            
            updateDisplay();
            
            if (remainingSeconds <= 0) {
                clearInterval(timer);
                isRunning = false;
                
                if (document.getElementById('pomodoro-btn').classList.contains('active')) {
                    completeSession();
                }
                
                const audio = new Audio('/static/assets/bell.mp3');
                audio.play();
                
                startBtn.disabled = false;
                pauseBtn.disabled = true;
            }
        }, 1000);
    }
    
    function pauseTimer() {
        clearInterval(timer);
        isRunning = false;
        startBtn.disabled = false;
        pauseBtn.disabled = true;
    }
    
    function resetTimer() {
        clearInterval(timer);
        isRunning = false;
        startBtn.disabled = false;
        pauseBtn.disabled = true;
        
        const activeMode = document.querySelector('.mode-btn.active');
        minutes = parseInt(activeMode.dataset.time);
        seconds = 0;
        totalSeconds = minutes * 60;
        remainingSeconds = totalSeconds;
        
        updateDisplay();
    }
    
    function completeSession() {
        sessionsCompleted++;
        sessionCount.textContent = sessionsCompleted;
        
        const icons = document.querySelectorAll('.session-icon');
        if (icons[sessionsCompleted - 1]) {
            icons[sessionsCompleted - 1].classList.add('completed');
        }
        
        showStatSelectionModal();
    }
    
    function showStatSelectionModal() {
        statSelectionModal.classList.add('show');
    }
    
    function hideStatSelectionModal() {
        statSelectionModal.classList.remove('show');
        
        if (sessionsCompleted >= targetSessionCount) {
            showCompletionMessage();
        }
    }
    
    function showCompletionMessage() {
        completedCount.textContent = sessionsCompleted;
        completionMessage.classList.add('show');
    }
    
    function selectStat(stat) {
        selectedStats.push(stat);
        
        updateUserStat(stat);
        
        hideStatSelectionModal();
    }
    
    function updateUserStat(stat) {
        const gain = stat === 'HP' ? 1.0 : 0.5;
        
        fetch('/activity', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                activity_type: 'pomodoro',
                single_stat: stat,
                stat_gain: gain
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                const notification = document.createElement('div');
                notification.className = 'stat-notification';
                notification.textContent = `+${gain} ${stat}`;
                document.body.appendChild(notification);
                
                setTimeout(() => {
                    notification.classList.add('show');
                }, 10);
                
                setTimeout(() => {
                    notification.classList.remove('show');
                    setTimeout(() => notification.remove(), 300);
                }, 2000);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
    
    function claimRewards() {
        sessionsCompleted = 0;
        selectedStats = [];
        initSessionIcons();
        completionMessage.classList.remove('show');
        
        const notification = document.createElement('div');
        notification.className = 'completion-notification';
        notification.textContent = 'Great job! All rewards claimed.';
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.classList.add('show');
        }, 10);
        
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => notification.remove(), 300);
        }, 3000);
    }
    
    startBtn.addEventListener('click', startTimer);
    pauseBtn.addEventListener('click', pauseTimer);
    resetBtn.addEventListener('click', resetTimer);
    claimRewardBtn.addEventListener('click', claimRewards);
    
    statOptionButtons.forEach(button => {
        button.addEventListener('click', function() {
            const stat = this.getAttribute('data-stat');
            selectStat(stat);
        });
    });
    
    modeButtons.forEach(button => {
        button.addEventListener('click', function() {
            modeButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            setTimerMode(parseInt(this.dataset.time));
        });
    });
    
    initSessionIcons();
    updateDisplay();
    
    const style = document.createElement('style');
    style.textContent = `
        .stat-notification {
            position: fixed;
            top: 20px;
            right: 20px;
            background: linear-gradient(145deg, orange, darkorange);
            color: white;
            padding: 15px 25px;
            border-radius: 8px;
            font-size: 1.2rem;
            font-weight: bold;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
            transform: translateX(120%);
            transition: transform 0.3s ease;
            z-index: 1000;
        }
        
        .stat-notification.show {
            transform: translateX(0);
        }
        
        .completion-notification {
            position: fixed;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%) translateY(100px);
            background: linear-gradient(145deg, #6a11cb, #2575fc);
            color: white;
            padding: 15px 25px;
            border-radius: 8px;
            font-size: 1.2rem;
            font-weight: bold;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
            transition: transform 0.3s ease;
            z-index: 1000;
        }
        
        .completion-notification.show {
            transform: translateX(-50%) translateY(0);
        }
    `;
    document.head.appendChild(style);
});
