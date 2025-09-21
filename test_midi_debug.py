#!/usr/bin/env python3
"""
MIDI入力デバッグテスト
"""

import time
import rtmidi

def test_midi_input():
    """MIDI入力のテスト"""
    print("MIDI入力デバッグテスト")
    print("=" * 30)

    try:
        midi_in = rtmidi.MidiIn()
        available_ports = midi_in.get_ports()

        if not available_ports:
            print("利用可能なMIDI入力ポートがありません")
            return

        print("利用可能なMIDI入力ポート:")
        for i, port in enumerate(available_ports):
            print(f"  {i}: {port}")

        # 最初のポートに自動接続（テスト用）
        port_index = 0
        if len(available_ports) > 1:
            port_index = 1  # loopMIDIがある場合はそちらを使用

        midi_in.open_port(port_index)
        midi_in.set_callback(midi_callback)

        print(f"\nポート '{available_ports[port_index]}' に接続しました")
        print("MIDI入力待機中... (Ctrl+Cで終了)")
        print("-" * 40)

        try:
            while True:
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("\n終了します...")
        finally:
            midi_in.close_port()

    except Exception as e:
        print(f"エラー: {e}")

def midi_callback(message, data=None):
    """MIDI入力コールバック"""
    msg, timestamp = message

    if len(msg) >= 2:
        status = msg[0]

        if status & 0xF0 == 0xB0:  # Control Change
            cc_number = msg[1]
            cc_value = msg[2] if len(msg) > 2 else 0
            channel = (status & 0x0F) + 1

            print(f"[MIDI入力] Ch.{channel} CC#{cc_number} = {cc_value} (0x{cc_value:02X}) [{' '.join(f'0x{b:02X}' for b in msg)}]")

        elif status & 0xF0 == 0x90:  # Note On
            note = msg[1]
            velocity = msg[2] if len(msg) > 2 else 0
            channel = (status & 0x0F) + 1

            print(f"[MIDI入力] Ch.{channel} Note On: {note} vel={velocity} [{' '.join(f'0x{b:02X}' for b in msg)}]")

        elif status & 0xF0 == 0x80:  # Note Off
            note = msg[1]
            velocity = msg[2] if len(msg) > 2 else 0
            channel = (status & 0x0F) + 1

            print(f"[MIDI入力] Ch.{channel} Note Off: {note} vel={velocity} [{' '.join(f'0x{b:02X}' for b in msg)}]")

        else:
            print(f"[MIDI入力] Raw: [{' '.join(f'0x{b:02X}' for b in msg)}]")
    else:
        print(f"[MIDI入力] Raw: [{' '.join(f'0x{b:02X}' for b in msg)}]")

if __name__ == "__main__":
    test_midi_input()