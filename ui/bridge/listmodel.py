"""Модель списка для QML поверх обычных словарей.

Главное отличие от «сбросить и заполнить заново»: ``set_items`` сравнивает
старый и новый списки по ключу и сообщает QML только о реальных изменениях
(вставках, удалениях, правках строк). Благодаря этому ``ListView`` может
анимировать появление и исчезновение карточек, а прокрутка и выделение не
прыгают при каждом обновлении данных.
"""

from __future__ import annotations

from typing import Any, Iterable

from PySide6.QtCore import (
    Property,
    QAbstractListModel,
    QByteArray,
    QModelIndex,
    QPersistentModelIndex,
    Qt,
    Signal,
    Slot,
)

_BASE_ROLE = Qt.ItemDataRole.UserRole + 1


class DictListModel(QAbstractListModel):
    """Список словарей с фиксированным набором ролей.

    Роли задаются при создании: каждый ключ словаря доступен в делегате QML
    как одноимённое свойство (``model.title`` или просто ``title``).
    """

    countChanged = Signal()

    def __init__(self, roles: Iterable[str], key: str = "id", parent=None) -> None:
        super().__init__(parent)
        self._roles = list(roles)
        if "model" in self._roles:
            # Роль «model» в делегате перекрывает сам объект model, и все
            # обращения вида model.title молча становятся undefined.
            raise ValueError("роль 'model' запрещена: переименуйте её, например в 'modelName'")
        if key not in self._roles:
            self._roles.insert(0, key)
        self._key = key
        self._role_ids = {name: _BASE_ROLE + i for i, name in enumerate(self._roles)}
        self._items: list[dict[str, Any]] = []

    # -- Qt API ----------------------------------------------------------------
    def rowCount(self, parent: QModelIndex | QPersistentModelIndex = QModelIndex()) -> int:  # noqa: N802
        return 0 if parent.isValid() else len(self._items)

    def data(self, index: QModelIndex | QPersistentModelIndex, role: int = Qt.ItemDataRole.DisplayRole) -> Any:
        if not index.isValid() or not 0 <= index.row() < len(self._items):
            return None
        name = self._roles[role - _BASE_ROLE] if role >= _BASE_ROLE else None
        return self._items[index.row()].get(name) if name else None

    def roleNames(self) -> dict[int, QByteArray]:  # noqa: N802
        return {rid: QByteArray(name.encode()) for name, rid in self._role_ids.items()}

    def _count(self) -> int:
        return len(self._items)

    count = Property(int, _count, notify=countChanged)

    # -- Python API ------------------------------------------------------------
    @property
    def items(self) -> list[dict[str, Any]]:
        return self._items

    @Slot(int, result="QVariantMap")
    def get(self, row: int) -> dict[str, Any]:
        return dict(self._items[row]) if 0 <= row < len(self._items) else {}

    def find(self, key_value: Any) -> int:
        for row, item in enumerate(self._items):
            if item.get(self._key) == key_value:
                return row
        return -1

    def update_row(self, key_value: Any, **changes: Any) -> None:
        """Точечная правка одной строки — без пересборки списка."""
        row = self.find(key_value)
        if row < 0:
            return
        item = self._items[row]
        changed = [name for name, value in changes.items() if item.get(name) != value]
        if not changed:
            return
        item.update(changes)
        idx = self.index(row)
        self.dataChanged.emit(idx, idx, [self._role_ids[n] for n in changed
                                         if n in self._role_ids])

    def append(self, item: dict[str, Any], limit: int | None = None) -> None:
        """Добавляет строку в конец; при превышении ``limit`` срезает начало."""
        if limit is not None and len(self._items) >= limit:
            drop = len(self._items) - limit + 1
            self.beginRemoveRows(QModelIndex(), 0, drop - 1)
            del self._items[:drop]
            self.endRemoveRows()
        row = len(self._items)
        self.beginInsertRows(QModelIndex(), row, row)
        self._items.append(dict(item))
        self.endInsertRows()
        self.countChanged.emit()

    def clear(self) -> None:
        if not self._items:
            return
        self.beginResetModel()
        self._items = []
        self.endResetModel()
        self.countChanged.emit()

    def set_items(self, new_items: list[dict[str, Any]]) -> None:
        """Приводит модель к новому списку минимальным набором изменений."""
        new_items = [dict(it) for it in new_items]
        old_keys = [it.get(self._key) for it in self._items]
        new_keys = [it.get(self._key) for it in new_items]
        if (len(set(new_keys)) != len(new_keys) or None in new_keys
                or len(set(old_keys)) != len(old_keys)):
            self._reset(new_items)
            return

        before = len(self._items)
        new_set = set(new_keys)
        # 1. удаляем то, чего больше нет (с конца, чтобы не сбивать индексы)
        for row in range(len(self._items) - 1, -1, -1):
            if self._items[row].get(self._key) not in new_set:
                self.beginRemoveRows(QModelIndex(), row, row)
                del self._items[row]
                self.endRemoveRows()

        # 2. если порядок оставшихся изменился — проще пересобрать целиком
        kept = [it.get(self._key) for it in self._items]
        if kept != [k for k in new_keys if k in set(kept)]:
            self._reset(new_items)
            return

        # 3. вставляем новые на свои места и правим изменившиеся
        for row, item in enumerate(new_items):
            key = item.get(self._key)
            if row < len(self._items) and self._items[row].get(self._key) == key:
                old = self._items[row]
                changed = [n for n in self._roles if old.get(n) != item.get(n)]
                if changed:
                    self._items[row] = item
                    idx = self.index(row)
                    self.dataChanged.emit(idx, idx, [self._role_ids[n] for n in changed])
            else:
                self.beginInsertRows(QModelIndex(), row, row)
                self._items.insert(row, item)
                self.endInsertRows()
        if len(self._items) != before:
            self.countChanged.emit()

    def _reset(self, items: list[dict[str, Any]]) -> None:
        self.beginResetModel()
        self._items = items
        self.endResetModel()
        self.countChanged.emit()
