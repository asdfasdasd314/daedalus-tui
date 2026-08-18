from .app import DaedalusTuiApp
from .debug_log import log_exception


def main() -> None:
    app = DaedalusTuiApp()
    try:
        app.run()
    except BaseException as error:
        log_exception("Textual run loop raised", error)
        app.shutdown_after_run()
        raise
    app.shutdown_after_run()


if __name__ == "__main__":
    main()
