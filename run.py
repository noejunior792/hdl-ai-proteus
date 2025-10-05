#!/usr/bin/env python3
"""
HDL AI Proteus - Startup Script

This script provides a convenient way to start the HDL AI Proteus API server
from the root directory of the project.
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    """Main startup function"""
    # Get the directory where this script is located
    script_dir = Path(__file__).parent.absolute()
    
    # Add src directory to Python path
    src_dir = script_dir / "src"
    if str(src_dir) not in sys.path:
        sys.path.insert(0, str(src_dir))
    
    # Change to the project directory
    os.chdir(script_dir)
    
    # Check if we're in a virtual environment
    if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("⚠️  Warning: You're not in a virtual environment!")
        print("   Consider creating one with: python3 -m venv venv && source venv/bin/activate")
        print()
    
    # Check if requirements are installed
    try:
        import flask
        import requests
    except ImportError:
        print("❌ Missing dependencies! Please install requirements:")
        print("   pip install -r requirements.txt")
        sys.exit(1)
    
    # Check if GHDL and Icarus Verilog are available
    tools_missing = []
    
    try:
        subprocess.run(['ghdl', '--version'], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        tools_missing.append('GHDL')
    
    try:
        subprocess.run(['iverilog', '-V'], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        tools_missing.append('Icarus Verilog')
    
    if tools_missing:
        print(f"⚠️  Warning: Missing HDL compilers: {', '.join(tools_missing)}")
        print("   Install with: sudo apt install ghdl iverilog")
        print("   The API will still work but HDL compilation will fail")
        print()
    
    # Create necessary directories
    for directory in ['build', 'export', 'temp', 'logs']:
        os.makedirs(directory, exist_ok=True)
    
    print("🚀 Starting HDL AI Proteus API...")
    print(f"📁 Project directory: {script_dir}")
    print(f"🐍 Python executable: {sys.executable}")
    print()
    
    # Import and run the Flask app
    try:
        from src.app import app, initialize_app
        
        # Initialize the application first
        initialize_app()
        
        print(f"🌐 Starting server on localhost:5000")
        print(f"🔧 Environment: development")
        print(f"📊 Log level: INFO")
        print()
        print("API Endpoints:")
        print(f"  Health Check: http://localhost:5000/health")
        print(f"  API Info:     http://localhost:5000/api/info")
        print(f"  Generate:     http://localhost:5000/generate")
        print()
        print("Press Ctrl+C to stop the server")
        print("=" * 60)
        
        # Run the Flask application with default settings
        app.run(
            host="0.0.0.0",
            port=5000,
            debug=True,
            threaded=True
        )
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("   Make sure you're in the correct directory and all dependencies are installed")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()