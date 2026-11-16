# EaseTrack — Compassionate Substance Reduction App (Mock UI)

A Streamlit mock UI for a blood alcohol/drug measurement tracking application designed around gradual harm reduction, positive reinforcement, and non-punitive recovery pacing.

## Features

- **Blood Content Tracking Graph**: Plots measured blood concentration over time alongside a personalized **Gentle Taper Target Curve**, **5-Day Smoothed Trend**, and **Safe Level Zone**.
- **Mock Blood Sensor Emulator**: Sidebar panel to simulate incoming Bluetooth blood readings (`On-Track Taper Reading`, `Below Safe Threshold`, `Temporary Step Back`, or custom slider values) for live showcase demos.
- **Non-Punitive Psychology & Pacing**: No "streak resets" or penalties when a user records a higher reading or relapses. Milestones and credits are cumulative and never revoked, and supportive feedback encourages continuing at the user's own pace.
- **Milestones, Goals & Rewards**: Visual progress trackers and permanently unlocked self-care milestones.

## Running Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```
