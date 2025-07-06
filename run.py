from mission_launch import create_app
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=80)