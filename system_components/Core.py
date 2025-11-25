from __future__ import annotations
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from system_components.LogSystem import LogSystem
    from system_components.ObjectRegistry import ObjectRegistry
    from system_components.SignalsSystem import SignalsSystem
    from system_components.Utils import Utils


class Core:
    _logger: LogSystem = None
    _registry: ObjectRegistry = None
    _signals: SignalsSystem = None
    _utils: Utils = None

    def __init__(self):
        pass

    def set_logger(self, logger: LogSystem = None):
        if logger is None:
            from system_components.LogSystem import LogSystem

            logger = LogSystem()
        self._logger = logger

    def set_registry(self, registry: ObjectRegistry = None):
        if registry is None:
            from system_components.ObjectRegistry import ObjectRegistry

            registry = ObjectRegistry()
        self._registry = registry

    def set_signals(self, signals: SignalsSystem = None):
        if signals is None:
            from system_components.SignalsSystem import SignalsSystem

            signals = SignalsSystem()
        self._signals = signals

    def set_utils(self, utils: Utils = None):
        if utils is None:
            from system_components.Utils import Utils

            utils = Utils()
        self._utils = utils

    def logger(self):
        """Возвращает логгер."""
        return self._logger

    def registry(self):
        """Возвращает реестр объектов."""
        return self._registry

    def signals(self):
        """Возвращает систему сигналов."""
        return self._signals

    def utils(self):
        """Возвращает набор утилит."""
        return self._utils
