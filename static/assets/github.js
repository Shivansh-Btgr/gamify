document.addEventListener('DOMContentLoaded', function() {
    const usernameForm = document.getElementById('username-form');
    const usernameFormContainer = document.getElementById('username-form-container');
    const profileSection = document.getElementById('profile-section');
    const profileUsername = document.getElementById('profile-username');
    const lastUpdateTime = document.getElementById('last-update-time');
    const refreshBtn = document.getElementById('refresh-btn');
    const avatarImg = document.getElementById('avatar-img');
    const profileBio = document.getElementById('profile-bio');
    const totalCommits = document.getElementById('total-commits');
    const recentActivity = document.getElementById('recent-activity');
    const currentStreak = document.getElementById('current-streak');
    const commitsChange = document.getElementById('commits-change');
    const commitsList = document.getElementById('commits-list');
    const noRewards = document.getElementById('no-rewards');
    const rewardsList = document.getElementById('rewards-list');
    const claimRewardsBtn = document.getElementById('claim-rewards-btn');
    const loadingOverlay = document.getElementById('loading-overlay');
    
    usernameForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const username = document.getElementById('github-username').value.trim();
        
        if (!username) {
            showNotification('Please enter a valid GitHub username', 'error');
            return;
        }
        
        showLoading();
        
        fetch(`/github/link-account`, {
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
                
                if (data.avatar_url) {
                    avatarImg.src = data.avatar_url;
                }
                
                if (data.bio) {
                    profileBio.textContent = data.bio;
                }
                
                totalCommits.textContent = data.stats.total_commits || '0';
                recentActivity.textContent = data.stats.recent_commits || '0';
                currentStreak.textContent = data.stats.streak || '0';
                
                updateCommitsList(data.recent_commits || []);
                
                usernameFormContainer.classList.add('hidden');
                profileSection.classList.remove('hidden');
                
                showNotification('GitHub account linked successfully!', 'success');
            } else {
                hideLoading();
                showNotification(data.message || 'Failed to link GitHub account', 'error');
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
        
        fetch(`/github/refresh-stats`)
        .then(response => response.json())
        .then(data => {
            hideLoading();
            
            if (data.status === 'success') {
                totalCommits.textContent = data.stats.total_commits || '0';
                recentActivity.textContent = data.stats.recent_commits || '0';
                currentStreak.textContent = data.stats.streak || '0';
                
                if (data.commits_diff && data.commits_diff > 0) {
                    commitsChange.innerHTML = `<span class="positive">+${data.commits_diff}</span>`;
                } else {
                    commitsChange.innerHTML = `<span>No new commits</span>`;
                }
                
                updateCommitsList(data.recent_commits || []);
                
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
        
        fetch(`/github/claim-rewards`, {
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
                
                commitsChange.innerHTML = `<span>No new commits</span>`;
                
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
    
    function updateCommitsList(commits) {
        commitsList.innerHTML = '';
        
        if (commits.length === 0) {
            const noCommits = document.createElement('div');
            noCommits.className = 'no-commits';
            noCommits.textContent = 'No recent commits found.';
            commitsList.appendChild(noCommits);
            return;
        }
        
        commits.forEach(commit => {
            const commitItem = document.createElement('div');
            commitItem.className = 'commit-item';
            commitItem.innerHTML = `
                <div class="commit-repo">${commit.repo}</div>
                <div class="commit-message">${commit.message}</div>
                <div class="commit-date">${commit.date}</div>
            `;
            commitsList.appendChild(commitItem);
        });
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
            background: linear-gradient(145deg, #2ea043, #238636);
        }
        
        .notification.error {
            background: linear-gradient(145deg, #ef4444, #dc2626);
        }
    `;
    document.head.appendChild(style);
});
