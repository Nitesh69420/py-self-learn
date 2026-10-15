"""
Assignment 2 - Question 1: Desktop Health & Break Reminder Daemon
Subject: Python Laboratory (DJS23APC203L)
Module Focus: Task Scheduling & System Alerts with schedule and plyer
"""

import sys
import time
from datetime import datetime
from plyer import notification
import schedule


def send_break_alert(title: str, message: str):
    """
    Triggers a native cross-platform OS toast notification.
    Timeout is configured to 5 seconds.
    """
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] Triggered Notification -> {title}: {message}")

    try:
        notification.notify(
            title=title,
            message=message,
            app_name="Ergonomic Wellness Daemon",
            timeout=5  # Display duration in seconds
        )
    except Exception as e:
        print(f"[-] Failed to display system toast: {e}")


def setup_schedules():
    """
    Registers periodic task triggers using the schedule library.
    """
    # -------------------------------------------------------------------------
    # TESTING CONFIGURATION (per problem statement):
    # - Hydration Alert: Every 10 seconds
    # - Posture Check: Every 20 seconds
    #
    # PRODUCTION TRANSLATION NOTE:
    # To run this in an actual ergonomic production setting, line 43 changes to:
    # schedule.every(45).minutes.do(send_break_alert, "Hydration Alert", ...)
    # -------------------------------------------------------------------------

    schedule.every(10).seconds.do(
        send_break_alert,
        title="Hydration Alert",
        message="Time to drink a glass of water and stay hydrated!"
    )

    schedule.every(20).seconds.do(
        send_break_alert,
        title="Posture Check",
        message="Sit up straight, roll your shoulders back, and look away from the screen."
    )


def main():
    print("=" * 60)
    print("      DESKTOP HEALTH & BREAK REMINDER DAEMON INITIALIZED    ")
    print("=" * 60)
    print("[*] Schedulers registered:")
    print("    - Hydration Alert : Every 10 seconds (Testing mode)")
    print("    - Posture Check   : Every 20 seconds")
    print("[*] Press Ctrl+C at any time to terminate the daemon safely.\n")

    setup_schedules()

    # Continuous background listener loop
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n" + "=" * 60)
        print("[!] KeyboardInterrupt (Ctrl+C) detected.")
        print("[+] Shutting down Ergonomic Daemon cleanly. Stay healthy!")
        print("=" * 60)
        sys.exit(0)


if __name__ == "__main__":
    main()  