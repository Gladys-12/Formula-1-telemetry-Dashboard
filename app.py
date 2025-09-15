# app.py
import streamlit as st
import fastf1
import pandas as pd
import matplotlib.pyplot as plt
import io
import os
cache_dir = 'f1_cache'

# Create the cache directory if it doesn't exist
if not os.path.exists(cache_dir):
    os.makedirs(cache_dir)

fastf1.Cache.enable_cache(cache_dir)
# Enable fastf1 cache in a local folder called "f1_cache"
fastf1.Cache.enable_cache('f1_cache')

st.set_page_config(page_title="F1 Telemetry Dashboard", layout="wide")
background_image_url = "https://mediacms01.apac.beiniz.biz/league_logo/SOUYL_LEAGUE_HEADER_INDONESIA_1920X1080.jpg"  # example F1 image

st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("{background_image_url}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown(
    "<h1 style='text-align: center;'>🏎️ Formula 1 Telemetry Dashboard</h1>", 
    unsafe_allow_html=True
)
col1, col2, col3 = st.columns([1, 2, 1])  

with col2:  # middle column
    st.header("🔧 Data Selection")
    year = st.selectbox("Year", list(range(2018, 2025)), index=5)
    event_input = st.text_input("Race name or round number (e.g. 'Italian Grand Prix' or '13')", "Italian Grand Prix")
    session_type = st.selectbox("Session", ["FP1", "FP2", "FP3", "Q", "R"], index=3)
    driver = st.text_input("Driver code (3 letters, e.g. VER, HAM)", "VER")

    load_btn = st.button("🚀 Load session & driver")


# Helper to convert lap timedeltas to seconds safely
def td_to_seconds(td):
    try:
        return td.total_seconds()
    except:
        return None

if load_btn:
    try:
        with st.spinner("Loading session metadata... (cached after first run)"):
            # fastf1 accepts round number as int, else race name string
            event_param = int(event_input) if event_input.isdigit() else event_input
            session = fastf1.get_session(year, event_param, session_type)
            session.load()  # loads laps metadata; telemetry loads when requested per lap
    except Exception as e:
        st.error(f"Failed to load session: {e}")
        st.stop()

    # pick driver laps
    laps = session.laps.pick_driver(driver.upper())
    if laps.empty:
        st.warning(f"No laps found for driver '{driver.upper()}' in this session.")
        st.stop()
    

    # Show basic lap table & summary
    st.subheader(f"{session.event['EventName']} — {session.name} — {driver.upper()}")
    # Show laps table (light)
    display_cols = ["LapNumber", "LapTime", "PitOutTime", "PitInTime", "Sector1Time", "Sector2Time", "Sector3Time"]
    st.dataframe(laps[display_cols].reset_index(drop=True))

    # Summary metrics
    best_lap = laps['LapTime'].min()
    avg_lap = laps['LapTime'].dropna().mean()
    st.metric("Best lap (hh:mm:ss.ms)", str(best_lap))
    st.metric("Average lap (hh:mm:ss.ms)", str(avg_lap))

    # Choose lap to visualize
    lap_nums = list(laps['LapNumber'].astype(int).unique())
    chosen_lapnum = st.selectbox("Choose Lap to view telemetry", lap_nums)

    selected_lap = laps[laps['LapNumber'] == chosen_lapnum].iloc[0]

    # Load car telemetry for just this lap (fastf1 caching makes repeated views fast)
    with st.spinner("Loading telemetry for chosen lap..."):
        try:
            car_data = selected_lap.get_car_data().add_distance()  # distance column added
        except Exception as e:
            st.error(f"Failed to load telemetry: {e}")
            st.stop()

    # Basic plots: Speed, Throttle, Brake vs Distance
    st.subheader(f"Telemetry for Lap {chosen_lapnum}")

    fig, ax = plt.subplots(3, 1, figsize=(10, 8), sharex=True)
    ax[0].plot(car_data['Distance'], car_data['Speed'], color='tab:blue')
    ax[0].set_ylabel('Speed (km/h)')
    ax[0].grid(True)

    if 'Throttle' in car_data.columns:
        ax[1].plot(car_data['Distance'], car_data['Throttle'], color='tab:orange')
        ax[1].set_ylabel('Throttle')
        ax[1].grid(True)
    else:
        ax[1].text(0.5, 0.5, 'Throttle not available', ha='center')

    if 'Brake' in car_data.columns:
        ax[2].plot(car_data['Distance'], car_data['Brake'], color='tab:red')
        ax[2].set_ylabel('Brake')
        ax[2].set_xlabel('Distance (m)')
        ax[2].grid(True)
    else:
        ax[2].text(0.5, 0.5, 'Brake not available', ha='center')

    st.pyplot(fig)

    # Small analytics: max speed, average speed
    max_speed = car_data['Speed'].max()
    avg_speed = car_data['Speed'].mean()
    st.write(f"**Max speed:** {max_speed:.1f} km/h   |   **Avg speed:** {avg_speed:.1f} km/h")

    # Download telemetry as CSV
    csv_buf = io.StringIO()
    car_data.to_csv(csv_buf, index=False)
    csv_bytes = csv_buf.getvalue().encode()
    st.download_button("Download telemetry CSV for this lap", data=csv_bytes, file_name=f"telemetry_{driver.upper()}_lap{chosen_lapnum}.csv", mime="text/csv")

    # Optional: show raw telemetry head
    if st.checkbox("Show raw telemetry table (first 50 rows)"):
        st.dataframe(car_data.head(50))

    st.success("Loaded telemetry successfully. Use the controls to explore other races/drivers.")
