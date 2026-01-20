// Jenkins CI/CD Demo App - Frontend JavaScript

// Configuration
const API_BASE_URL = 'http://localhost:5000';

// DOM Elements
const checkApiBtn = document.getElementById('checkApiBtn');
const statusIndicator = document.getElementById('statusIndicator');
const statusDot = statusIndicator.querySelector('.status-dot');
const statusText = statusIndicator.querySelector('.status-text');
const apiResponse = document.getElementById('apiResponse');
const appVersion = document.getElementById('appVersion');

// Application State
let isChecking = false;

// Initialize the application
document.addEventListener('DOMContentLoaded', () => {
    console.log('🚀 CI/CD Demo App Initialized');
    setVersion();
    checkApiStatus();
    initializeEventListeners();
    startPipelineAnimation();
});

// Set up event listeners
function initializeEventListeners() {
    checkApiBtn.addEventListener('click', handleCheckApiClick);
}

// Handle API check button click
async function handleCheckApiClick() {
    if (isChecking) return;
    
    isChecking = true;
    checkApiBtn.disabled = true;
    checkApiBtn.innerHTML = '<span class="btn-icon">⏳</span> Checking...';
    
    await checkApiStatus();
    
    isChecking = false;
    checkApiBtn.disabled = false;
    checkApiBtn.innerHTML = '<span class="btn-icon">⚡</span> Check API Status';
}

// Check API status
async function checkApiStatus() {
    updateStatus('checking', 'Checking...');
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/health`, {
            method: 'GET',
            headers: {
                'Accept': 'application/json',
            },
            mode: 'cors',
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        updateStatus('online', 'Online');
        displayResponse(data);
        
        // Also fetch additional info
        fetchAppInfo();
        
    } catch (error) {
        console.error('API Error:', error);
        updateStatus('offline', 'Offline');
        displayResponse({
            error: 'Failed to connect to API',
            message: error.message,
            hint: 'Make sure the Flask backend is running on port 5000'
        });
    }
}

// Fetch additional app info
async function fetchAppInfo() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/info`);
        const data = await response.json();
        if (data.version) {
            appVersion.textContent = data.version;
        }
    } catch (error) {
        console.log('Could not fetch app info:', error);
    }
}

// Update status indicator
function updateStatus(status, text) {
    statusDot.className = 'status-dot';
    
    switch (status) {
        case 'online':
            statusDot.classList.add('online');
            statusText.style.color = 'var(--success)';
            break;
        case 'offline':
            statusDot.classList.add('offline');
            statusText.style.color = 'var(--error)';
            break;
        default:
            statusText.style.color = 'var(--warning)';
    }
    
    statusText.textContent = text;
}

// Display API response
function displayResponse(data) {
    const pre = apiResponse.querySelector('pre');
    pre.textContent = JSON.stringify(data, null, 2);
}

// Set version from build
function setVersion() {
    // This could be replaced during build process
    appVersion.textContent = '1.0.0';
}

// Pipeline animation enhancement
function startPipelineAnimation() {
    const stages = document.querySelectorAll('.pipeline-stage');
    let currentStage = 0;
    
    setInterval(() => {
        stages.forEach((stage, index) => {
            if (index === currentStage) {
                stage.style.borderColor = 'var(--primary)';
                stage.style.boxShadow = '0 0 30px rgba(99, 102, 241, 0.5)';
            } else {
                stage.style.borderColor = 'var(--glass-border)';
                stage.style.boxShadow = 'none';
            }
        });
        
        currentStage = (currentStage + 1) % stages.length;
    }, 1500);
}

// Smooth scroll for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Console easter egg
console.log(`
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║   🚀 Jenkins CI/CD Demo Application                       ║
║                                                           ║
║   Built with:                                             ║
║   • Frontend: HTML, CSS, JavaScript                       ║
║   • Backend:  Python Flask                                ║
║   • CI/CD:    Jenkins Pipelines                           ║
║   • Infra:    Docker Containers                           ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
`);
