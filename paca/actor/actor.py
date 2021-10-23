# SPDX-License-Identifier: X11
#
# Copyright (c) 2021, Tadeu Bastos.  All rights reserved.

from .context import Context
from .ref import Ref

from asyncio import AbstractEventLoop, get_event_loop, gather as asyncio_gather
from collections import deque
from inspect import isawaitable
from typing import Any, Awaitable, List, Optional, Type
from uuid import UUID
from random import getrandbits


class Actor:

    __actor_id: UUID

    __loop: AbstractEventLoop

    __mailbox: deque[Any]

    __tasks: List[Awaitable[Any]]

    __closed: bool

    _receive: Any

    def __new__(
        cls: Type['Actor'],
        *args: Any,
        loop: Optional[AbstractEventLoop] = None,
        maxlen: Optional[int] = None,
        **kwargs: Any,
    ) -> Any:
        instance = super().__new__(cls)
        instance.__actor_id = cls.__new_actor_id()
        instance.__loop = cls.__new_event_loop(loop)
        instance.__mailbox = cls.__new_mailbox(maxlen=maxlen)
        instance.__tasks = cls.__new_tasks()
        instance.__closed = False
        return instance

    @staticmethod
    def __new_actor_id() -> UUID:
        return UUID(int=getrandbits(128), version=4)

    @staticmethod
    def __new_event_loop(
        loop: Optional[AbstractEventLoop]
    ) -> AbstractEventLoop:
        if loop is None:
            loop = get_event_loop()
        if not isinstance(loop, AbstractEventLoop):
            error_msg = 'object of type \'{}\' is not an event loop'.format(
                type(loop).__name__)
            raise TypeError(error_msg)
        return loop

    @staticmethod
    def __new_mailbox(maxlen=None) -> deque:
        return deque(maxlen=maxlen)

    @staticmethod
    def __new_tasks() -> List:
        return list()

    @property
    def ref(self) -> Ref:
        return Ref(type(self), self.__actor_id, self.__put_message)

    @property
    def actor_id(self) -> UUID:
        return self.__actor_id

    @property
    def context(self) -> Context:
        return Context(self.ref, self.close)

    async def close(self, gather: bool = True) -> None:
        self.__closed = True
        if gather:
            await asyncio_gather(*self.__tasks)

    async def __areceive(self, *args: Any, **kwargs: Any) -> Any:
        if self.__closed:
            # TODO raise an exception?
            return
        task_or_result = self._receive(*args, **kwargs)
        if isawaitable(task_or_result):
            result = await task_or_result
        else:
            result = task_or_result
        return result

    def __put_message(self, *args: Any, **kwargs: Any) -> Awaitable[Any]:

        async def process_mailbox() -> Any:
            # XXX deque is thread-safe, does it require a lock?
            args, kwargs = self.__mailbox.popleft()
            return await self.__areceive(*args, **kwargs)
            return await task

        full_msg = args, kwargs
        # XXX deque is thread-safe, does it require a lock?
        self.__mailbox.append(full_msg)
        task = self.__loop.create_task(process_mailbox())
        self.__tasks.append(task)
        task.add_done_callback(lambda t: self.__tasks.remove(t))
        return task
