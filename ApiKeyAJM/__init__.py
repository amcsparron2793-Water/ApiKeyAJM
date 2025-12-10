from EasyLoggerAJM.UncaughtExceptionHook.uncaught_exception_hook import UncaughtExceptionHook


class ApiKeyUncaughtHook(UncaughtExceptionHook):
    def _log_exception(self, exc_type, exc_value, tb):
        self._basic_log_to_file(exc_type, exc_value, tb)
        super()._log_exception(exc_type, exc_value, tb)


def install_api_key_uncaught_hook() -> None:
    ApiKeyUncaughtHook.set_sys_excepthook()


from ApiKeyAJM.logger import APIKeyLogger
from ApiKeyAJM.api_key_ajm import APIKeyFromFile, RemoteAPIKey

__all__ = ['APIKeyLogger', 'APIKeyFromFile', 'RemoteAPIKey',
           'ApiKeyUncaughtHook', 'install_api_key_uncaught_hook']
