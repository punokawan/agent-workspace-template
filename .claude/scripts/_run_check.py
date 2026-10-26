#!/usr/bin/env python3
"""Run one verification command with total and output-idle timeouts."""

from __future__ import annotations

import os
import selectors
import signal
import subprocess
import sys
import time


def main() -> int:
    if len(sys.argv) < 5:
        print("usage: _run_check.py <log> <timeout-seconds> <stall-seconds> <command...>", file=sys.stderr)
        return 2

    log_path, timeout_text, stall_text, *command = sys.argv[1:]
    timeout = int(timeout_text)
    stall = int(stall_text)
    started = last_output = time.monotonic()

    with open(log_path, "wb") as log:
        process = subprocess.Popen(
            command,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            start_new_session=True,
        )
        assert process.stdout is not None
        selector = selectors.DefaultSelector()
        selector.register(process.stdout, selectors.EVENT_READ)

        while process.poll() is None:
            for key, _ in selector.select(timeout=1):
                chunk = os.read(key.fileobj.fileno(), 65536)
                if chunk:
                    log.write(chunk)
                    log.flush()
                    last_output = time.monotonic()

            now = time.monotonic()
            reason = None
            if timeout > 0 and now - started >= timeout:
                reason = f"total timeout after {timeout}s"
            elif stall > 0 and now - last_output >= stall:
                reason = f"no output for {stall}s"
            if reason:
                log.write(f"\nSTUDIO VERIFY STOPPED: {reason}\n".encode())
                os.killpg(process.pid, signal.SIGTERM)
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    os.killpg(process.pid, signal.SIGKILL)
                    process.wait()
                return 124

        remainder = process.stdout.read()
        if remainder:
            log.write(remainder)
        return process.returncode


if __name__ == "__main__":
    raise SystemExit(main())
