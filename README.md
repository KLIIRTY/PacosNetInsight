# 🔥 Pacos NetInsight

Pacos NetInsight is an **AI-powered network anomaly detection dashboard** built in Python and Streamlit. It monitors network traffic logs, detects suspicious activity using machine learning, assigns risk levels, and provides interactive visualizations in real-time.

---

## 🌐 Live Demo
Check out the live app here: [Pacos NetInsight](https://pacosnetinsight.streamlit.app/)

---

## 🛠 Features
- **Network Log Analysis:** Reads network traffic logs from CSV files.  
- **Anomaly Detection:** Uses `IsolationForest` to detect suspicious activity.  
- **Risk Assessment:** Assigns HIGH, MEDIUM, or LOW risk levels based on packet size, failed logins, and ports.  
- **Interactive Dashboard:** Streamlit-based dashboard with:
  - Summary statistics
  - Suspicious activity table
  - Traffic visualization over time  
- **Real-time Deployment:** Updates automatically on GitHub push using Streamlit Cloud.

---

## ⚙️ Installation / Running Locally

1. Clone the repository:

```bash
git clone https://github.com/KLIIRTY/PacosNetInsight.git
cd PacosNetInsight
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
pip install -r requirements.txt
pip install -r requirements.txt
streamlit run src/app.py

NetPacos/
├── data/                   # Sample network logs
│   └── network_log.csv
├── src/
│   ├── app.py              # Streamlit dashboard
│   ├── parser.py           # Network log parser
│   ├── features.py         # Feature engineering
│   └── model.py            # Anomaly detection logic
├── requirements.txt        # Python dependencies
└── README.md
``` 
🧰 Tech Stack

Python 3.12

pandas, numpy

scikit-learn (IsolationForest)

matplotlib

Streamlit for the dashboard and deployment on Streamlit Cloud   
🚀 Deployment

Deployed on Streamlit Cloud. Any push to the main branch triggers an automatic redeploy.