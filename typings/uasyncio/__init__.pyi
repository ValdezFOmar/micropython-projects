from _typeshed import Incomplete as Incomplete

def ticks_diff(*args, **kwargs) -> Incomplete: ...
def run_until_complete(*args, **kwargs) -> Incomplete: ...
def create_task(*args, **kwargs) -> Incomplete: ...
def wait_for_ms(*args, **kwargs) -> Incomplete: ...
def run(*args, **kwargs) -> Incomplete: ...
def new_event_loop(*args, **kwargs) -> Incomplete: ...
def current_task(*args, **kwargs) -> Incomplete: ...
def get_event_loop(*args, **kwargs) -> Incomplete: ...
def ticks(*args, **kwargs) -> Incomplete: ...
def sleep_ms(*args, **kwargs) -> Incomplete: ...
def ticks_add(*args, **kwargs) -> Incomplete: ...
def sleep(*args, **kwargs) -> Incomplete: ...

wait_for: Incomplete
gather: Incomplete

class Loop:
    def call_exception_handler(self, *args, **kwargs) -> Incomplete: ...
    def run_forever(self, *args, **kwargs) -> Incomplete: ...
    def set_exception_handler(self, *args, **kwargs) -> Incomplete: ...
    def get_exception_handler(self, *args, **kwargs) -> Incomplete: ...
    def default_exception_handler(self, *args, **kwargs) -> Incomplete: ...
    def run_until_complete(self, *args, **kwargs) -> Incomplete: ...
    def close(self, *args, **kwargs) -> Incomplete: ...
    def stop(self, *args, **kwargs) -> Incomplete: ...
    def create_task(self, *args, **kwargs) -> Incomplete: ...
    def __init__(self, *argv, **kwargs) -> None: ...

class IOQueue:
    def queue_write(self, *args, **kwargs) -> Incomplete: ...
    def queue_read(self, *args, **kwargs) -> Incomplete: ...
    def wait_io_event(self, *args, **kwargs) -> Incomplete: ...
    def remove(self, *args, **kwargs) -> Incomplete: ...
    def __init__(self, *argv, **kwargs) -> None: ...

class Event:
    def set(self, *args, **kwargs) -> Incomplete: ...
    def is_set(self, *args, **kwargs) -> Incomplete: ...
    def clear(self, *args, **kwargs) -> Incomplete: ...
    wait: Incomplete
    def __init__(self, *argv, **kwargs) -> None: ...

class CancelledError(Exception): ...
