def optimize_signal(traffic_data):
    """
    교통량을 기반으로 신호주기를 추천합니다.
    """

    # 방향별 총 교통량
    total_volume = (
        traffic_data["lrgGoTfvl"]
        + traffic_data["lrgLeftTfvl"]
        + traffic_data["lrgRghtTfvl"]
        + traffic_data["mddlGoTfvl"]
        + traffic_data["mddlLeftTfvl"]
        + traffic_data["mddlRghtTfvl"]
        + traffic_data["smalGoTfvl"]
        + traffic_data["smalLeftTfvl"]
        + traffic_data["smalRghtTfvl"]
    )

    # 교통량에 따른 기본 신호주기
    if total_volume < 100:
        cycle = 60
    elif total_volume < 300:
        cycle = 75
    elif total_volume < 500:
        cycle = 90
    elif total_volume < 800:
        cycle = 105
    else:
        cycle = 120

    # 보행자가 많은 경우 보행시간을 고려해 최소 90초
    pedestrian = traffic_data["walkCnt"]

    if pedestrian >= 100 and cycle < 90:
        cycle = 90

    # 대기행렬이 긴 경우 주기 증가
    queue_length = traffic_data["intlAtmpHeatLngt"]

    if queue_length >= 100 and cycle < 120:
        cycle += 15

    return {
        "recommended_cycle": cycle,
        "traffic_volume": int(total_volume),
        "pedestrian": int(pedestrian),
        "queue_length": int(queue_length)
    }