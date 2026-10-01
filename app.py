import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import textwrap

from algorithm.signal_optimizer import optimize_signal


# =========================================================
# 페이지 설정
# =========================================================

st.set_page_config(
    page_title="Busan Adaptive Traffic Signal Control",
    page_icon="🚦",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =========================================================
# HTML 출력 함수
# =========================================================

def html(content):
    st.html(textwrap.dedent(content).strip())


# =========================================================
# CSS
# =========================================================

html("""
<style>
def ht
.stApp {
    background: #071018;
    color: #e8f1f5;
}

.block-container {
    max-width: 1800px;
    padding: 1rem 1.2rem 2rem 1.2rem;
}

header[data-testid="stHeader"] {
    background: #071018;
}

.topbar {
    background: linear-gradient(90deg, #0b1720, #101f2a);
    border: 1px solid #263b47;
    border-radius: 8px;
    padding: 13px 20px;
    margin-bottom: 12px;
}

.main-title {
    font-size: 23px;
    font-weight: 700;
    letter-spacing: 1px;
}

.sub-title {
    margin-top: 4px;
    color: #78929e;
    font-size: 11px;
}

.panel {
    background: #0d1821;
    border: 1px solid #263b47;
    border-radius: 8px;
    padding: 15px;
    box-shadow: 0 0 18px rgba(0,0,0,.25);
}

.panel-title {
    font-size: 14px;
    font-weight: 700;
    color: #dce8ed;
    border-bottom: 1px solid #263b47;
    padding-bottom: 9px;
    margin-bottom: 12px;
}

.metric-box {
    background: #101e28;
    border: 1px solid #293f4b;
    border-radius: 7px;
    padding: 13px 8px;
    text-align: center;
    min-height: 82px;
}

.metric-label {
    color: #8299a5;
    font-size: 10px;
    letter-spacing: .5px;
}

.metric-value {
    margin-top: 7px;
    font-size: 23px;
    font-weight: 700;
    color: #e9f0f3;
}

.blue {
    color: #56baff;
}

.green {
    color: #49e69b;
}

.red {
    color: #ff5964;
}

.yellow {
    color: #f3c957;
}

.status {
    display: inline-block;
    background: #103a2a;
    color: #4de49b;
    border: 1px solid #1d6c4c;
    border-radius: 12px;
    padding: 4px 9px;
    font-size: 10px;
}

.info-row {
    font-size: 11px;
    color: #9eb1ba;
    padding: 8px 0;
    border-bottom: 1px solid #20323b;
}

.info-value {
    float: right;
    color: #4de49b;
}

/* 교차로 */

.intersection {
    height: 475px;
    position: relative;
    overflow: hidden;
    border-radius: 7px;
    background:
        radial-gradient(
            circle at 50% 50%,
            #27363d 0%,
            #18252c 38%,
            #101a20 75%
        );
    border: 1px solid #344953;
}

/* 도로 */

.road-h {
    position: absolute;
    left: -5%;
    right: -5%;
    top: 39%;
    height: 135px;
    background: #242d31;
    border-top: 2px solid #536168;
    border-bottom: 2px solid #536168;
}

.road-v {
    position: absolute;
    top: -5%;
    bottom: -5%;
    left: 41%;
    width: 135px;
    background: #242d31;
    border-left: 2px solid #536168;
    border-right: 2px solid #536168;
}

.center-road {
    position: absolute;
    width: 135px;
    height: 135px;
    left: 41%;
    top: 39%;
    background: #30393d;
}

/* 횡단보도 */

.crosswalk {
    position: absolute;
    z-index: 3;
    opacity: .9;
}

.crosswalk-h {
    width: 120px;
    height: 25px;
    background: repeating-linear-gradient(
        90deg,
        white 0px,
        white 8px,
        transparent 8px,
        transparent 15px
    );
}

.crosswalk-v {
    width: 25px;
    height: 120px;
    background: repeating-linear-gradient(
        0deg,
        white 0px,
        white 8px,
        transparent 8px,
        transparent 15px
    );
}

/* 차량 */

.car {
    position: absolute;
    width: 34px;
    height: 17px;
    border-radius: 4px;
    z-index: 5;
    box-shadow: 0 2px 4px rgba(0,0,0,.5);
}

.car-red {
    background: #d95050;
}

.car-blue {
    background: #438fc0;
}

.car-white {
    background: #d7dde0;
}

.car-yellow {
    background: #d99c3b;
}

.car-gray {
    background: #657984;
}

/* 신호 */

.light {
    position: absolute;
    z-index: 8;
    width: 15px;
    height: 15px;
    border-radius: 50%;
    box-shadow: 0 0 12px currentColor;
}

.light-red {
    background: #ff3f4c;
    color: #ff3f4c;
}

.light-green {
    background: #45e397;
    color: #45e397;
}

.light-yellow {
    background: #f3c84b;
    color: #f3c84b;
}

/* 흐름 화살표 */

.arrow-green {
    position: absolute;
    z-index: 7;
    color: #43e496;
    font-size: 32px;
    font-weight: bold;
}

.arrow-red {
    position: absolute;
    z-index: 7;
    color: #ff525e;
    font-size: 32px;
    font-weight: bold;
}

/* 교통량 라벨 */

.traffic-label {
    position: absolute;
    z-index: 10;
    background: rgba(5, 12, 16, .9);
    border: 1px solid #40525b;
    border-radius: 4px;
    padding: 4px 7px;
    color: white;
    font-size: 10px;
}

/* 지도 오버레이 */

.sensor-map {
    height: 270px;
    position: relative;
    background:
        linear-gradient(35deg, transparent 45%, #273d46 46%, #273d46 49%, transparent 50%),
        linear-gradient(-35deg, transparent 45%, #273d46 46%, #273d46 49%, transparent 50%),
        #111c23;
    overflow: hidden;
    border-radius: 6px;
    border: 1px solid #263b47;
}

.sensor-road {
    position: absolute;
    background: #273b44;
}

.sensor-road.h {
    width: 100%;
    height: 30px;
    top: 48%;
}

.sensor-road.v {
    height: 100%;
    width: 30px;
    left: 48%;
}

.sensor-dot {
    position: absolute;
    width: 13px;
    height: 13px;
    border-radius: 50%;
    box-shadow: 0 0 8px currentColor;
}

.dot-red {
    background: #ff4757;
    color: #ff4757;
}

.dot-blue {
    background: #38aef2;
    color: #38aef2;
}

.dot-green {
    background: #42e294;
    color: #42e294;
}

.dot-yellow {
    background: #f1c84b;
    color: #f1c84b;
}

/* 알림 */

.alert {
    padding: 9px 4px;
    border-bottom: 1px solid #23353e;
    font-size: 11px;
    color: #a8bac2;
}

</style>
""")


# =========================================================
# 데이터 불러오기
# =========================================================

try:
    traffic = pd.read_csv(
        "data/traffic.csv",
        encoding="utf-8-sig"
    )
except Exception as e:
    st.error(f"traffic.csv를 불러올 수 없습니다: {e}")
    st.stop()


try:
    intersection = pd.read_csv(
        "data/intersection.csv",
        encoding="utf-8-sig"
    )
except Exception:
    intersection = pd.DataFrame()


# =========================================================
# 데이터 확인
# =========================================================

if "ixrNm" not in traffic.columns:
    st.error("traffic.csv에 ixrNm 컬럼이 없습니다.")
    st.stop()


intersection_names = (
    traffic["ixrNm"]
    .dropna()
    .astype(str)
    .unique()
    .tolist()
)

if len(intersection_names) == 0:
    st.error("교차로 데이터가 없습니다.")
    st.stop()


# =========================================================
# 상단
# =========================================================

html("""
<div class="topbar">
    <div class="main-title">
        🚦 BUSAN ADAPTIVE TRAFFIC SIGNAL CONTROL
    </div>
    <div class="sub-title">
        SMART INTERSECTION · V2I COMMUNICATION · REAL-TIME TRAFFIC ANALYTICS · SIGNAL OPTIMIZATION
    </div>
</div>
""")


# =========================================================
# 교차로 선택
# =========================================================

selected = st.selectbox(
    "분석 교차로",
    intersection_names
)


# =========================================================
# 선택 데이터
# =========================================================

data = traffic[
    traffic["ixrNm"].astype(str) == selected
].copy()


traffic_columns = [
    "lrgGoTfvl",
    "lrgLeftTfvl",
    "lrgRghtTfvl",
    "mddlGoTfvl",
    "mddlLeftTfvl",
    "mddlRghtTfvl",
    "smalGoTfvl",
    "smalLeftTfvl",
    "smalRghtTfvl"
]


for col in traffic_columns:
    if col not in data.columns:
        data[col] = 0

if "walkCnt" not in data.columns:
    data["walkCnt"] = 0

if "intlAtmpHeatLngt" not in data.columns:
    data["intlAtmpHeatLngt"] = 0


for col in traffic_columns + [
    "walkCnt",
    "intlAtmpHeatLngt"
]:
    data[col] = pd.to_numeric(
        data[col],
        errors="coerce"
    ).fillna(0)


# =========================================================
# 교통량
# =========================================================

total_traffic = int(
    data[traffic_columns].sum().sum()
)

pedestrians = int(
    data["walkCnt"].sum()
)

queue_length = int(
    data["intlAtmpHeatLngt"].sum()
)


# =========================================================
# 신호 최적화
# =========================================================

optimization_input = pd.Series({
    col: data[col].sum()
    for col in traffic_columns
})

optimization_input["walkCnt"] = data["walkCnt"].sum()
optimization_input["intlAtmpHeatLngt"] = data["intlAtmpHeatLngt"].sum()


try:

    result = optimize_signal(
        optimization_input
    )

    if isinstance(result, dict):
        recommended_cycle = result.get(
            "recommended_cycle",
            90
        )
    else:
        recommended_cycle = int(result)

except Exception:

    # 최적화 함수에 문제가 있어도
    # 대시보드는 일단 실행되도록 함

    recommended_cycle = 90


recommended_cycle = int(recommended_cycle)


# =========================================================
# 가상 현재 주기
# =========================================================

current_cycle = 90

occupancy = min(
    95,
    max(
        20,
        int(
            40 +
            total_traffic / max(len(data), 1) / 10
        )
    )
)


# =========================================================
# 상단 지표
# =========================================================

c1, c2, c3, c4, c5 = st.columns(5)


with c1:

    html(f"""
    <div class="metric-box">
        <div class="metric-label">
            INTERSECTION
        </div>

        <div class="metric-value blue">
            {selected}
        </div>
    </div>
    """)


with c2:

    html(f"""
    <div class="metric-box">
        <div class="metric-label">
            CYCLE TIME
        </div>

        <div class="metric-value">
            {recommended_cycle}s
        </div>
    </div>
    """)


with c3:

    html(f"""
    <div class="metric-box">
        <div class="metric-label">
            TRAFFIC VOLUME
        </div>

        <div class="metric-value">
            {total_traffic:,}
        </div>
    </div>
    """)


with c4:

    html(f"""
    <div class="metric-box">
        <div class="metric-label">
            QUEUE LENGTH
        </div>

        <div class="metric-value red">
            {queue_length}
        </div>
    </div>
    """)


with c5:

    html(f"""
    <div class="metric-box">
        <div class="metric-label">
            OCCUPANCY
        </div>

        <div class="metric-value green">
            {occupancy}%
        </div>
    </div>
    """)


st.write("")


# =========================================================
# 메인 3열
# =========================================================

left, center, right = st.columns(
    [1.05, 2.15, 1.05]
)


# =========================================================
# LEFT
# =========================================================

with left:

    html(f"""
    <div class="panel">

        <div class="panel-title">
            V2I COMMUNICATION MODULE
        </div>

        <div style="
            text-align:center;
            padding:15px 0;
        ">

            <div style="font-size:38px;">
                🚗
            </div>

            <div style="
                font-size:11px;
                color:#90a7b2;
            ">
                ON-BOARD UNIT
            </div>

        </div>

        <div style="
            text-align:center;
            color:#43e496;
            font-size:22px;
        ">
            ↓
        </div>

        <div style="
            border:1px solid #31505d;
            border-radius:6px;
            padding:14px;
            text-align:center;
            background:#10212a;
        ">

            <div style="
                font-weight:bold;
                font-size:12px;
            ">
                ROAD SIDE UNIT
            </div>

            <div style="
                color:#78929e;
                font-size:10px;
                margin-top:5px;
            ">
                SMART TRAFFIC CONTROLLER
            </div>

        </div>

        <div style="
            text-align:center;
            color:#43e496;
            font-size:22px;
        ">
            ↓
        </div>

        <div style="
            text-align:center;
            margin:8px 0 15px 0;
        ">
            <span class="status">
                ● V2I ACTIVE
            </span>
        </div>

        <div class="info-row">
            Intersection ID
            <span class="info-value">
                BUS-{abs(hash(selected)) % 10000}
            </span>
        </div>

        <div class="info-row">
            Latency
            <span class="info-value">
                12 ms
            </span>
        </div>

        <div class="info-row">
            Data Status
            <span class="info-value">
                ACTIVE
            </span>
        </div>

        <div class="info-row">
            Pedestrians
            <span class="info-value">
                {pedestrians:,}
            </span>
        </div>

    </div>
    """)


# =========================================================
# CENTER DIGITAL TWIN
# =========================================================

with center:

    # 방향별 교통량
    direction_values = []

    for _, row in data.iterrows():

        volume = sum(
            float(row[col])
            for col in traffic_columns
        )

        direction_values.append(
            volume
        )

    while len(direction_values) < 4:
        direction_values.append(0)

    v1 = int(direction_values[0])
    v2 = int(direction_values[1])
    v3 = int(direction_values[2])
    v4 = int(direction_values[3])

    html(f"""
    <div class="panel">

        <div class="panel-title">
            DIGITAL TWIN · {selected}
        </div>

        <div class="intersection">

            <div class="road-h"></div>

            <div class="road-v"></div>

            <div class="center-road"></div>


            <!-- 횡단보도 -->

            <div class="crosswalk crosswalk-h"
                 style="
                 left:calc(41% - 45px);
                 top:34%;
                 ">
            </div>

            <div class="crosswalk crosswalk-h"
                 style="
                 left:calc(41% - 45px);
                 top:68%;
                 ">
            </div>

            <div class="crosswalk crosswalk-v"
                 style="
                 left:34%;
                 top:calc(39% + 8px);
                 ">
            </div>

            <div class="crosswalk crosswalk-v"
                 style="
                 left:59%;
                 top:calc(39% + 8px);
                 ">
            </div>


            <!-- 신호 -->

            <div class="light light-red"
                 style="
                 left:37%;
                 top:36%;
                 ">
            </div>

            <div class="light light-green"
                 style="
                 left:59%;
                 top:49%;
                 ">
            </div>

            <div class="light light-red"
                 style="
                 left:45%;
                 top:70%;
                 ">
            </div>

            <div class="light light-green"
                 style="
                 left:52%;
                 top:28%;
                 ">
            </div>


            <!-- 차량 -->

            <div class="car car-red"
                 style="
                 left:12%;
                 top:47%;
                 ">
            </div>

            <div class="car car-blue"
                 style="
                 left:22%;
                 top:55%;
                 ">
            </div>

            <div class="car car-white"
                 style="
                 left:59%;
                 top:47%;
                 ">
            </div>

            <div class="car car-yellow"
                 style="
                 left:74%;
                 top:55%;
                 ">
            </div>

            <div class="car car-gray"
                 style="
                 left:45%;
                 top:10%;
                 transform:rotate(90deg);
                 ">
            </div>

            <div class="car car-red"
                 style="
                 left:50%;
                 top:18%;
                 transform:rotate(90deg);
                 ">
            </div>

            <div class="car car-blue"
                 style="
                 left:42%;
                 top:79%;
                 transform:rotate(90deg);
                 ">
            </div>


            <!-- 흐름 -->

            <div class="arrow-green"
                 style="
                 left:50%;
                 top:51%;
                 ">
                ↑
            </div>

            <div class="arrow-green"
                 style="
                 left:54%;
                 top:53%;
                 ">
                →
            </div>

            <div class="arrow-red"
                 style="
                 left:36%;
                 top:51%;
                 ">
                ←
            </div>


            <!-- 교통량 -->

            <div class="traffic-label"
                 style="
                 left:7%;
                 top:38%;
                 ">
                {v1:,} veh/min
            </div>

            <div class="traffic-label"
                 style="
                 right:7%;
                 top:38%;
                 ">
                {v2:,} veh/min
            </div>

            <div class="traffic-label"
                 style="
                 left:44%;
                 top:5%;
                 ">
                {v3:,} veh/min
            </div>

            <div class="traffic-label"
                 style="
                 left:44%;
                 bottom:5%;
                 ">
                {v4:,} veh/min
            </div>


            <!-- 하단 상태 -->

            <div style="
                position:absolute;
                left:12px;
                bottom:10px;
                z-index:20;
                background:rgba(5,12,16,.9);
                border:1px solid #304650;
                border-radius:5px;
                padding:7px 10px;
                font-size:10px;
            ">

                Digital Twin<br>

                <span style="color:#43e496;">
                    ● V2I STATUS: ACTIVE
                </span>

            </div>


            <div style="
                position:absolute;
                right:12px;
                bottom:10px;
                z-index:20;
                background:rgba(5,12,16,.9);
                border:1px solid #304650;
                border-radius:5px;
                padding:7px 10px;
                font-size:10px;
            ">

                OCCUPANCY:
                <span style="color:#43e496;">
                    {occupancy}%
                </span>

            </div>

        </div>

    </div>
    """)


# =========================================================
# RIGHT
# =========================================================

with right:

    html(f"""
    <div class="panel">

        <div class="panel-title">
            ADAPTIVE TRAFFIC SIGNAL CONTROL
        </div>

        <div class="metric-box">
            <div class="metric-label">
                CURRENT CYCLE
            </div>

            <div class="metric-value">
                {current_cycle}s
            </div>
        </div>

        <br>

        <div class="metric-box">
            <div class="metric-label">
                OPTIMIZED CYCLE
            </div>

            <div class="metric-value green">
                {recommended_cycle}s
            </div>
        </div>

        <br>

        <div class="metric-box">
            <div class="metric-label">
                CURRENT PHASE
            </div>

            <div class="metric-value">
                3 → 1
            </div>
        </div>

        <br>

        <div class="metric-box">
            <div class="metric-label">
                NEXT PHASE
            </div>

            <div class="metric-value yellow">
                87s
            </div>
        </div>

        <br>

        <div style="
            font-size:10px;
            color:#8299a5;
        ">
            SIGNAL STATUS
        </div>

        <div style="
            margin-top:7px;
            color:#49e69b;
            font-size:12px;
        ">
            ● ADAPTIVE CONTROL ACTIVE
        </div>

    </div>
    """)


# =========================================================
# 아래 영역
# =========================================================

st.write("")

bottom1, bottom2, bottom3 = st.columns(
    [1.05, 1.4, 1]
)


# =========================================================
# SENSOR MAP
# =========================================================

with bottom1:

    html("""
    <div class="panel">

        <div class="panel-title">
            IoT SENSOR NETWORK MAP
        </div>

        <div class="sensor-map">

            <div class="sensor-road h"></div>
            <div class="sensor-road v"></div>

            <div class="sensor-dot dot-red"
                 style="left:18%;top:30%;">
            </div>

            <div class="sensor-dot dot-blue"
                 style="left:30%;top:65%;">
            </div>

            <div class="sensor-dot dot-green"
                 style="left:72%;top:30%;">
            </div>

            <div class="sensor-dot dot-yellow"
                 style="left:72%;top:65%;">
            </div>

            <div class="sensor-dot dot-green"
                 style="left:48%;top:20%;">
            </div>

            <div class="sensor-dot dot-red"
                 style="left:48%;top:75%;">
            </div>

            <div class="sensor-dot dot-blue"
                 style="left:25%;top:48%;">
            </div>

            <div class="sensor-dot dot-yellow"
                 style="left:78%;top:48%;">
            </div>

        </div>

        <div style="
            font-size:10px;
            color:#9db0b9;
            margin-top:10px;
        ">
            🔴 Traffic Camera
            &nbsp;&nbsp;
            🔵 LiDAR
            &nbsp;&nbsp;
            🟢 Loop Detector
            &nbsp;&nbsp;
            🟡 RSU
        </div>

    </div>
    """)


# =========================================================
# TRAFFIC ANALYTICS
# =========================================================

with bottom2:

    direction_names = []
    direction_volumes = []

    for _, row in data.iterrows():

        direction_names.append(
            str(row["istlLctn"])
        )

        volume = sum(
            float(row[col])
            for col in traffic_columns
        )

        direction_volumes.append(
            volume
        )

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=direction_names,
            y=direction_volumes,
            marker_color="#35b9e8",
            text=[
                int(x)
                for x in direction_volumes
            ],
            textposition="auto"
        )
    )

    fig.update_layout(
        title="Real-time Traffic Volume",
        height=320,
        margin=dict(
            l=40,
            r=20,
            t=50,
            b=60
        ),
        paper_bgcolor="#0d1821",
        plot_bgcolor="#0d1821",
        font=dict(
            color="#b9cbd2"
        ),
        xaxis=dict(
            gridcolor="#20343d"
        ),
        yaxis=dict(
            gridcolor="#20343d",
            title="veh/hr"
        )
    )

    html("""
    <div class="panel">
        <div class="panel-title">
            TRAFFIC DATA ANALYTICS
        </div>
    </div>
    """)

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "displayModeBar": False
        }
    )


# =========================================================
# PERFORMANCE INDEX
# =========================================================

with bottom3:

    performance = int(
        max(
            35,
            min(
                98,
                100
                - min(queue_length, 100) * 0.3
                - min(total_traffic / 100, 30)
            )
        )
    )

    html(f"""
    <div class="panel">

        <div class="panel-title">
            INTERSECTION PERFORMANCE INDEX
        </div>

        <div style="
            text-align:center;
            padding:25px 0;
        ">

            <div style="
                width:145px;
                height:145px;
                border-radius:50%;
                border:13px solid #263b45;
                border-top-color:#43e496;
                border-right-color:#43e496;
                margin:auto;
                display:flex;
                align-items:center;
                justify-content:center;
            ">

                <div>

                    <div style="
                        color:#43e496;
                        font-size:35px;
                        font-weight:bold;
                    ">
                        {performance}
                    </div>

                    <div style="
                        color:#8299a5;
                        font-size:11px;
                    ">
                        /100
                    </div>

                </div>

            </div>

        </div>

        <div class="alert">
            🟢 Signal optimization active
        </div>

        <div class="alert">
            🟡 Traffic monitoring active
        </div>

        <div class="alert">
            🔵 V2I communication active
        </div>

    </div>
    """)


# =========================================================
# 하단 시스템 상태
# =========================================================

st.write("")

html(f"""
<div class="panel">

    <div class="panel-title">
        SYSTEM STATUS / ANOMALY DETECTION
    </div>

    <div class="alert">
        🟢 Traffic:
        <b>{total_traffic:,}</b>
        vehicles detected
    </div>

    <div class="alert">
        🟡 Pedestrian:
        <b>{pedestrians:,}</b>
        detected
    </div>

    <div class="alert">
        🟢 Recommended Signal Cycle:
        <b>{recommended_cycle}s</b>
    </div>

    <div class="alert">
        🔵 Data Source:
        <b>Busan Smart Intersection API</b>
    </div>

</div>
""")


# =========================================================
# 자동 새로고침 안내
# =========================================================

st.caption(
    "Busan Smart Intersection · Adaptive Signal Optimization Dashboard"
)