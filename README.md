# space-invaders

Python（Pygame）によるシンプルなスペースインベーダーゲームです。

## 必要環境
- Python 3.12.x
- pip
- SDL2（Homebrewで自動インストール済み）

## セットアップ手順
1. Python 3.12.x をインストール（pyenv推奨）
2. 必要なライブラリをインストール

```sh
pip install -r requirements.txt
```

## ゲームの実行方法

```sh
python main.py
```

## テストの実行方法

```sh
pytest test_game.py
```

## 操作方法
- ←キー／→キー：プレイヤー（自機）の左右移動
- スペースキー：弾を発射
- ウィンドウ右上の×ボタン：ゲーム終了

## ディレクトリ構成

```
space-invaders/
├── main.py           # ゲーム本体
├── test_game.py      # ゲームロジックのテスト
├── requirements.txt  # 依存パッケージ
├── .gitignore        # git管理除外ファイル
└── README.md         # このファイル
```

## 注意事項
- Python 3.13 ではPygameが動作しません。必ず3.12系を使用してください。
- macOSの場合、初回セットアップ時にHomebrewでSDL2関連ライブラリのインストールが必要です。
