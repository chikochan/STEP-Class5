# Google STEP Class 5 Homework

## 方針

貪欲法で経路を一つ見つけた後に、2-opt法のような局所探索法を用いて経路長を改善する。


## 局所探索法

以下の二つの方法を用いた。

###   2-opt法 (two_opt関数)
二つの辺、A→B、C→Dが交わっている時、A→C、B→Dとつなぎ変える。

交わっている場合は三角不等式より、AB間、CD間の距離の和がAC間、BD間の距離の和よりも大きくなることを用いる。

<img src="https://user-images.githubusercontent.com/49418561/121517202-0bc79b00-ca2a-11eb-9cb1-939e4497404e.jpg" width="400">



A,Bを決めた後、Cは経路の中でA,Bより後方の位置にある頂点とする。Cが経路の最後の頂点の場合はdは経路の最初の頂点となることに注意すると、全ての頂点数をNとしてDのインデックスは
```
d_index=(c_index+1)%N
```
となる。

このつなぎ変えは、BからCまでの経路を逆順にすれば行うことができる。

辺のつなぎ変えによって新たに交点が生じる場合があるため、つなぎ変えの必要な辺の組み合わせがなくなるまで操作を繰り返す。

### 部分列の移動(move_subsequence関数)

部分列の長さを固定して、移動させたい部分列をE1→E2→…→Enとする。
A→E1→E2→…→En→BとC→Dの二つの経路を取り出し、
A→E1→E2→…→En→BとC→Dの経路の距離の和がA→BとC→En→…→E2→E1→Dの距離の和よりも大きい時にはA→BとC→En→…→E2→E1→Dへとつなぎ変える。

<img src="https://user-images.githubusercontent.com/49418561/121442907-7dbac880-c9c7-11eb-8766-48b336a8fa94.jpg" width="800">


（※A→BとC→E1→E2→…→En→Dへのつなぎ変えも考えられるが、交点が存在しない状況では上図のようにA,Bの近くではA→BとC→Dの向きが逆だと考えられるのでここでは行わない。）


A,Bを決めたのち、C,DはEに含まれない任意の辺とする。

場合分けなしでこのつなぎ変えを行うために、

1. 経路中のE1からEnまでを-1で置き換える。
（この時点ではインデックスに変化なし）
2. C→Dの間にEn→…→E2→E1を挿入する。具体的には、Dが元々あった位置にE1、E2、…、Enの順に挿入する。
（インデックスが変化する）
3. -1になっている部分を削除する

の順に計算を行う。

つなぎ変えの必要な辺の組み合わせがなくなるまで操作を繰り返す。

## 貪欲法の変更(greedy関数)

局所探索法による局所的な変更だけでなく、大域的な経路の変更を行うためには、最初に見つける経路を変更すれば良いと考えられる。

そこで、貪欲法で最も近い頂点を求める際、上下方向に座標を拡大してから頂点間の距離を求めることにする。


expansion_rateを上下方向への拡大率とすると、距離の二乗は
```
(city1[0] - city2[0]) ** 2 + ((city1[1] - city2[1])*expansion_rate) ** 2
```
と計算できる。

expansion_rate>1の時は左右方向に移動しやすくなり、expansion_rate<1の時は上下方向に移動しやすくなる。


## 実行方法

テスト環境: Python 3.9.2

n=0,1,2,3,4,5,6として、以下のように実行してください。

```
python3 homework.py input_n.csv (outputのファイル名)
```

N=2048の時は実行に10分程度かかります。


## 結果

2-opt法と部分列の移動の順序や、expansion_rateの値をいろいろと試したところ、（思いつきで試しただけなので、全ては確認できていません。）

input_0.csv,input_1.csv,input_2.csvに関しては、

```
expansion_rate = 1.0
tour = greedy(cities, expansion_rate)
tour = two_opt(tour, dist)
tour = move_subsequence(tour, dist, 1)
```
の順に行うと、それぞれ3291.62,3778.72,4494.42という結果を得られた。

input_3.csvに関しては、
```
expansion_rate = 1.5
tour = greedy(cities, expansion_rate)
tour = move_subsequence(tour, dist, 5)
for _ in range(2):
    tour = two_opt(tour, dist)
    tour = move_subsequence(tour, dist, 4)
    tour = move_subsequence(tour, dist, 3)
    tour = move_subsequence(tour, dist, 2)
    tour = move_subsequence(tour, dist, 1)
```
とすると8118.40という結果が得られた。

input_4.csvに関しては、
```
expansion_rate = 1.15
tour = greedy(cities, expansion_rate)
tour = move_subsequence(tour, dist, 4)
tour = two_opt(tour, dist)
tour = move_subsequence(tour, dist, 3)
tour = move_subsequence(tour, dist, 2)
tour = move_subsequence(tour, dist, 1)
```

とすると、10577.07という結果が得られた。

input_5.csvに関しては、
```
expansion_rate = 1.37
tour = greedy(cities, expansion_rate)
for _ in range(2):
    tour = two_opt(tour, dist)
    tour = move_subsequence(tour, dist, 5)
    tour = move_subsequence(tour, dist, 4)
    tour = move_subsequence(tour, dist, 3)
    tour = move_subsequence(tour, dist, 2)
    tour = move_subsequence(tour, dist, 1)
```
とすると20547.67という結果が得られた。

input_6.csvに関しては、
```
expansion_rate = 1.15
tour = greedy(cities, expansion_rate)
for _ in range(4):
    tour = two_opt(tour, dist)
    tour = move_subsequence(tour, dist, 7)
    tour = move_subsequence(tour, dist, 6)
    tour = move_subsequence(tour, dist, 5)
    tour = move_subsequence(tour, dist, 4)
    tour = move_subsequence(tour, dist, 3)
    tour = move_subsequence(tour, dist, 2)
    tour = move_subsequence(tour, dist, 1)
```
とすると40789.95という結果が得られた。










