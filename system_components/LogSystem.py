import logging
from system_components.Core_Builded import core

SIGNAL_LEVEL = 25
logging.addLevelName(
    SIGNAL_LEVEL, "SIGNAL"
)  # Добавляем уровень логирования для сигналов


def signal(self, message, *args, **kws):
    if self.isEnabledFor(SIGNAL_LEVEL):
        self._log(SIGNAL_LEVEL, message, args, **kws)


logging.Logger.signal = signal


class LogSystem:
    """
    Гибкая система логирования.
    - log_file: имя файла (если None, лог в файл не ведётся).
    - log_to_console: логировать ли в консоль.
    - log_levels: список уровней, которые записываются.
    """

    _instance = None  # Храним единственный экземпляр

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(LogSystem, cls).__new__(cls)
            cls._instance._init(*args, **kwargs)  # Вызываем _init вместо __init__
        return cls._instance

    def _init(self, log_file=None, log_to_console=True, log_levels=None):
        """Инициализация логгера, выполняется только один раз."""
        self.logger = logging.getLogger("Clusters")
        self.logger.setLevel(logging.DEBUG)  # Общий уровень логирования
        self.log_levels = log_levels
        self.uid = core.utils().uid()
        self.system_name = "LogSystem"
        core.registry().register(self)
        if not self.logger.hasHandlers():  # Проверяем, есть ли уже обработчики
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )

            self.log_levels = (
                set(log_levels)
                if log_levels
                else {"debug", "info", "warning", "error", "signal"}
            )
            # Файловый логгер (если указан log_file)
            if log_file:
                file_handler = logging.FileHandler(log_file, encoding="utf-8")
                file_handler.setFormatter(formatter)
                file_handler.setLevel(logging.DEBUG)
                self.logger.addHandler(file_handler)

            # Логгер в консоль (если включено)
            if log_to_console:
                console_handler = logging.StreamHandler()
                console_handler.setFormatter(formatter)
                console_handler.setLevel(logging.DEBUG)
                self.logger.addHandler(console_handler)

    def log(self, level, message):
        """Логирует сообщение с заданным уровнем, если уровень разрешён."""
        if level in self.log_levels:
            if level == "info":
                self.logger.info(message)
            elif level == "signal":
                self.logger.signal(message)
            elif level == "warning":
                self.logger.warning(message)
            elif level == "error":
                self.logger.error(message)
            elif level == "debug":
                self.logger.debug(message)
            else:
                self.logger.error(f"⚠️ [Неизвестный уровень]: {message}")

    def debug(self, message):
        self.log("debug", message)

    def info(self, message):
        self.log("info", message)

    def warning(self, message):
        self.log("warning", message)

    def error(self, message):
        self.log("error", message)

    def signal(self, message):
        self.log("signal", message)
