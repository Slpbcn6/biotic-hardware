import sys
import threading
import time

import pytest

_START_AFTER_SECONDS = 2.0
_FRAME_SECONDS = 0.5
_MAX_DOTS = 3


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_call(item):
    writer = item.config.get_terminal_writer()
    capture_manager = item.config.pluginmanager.getplugin("capturemanager")
    verbose = item.config.getoption("verbose", 0)

    if writer is None or not getattr(writer, "hasmarkup", False) or verbose < 1:
        yield
        return

    stop = threading.Event()
    started = time.monotonic()
    shown = {"dots": 0}

    def _emit(text):
        with capture_manager.global_and_fixture_disabled():
            sys.stdout.write(text)
            sys.stdout.flush()

    def _erase():
        n = shown["dots"]
        if n > 0:
            _emit("\b" * n + " " * n + "\b" * n)
            shown["dots"] = 0

    def _animate():
        count = 0
        while not stop.wait(_FRAME_SECONDS):
            if time.monotonic() - started < _START_AFTER_SECONDS:
                continue
            _erase()
            count = count % _MAX_DOTS + 1
            _emit("." * count)
            shown["dots"] = count

    worker = threading.Thread(target=_animate, daemon=True)
    worker.start()
    try:
        yield
    finally:
        stop.set()
        worker.join(timeout=2.0)
        _erase()