from EasyLoggerAJM import EasyLogger


class APIKeyLogger(EasyLogger):
    DEFAULT_LOG_SPEC = "hourly"

    def __init__(self, project_name="APIKeyAJM", **kwargs):
        self.log_spec = kwargs.pop('log_spec', self.__class__.DEFAULT_LOG_SPEC)
        self.show_warn_logs = kwargs.pop('show_warning_logs_in_console', True)

        super().__init__(project_name=project_name, log_spec=self.log_spec,
                         show_warning_logs_in_console=self.show_warn_logs, **kwargs)
