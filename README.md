# 🎮 Gamify - Productivity RPG Platform

Transform your productivity journey into an exciting RPG adventure! Gamify combines real-world achievements with character progression, turning coding sessions, problem-solving, and focus time into stat boosts for your virtual monster.


## 🌟 Features

### 🎯 Core Gamification
- **Real-world Integration**: Earn stat boosts through actual productivity activities
- **Visual Progress**: Radar charts and progress bars to track your growth

### 💻 Productivity Tracking
- **GitHub Integration**: Track commits and coding streaks for programming stat boosts
- **LeetCode Progress**: Monitor problem-solving achievements with difficulty-based rewards
- **Pomodoro Timer**: Focus sessions with customizable stat reward selection

### ⚔️ Battle System
- **Monster Battles**: Use your earned stats in strategic turn-based combat
- **Diverse Movesets**: 6 unique moves with special effects:
  - **Slash**: High-damage physical attack
  - **Hyper Beam**: Powerful special attack
  - **Quick Attack**: Always goes first
  - **Mud Shot**: Damages and reduces enemy speed
  - **Protect**: 60% chance to block attacks and counter
  - **Drain**: Damage that heals the user

### 🎨 UI/UX
- **Responsive Design**: Works seamlessly on desktop and mobile
- **Animations**: Engaging transitions and hover effects
- **Audio Enabled**: Optional battle music with toggle controls

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- MongoDB (local or cloud instance)
- Modern web browser

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd Gamify
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Environment Setup**
Create a `.env` file in the root directory:
```env
MONGO_URI=your_mongodb_connection_string
SECRET_KEY=your_secret_key_here
```

4. **Run the application**
```bash
python app.py
```

5. **Open your browser**
Navigate to `http://localhost:5000`

## 📖 How to Play

### 1. Create Your Account
- Sign up with a unique username and password
- Your character starts with base stats ready for growth

### 2. Link Your Accounts
- **GitHub**: Connect your GitHub username to track coding activity
- **LeetCode**: Link your LeetCode profile to monitor problem-solving progress

### 3. Earn Stat Boosts
- **GitHub Commits**: Each commit earns random stat improvements
- **LeetCode Problems**: 
  - Easy: +0.5 to random stat
  - Medium: +1.0 to random stat  
  - Hard: +2.0 to random stat
- **Pomodoro Sessions**: Complete focus sessions to choose specific stat upgrades

### 4. Battle Your Monster
- Use accumulated stats in turn-based combat
- Master different move types and strategies
- Defeat computer opponents with tactical gameplay

## 🛠️ Technical Architecture

### Backend Stack
- **Flask**: Lightweight web framework
- **MongoDB**: Document database for user data and stats
- **Python**: Core application logic

### Frontend Stack
- **HTML5/CSS3**: Semantic markup and modern styling
- **Vanilla JavaScript**: Interactive functionality without framework overhead
- **Chart.js**: Beautiful radar charts for stat visualization
- **Font Awesome**: Professional iconography

### Key Components

#### Authentication System
- Secure user registration and login
- Session management with Flask sessions
- Password hashing for security

#### Activity Integration
- **GitHub API**: Real-time commit tracking and streak calculation
- **LeetCode Scraping**: Problem submission monitoring
- **Local Pomodoro**: Built-in timer with session tracking

#### Battle Engine
- Turn-based combat system
- Move priority and speed calculations
- Special effects and status conditions
- Dynamic damage calculations based on stats

## 📁 Project Structure

```
Gamify/
├── app.py                 # Main Flask application
├── utils.py              # Utility functions
├── error_handlers.py     # Standardized error handling
├── requirements.txt      # Python dependencies
├── .env                 # Environment variables (create this)
├── templates/           # HTML templates
│   ├── index.html       # Login/Register page
│   ├── main_menu.html   # Dashboard with stats
│   ├── battle.html      # Battle interface
│   ├── github.html      # GitHub integration
│   ├── leetcode.html    # LeetCode tracking
│   └── pomodoro.html    # Focus timer
├── static/              # Static assets
│   ├── css/            # Stylesheets
│   ├── js/             # JavaScript files
│   └── assets/         # Images and audio
└── README.md           # This file
```

## 🎮 Battle System Deep Dive

### Move Details
| Move | Type | Power | Effect |
|------|------|-------|--------|
| Slash | Physical | High | Basic strong attack |
| Hyper Beam | Special | Very High | Special-based damage |
| Quick Attack | Physical | Low | +2 Priority (always first) |
| Mud Shot | Physical | Medium | Reduces target speed |
| Protect | Status | - | 60% chance to block + counter |
| Drain | Mixed | Medium | Heals user for 50% damage dealt |

### Combat Mechanics
- **Speed Priority**: Faster monsters usually move first
- **Move Priority**: Some moves override speed (Quick Attack)
- **Type Effectiveness**: Physical vs Special damage calculations
- **Status Effects**: Speed reduction, protection, healing
- **Strategic Depth**: Counter-play with Protect, speed control, sustain

## 🏆 Reward System

### GitHub Rewards
- **Per Commit**: Random stat boost
- **Streak Bonus**: Additional rewards for consecutive days
- **Repository Diversity**: Bonuses for contributing to multiple projects

### LeetCode Rewards
- **Difficulty Scaling**: Harder problems = bigger stat gains
- **Consistent Progress**: Regular solving maintains momentum
- **Skill Recognition**: Different stats for different problem types

### Pomodoro Rewards
- **Focused Sessions**: Choose your stat improvement
- **Session Completion**: Immediate feedback and growth
- **Customizable**: Target the stats you want to develop
