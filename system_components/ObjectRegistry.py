from system_components.Core_Builded import core
from typing import Any, Dict, List, Optional, Type
from weakref import WeakValueDictionary


class ObjectRegistry:
    """
    Хранилище всех объектов игры, индексированных по UID и system_name.

    Предоставляет доступ к:
    - Получению объекта по UID или system_name
    - Фильтрации по типу или атрибутам
    - Управлению версиями
    - Удалению объектов
    """

    uid: str
    # objects: WeakValueDictionary[str, object]  # {uid: объект}
    objects: Dict[
        str, object
    ]  # NB! {uid: объект} на время отладки это обычный словарь, чтобы проще было отлавливать ошибки. Плюс в Кластерах не так много обхъектов, можно и постоянно так держать.
    system_name_to_uid_registry: Dict[str, str]
    system_name: str

    def __init__(self):
        self.uid = core.utils().uid()
        # self.objects: WeakValueDictionary[str, object] = (
        #     WeakValueDictionary()
        # )  # {uid: объект}
        self.objects: Dict[str, object] = (
            {}
        )  # NB! {uid: объект} на время отладки это обычный словарь, чтобы проще было отлавливать ошибки. Плюс в Кластерах не так много обхъектов, можно и постоянно так держать.
        self.system_name = "ObjectsRegistry"
        self.system_name_to_uid_registry = {}  # {system_name: uid}
        self.register(obj=self)

    def register(self, obj: object):
        """Добавляет объект в реестр, индексируя по uid и system_name (если есть)."""
        self.objects[obj.uid] = obj
        if hasattr(obj, "system_name"):
            self.system_name_to_uid_registry[obj.system_name] = obj.uid

    def get(self, uid: str) -> Optional[Any]:
        """Возвращает объект по UID (или None, если не найден)."""
        return self.objects.get(uid, None)

    def get_by_system_name(self, system_name: str) -> Optional[Any]:
        """Возвращает объект по system_name (или None, если не найден)."""
        uid = self.system_name_to_uid_registry.get(system_name)
        result = self.objects.get(uid, None)
        return result

    def get_all(self) -> List[Any]:
        """Возвращает список всех объектов в реестре."""
        result = list(self.objects.values())
        return result

    def get_all_system_names(self) -> List[str]:
        """Возвращает список всех system_name в реестре."""
        result = list(self.system_name_to_uid_registry.keys())
        return result

    def get_all_by_type(self, cls: Type) -> List[Any]:
        """Возвращает все объекты заданного типа."""
        result = [obj for obj in self.objects.values() if isinstance(obj, cls)]
        return result

    def get_all_by_attr(self, attr_name: str, attr_value: Any) -> List[Any]:
        """Возвращает объекты, у которых есть указанный атрибут с заданным значением."""
        result = [
            obj
            for obj in self.objects.values()
            if hasattr(obj, attr_name) and getattr(obj, attr_name) == attr_value
        ]
        return result

    def remove(self, uid_or_system_name: str):
        """
        Удаляет объект из реестра и индекса по system_name (если был).
        """
        if uid_or_system_name in self.system_name_to_uid_registry:
            uid = self.get_by_system_name(uid_or_system_name).get("uid", None)
        else:
            uid = uid_or_system_name
        if uid in self.objects:
            system_name = getattr(self.objects[uid], "system_name", None)
            if system_name in self.system_name_to_uid_registry:
                del self.system_name_to_uid_registry[system_name]
                del self.objects[uid]
            else:
                del self.objects[uid]
