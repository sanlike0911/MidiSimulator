#!/usr/bin/env python3
"""
MIDI Simulator セットアップ・実行スクリプト
"""

import subprocess
import sys
import os

def install_requirements():
    """必要なパッケージをインストール"""
    print("必要なパッケージをインストール中...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ パッケージのインストールが完了しました")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ パッケージのインストールに失敗しました: {e}")
        return False

def check_dependencies():
    """依存関係をチェック"""
    missing_packages = []

    try:
        import pygame
        print("✓ pygame が利用可能です")
    except ImportError:
        missing_packages.append("pygame")

    try:
        import rtmidi
        print("✓ python-rtmidi が利用可能です")
    except ImportError:
        missing_packages.append("python-rtmidi")

    return missing_packages

def run_simulator():
    """シミュレーターを実行"""
    print("\nMIDI Simulator を起動中...")
    try:
        import midi_simulator
        midi_simulator.main()
    except Exception as e:
        print(f"✗ 実行エラー: {e}")
        return False
    return True

def main():
    print("MIDI Simulator セットアップ")
    print("=" * 40)

    # 依存関係チェック
    missing = check_dependencies()

    if missing:
        print(f"\n不足しているパッケージ: {', '.join(missing)}")
        print("インストールを実行しますか? (y/n): ", end="")

        if input().lower() in ['y', 'yes']:
            if not install_requirements():
                return
        else:
            print("セットアップを中止しました")
            return

    # 再度チェック
    missing = check_dependencies()
    if missing:
        print(f"✗ まだ不足しているパッケージがあります: {', '.join(missing)}")
        return

    print("\n✓ すべての依存関係が満たされています")
    print("\nシミュレーターを起動しますか? (y/n): ", end="")

    if input().lower() in ['y', 'yes']:
        run_simulator()
    else:
        print("セットアップ完了。後で 'python midi_simulator.py' で起動してください。")

if __name__ == "__main__":
    main()