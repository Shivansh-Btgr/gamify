from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
import os
import random
from dotenv import load_dotenv
from bson.objectid import ObjectId
import requests
from datetime import datetime
import json

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'default-secret-key')


# Connect to MongoDB
client = MongoClient(os.getenv('MONGO_URI', 'mongodb://localhost:27017/'))
db = client['gamify_db']
users_collection = db['users']

# Default stats for new users
DEFAULT_STATS = {
    "HP": 20,
    "atk": 5,
    "def": 5,
    "spA": 5,
    "spD": 5,
    "Spe": 5
}

MONSTER_IMAGES = ['Atrox.png', 'Charmadillo.png', 'Cindrill.png', 'Cleaf.png', 'Draem.png', 'Finiette.png', 'Finsta.png', 'Friolera.png', 'Gulfin.png', 'Ivieron.png', 'Jacana.png', 'Larvae.png', 'Pluma.png', 'Plumette.png', 'Pouch.png', 'Sparchu.png']

# Activity rewards configuration
ACTIVITY_REWARDS = {
    'github': {
        'HP': 1,
        'atk': 0.5,
        'def': 0.5,
        'spA': 1,
        'spD': 0.5,
        'Spe': 0.5
    },
    'reading': {
        'HP': 0.5,
        'atk': 0.5,
        'def': 0.5,
        'spA': 1,
        'spD': 1,
        'Spe': 0.5
    },
    'pomodoro': {
        'HP': 0.5,
        'atk': 0.5,
        'def': 1,
        'spA': 0.5,
        'spD': 0.5,
        'Spe': 1
    }
}

# Stat increase for LeetCode problems by difficulty
LEETCODE_REWARDS = {
    'easy': 0.5,
    'medium': 1.0,
    'hard': 2.0
}

# LeetScan API base URL
LEETSCAN_API_URL = "https://leetscan.vercel.app/"

# GitHub API base URL
GITHUB_API_URL = "https://api.github.com/"

# GitHub reward configuration
GITHUB_REWARDS = {
    'commit': {
        'value': 0.5,  # Base value per commit
        'streak_bonus': 0.1,  # Additional value per day in streak
        'max_streak_bonus': 1.0  # Maximum streak bonus
    }
}

@app.route('/')
def home():
    if 'user_id' in session:
        return redirect(url_for('main_menu'))
    return render_template('login.html')

@app.route('/signup', methods=['POST'])
def signup():
    data = request.form
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    confirm_password = data.get('confirm_password')
    
    # Validate form data
    if not all([name, email, password, confirm_password]) or password != confirm_password:
        return jsonify({'status': 'error', 'message': 'Invalid form data'})
    
    # Check if user already exists
    existing_user = users_collection.find_one({'email': email})
    if existing_user:
        return jsonify({'status': 'error', 'message': 'Email already exists'})
    
    # Create new user with default stats
    new_user = {
        'name': name,
        'email': email,
        'password': generate_password_hash(password),
        'stats': DEFAULT_STATS
    }
    
    result = users_collection.insert_one(new_user)
    
    # Store user in session
    session['user_id'] = str(result.inserted_id)
    session['name'] = name
    session['stats'] = DEFAULT_STATS
    
    return jsonify({'status': 'success', 'redirect': url_for('main_menu')})

@app.route('/login', methods=['POST'])
def login():
    data = request.form
    email = data.get('email')
    password = data.get('password')
    
    # Find user
    user = users_collection.find_one({'email': email})
    if not user or not check_password_hash(user['password'], password):
        return jsonify({'status': 'error', 'message': 'Invalid email or password'})
    
    # Store user in session
    session['user_id'] = str(user['_id'])
    session['name'] = user['name']
    session['stats'] = user['stats']
    
    return jsonify({'status': 'success', 'redirect': url_for('main_menu')})

@app.route('/main-menu')
def main_menu():
    if 'user_id' not in session:
        return redirect(url_for('home'))
    
    return render_template('main_menu.html', 
                          name=session.get('name', 'Player'), 
                          stats=session.get('stats', DEFAULT_STATS))

@app.route('/battle')
def battle():
    if 'user_id' not in session:
        return redirect(url_for('home'))
    
    # Get user stats from session
    user_monster = random.choice(MONSTER_IMAGES)
    pc_monster = random.choice(MONSTER_IMAGES)
    
    # Make sure user and PC don't get the same monster
    while pc_monster == user_monster:
        pc_monster = random.choice(MONSTER_IMAGES)
    
    # Create list of all possible moves
    all_moves = [
        {"id": "slash", "name": "Slash", "type": "physical", "priority": 0},
        {"id": "hyperbeam", "name": "Hyper Beam", "type": "special", "priority": 0},
        {"id": "quickattack", "name": "Quick Attack", "type": "physical", "priority": 1},
        {"id": "mudshot", "name": "Mud Shot", "type": "physical", "priority": 0, "side_effect": "speed"},
        {"id": "protect", "name": "Protect", "type": "status", "priority": 0},
        {"id": "counter", "name": "Counter", "type": "physical", "priority": -1},
        {"id": "drain", "name": "Drain", "type": "mixed", "priority": 0, "side_effect": "heal"}
    ]
    
    # Select 4 random moves for user and PC
    user_moves = random.sample(all_moves, 4)
    pc_moves = random.sample(all_moves, 4)
    
    # Define user stats and pc stats - this was missing
    user_stats = session.get('stats', DEFAULT_STATS)
    
    # Create PC stats with some randomness
    pc_stats = {
        "HP": random.randint(15, 25),
        "atk": random.randint(4, 7),
        "def": random.randint(4, 7),
        "spA": random.randint(4, 7),
        "spD": random.randint(4, 7),
        "Spe": random.randint(4, 7)
    }
    
    return render_template(
        'battle.html', 
        user_monster=user_monster,
        pc_monster=pc_monster,
        user_stats=user_stats,
        pc_stats=pc_stats,
        user_moves=user_moves,
        pc_moves=pc_moves,
        name=session.get('name', 'Player')
    )

@app.route('/leetcode')
def leetcode():
    if 'user_id' not in session:
        return redirect(url_for('home'))
    
    # Get user
    user = users_collection.find_one({'_id': ObjectId(session['user_id'])})
    
    # Check if user has LeetCode account linked
    leetcode_username = user.get('leetcode_username', '')
    
    # Get last update time
    last_update = user.get('leetcode_last_update', 'Never')
    
    # Get current stats
    current_stats = user.get('leetcode_stats', {
        'total': 0,
        'easy': 0,
        'medium': 0,
        'hard': 0
    })
    
    # Get solved diff
    solved_diff = user.get('leetcode_solved_diff', {
        'total': 0,
        'easy': 0,
        'medium': 0,
        'hard': 0
    })
    
    # Get rewards
    rewards = user.get('leetcode_rewards', [])
    
    return render_template('leetcode.html', 
                          leetcode_username=leetcode_username,
                          last_update=last_update,
                          current_stats=current_stats,
                          solved_diff=solved_diff,
                          rewards=rewards)

@app.route('/leetcode/link-account', methods=['POST'])
def link_leetcode_account():
    if 'user_id' not in session:
        return jsonify({'status': 'error', 'message': 'Not logged in'})
    
    data = request.json
    username = data.get('username')
    
    if not username:
        return jsonify({'status': 'error', 'message': 'Username is required'})
    
    # Try to fetch LeetCode stats
    try:
        response = requests.get(LEETSCAN_API_URL + username)
        leetcode_data = response.json()
        
        if 'error' in leetcode_data:
            return jsonify({'status': 'error', 'message': 'Invalid LeetCode username'})
        
        # Extract solving count
        solving_count = leetcode_data #
        
        stats = {
            'total': solving_count.get('totalSubmissions', 0),
            'easy': solving_count.get('easySolved', 0),
            'medium': solving_count.get('mediumSolved', 0),
            'hard': solving_count.get('hardSolved', 0)
        }
        
        # Update user in database
        users_collection.update_one(
            {'_id': ObjectId(session['user_id'])},
            {'$set': {
                'leetcode_username': username,
                'leetcode_stats': stats,
                'leetcode_last_update': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'leetcode_solved_diff': {
                    'total': 0,
                    'easy': 0,
                    'medium': 0,
                    'hard': 0
                },
                'leetcode_rewards': []
            }}
        )
        
        return jsonify({
            'status': 'success',
            'message': 'LeetCode account linked successfully',
            'stats': stats
        })
        
    except Exception as e:
        print(f"Error linking LeetCode account: {e}")
        return jsonify({'status': 'error', 'message': 'Failed to fetch LeetCode data'})

@app.route('/leetcode/refresh-stats')
def refresh_leetcode_stats():
    if 'user_id' not in session:
        return jsonify({'status': 'error', 'message': 'Not logged in'})
    
    # Get user
    user = users_collection.find_one({'_id': ObjectId(session['user_id'])})
    
    if not user or 'leetcode_username' not in user:
        return jsonify({'status': 'error', 'message': 'LeetCode account not linked'})
    
    username = user['leetcode_username']
    old_stats = user.get('leetcode_stats', {
        'total': 0,
        'easy': 0,
        'medium': 0,
        'hard': 0
    })
    
    # Try to fetch new LeetCode stats
    try:
        response = requests.get(LEETSCAN_API_URL + username)
        leetcode_data = response.json()
        
        if 'error' in leetcode_data:
            return jsonify({'status': 'error', 'message': 'Failed to fetch LeetCode data'})
        
        # Extract solving count
        solving_count = leetcode_data #
        
        new_stats = {
            'total': solving_count.get('totalSubmissions', 0),
            'easy': solving_count.get('easySolved', 0),
            'medium': solving_count.get('mediumSolved', 0),
            'hard': solving_count.get('hardSolved', 0)
        }
        
        # Calculate differences
        solved_diff = {
            'total': max(0, new_stats['total'] - old_stats['total']),
            'easy': max(0, new_stats['easy'] - old_stats['easy']),
            'medium': max(0, new_stats['medium'] - old_stats['medium']),
            'hard': max(0, new_stats['hard'] - old_stats['hard'])
        }
        
        # Calculate rewards
        rewards = []
        
        # For each difficulty level
        for difficulty in ['easy', 'medium', 'hard']:
            if solved_diff[difficulty] > 0:
                # For each problem solved
                for _ in range(solved_diff[difficulty]):
                    # Determine reward amount
                    reward_amount = LEETCODE_REWARDS[difficulty]
                    
                    # Randomly select a stat to improve
                    stat = random.choice(['HP', 'atk', 'def', 'spA', 'spD', 'Spe'])
                    
                    # Add to rewards list
                    rewards.append({
                        'stat': stat,
                        'value': reward_amount
                    })
        
        # Update user in database
        users_collection.update_one(
            {'_id': ObjectId(session['user_id'])},
            {'$set': {
                'leetcode_stats': new_stats,
                'leetcode_last_update': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'leetcode_solved_diff': solved_diff,
                'leetcode_rewards': rewards
            }}
        )
        
        return jsonify({
            'status': 'success',
            'message': 'LeetCode stats refreshed successfully',
            'current_stats': new_stats,
            'solved_diff': solved_diff,
            'rewards': rewards
        })
        
    except Exception as e:
        print(f"Error refreshing LeetCode stats: {e}")
        return jsonify({'status': 'error', 'message': 'Failed to fetch LeetCode data'})

@app.route('/leetcode/claim-rewards', methods=['POST'])
def claim_leetcode_rewards():
    if 'user_id' not in session:
        return jsonify({'status': 'error', 'message': 'Not logged in'})
    
    # Get user
    user = users_collection.find_one({'_id': ObjectId(session['user_id'])})
    
    if not user or 'leetcode_rewards' not in user:
        return jsonify({'status': 'error', 'message': 'No rewards to claim'})
    
    rewards = user.get('leetcode_rewards', [])
    
    if not rewards:
        return jsonify({'status': 'error', 'message': 'No rewards to claim'})
    
    # Apply rewards to user stats
    for reward in rewards:
        stat = reward.get('stat')
        value = reward.get('value')
        
        if stat in user['stats']:
            user['stats'][stat] += value
    
    # Update user in database
    users_collection.update_one(
        {'_id': ObjectId(session['user_id'])},
        {'$set': {
            'stats': user['stats'],
            'leetcode_solved_diff': {
                'total': 0,
                'easy': 0,
                'medium': 0,
                'hard': 0
            },
            'leetcode_rewards': []
        }}
    )
    
    # Update session
    session['stats'] = user['stats']
    
    return jsonify({
        'status': 'success',
        'message': 'Rewards claimed successfully'
    })

@app.route('/github')
def github():
    if 'user_id' not in session:
        return redirect(url_for('home'))
    
    # Get user
    user = users_collection.find_one({'_id': ObjectId(session['user_id'])})
    
    # Check if user has GitHub account linked
    github_username = user.get('github_username', '')
    
    # Get last update time
    last_update = user.get('github_last_update', 'Never')
    
    # Get GitHub profile data
    github_avatar = user.get('github_avatar', '')
    github_bio = user.get('github_bio', '')
    
    # Get commits stats
    commits_stats = user.get('github_stats', {
        'total_commits': 0,
        'recent_commits': 0,
        'streak': 0
    })
    
    # Get commits diff for rewards
    commits_diff = user.get('github_commits_diff', 0)
    
    # Get recent commits
    recent_commits = user.get('github_recent_commits', [])
    
    # Get rewards
    rewards = user.get('github_rewards', [])
    
    return render_template('github.html', 
                           github_username=github_username,
                           last_update=last_update,
                           github_avatar=github_avatar,
                           github_bio=github_bio,
                           commits_stats=commits_stats,
                           commits_diff=commits_diff,
                           recent_commits=recent_commits,
                           rewards=rewards)

@app.route('/github/link-account', methods=['POST'])
def link_github_account():
    if 'user_id' not in session:
        return jsonify({'status': 'error', 'message': 'Not logged in'})
    
    data = request.json
    username = data.get('username')
    
    if not username:
        return jsonify({'status': 'error', 'message': 'Username is required'})
    
    # Try to fetch GitHub profile data
    try:
        # Fetch user profile from GitHub API
        headers = {}
        if os.getenv('GITHUB_TOKEN'):
            headers['Authorization'] = f'token {os.getenv("GITHUB_TOKEN")}'
            
        profile_response = requests.get(f"{GITHUB_API_URL}users/{username}", headers=headers)
        
        if profile_response.status_code != 200:
            return jsonify({'status': 'error', 'message': 'Invalid GitHub username'})
        
        profile_data = profile_response.json()
        
        # Fetch user repositories
        repos_response = requests.get(f"{GITHUB_API_URL}users/{username}/repos", headers=headers)
        repos_data = repos_response.json() if repos_response.status_code == 200 else []
        
        # Fetch recent commits (we'll need to check each repository)
        recent_commits = []
        total_commits = 0
        
        for repo in repos_data[:5]:  # Limit to 5 repos to avoid rate limits
            repo_name = repo['name']
            commits_url = f"{GITHUB_API_URL}repos/{username}/{repo_name}/commits"
            commits_response = requests.get(commits_url, headers=headers)
            
            if commits_response.status_code == 200:
                repo_commits = commits_response.json()
                total_commits += len(repo_commits)
                
                # Add recent commit info
                for commit in repo_commits[:3]:  # Get top 3 recent commits per repo
                    commit_data = {
                        'repo': repo_name,
                        'message': commit['commit']['message'],
                        'date': commit['commit']['author']['date']
                    }
                    recent_commits.append(commit_data)
        
        # Calculate streak (simplified version - actual calculation would be more complex)
        # This is a placeholder - real implementation would analyze commit dates
        streak = min(7, total_commits // 5)  # Just a simple formula for example
        
        # Prepare stats
        stats = {
            'total_commits': total_commits,
            'recent_commits': len(recent_commits),
            'streak': streak
        }
        
        # Update user in database
        users_collection.update_one(
            {'_id': ObjectId(session['user_id'])},
            {'$set': {
                'github_username': username,
                'github_avatar': profile_data.get('avatar_url', ''),
                'github_bio': profile_data.get('bio', 'No bio available'),
                'github_stats': stats,
                'github_last_update': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'github_commits_diff': 0,
                'github_recent_commits': recent_commits[:10],  # Store only 10 most recent commits
                'github_rewards': []
            }}
        )
        
        return jsonify({
            'status': 'success',
            'message': 'GitHub account linked successfully',
            'avatar_url': profile_data.get('avatar_url', ''),
            'bio': profile_data.get('bio', 'No bio available'),
            'stats': stats,
            'recent_commits': recent_commits[:10]  # Return only 10 most recent commits
        })
        
    except Exception as e:
        print(f"Error linking GitHub account: {e}")
        return jsonify({'status': 'error', 'message': 'Failed to fetch GitHub data'})

@app.route('/github/refresh-stats')
def refresh_github_stats():
    if 'user_id' not in session:
        return jsonify({'status': 'error', 'message': 'Not logged in'})
    
    # Get user
    user = users_collection.find_one({'_id': ObjectId(session['user_id'])})
    
    if not user or 'github_username' not in user:
        return jsonify({'status': 'error', 'message': 'GitHub account not linked'})
    
    username = user['github_username']
    old_stats = user.get('github_stats', {
        'total_commits': 0,
        'recent_commits': 0,
        'streak': 0
    })
    
    # Try to fetch new GitHub stats
    try:
        # Set up headers with token if available
        headers = {}
        if os.getenv('GITHUB_TOKEN'):
            headers['Authorization'] = f'token {os.getenv("GITHUB_TOKEN")}'
            
        # Fetch user profile from GitHub API
        profile_response = requests.get(f"{GITHUB_API_URL}users/{username}", headers=headers)
        
        if profile_response.status_code != 200:
            return jsonify({'status': 'error', 'message': 'Failed to fetch GitHub profile'})
        
        profile_data = profile_response.json()
        
        # Fetch user repositories
        repos_response = requests.get(f"{GITHUB_API_URL}users/{username}/repos", headers=headers)
        repos_data = repos_response.json() if repos_response.status_code == 200 else []
        
        # Fetch recent commits (we'll need to check each repository)
        recent_commits = []
        total_commits = 0
        
        for repo in repos_data[:5]:  # Limit to 5 repos to avoid rate limits
            repo_name = repo['name']
            commits_url = f"{GITHUB_API_URL}repos/{username}/{repo_name}/commits"
            commits_response = requests.get(commits_url, headers=headers)
            
            if commits_response.status_code == 200:
                repo_commits = commits_response.json()
                total_commits += len(repo_commits)
                
                # Add recent commit info
                for commit in repo_commits[:3]:  # Get top 3 recent commits per repo
                    commit_data = {
                        'repo': repo_name,
                        'message': commit['commit']['message'],
                        'date': commit['commit']['author']['date']
                    }
                    recent_commits.append(commit_data)
        
        # Calculate streak (simplified version - actual calculation would be more complex)
        # This is a placeholder - real implementation would analyze commit dates
        streak = min(7, total_commits // 5)  # Just a simple formula for example
        
        # Prepare stats
        new_stats = {
            'total_commits': total_commits,
            'recent_commits': len(recent_commits),
            'streak': streak
        }
        
        # Calculate difference in commits
        commits_diff = max(0, new_stats['total_commits'] - old_stats['total_commits'])
        
        # Calculate rewards
        rewards = []
        
        if commits_diff > 0:
            # Calculate streak bonus
            streak_bonus = min(
                GITHUB_REWARDS['commit']['streak_bonus'] * new_stats['streak'],
                GITHUB_REWARDS['commit']['max_streak_bonus']
            )
            
            # Total reward value per commit
            reward_per_commit = GITHUB_REWARDS['commit']['value'] + streak_bonus
            
            # For each new commit
            for _ in range(commits_diff):
                # Randomly select a stat to improve
                stat = random.choice(['HP', 'atk', 'def', 'spA', 'spD', 'Spe'])
                
                # Add to rewards list
                rewards.append({
                    'stat': stat,
                    'value': reward_per_commit
                })
        
        # Update user in database
        users_collection.update_one(
            {'_id': ObjectId(session['user_id'])},
            {'$set': {
                'github_avatar': profile_data.get('avatar_url', ''),
                'github_bio': profile_data.get('bio', 'No bio available'),
                'github_stats': new_stats,
                'github_last_update': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'github_commits_diff': commits_diff,
                'github_recent_commits': recent_commits[:10],  # Store only 10 most recent commits
                'github_rewards': rewards
            }}
        )
        
        return jsonify({
            'status': 'success',
            'message': 'GitHub stats refreshed successfully',
            'stats': new_stats,
            'commits_diff': commits_diff,
            'recent_commits': recent_commits[:10],
            'rewards': rewards
        })
        
    except Exception as e:
        print(f"Error refreshing GitHub stats: {e}")
        return jsonify({'status': 'error', 'message': 'Failed to fetch GitHub data'})

@app.route('/github/claim-rewards', methods=['POST'])
def claim_github_rewards():
    if 'user_id' not in session:
        return jsonify({'status': 'error', 'message': 'Not logged in'})
    
    # Get user
    user = users_collection.find_one({'_id': ObjectId(session['user_id'])})
    
    if not user or 'github_rewards' not in user:
        return jsonify({'status': 'error', 'message': 'No rewards to claim'})
    
    rewards = user.get('github_rewards', [])
    
    if not rewards:
        return jsonify({'status': 'error', 'message': 'No rewards to claim'})
    
    # Apply rewards to user stats
    for reward in rewards:
        stat = reward.get('stat')
        value = reward.get('value')
        
        if stat in user['stats']:
            user['stats'][stat] += value
    
    # Update user in database
    users_collection.update_one(
        {'_id': ObjectId(session['user_id'])},
        {'$set': {
            'stats': user['stats'],
            'github_commits_diff': 0,
            'github_rewards': []
        }}
    )
    
    # Update session
    session['stats'] = user['stats']
    
    return jsonify({
        'status': 'success',
        'message': 'Rewards claimed successfully'
    })

@app.route('/pomodoro')
def pomodoro():
    if 'user_id' not in session:
        return redirect(url_for('home'))
    
    return render_template('pomodoro.html')

@app.route('/activity', methods=['POST'])
def log_activity():
    if 'user_id' not in session:
        return jsonify({'status': 'error', 'message': 'Not logged in'})
    
    data = request.json
    activity_type = data.get('activity_type')
    
    if activity_type not in ACTIVITY_REWARDS:
        return jsonify({'status': 'error', 'message': 'Invalid activity type'})
    
    # Get current user stats
    user = users_collection.find_one({'_id': ObjectId(session['user_id'])})
    if not user:
        return jsonify({'status': 'error', 'message': 'User not found'})
    
    stats_gained = []
    
    # Handle single stat update for pomodoro
    if activity_type == 'pomodoro' and 'single_stat' in data:
        stat = data.get('single_stat')
        gain = data.get('stat_gain', 0.5)  # Default to 0.5 if not specified
        
        if stat in user['stats']:
            user['stats'][stat] += gain
            stats_gained.append(f"+{gain} {stat}")
    
    # Handle pomodoro with custom stat allocation
    elif activity_type == 'pomodoro' and 'selected_stats' in data:
        selected_stats = data.get('selected_stats', [])
        for stat in selected_stats:
            if stat in user['stats']:
                # HP gets +1, other stats get +0.5
                gain = 1.0 if stat == 'HP' else 0.5
                user['stats'][stat] += gain
                stats_gained.append(f"+{gain} {stat}")
    else:
        # Handle other activity types with fixed rewards
        rewards = ACTIVITY_REWARDS[activity_type]
        
        # For pomodoro without custom selection, multiply by sessions completed if provided
        sessions_multiplier = 1
        if activity_type == 'pomodoro' and 'sessions_completed' in data:
            sessions_multiplier = min(data.get('sessions_completed'), 4)  # Cap at 4 sessions max
        
        # Update stats
        for stat, value in rewards.items():
            if stat in user['stats']:
                # Round to nearest 0.5
                gain = round((value * sessions_multiplier) * 2) / 2
                user['stats'][stat] += gain
                stats_gained.append(f"+{gain} {stat}")
    
    # Update user in database
    users_collection.update_one(
        {'_id': ObjectId(session['user_id'])},
        {'$set': {'stats': user['stats']}}
    )
    
    # Update session
    session['stats'] = user['stats']
    
    return jsonify({
        'status': 'success',
        'message': 'Activity logged successfully',
        'stats_gained': stats_gained
    })

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)