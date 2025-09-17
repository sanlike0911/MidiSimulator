#!/usr/bin/env python3
"""
MIDI Simulator - 14-bit CC Gamepad Controller
ゲームパッドの入力を14ビットMIDI CCメッセージに変換
"""

import pygame
import rtmidi
import time
import sys
from typing import Tuple, Optional

class GamepadMidiController:
    def __init__(self):
        self.midi_out = None
        self.joystick = None
        self.running = True

        # MIDI CC番号定義
        self.CC_LEFT_X_MSB = 16
        self.CC_LEFT_X_LSB = 48
        self.CC_LEFT_Y_MSB = 17
        self.CC_LEFT_Y_LSB = 49
        self.CC_RIGHT_X_MSB = 18
        self.CC_RIGHT_X_LSB = 50
        self.CC_RIGHT_Y_MSB = 19
        self.CC_RIGHT_Y_LSB = 51

        # 14ビット値の範囲
        self.NEUTRAL_POSITION = 8192
        self.MAX_14BIT_VALUE = 16383
        self.DEADZONE = 0.1

        # 前回の値を保存（変化時のみ送信）
        self.prev_left_stick = (0.0, 0.0)
        self.prev_right_stick = (0.0, 0.0)

        print("MIDI Simulator - 14-bit CC Gamepad Controller")
        print("=" * 50)

    def select_midi_port(self) -> Optional[int]:
        """利用可能なMIDIポートを表示し、ユーザーに選択させる"""
        try:
            self.midi_out = rtmidi.MidiOut()
            available_ports = self.midi_out.get_ports()

            if not available_ports:
                print("利用可能なMIDIポートがありません")
                print("仮想MIDIポートを作成しますか? (y/n): ", end="")
                if input().lower() in ['y', 'yes', 'はい']:
                    return -1  # 仮想ポートを示す特別な値
                else:
                    return None

            print("\n利用可能なMIDIポート:")
            for i, port in enumerate(available_ports):
                print(f"  {i}: {port}")

            print(f"  {len(available_ports)}: 仮想MIDIポートを作成")

            while True:
                try:
                    choice = input(f"\nMIDIポートを選択してください (0-{len(available_ports)}): ")
                    port_index = int(choice)

                    if port_index == len(available_ports):
                        return -1  # 仮想ポート
                    elif 0 <= port_index < len(available_ports):
                        return port_index
                    else:
                        print(f"無効な選択です。0-{len(available_ports)}の範囲で入力してください。")

                except ValueError:
                    print("数字を入力してください。")
                except KeyboardInterrupt:
                    return None

        except Exception as e:
            print(f"MIDIポート検索エラー: {e}")
            return None

    def init_midi(self, port_index: Optional[int] = None) -> bool:
        """MIDI出力を初期化"""
        try:
            if port_index is None:
                port_index = self.select_midi_port()

            if port_index is None:
                return False

            if not self.midi_out:
                self.midi_out = rtmidi.MidiOut()

            if port_index == -1:
                # 仮想MIDIポートを作成
                self.midi_out.open_virtual_port("MIDI Simulator")
                print("仮想MIDIポート 'MIDI Simulator' を作成しました")
            else:
                available_ports = self.midi_out.get_ports()
                if port_index < len(available_ports):
                    self.midi_out.open_port(port_index)
                    print(f"MIDIポート '{available_ports[port_index]}' に接続しました")
                else:
                    print("選択されたポートが利用できません")
                    return False

            return True

        except Exception as e:
            print(f"MIDI初期化エラー: {e}")
            return False

    def select_gamepad(self) -> Optional[int]:
        """利用可能なゲームパッドを表示し、ユーザーに選択させる"""
        try:
            pygame.init()
            pygame.joystick.init()

            gamepad_count = pygame.joystick.get_count()

            if gamepad_count == 0:
                print("ゲームパッドが接続されていません")
                return None

            if gamepad_count == 1:
                # ゲームパッドが1つだけの場合は自動選択
                joystick = pygame.joystick.Joystick(0)
                print(f"\nゲームパッドを検出しました: {joystick.get_name()}")
                return 0

            print(f"\n{gamepad_count}個のゲームパッドが見つかりました:")
            for i in range(gamepad_count):
                joystick = pygame.joystick.Joystick(i)
                print(f"  {i}: {joystick.get_name()}")

            while True:
                try:
                    choice = input(f"\nゲームパッドを選択してください (0-{gamepad_count-1}): ")
                    gamepad_index = int(choice)

                    if 0 <= gamepad_index < gamepad_count:
                        return gamepad_index
                    else:
                        print(f"無効な選択です。0-{gamepad_count-1}の範囲で入力してください。")

                except ValueError:
                    print("数字を入力してください。")
                except KeyboardInterrupt:
                    return None

        except Exception as e:
            print(f"ゲームパッド検索エラー: {e}")
            return None

    def init_gamepad(self, gamepad_index: Optional[int] = None) -> bool:
        """ゲームパッドを初期化"""
        try:
            if gamepad_index is None:
                gamepad_index = self.select_gamepad()

            if gamepad_index is None:
                return False

            if not pygame.get_init():
                pygame.init()
                pygame.joystick.init()

            if gamepad_index >= pygame.joystick.get_count():
                print("選択されたゲームパッドが利用できません")
                return False

            self.joystick = pygame.joystick.Joystick(gamepad_index)
            self.joystick.init()

            print(f"ゲームパッド接続: {self.joystick.get_name()}")
            print(f"軸数: {self.joystick.get_numaxes()}")
            print(f"ボタン数: {self.joystick.get_numbuttons()}")

            return True

        except Exception as e:
            print(f"ゲームパッド初期化エラー: {e}")
            return False

    def convert_to_midi_value(self, analog_value: float) -> int:
        """アナログ値(-1.0～1.0)を14ビットMIDI値(0-16383)に変換"""
        # デッドゾーン適用
        if abs(analog_value) < self.DEADZONE:
            analog_value = 0.0

        # -1.0～1.0 を 0.0～1.0 に正規化
        normalized = (analog_value + 1.0) * 0.5

        # 0-16383の範囲にスケール
        midi_value = int(normalized * self.MAX_14BIT_VALUE)
        return max(0, min(self.MAX_14BIT_VALUE, midi_value))

    def send_14bit_cc(self, cc_lsb: int, cc_msb: int, value: int):
        """14ビットCC送信（LSB→MSB順）"""
        if not self.midi_out:
            return

        # 14ビット値を7ビットずつに分割
        lsb = value & 0x7F  # 下位7ビット
        msb = (value >> 7) & 0x7F  # 上位7ビット

        # LSBを先に送信
        cc_lsb_msg = [0xB0, cc_lsb, lsb]
        self.midi_out.send_message(cc_lsb_msg)

        # MSBを後から送信
        cc_msb_msg = [0xB0, cc_msb, msb]
        self.midi_out.send_message(cc_msb_msg)

    def get_stick_values(self) -> Tuple[Tuple[float, float], Tuple[float, float]]:
        """スティック値を取得"""
        if not self.joystick:
            return (0.0, 0.0), (0.0, 0.0)

        # 左スティック (通常は軸0,1)
        left_x = self.joystick.get_axis(0) if self.joystick.get_numaxes() > 0 else 0.0
        left_y = -self.joystick.get_axis(1) if self.joystick.get_numaxes() > 1 else 0.0  # Y軸反転

        # 右スティック (通常は軸2,3または4,5)
        right_x = self.joystick.get_axis(2) if self.joystick.get_numaxes() > 2 else 0.0
        right_y = -self.joystick.get_axis(3) if self.joystick.get_numaxes() > 3 else 0.0  # Y軸反転

        return (left_x, left_y), (right_x, right_y)

    def process_input(self):
        """入力処理とMIDI送信"""
        pygame.event.pump()

        left_stick, right_stick = self.get_stick_values()

        # 左スティック処理
        if abs(left_stick[0] - self.prev_left_stick[0]) > 0.001 or \
           abs(left_stick[1] - self.prev_left_stick[1]) > 0.001:

            x_value = self.convert_to_midi_value(left_stick[0])
            y_value = self.convert_to_midi_value(left_stick[1])

            self.send_14bit_cc(self.CC_LEFT_X_LSB, self.CC_LEFT_X_MSB, x_value)
            self.send_14bit_cc(self.CC_LEFT_Y_LSB, self.CC_LEFT_Y_MSB, y_value)

            print(f"左スティック X:{left_stick[0]:6.3f}→{x_value:5d} Y:{left_stick[1]:6.3f}→{y_value:5d}")
            self.prev_left_stick = left_stick

        # 右スティック処理
        if abs(right_stick[0] - self.prev_right_stick[0]) > 0.001 or \
           abs(right_stick[1] - self.prev_right_stick[1]) > 0.001:

            x_value = self.convert_to_midi_value(right_stick[0])
            y_value = self.convert_to_midi_value(right_stick[1])

            self.send_14bit_cc(self.CC_RIGHT_X_LSB, self.CC_RIGHT_X_MSB, x_value)
            self.send_14bit_cc(self.CC_RIGHT_Y_LSB, self.CC_RIGHT_Y_MSB, y_value)

            print(f"右スティック X:{right_stick[0]:6.3f}→{x_value:5d} Y:{right_stick[1]:6.3f}→{y_value:5d}")
            self.prev_right_stick = right_stick

    def run(self):
        """メインループ"""
        print("\n=== デバイス選択 ===")

        if not self.init_midi():
            print("MIDIデバイスの初期化に失敗しました")
            return False

        if not self.init_gamepad():
            print("ゲームパッドの初期化に失敗しました")
            return False

        print("\n動作開始 (Ctrl+Cで終了)")
        print("スティックを動かしてMIDI CCを送信してください")
        print("-" * 50)

        try:
            while self.running:
                self.process_input()
                time.sleep(0.01)  # 100Hz更新

        except KeyboardInterrupt:
            print("\n終了します...")
        finally:
            self.cleanup()

    def cleanup(self):
        """リソースの解放"""
        if self.joystick:
            self.joystick.quit()

        if self.midi_out:
            self.midi_out.close_port()

        pygame.quit()
        print("リソースを解放しました")

def main():
    controller = GamepadMidiController()
    controller.run()

if __name__ == "__main__":
    main()