# 9月（2019）のレース結果

まずはレースに出てみたかったのでとりあえずモデルを作ってレースに出ることにしました。

9月のレースコースはこちらでした。

<img src="https://github.com/shigefumi0914/DeepRacer/blob/master/Image/Course_Sep.png" width=50%>

なので練習用コースのCumulo Carrera Trainingで走らせることにしました。
とりあえず色々試行錯誤しながら、ActionSpaceと報酬関数を作りました。

ActionSpaceは少ない方がいいという記事があったので角度は-30度、0度、30度の3パターンと速度は7m/sと3.5m/sの2パターンで設定することにしました。
ActionSpaceが多いと学習量が多くて収束しにくいとか。

<img src="https://github.com/shigefumi0914/DeepRacer/blob/master/Image/ActionSpace_Sep.png" width=50%>

## 報酬関数①の考え方

waypointsを利用してコースが直線かカーブかを正確に判定して、直線の時はスピードが高い方に多くの報酬を、カーブの時はスピードが低い方に報酬を与えることにしました。

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

## 報酬関数②の考え方

コースの真ん中を走ると報酬が高いように設定しました。

```python
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

    reward += distance_from_center_reward
```

## 報酬関数③の考え方

ステアリングに報酬を与えました。

```python
    steering_reward = 1e-3
    if distance_from_center > 0:
        if is_left_of_center and steering_angle <= 0:
            steering_reward = 1.0
        elif (not is_left_of_center) and steering_angle >= 0:
            steering_reward = 1.0
    else:
        if steering_angle == 0:
            steering_reward = 1.0
            
    reward += steering_reward
```
これらを取り入れてこのように報酬関数を作成した。

[報酬関数]https://github.com/shigefumi0914/DeepRacer/blob/master/Rewad_Fun_Sep.py

ハイパーパラメータはよくわからなかったのでデフォルトのままです。

この設定でCumulo Carrera Trainingコースを2時間学習させました。

その時のグラフがこちら

<img src="https://github.com/shigefumi0914/DeepRacer/blob/master/Image/Learning_1.png" width=50%>

グラフから学習が進むにつれて報酬が上がっていることがわかります。正しく学習出来ていると思います。

またエピソードからも何回か100になっていて完走出来ています。

なのでもうすこし同様のコースで学習させようと思いました。

次にまた同じコースを2時間追加で学習させました。

その時のグラフがこちら

<img src="https://github.com/shigefumi0914/DeepRacer/blob/master/Image/Learning_2.png" width=50%>

しかしながら先ほどとは違い、あまり報酬は上がりませんでした。

エピソードは先ほどより多く完走出来ていることがわかります。たぶんこれ以上学習させても賢くならなさそうでした。

ということで本番コースを走らせたらこのような結果になりました。

1338人中なんと314位という結果に。トータルコストも4時間学習させただけなので500円くらいです。ただそれまでに試行錯誤していたので6000円ほどかかってます。 

やはり15秒というのが一つの壁のようです。

次回10月のレースもやってみようと思います。



