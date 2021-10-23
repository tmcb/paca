# SPDX-License-Identifier: X11
#
# Copyright (c) 2021, Tadeu Bastos.  All rights reserved.

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .actor import Actor

from uuid import UUID
from typing import Any, Awaitable, Callable, Type


class Ref:

    __actor_cls: Type['Actor']
    __actor_id: UUID

    def __init__(
        self,
        actor_cls: Type['Actor'],
        actor_id: UUID,
        put_message: Callable[..., Any],
    ) -> None:
        self.__actor_cls = actor_cls
        self.__actor_id = actor_id
        self.__put_message = put_message

    @property
    def actor_id(self):
        return self.__actor_id

    def tell(self, *args: Any, **kwargs: Any) -> None:
        _ = self.__put_message(*args, **kwargs)

    def ask(self, *args: Any, **kwargs: Any) -> Awaitable[Any]:
        return self.__put_message(*args, **kwargs)

    def __lt__(self, message: Any) -> None:
        self.tell(message)

    def __le__(self, message: Any) -> Awaitable[Any]:
        return self.ask(message)

    def __repr__(self) -> str:
        return '<ref to actor <{}.{}#{}>>'.format(
            type(self).__module__,
            self.__actor_cls.__qualname__,
            self.__actor_id,
        )
