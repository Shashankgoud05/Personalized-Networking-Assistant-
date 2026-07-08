import os
import sys
import subprocess
import time
import signal

def main():
    print("=====================================================================")
    print("      🚀 Personalized Networking Assistant Orchestrator Launcher 🚀   ")
    print("=====================================================================")
    
    # Ensure we are in the project root directory
    project_root = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_root)
    sys.path.insert(0, project_root)
    
    # Verify file existence before booting processes
    backend_main = os.path.join("backend", "main.py")
    frontend_app = os.path.join("frontend", "app.py")
    if not os.path.exists(backend_main) or not os.path.exists(frontend_app):
        print("❌ Error: Missing core code directories. Make sure you run inside the root folder.")
        sys.exit(1)
        
    print("🔧 Booting services. Hold tight...")
    
    # Construct subprocess commands using current python interpreter to avoid global path conflicts
    fastapi_cmd = [sys.executable, "-m", "uvicorn", "backend.main:app", "--host", "127.0.0.1", "--port", "8000"]
    streamlit_cmd = [sys.executable, "-m", "streamlit", "run", "frontend/app.py", "--server.port", "8501"]
    
    processes = []
    
    try:
        # Start FastAPI backend
        print("⚡ Launching FastAPI Backend Server on http://127.0.0.1:8000...")
        backend_process = subprocess.Popen(
            fastapi_cmd,
            cwd=project_root,
            stdout=None, # Output directly to parent terminal stdout
            stderr=None
        )
        processes.append(backend_process)
        
        # Wait a short moment to let backend bind to 8000
        time.sleep(2)
        
        # Start Streamlit frontend
        print("🎨 Launching Streamlit Web App Interface on http://127.0.0.1:8501...")
        frontend_process = subprocess.Popen(
            streamlit_cmd,
            cwd=project_root,
            stdout=None,
            stderr=None
        )
        processes.append(frontend_process)
        
        print("\n✅ Both servers are running. Press Ctrl+C in this terminal window to stop all services.")
        
        # Keep orchestrator alive checking child health states
        while True:
            for p in processes:
                if p.poll() is not None:
                    print(f"⚠️ Process {p.args} stopped unexpectedly with code {p.returncode}.")
                    raise KeyboardInterrupt
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n🛑 Shutting down server processes... Graceful exit initiated.")
        for p in processes:
            if p.poll() is None:
                print(f"Terminating subprocess pid: {p.pid}...")
                try:
                    # Windows process terminate command
                    p.terminate()
                    p.wait(timeout=3)
                except subprocess.TimeoutExpired:
                    print("Force-killing unresponsive process...")
                    p.kill()
        print("👋 Services successfully stopped. Have a great networking session!")
        sys.exit(0)

if __name__ == "__main__":
    main()
