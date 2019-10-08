# 9月（2019）のレース結果


9月のコースはこちらでした。
<img src="https://github.com/shigefumi0914/DeepRacer/blob/master/Image/Course_Sep.png" width=50%>

とりあえず色々試行錯誤しながら、ActionSpaceと報酬関数を作りました。

ActionSpaceは少ない方がいいと記事が書いてたので角度は-30度、0度、30度の3パターンと速度は7m/sと3.5m/sの2パターンで設定することにした。
ActionSpaceが多いと学習量が多くて収束しにくいとか。

<img src="https://github.com/shigefumi0914/DeepRacer/blob/master/Image/ActionSpace_Sep.png" width=50%>


[報酬関数]https://github.com/shigefumi0914/DeepRacer/blob/master/Rewad_Fun_Sep.py
