# SPDX-License-Identifier: X11
#
# Copyright (c) 2021, Tadeu Bastos.  All rights reserved.


from .ref import Ref

from typing import Any, Callable, Coroutine


class Context:

    __ref: Ref

    def __init__(
        self,
        actor_ref: Ref,
        actor_close: Callable[[], Coroutine[Any, Any, None]],
    ) -> None:
        self.__ref = actor_ref
        self.__close = actor_close

    async def __aenter__(self) -> Ref:
        return self.__ref

    async def __aexit__(
        self, exc_type: Any, exc_value: Any, traceback: Any
    ) -> None:
        await self.__close()
