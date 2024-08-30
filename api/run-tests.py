import subprocess
import sys
import os
import threading
import time
import datetime
from enum import Enum


api_ready_timeout = 10
tests_timeout = 120


class ErrorCodes(Enum):
    API_NOT_READY = 101


def start_api() -> subprocess.Popen[bytes]:
    command = "python -m fastapi_cli dev --no-reload"
    print("Start app:", command)
    return subprocess.Popen(
        args=command.split(" "),
        env={
            **os.environ,
            "FORCE_COLOR": "TRUE",
            "PY_COLORS": "TRUE",
        },
        stderr=subprocess.PIPE,
    )


def start_tests() -> subprocess.Popen[bytes]:
    command = "npx -y @usebruno/cli run"
    working = "tests"
    print("start tests:", command, "in:", working)
    return subprocess.Popen(
        args=command.split(" "),
        cwd=working,
    )


api_process = start_api()
api_started = time.time()
api_ready = False

ready_message = "Application startup complete."

print("wait for API message:", ready_message)

while True:
    assert api_process.stderr is not None
    line = api_process.stderr.readline()
    sys.stderr.buffer.write(line)
    sys.stderr.buffer.flush()

    # Cancel when process is finised
    if api_process.poll() is not None:
        break

    # Check if the output contains the specific string
    if ready_message.encode() in line:
        print("Detected API ready message:", ready_message)
        if not api_ready:
            api_ready = True
            tests_process = start_tests()
            tests_started = time.time()

            # Wait with a timeout that the tests finishes
            tests_exit_code = tests_process.wait(tests_timeout)
            print("Tests done!")

            # Shutdown api and wait with another timeout
            api_process.terminate()
            api_exit_code = api_process.wait(10)
            print("API done!")

            # Log exit codes and elapsed time
            api_time_elapsed = datetime.timedelta(seconds=(time.time() - api_started))
            tests_time_elapsed = datetime.timedelta(seconds=(time.time() - tests_started))
            print(f"API ended after {api_time_elapsed} with exit code:", api_exit_code)
            print(f"Tests ended {tests_time_elapsed} with exit code:", tests_exit_code)
            sys.exit(tests_exit_code)


def timeout_for_api_ready_message() -> None:
    time.sleep(api_ready_timeout)
    if not api_ready:
        api_process.terminate()
        sys.exit(ErrorCodes.API_NOT_READY.value)

threading.Thread(target=timeout_for_api_ready_message).start()
