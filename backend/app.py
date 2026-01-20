"""
Flask Backend for Jenkins CI/CD Demo Application
A simple REST API to demonstrate CI/CD pipelines
"""

import os
import datetime
from flask import Flask, jsonify, request
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)

# Enable CORS for frontend communication
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Application metadata
APP_VERSION = os.environ.get('APP_VERSION', '1.0.0')
APP_NAME = "Jenkins CI/CD Demo API"
BUILD_NUMBER = os.environ.get('BUILD_NUMBER', 'local')


@app.route('/')
def home():
    """Root endpoint - Welcome message"""
    return jsonify({
        "message": "Welcome to Jenkins CI/CD Demo API",
        "version": APP_VERSION,
        "docs": "/api/info",
        "endpoints": {
            "health": "/api/health",
            "info": "/api/info",
            "echo": "/api/echo"
        }
    })


@app.route('/api/health')
def health():
    """Health check endpoint for container orchestration"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "service": APP_NAME
    })


@app.route('/api/info')
def info():
    """Application information endpoint"""
    return jsonify({
        "name": APP_NAME,
        "version": APP_VERSION,
        "build_number": BUILD_NUMBER,
        "python_version": os.popen('python --version').read().strip(),
        "endpoints": [
            {"path": "/", "method": "GET", "description": "Welcome message"},
            {"path": "/api/health", "method": "GET", "description": "Health check"},
            {"path": "/api/info", "method": "GET", "description": "Application info"},
            {"path": "/api/echo", "method": "POST", "description": "Echo service"},
        ],
        "timestamp": datetime.datetime.utcnow().isoformat()
    })


@app.route('/api/echo', methods=['POST'])
def echo():
    """Echo endpoint - returns the data sent to it"""
    data = request.get_json(silent=True) or {}
    return jsonify({
        "received": data,
        "message": "Echo successful!",
        "timestamp": datetime.datetime.utcnow().isoformat()
    })


@app.route('/api/pipeline-status')
def pipeline_status():
    """Simulated pipeline status endpoint"""
    return jsonify({
        "pipeline": "Jenkins CI/CD Demo",
        "stages": [
            {"name": "Build", "status": "success", "duration": "45s"},
            {"name": "Test", "status": "success", "duration": "1m 23s"},
            {"name": "Docker Build", "status": "success", "duration": "2m 10s"},
            {"name": "Deploy", "status": "success", "duration": "30s"}
        ],
        "overall_status": "success",
        "build_number": BUILD_NUMBER
    })


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        "error": "Not Found",
        "message": "The requested endpoint does not exist",
        "status": 404
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        "error": "Internal Server Error",
        "message": "An unexpected error occurred",
        "status": 500
    }), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    print(f"""
    ╔═══════════════════════════════════════════════════════╗
    ║                                                       ║
    ║   🚀 Jenkins CI/CD Demo API                           ║
    ║                                                       ║
    ║   Version:  {APP_VERSION:<10}                              ║
    ║   Build:    {BUILD_NUMBER:<15}                         ║
    ║   Port:     {port:<10}                              ║
    ║                                                       ║
    ╚═══════════════════════════════════════════════════════╝
    """)
    
    app.run(host='0.0.0.0', port=port, debug=debug)
