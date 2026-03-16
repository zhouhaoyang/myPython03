"""存储 TCP 服务端收到的消息。"""

from __future__ import annotations

from dataclasses import dataclass, field
from threading import Lock
from typing import List


@dataclass
class MessageStore:
    """线程安全的消息缓存。"""

    _messages: List[str] = field(default_factory=list)
    _lock: Lock = field(default_factory=Lock)

    def add(self, message: str) -> None:
        """添加一条消息。"""
        with self._lock:
            self._messages.append(message)

    def all_messages(self) -> List[str]:
        """返回当前所有消息副本。"""
        with self._lock:
            return list(self._messages)
