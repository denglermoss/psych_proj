from datetime import datetime, timedelta
import altair as alt
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="EaseTrack",
    layout="centered",
)

st.markdown(
    """
    <style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 780px;
    }
    .message-card {
        background-color: #eef7f4;
        border-left: 4px solid #2e7d67;
        border-radius: 8px;
        padding: 1rem 1.2rem;
        margin-bottom: 1.5rem;
        color: #1c3b32;
    }
    .message-card-gentle {
        background-color: #f3f6fb;
        border-left: 4px solid #4a74a8;
        border-radius: 8px;
        padding: 1rem 1.2rem;
        margin-bottom: 1.5rem;
        color: #1f334d;
    }
    .reward-card {
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 0.9rem 1rem;
        background: #ffffff;
        height: 100%;
    }
    .reward-status {
        font-size: 0.78rem;
        font-weight: 600;
        color: #2e7d67;
        margin-bottom: 0.25rem;
    }
    .reward-status-locked {
        font-size: 0.78rem;
        font-weight: 600;
        color: #64748b;
        margin-bottom: 0.25rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def default_readings() -> pd.DataFrame:
    base_date = datetime(2026, 11, 3)
    measured = [0.10, 0.095, 0.09, 0.085, 0.095, 0.08, 0.075, 0.07, 0.085, 0.065, 0.06, 0.055, 0.05, 0.045]
    goal = [round(0.10 - i * 0.004, 3) for i in range(len(measured))]
    dates = [base_date + timedelta(days=i) for i in range(len(measured))]
    return pd.DataFrame(
        {
            "Date": dates,
            "Blood Level": measured,
            "Gentle Goal": goal,
        }
    )


if "readings" not in st.session_state:
    st.session_state.readings = default_readings()

if "points" not in st.session_state:
    st.session_state.points = 150

with st.sidebar:
    st.subheader("Mock Blood Sensor")
    st.caption("Send a simulated device reading to the app.")

    substance = st.selectbox("Substance", ["Alcohol (% BAC)", "Drug Level (ng/mL)"])
    new_val = st.slider("Simulated Reading", min_value=0.00, max_value=0.14, value=0.04, step=0.005)

    if st.button("Send Reading to App", type="primary", use_container_width=True):
        df = st.session_state.readings
        next_date = df["Date"].iloc[-1] + timedelta(days=1)
        next_goal = max(0.02, round(float(df["Gentle Goal"].iloc[-1]) - 0.003, 3))
        new_row = pd.DataFrame(
            {
                "Date": [next_date],
                "Blood Level": [new_val],
                "Gentle Goal": [next_goal],
            }
        )
        st.session_state.readings = pd.concat([df, new_row], ignore_index=True)
        st.session_state.points += 20
        st.rerun()

    if st.button("Reset Demo Data", use_container_width=True):
        st.session_state.readings = default_readings()
        st.session_state.points = 150
        st.rerun()

df = st.session_state.readings
latest_level = float(df["Blood Level"].iloc[-1])
latest_goal = float(df["Gentle Goal"].iloc[-1])

st.title("EaseTrack")
st.caption("Gentle, judgment-free reduction at your own pace.")

if latest_level > latest_goal + 0.01:
    st.markdown(
        """
        <div class="message-card-gentle">
            <strong>Thanks for checking in today.</strong><br>
            Today's reading was a step higher than your goal line, and that is okay. Recovery is a gradual process —
            none of your rewards or milestones are ever lost. We will simply pick back up tomorrow at your own pace.
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        """
        <div class="message-card">
            <strong>You are making steady progress.</strong><br>
            Your blood measurements are trending down smoothly. Keep easing off gently at a pace that feels safe and comfortable for you.
        </div>
        """,
        unsafe_allow_html=True,
    )

st.subheader("Your Blood Levels Over Time")

plot_df = df.melt(
    id_vars=["Date"],
    value_vars=["Blood Level", "Gentle Goal"],
    var_name="Series",
    value_name="Value",
)

chart = (
    alt.Chart(plot_df)
    .mark_line(point=True, strokeWidth=3)
    .encode(
        x=alt.X("Date:T", title=None, axis=alt.Axis(format="%b %d")),
        y=alt.Y("Value:Q", title=substance, scale=alt.Scale(domain=[0, 0.14])),
        color=alt.Color(
            "Series:N",
            title=None,
            scale=alt.Scale(
                domain=["Blood Level", "Gentle Goal"],
                range=["#1f6f5b", "#94a3b8"],
            ),
            legend=alt.Legend(orient="top"),
        ),
        strokeDash=alt.StrokeDash(
            "Series:N",
            scale=alt.Scale(
                domain=["Blood Level", "Gentle Goal"],
                range=[[1, 0], [5, 4]],
            ),
            legend=None,
        ),
        tooltip=[
            alt.Tooltip("Date:T", title="Date", format="%b %d"),
            alt.Tooltip("Series:N", title="Measurement"),
            alt.Tooltip("Value:Q", title="Level", format=".3f"),
        ],
    )
    .properties(height=300)
)

st.altair_chart(chart, use_container_width=True)

st.subheader("Goals & Rewards")
st.write(f"Reward Points: **{st.session_state.points} pts** *(points never reset)*")

start_val = float(df["Blood Level"].iloc[0])
progress = min(1.0, max(0.0, (start_val - latest_level) / (start_val - 0.03)))
st.progress(progress, text="Goal: Gradually ease down to your safe target level (0.030)")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """
        <div class="reward-card">
            <div class="reward-status">UNLOCKED</div>
            <strong>First Week Logged</strong>
            <p style="font-size: 0.85rem; color: #475569; margin-top: 0.3rem;">
                7 check-ins completed.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        """
        <div class="reward-card">
            <div class="reward-status">UNLOCKED</div>
            <strong>Gentle Step Down</strong>
            <p style="font-size: 0.85rem; color: #475569; margin-top: 0.3rem;">
                Reduced baseline level by 30%.<br><em>Reward: $5 Coffee Card</em>
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col3:
    safe_unlocked = latest_level <= 0.035
    status_class = "reward-status" if safe_unlocked else "reward-status-locked"
    status_label = "UNLOCKED" if safe_unlocked else "IN PROGRESS"
    st.markdown(
        f"""
        <div class="reward-card">
            <div class="{status_class}">{status_label}</div>
            <strong>Safe Zone Milestone</strong>
            <p style="font-size: 0.85rem; color: #475569; margin-top: 0.3rem;">
                Reach 0.035 or below.<br><em>Reward: $15 Wellness Gift</em>
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
