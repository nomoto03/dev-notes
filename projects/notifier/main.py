import os
import random
import threading
import time
from tkinter import Tk, Label, Button, Toplevel
from win10toast import ToastNotifier

# --- 設定 ---
MESSAGES = [
    "セルフコントロール",
    "小さな積み重ね"
]
NOTIFY_INTERVAL = 60  # 秒（通知間隔）
FORCE_POPUP_THRESHOLD = 3  # 何回未対応で強制ポップアップ
NOTIFIER_DURATION = 5  # 通知表示秒数

# 状態管理
notifier = ToastNotifier()
unseen_count = 0
lock = threading.Lock()

# 通知時のメッセージを作成
def make_notification_message():
    message = random.choice(MOTIVATION_MESSAGES)
    return message

# 通知クリック時のコールバック
def on_notification_clicked():
    global unseen_count
    with lock:
        unseen_count = 0  # 未対応カウントをリセット
    print("[通知] タスク確認済み")

# トースト通知を表示
def show_toast_notification():
    message = make_notification_message()
    notifier.show_toast(
        "タスク確認",
        message,
        duration=NOTIFIER_DURATION,
        icon_path=None,
        threaded=True,
        callback_on_click=on_notification_clicked
    )

# 強制ポップアップを表示
def show_force_popup():
    def on_do_now():
        nonlocal popup
        with lock:
            global unseen_count
            unseen_count = 0
        print("[ポップアップ] 今やるを選択")
        popup.destroy()
    
    def on_snooze():
        print("[ポップアップ] スヌーズを選択")
        popup.destroy()
        # スヌーズ後、すぐ通知を再開するため unseen_count はそのままにする
    
    popup = Tk()
    popup.title("タスク確認")
    popup.geometry("300x150")
    popup.attribute("-topmost", True)  # 常に最前面に表示
    popup.resizable(False, False)

    Label(popup, text=random.choice(MOTIVATION_MESSAGES), font=("Arial", 10), pady=5).pack()

    btn_frame = Tk.Frame(popup)
    btn_frame.pack(pady=10)

    Button(btn_frame, text="今やる", command=on_do_now).pack(side="left", padx=15)
    Button(btn_frame, text="スヌーズ", command=on_snooze).pack(side="right", padx=15)

    popup.mainloop()

# メイン監視ループ
def notification_loop():
    global unseen_count
    while True:
        with lock:
            count = unseen_count
        
        if count >= FORCE_POPUP_THRESHOLD:
            print(f"[通知] {count}回未対応。強制ポップアップを表示")
            show_force_popup()
            with lock:
                unseen_count = 0 # ポップアップ後はカウントをリセット
        else:
            print(f"[通知] トースト通知を表示 {count}回未対応。")
            show_toast_notification()
            with lock:
                unseen_count += 1
        time.sleep(NOTIFY_INTERVAL)

if __name__ == "__main__":
    print("Notifier is starting...")
    thread = threading.Thread(target=notification_loop, daemon=True)
    thread.start()

    while True:
        try:
            time.sleep(1)  # メインスレッドは何もしない
        except KeyboardInterrupt:
            print("Notifier is stopping...")
            break