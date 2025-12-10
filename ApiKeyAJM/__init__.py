from EasyLoggerAJM.UncaughtExceptionHook.uncaught_exception_hook import UncaughtExceptionHook


class ApiKeyUncaughtHook(UncaughtExceptionHook):
    def _log_exception(self, exc_type, exc_value, tb):
        self._basic_log_to_file(exc_type, exc_value, tb)
        super()._log_exception(exc_type, exc_value, tb)


ApiKeyUncaughtHook().set_sys_excepthook()

from ApiKeyAJM.api_key_ajm import APIKeyFromFile, RemoteAPIKey
