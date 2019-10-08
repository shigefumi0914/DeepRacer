def reward_function(params):
    # パラメータ取得
    all_wheels_on_track = params['all_wheels_on_track']
    x = params['x']
    y = params['y']
    distance_from_center = params['distance_from_center']
    is_left_of_center = params['is_left_of_center']
    heading = params['heading']
    progress = params['progress']
    steps = params['steps']
    speed = params['speed']
    steering_angle = params['steering_angle']
    track_width = params['track_width']
    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']

    reward = 0

    # 車両がトラックラインの外側に出たらペナルティ
    if not all_wheels_on_track:
        print("off_track")
        return 1e-3

    # 車両がどこにいるかを見ている
    import math
    DIF = 20
    STRAIGHT = 0
    CURVE = 1
    target_waypoint = 0
    track_directions = []
    track_waypoints = [waypoints[closest_waypoints[1]]]
    
    for i in range(1, DIF):
        if closest_waypoints[1] + i >= len(waypoints):
            next_waypoint = waypoints[closest_waypoints[1] + i - len(waypoints)]
            track_waypoints.append(waypoints[closest_waypoints[1] + i - len(waypoints)])
        else:
            next_waypoint = waypoints[closest_waypoints[1] + i]
            track_waypoints.append(waypoints[closest_waypoints[1] + i])
 
        if closest_waypoints[1] + i - 1 >= len(waypoints):
            prev_waypoint = waypoints[closest_waypoints[1] + i - 1 - len(waypoints)]
        else:
            prev_waypoint = waypoints[closest_waypoints[1] + i - 1]
        track_direction = math.atan2(next_waypoint[1] - prev_waypoint[1], next_waypoint[0] - prev_waypoint[0])
        track_directions.append(track_direction)
 
    if track_directions[4] - track_directions[0] < 0.3:
       direction_type = STRAIGHT
       print("direction_type: STRAIGHT")
    else:
       direction_type = CURVE
       print("direction_type: CURVE")

    diff_x = abs(track_waypoints[19][0] - track_waypoints[0][0])
    diff_y = abs(track_waypoints[19][1] - track_waypoints[0][1])
 
    SPEED_THRESHOLD = 4.0
    if diff_x < 0.5 or diff_y < 0.5:
        print("ほぼストレート")
        if speed < SPEED_THRESHOLD:
        # 低速走行の為、報酬は少なめ
         reward = 0.3
        else:
        # 高速走行の為、報酬は多め
         reward = 1.0 
    else:
        print("たぶんカーブ") 
        if speed > SPEED_THRESHOLD:
        # 高速走行の為、報酬は少なめ
         reward = 0.3
        else:
        # 低速走行の為、報酬は多め
         reward = 1.0 
    return reward

    # 車両がトラックの中心に近いほど多くの報酬を返す
    distance_from_center_reward = 0
    marker_1 = 0.1 * track_width
    marker_2 = 0.2 * track_width
    marker_3 = 0.3 * track_width
    if distance_from_center >= 0.0 and distance_from_center <= marker_1:
        distance_from_center_reward = 1
    elif distance_from_center <= marker_2:
        distance_from_center_reward = 0.6
    elif distance_from_center <= marker_3:
        distance_from_center_reward = 0.3
    else:
        return 1e-3

    print("distance_from_center_reward: %.2f" % distance_from_center_reward)
    reward += distance_from_center_reward

    print("total reward: %.2f" % reward)

    # ステアリングを報酬に反映させる
    # 左が正、右が負
    steering_reward = 1e-3
    if distance_from_center > 0:
        if is_left_of_center and steering_angle <= 0:
            steering_reward = 1.0
        elif (not is_left_of_center) and steering_angle >= 0:
            steering_reward = 1.0
    else:
        if steering_angle == 0:
            steering_reward = 1.0
    print("steering_reward: %.2f" % steering_reward)
    reward += steering_reward

    print("total reward: %.2f" % reward)
    return float(reward)