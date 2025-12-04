import sys
from system_components.Core_Builded import core


class ShortcutsManager:
    uid: str
    shortcuts: dict[str, str]
    system_name: str

    def __init__(self):
        self.uid = core.utils().uid()
        self.system_name = "ShortcutsManager"
        core.registry().register(self)
        self.shortcuts = {}

    def create(self, alias: str, object_uid: str):
        if alias in self.shortcuts:
            core.logger().warning(f"Shortcut '{alias}' already exists. Overwriting.")
        self.shortcuts[alias] = object_uid

    def get(self, alias):
        """Получает данные по шорткату."""
        if alias in self.shortcuts:
            object_uid = self.shortcuts.get(alias)
            object = core.registry().get(object_uid)
            return object
        else:
            core.logger().warning(f"Shortcut '{alias}' not found.")
            return None

    def remove(self, alias):
        """Удаляет шорткат"""
        if alias in self.shortcuts:
            del self.shortcuts[alias]
        else:
            core.logger().warning(f"Shortcut '{alias}' not found for removal.")
