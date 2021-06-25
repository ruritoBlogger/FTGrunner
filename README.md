# FTGrunner

FightingICE の開発や実行をサポートします.

動作環境は Windows 又は Linux を想定しています(Mac は知らん)

## 前準備

ルートディレクトリに`FTG4.50/`を配置してください.
`FTG4.50/`は, [こちら](http://www.ice.ci.ritsumei.ac.jp/~ftgaic/index-2.html)から取得出来ます.

また, 動作させたい AI の種類によっては依存パッケージが必要になる場合があります. その時は, `FTG4.50/lib` に依存パッケージを入れてください.

## FightingICE の実行

`builder.py`を実行することによって, FightingICE を実行する環境を生成します.
生成先のディレクトリなどは`builder.py`を編集して変えてください.その内リファクタリングします.

## FightingICE を用いた学習の実行

`train.py`を実行することによって, FightingICE を用いた学習を実行します.
学習させたい AI やキャラクター, 試行回数などは`train.py`を編集して変えてください.その内リファクタリングします.
