# 🏎️ Formula 1 Telemetry Dashboard

An interactive dashboard built with **Streamlit**, **FastF1**, and **PySpark** to analyze Formula 1 telemetry data (speed, throttle, braking).  
Enhanced with **driver photos, car images, and team colors** for a professional, portfolio-ready UI.

---

## 🚀 Features
- Select **year, race, session, and driver** to load telemetry
- Visualize **Speed / Throttle / Brake vs Distance**
- Display **driver card** (photo + team + car image)
- Export telemetry to **CSV**
- Run **PySpark aggregation** across multiple laps/drivers
- Enhanced UI with team colors & metrics

---

## 📸 Screenshots


-Telemerty Dashboard
<img width="1915" height="807" alt="image" src="https://github.com/user-attachments/assets/b9eb3bb0-5810-43a9-aa72-b1e21fd37f65" />
<img width="1877" height="818" alt="image" src="https://github.com/user-attachments/assets/3264fbbb-8419-4022-ae6f-1b196e86188c" />
<img width="1831" height="633" alt="image" src="https://github.com/user-attachments/assets/636986cd-9c70-4927-9868-6bdb661c93f2" />
<img width="1846" height="852" alt="image" src="https://github.com/user-attachments/assets/9d9ab64d-20b9-4b89-8f15-5ef163919806" />




---

## ⚡ Setup Instructions

```bash
# Clone repo
git clone https://github.com/YOURUSERNAME/f1-telemetry-dashboard.git
cd f1-telemetry-dashboard

# Create virtual environment
python -m venv venv
source venv/bin/activate   # or .\venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

## Run the app:
streamlit run app.py

📊 PySpark Aggregation

To run aggregation across exported telemetry CSVs:

python spark_analysis.py


Outputs average and max speeds across all laps/drivers.

🛠️ Tech Stack

Python (Streamlit, Pandas, Matplotlib, FastF1)

PySpark (data aggregation)

Streamlit Cloud (optional deployment)
