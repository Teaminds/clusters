from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from system_components.LogSystem import LogSystem
    from system_components.ObjectRegistry import ObjectRegistry
    from system_components.SignalsSystem import SignalsSystem
    from system_components.Utils import Utils
    from system_components.ShortcutsSystem import ShortcutsManager


class Core:
    _logger: LogSystem = None
    _registry: ObjectRegistry = None
    _signals: SignalsSystem = None
    _utils: Utils = None
    _shortcuts: ShortcutsManager = None

    def __init__(self):
        self.system_name = "Core"
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
        if self.uid is not None:
            self._registry.register(self)

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
        self.uid = self.utils().uid()
        if self._registry is not None:
            self._registry.register(self)

    def set_shortcuts(self, shortcuts: ShortcutsManager = None):
        if shortcuts is None:
            from system_components.ShortcutsSystem import ShortcutsManager

            shortcuts = ShortcutsManager()
        self._shortcuts = shortcuts

    def logger(self) -> LogSystem:
        """Возвращает логгер."""
        return self._logger

    def registry(self) -> ObjectRegistry:
        """Возвращает реестр объектов."""
        return self._registry

    def signals(self) -> SignalsSystem:
        """Возвращает систему сигналов."""
        return self._signals

    def utils(self) -> Utils:
        """Возвращает набор утилит."""
        return self._utils

    def shortcuts(self) -> ShortcutsManager:
        """Возвращает менеджер шорткатов."""
        return self._shortcuts
