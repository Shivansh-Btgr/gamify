document.addEventListener('DOMContentLoaded', function() {
    const usernameForm = document.getElementById('username-form');
    const usernameFormContainer = document.getElementById('username-form-container');
    const profileSection = document.getElementById('profile-section');
    const profileUsername = document.getElementById('profile-username');
    const lastUpdateTime = document.getElementById('last-update-time');
    const refreshBtn = document.getElementById('refresh-btn');
    const totalSolved = document.getElementById('total-solved');
    const easySolved = document.getElementById('easy-solved');
    const mediumSolved = document.getElementById('medium-solved');
    const hardSolved = document.getElementById('hard-solved');
    const totalChange = document.getElementById('total-change');
    const easyChange = document.getElementById('easy-change');
    const mediumChange = document.getElementById('medium-change');
    const hardChange = document.getElementById('hard-change');
    const noRewards = document.getElementById('no-rewards');
    const rewardsList = document.getElementById('rewards-list');
    const claimRewardsBtn = document.getElementById('claim-rewards-btn');
    const loadingOverlay = document.getElementById('loading-overlay');
    
    usernameForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const username = document.getElementById('leetcode-username').value.trim();
        
        if (!username) {
            showNotification('Please enter a valid LeetCode username', 'error');
            return;
        }
        
        showLoading();
        
        fetch(`/leetcode/link-account`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username: username })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                hideLoading();
                
                profileUsername.textContent = username;
                lastUpdateTime.textContent = new Date().toLocaleString();
                totalSolved.textContent = data.stats.total || '0';
                easySolved.textContent = data.stats.easy || '0';
                mediumSolved.textContent = data.stats.medium || '0';
                hardSolved.textContent = data.stats.hard || '0';
                
                usernameFormContainer.classList.add('hidden');
                profileSection.classList.remove('hidden');
                
                showNotification('LeetCode account linked successfully!', 'success');
            } else {
                hideLoading();
                showNotification(data.message || 'Failed to link LeetCode account', 'error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            hideLoading();
            showNotification('An error occurred. Please try again.', 'error');
        });
    });
    
    refreshBtn.addEventListener('click', function() {
        showLoading();
        
        fetch(`/leetcode/refresh-stats`)
        .then(response => response.json())
        .then(data => {
            hideLoading();
            
            if (data.status === 'success') {
                totalSolved.textContent = data.current_stats.total || '0';
                easySolved.textContent = data.current_stats.easy || '0';
                mediumSolved.textContent = data.current_stats.medium || '0';
                hardSolved.textContent = data.current_stats.hard || '0';
                
                updateStatChange(totalChange, data.solved_diff.total);
                updateStatChange(easyChange, data.solved_diff.easy);
                updateStatChange(mediumChange, data.solved_diff.medium);
                updateStatChange(hardChange, data.solved_diff.hard);
                
                lastUpdateTime.textContent = new Date().toLocaleString();
                
                if (data.rewards && data.rewards.length > 0) {
                    noRewards.classList.add('hidden');
                    rewardsList.classList.remove('hidden');
                    claimRewardsBtn.classList.remove('hidden');
                    
                    rewardsList.innerHTML = '';
                    data.rewards.forEach(reward => {
                        const rewardItem = document.createElement('div');
                        rewardItem.className = 'reward-item';
                        rewardItem.innerHTML = `
                            <div class="reward-stat">${reward.stat}</div>
                            <div class="reward-value">+${reward.value}</div>
                        `;
                        rewardsList.appendChild(rewardItem);
                    });
                } else {
                    noRewards.classList.remove('hidden');
                    rewardsList.classList.add('hidden');
                    claimRewardsBtn.classList.add('hidden');
                }
                
                showNotification('Stats refreshed successfully!', 'success');
            } else {
                showNotification(data.message || 'Failed to refresh stats', 'error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            hideLoading();
            showNotification('An error occurred. Please try again.', 'error');
        });
    });
    
    claimRewardsBtn.addEventListener('click', function() {
        showLoading();
        
        fetch(`/leetcode/claim-rewards`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then(response => response.json())
        .then(data => {
            hideLoading();
            
            if (data.status === 'success') {
                noRewards.classList.remove('hidden');
                rewardsList.classList.add('hidden');
                claimRewardsBtn.classList.add('hidden');
                rewardsList.innerHTML = '';
                
                resetStatChanges();
                
                showNotification('Rewards claimed successfully!', 'success');
            } else {
                showNotification(data.message || 'Failed to claim rewards', 'error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            hideLoading();
            showNotification('An error occurred. Please try again.', 'error');
        });
    });
    
    function updateStatChange(element, change) {
        if (change > 0) {
            element.innerHTML = `<span class="positive">+${change}</span>`;
        } else {
            element.innerHTML = `<span>No new problems</span>`;
        }
    }
    
    function resetStatChanges() {
        totalChange.innerHTML = `<span>No new problems</span>`;
        easyChange.innerHTML = `<span>No new problems</span>`;
        mediumChange.innerHTML = `<span>No new problems</span>`;
        hardChange.innerHTML = `<span>No new problems</span>`;
    }
    
    function showLoading() {
        loadingOverlay.classList.remove('hidden');
    }
    
    function hideLoading() {
        loadingOverlay.classList.add('hidden');
    }
    
    function showNotification(message, type) {
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.textContent = message;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.classList.add('show');
        }, 10);
        
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => notification.remove(), 300);
        }, 3000);
    }
    
    const style = document.createElement('style');
    style.textContent = `
        .notification {
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 15px 25px;
            border-radius: 8px;
            font-size: 1rem;
            color: white;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
            transform: translateX(120%);
            transition: transform 0.3s ease;
            z-index: 1000;
        }
        
        .notification.show {
            transform: translateX(0);
        }
        
        .notification.success {
            background: linear-gradient(145deg, #10b981, #059669);
        }
        
        .notification.error {
            background: linear-gradient(145deg, #ef4444, #dc2626);
        }
    `;
    document.head.appendChild(style);
});
