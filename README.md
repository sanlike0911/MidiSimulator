# MIDI Simulator - Python版

ゲームパッドの入力を14ビットMIDI CCメッセージに変換するPythonアプリケーションです。

## 仕様

### 14ビットCC対応軸

**左スティック:**

- X軸: CC#16 (MSB) / CC#48 (LSB)
- Y軸: CC#17 (MSB) / CC#49 (LSB)

**右スティック:**

- X軸: CC#18 (MSB) / CC#50 (LSB)
- Y軸: CC#19 (MSB) / CC#51 (LSB)

### 値域と分解能

- **分解能**: 各軸16,384段階（2^14）
- **値域**: 0-16383
- **中央位置**: 8192（ニュートラル）
- **移動範囲**:
  - 上/右方向: 8193-16383（8,191段階）
  - 下/左方向: 0-8191（8,192段階）

### MIDI送信順序

各軸について以下の順序でメッセージを送信：

1. LSB送信（下位7ビット）
2. MSB送信（上位7ビット）

## インストールと実行

### 方法1: 仮想環境を使用（推奨）

1. **仮想環境の作成**

```bash
python -m venv .venv
```

2. **仮想環境のアクティベート**

Windows:

```bash
.venv\Scripts\activate
```

macOS/Linux:

```bash
source .venv/bin/activate
```

3. **依存関係のインストール**

```bash
pip install -r requirements.txt
```

4. **アプリケーションの実行**

```bash
python midi_simulator.py
```

5. **仮想環境の終了**

```bash
deactivate
```

### 方法2: 自動セットアップ

```bash
python setup.py
```

### 方法3: システム環境に直接インストール

1. **依存関係のインストール**

```bash
pip install -r requirements.txt
```

2. **アプリケーションの実行**

```bash
python midi_simulator.py
```

## 必要な環境

- Python 3.7以降
- ゲームパッド（Xbox Controller、PlayStation Controller等）
- MIDIデバイスまたはMIDI対応ソフトウェア

## 依存パッケージ

- `pygame` - ゲームパッド入力処理
- `python-rtmidi` - MIDI出力

## 使用方法

1. **ゲームパッドの接続**
   - ゲームパッドをPCに接続
   - Windowsで認識されていることを確認

2. **アプリケーションの起動**
   - コマンドプロンプトまたはターミナルで実行
   - 起動時にデバイス選択メニューが表示される

3. **MIDIポートの選択**
   - 利用可能なMIDIポートが一覧表示される
   - 番号を入力してポートを選択
   - 仮想MIDIポートの作成も可能

4. **ゲームパッドの選択**
   - 複数のゲームパッドが接続されている場合は選択メニューが表示される
   - 1つのみの場合は自動的に選択される

5. **MIDI送信**
   - スティックを動かすとリアルタイムでMIDI CCが送信される
   - コンソールに送信状況が表示される

6. **終了**
   - `Ctrl+C` で終了

## 設定項目

コード内で調整可能な設定：

- `DEADZONE`: デッドゾーンの範囲（デフォルト: 0.1）
- CC番号の変更（コード内の定数を変更）
- 更新レート（デフォルト: 100Hz）

## WindowsでのMIDIデバイス認識設定

### 仮想MIDIポートの作成

MIDIシミュレーターをWindowsのMIDIデバイスとして認識させるには、仮想MIDIポートが必要です。

#### 方法1: loopMIDI（推奨）

1. **loopMIDIのダウンロード**
   - [Tobias Erichsen's loopMIDI](https://www.tobias-erichsen.de/software/loopmidi.html)からダウンロード
   - インストール実行

2. **仮想ポートの作成**
   - loopMIDIを起動
   - 下部の「New port-name」に「MIDI Simulator」と入力
   - 「+」ボタンをクリックして仮想ポートを作成

3. **アプリケーションでの使用**
   - MIDIシミュレーターが自動的に「MIDI Simulator」ポートを検出
   - DAWやMIDI対応ソフトで「MIDI Simulator」を入力デバイスとして選択

#### 方法2: Windows標準のMIDIマッパー

1. **コントロールパネル > サウンド**
2. **「録音」タブ > 「MIDI」を右クリック > 「有効にする」**
3. **MIDIシミュレーターが標準のMIDIデバイスに送信**

### DAWでの設定例

#### Reaper

1. **Options > Preferences > Audio > MIDI Devices**
2. **Input devices: 「MIDI Simulator」を有効化**
3. **新しいトラック作成 > 入力を「MIDI Simulator」に設定**

#### FL Studio

1. **Options > MIDI Settings**
2. **Input: 「MIDI Simulator」を選択してEnableにチェック**

#### Ableton Live

1. **Options > Preferences > Link/Tempo/MIDI**
2. **MIDI Ports: 「MIDI Simulator」のTrackとRemoteを有効化**

## トラブルシューティング

### ゲームパッドが認識されない場合

1. Windowsのデバイスマネージャーで認識を確認
2. ゲームパッドのドライバーを再インストール
3. 他のゲームパッド関連ソフトウェアを終了

### MIDIが送信されない場合

1. 仮想MIDIポート（loopMIDI）が作成・起動されているか確認
2. MIDIデバイス/ソフトウェアが他のアプリで使用されていないか確認
3. DAWのMIDI入力設定を確認
4. ファイアウォール設定を確認

### 仮想MIDIポートが認識されない場合

1. loopMIDIを管理者権限で起動
2. Windowsサービス「Windows Audio」を再起動
3. MIDIシミュレーターを再起動

### インストールエラーの場合

1. Python版数を確認（3.7以降）
2. 管理者権限でインストール実行
3. Visual C++ Build Toolsのインストール（Windows）

## MIDI CC一覧

| 軸 | MSB CC | LSB CC | 説明 |
|---|--------|--------|------|
| 左スティック X | CC#16 | CC#48 | General Purpose Controller 1 |
| 左スティック Y | CC#17 | CC#49 | General Purpose Controller 2 |
| 右スティック X | CC#18 | CC#50 | General Purpose Controller 3 |
| 右スティック Y | CC#19 | CC#51 | General Purpose Controller 4 |

## 実行例

```
MIDI Simulator - 14-bit CC Gamepad Controller
==================================================

=== デバイス選択 ===

利用可能なMIDIポート:
  0: Microsoft GS Wavetable Synth 0
  1: loopMIDI Port 1
  2: 仮想MIDIポートを作成

MIDIポートを選択してください (0-2): 1
MIDIポート 'loopMIDI Port 1' に接続しました

ゲームパッドを検出しました: Xbox Controller
ゲームパッド接続: Xbox Controller
軸数: 6
ボタン数: 11

動作開始 (Ctrl+Cで終了)
スティックを動かしてMIDI CCを送信してください
--------------------------------------------------
左スティック X: 0.234→ 6553 Y:-0.456→ 4915
右スティック X:-0.123→ 7372 Y: 0.789→11796
```

## 動作環境

- Windows 10/11
- macOS 10.14以降
- Linux (Ubuntu 18.04以降推奨)
- Python 3.7以降
