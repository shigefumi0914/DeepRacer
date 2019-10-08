# 9月（2019）のレース結果


9月のコースはこちらでした。
<img src="https://github.com/shigefumi0914/DeepRacer/blob/master/Image/Course_Sep.png" width=50%>

とりあえず色々試行錯誤しながら、ActionSpaceと報酬関数を作りました。

ActionSpaceは少ない方がいいと記事が書いてたので角度は-30度、0度、30度の3パターンと速度は7m/sと3.5m/sの2パターンで設定することにした。
ActionSpaceが多いと学習量が多くて収束しにくいとか。

<img src="https://github.com/shigefumi0914/DeepRacer/blob/master/Image/ActionSpace_Sep.png" width=50%>


[報酬関数]https://github.com/shigefumi0914/DeepRacer/blob/master/Rewad_Fun_Sep.py

```python
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
```
