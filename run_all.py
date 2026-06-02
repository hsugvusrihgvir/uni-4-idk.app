import subprocess
import sys
import threading
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent
PROCESSES = [
    ("backend", ROOT_DIR / "server", [sys.executable, "-m", "uvicorn", "app.main:app", "--reload"]),
    ("telegram", ROOT_DIR / "server", [sys.executable, "-m", "app.bot.telegram_bot"]),
    ("frontend", ROOT_DIR / "client", ["npm.cmd" if sys.platform == "win32" else "npm", "run", "dev"]),
]


def stream_output(name: str, process: subprocess.Popen) -> None:
    if process.stdout is None:
        return

    for line in process.stdout:
        print(f"[{name}] {line}", end="", flush=True)


def main() -> int:
    processes: list[tuple[str, subprocess.Popen]] = []

    try:
        for name, cwd, command in PROCESSES:
            process = subprocess.Popen(
                command,
                cwd=cwd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
            )
            processes.append((name, process))
            threading.Thread(target=stream_output, args=(name, process), daemon=True).start()
            print(f"[run_all] started {name}: {' '.join(command)}", flush=True)

        while True:
            for name, process in processes:
                code = process.poll()
                if code is not None:
                    print(f"[run_all] {name} exited with code {code}", flush=True)
                    return code

            threading.Event().wait(1)
    except KeyboardInterrupt:
        print("[run_all] stopping processes", flush=True)
        return 0
    finally:
        for _, process in processes:
            if process.poll() is None:
                process.terminate()

        for _, process in processes:
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                process.kill()


if __name__ == "__main__":
    raise SystemExit(main())
