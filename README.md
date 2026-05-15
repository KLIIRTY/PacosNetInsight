Pacos NetInsight
AI-Powered Network Intelligence & Telemetry Dashboard
Pacos NetInsight is a containerized Network Operations Center (NOC) tool designed for real-time anomaly detection and predictive traffic forecasting. Built for the era of 5G and Software-Defined Networking (SDN), it leverages machine learning to transform raw network logs into actionable security intelligence.

🚀 Core Specializations
Anomaly Detection: Utilizes Isolation Forest algorithms to detect suspicious packet flows and zero-day threats.

Predictive Telemetry: Integrated with Facebook Prophet to forecast network traffic trends and identify potential capacity bottlenecks.

Cloud-Native Architecture: Fully containerized using Docker for seamless deployment in Virtualized Network Function (VNF) environments.

Infrastructure as Code (IaC): Optimized for VS Code Dev Containers to ensure 100% environment parity.

🛠 Tech Stack
Language: Python 3.11+

Framework: Streamlit (NOC Dashboard)

ML Engines: Scikit-learn (Isolation Forest), Facebook Prophet (Forecasting)

Infrastructure: Docker, Dev Containers

Data Science: Pandas, NumPy, SciPy

📦 Getting Started (The "NOC" Way)
Option 1: Using Dev Containers (Recommended)
This project is pre-configured for VS Code Dev Containers. This ensures your Mac stays cool and your environment is perfectly isolated.

Clone the repo: git clone https://github.com/KLIIRTY/PacosNetInsight.git

Open the folder in VS Code.

Click "Reopen in Container" when prompted.

The dashboard will automatically launch at http://localhost:8501.
Option 2: Using Standard Docker
docker build -t pacos-netinsight .
docker run -p 8501:8501 pacos-netinsight
📂 Project Architecture
PacosNetInsight/
├── .devcontainer/     # Environment Orchestration
├── .streamlit/        # Dashboard Configuration
├── data/              # Network Telemetry Logs
├── src/               
│   ├── app.py         # NOC Dashboard Interface
│   ├── model.py       # ML Anomaly Detection Logic
│   ├── prediction.py  # Prophet Forecasting Engine
│   └── generate_logs.py # Synthetic Telemetry Generator
├── Dockerfile         # VNF Build Instructions
├── requirements.txt   # Dependency Manifest
└── README.md          # Engineering Documentation
🧪 Testing & Validation
The system uses pytest to ensure logic consistency across network parsing and ML modules:
pytest
👨‍💻 Author
Kelvin Njiru NOC Engineer | Specialized in 5G, NFV, and SDN labs:https://kelvinjiru.netlify.app/networking
