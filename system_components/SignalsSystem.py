from __future__ import annotations
from system_components.Core_Builded import core
from typing import Dict, List
from collections import deque


class SignalsSystem:
    """Система сигналов (событий). Позволяет объектам подписываться на сигналы и получать уведомления."""

    uid: str
    subscriptions: Dict
    subscriptions_by_uid: Dict[str, List[str]]
    signals_archive: deque
    system_name: str

    def __init__(self):
        self.subscriptions = {}
        self.subscriptions_by_uid = {}
        self.signals_archive = deque(maxlen=500)
        self.uid = core.utils().uid()
        self.system_name = "SignalsSystem"
        core.registry().register(self)

    def subscribe(
        self,
        signal_names: str | List[str],
        object_uid: str,
        method_name: str,
        allow_duplicates: bool = False,
        priority: int = 0,
    ):
        """Подписывает объект на один или несколько сигналов."""
        if isinstance(signal_names, str):
            signal_names = [signal_names]

        for signal_name in signal_names:
            if signal_name not in self.subscriptions:
                self.subscriptions[signal_name] = []
            callback_blueprint = (object_uid, method_name, priority)
            if allow_duplicates:
                self.subscriptions[signal_name].append(callback_blueprint)
                core.logger().info(
                    f"Подписка оформлена: {callback_blueprint} на {signal_name}"
                )
            else:
                subscriable = True
                for subscripstion in self.subscriptions[signal_name]:
                    if (
                        subscripstion[0] == callback_blueprint[0]
                        and subscripstion[1] == callback_blueprint[1]
                    ):
                        subscriable = False
                        break
                if subscriable:
                    self.subscriptions[signal_name].append(callback_blueprint)
                    if object_uid not in self.subscriptions_by_uid:
                        self.subscriptions_by_uid[object_uid] = {}
                    if method_name not in self.subscriptions_by_uid[object_uid]:
                        self.subscriptions_by_uid[object_uid][method_name] = []
                    self.subscriptions_by_uid[object_uid][method_name].append(
                        signal_name
                    )
                    core.logger().info(
                        f"Подписка оформлена: {callback_blueprint} на {signal_name}"
                    )

    def unsubscribe(
        self, signal_names: str | List[str], object_uid: str, method_name: str
    ):
        """Отписывает объект от одного или нескольких сигналов."""
        if isinstance(signal_names, str):
            signal_names = [signal_names]
        callback_blueprint = (object_uid, method_name)
        for signal_name in signal_names:
            if signal_name in self.subscriptions:
                for subscripstion in self.subscriptions[signal_name]:
                    if (
                        subscripstion[0] == callback_blueprint[0]
                        and subscripstion[1] == callback_blueprint[1]
                    ):
                        self.subscriptions[signal_name].remove(subscripstion)
                        self.subscriptions_by_uid[object_uid][method_name].remove(
                            signal_name
                        )
                        core.logger().info(
                            f"Отписка: {callback_blueprint} от {signal_name}"
                        )

                if len(self.subscriptions[signal_name]) == 0:
                    del self.subscriptions[signal_name]
                    core.logger().info(
                        f"Сигнал {signal_name} удалён, подписчиков не осталось"
                    )
                if len(self.subscriptions_by_uid[object_uid][method_name]) == 0:
                    del self.subscriptions_by_uid[object_uid][method_name]
                if len(self.subscriptions_by_uid[object_uid]) == 0:
                    del self.subscriptions_by_uid[object_uid]
        self.version.increase()

    def notify(self, signal_names: str | List[str], /, *args, **kwargs):
        """Уведомляет всех подписчиков о наступлении одного или нескольких сигналов."""
        if isinstance(signal_names, str):
            signal_names = [signal_names]

        for signal_name in signal_names:
            core.logger().signal(f"{signal_name}")
            self.signals_archive.append(signal_name)
            if signal_name in self.subscriptions:
                sorted_callbacks = sorted(
                    self.subscriptions[signal_name],
                    key=lambda x: x[2],  # Сортируем по `priority`
                    reverse=True,  # От большего к меньшему
                )
                for callback_blueprint in sorted_callbacks:
                    callback = self.generate_callback(
                        callback_blueprint[0], callback_blueprint[1]
                    )
                    callback_name = callback.__name__
                    core.logger().debug(
                        f"   🔹 Вызов: {callback_blueprint} - {callback_name} - args: {str(args)} - kwargs: {str(kwargs)}"
                    )
                    callback(*args, **kwargs)

    def generate_callback(self, object_uid: str, method_name: str):
        """Генерирует вызываемый метод по UID объекта и имени метода."""
        obj = core.registry().get(object_uid)
        callback = getattr(obj, method_name)
        return callback

    def get_subscriptions_by_uid(self, object_uid: str) -> List:
        """Возвращает список сигналов, на которые подписан объект по UID и имени метода."""
        if object_uid in self.subscriptions_by_uid:
            return self.subscriptions_by_uid[object_uid]
        return []

    def tick(self):
        """Вызывает триггер 'tick'."""
        self.notify("tick_back")
        self.notify("tick_ui_adapter")
        self.notify("tick_ui_itself")
