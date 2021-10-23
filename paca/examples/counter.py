# SPDX-License-Identifier: X11
#
# Copyright (c) 2021, Tadeu Bastos.  All rights reserved.


from paca.actor import Actor

from asyncio import (
    gather as asyncio_gather, get_event_loop, sleep as asyncio_sleep)
from multimethod import multimethod


class Counter(Actor):

    class Message:

        class Increment:
            pass

        class Get:
            pass

    def __init__(self, counter: int = 0) -> None:
        self.__counter = counter

    @property
    def counter(self):
        return self.__counter

    @multimethod  # type: ignore[no-redef]
    async def _receive(self, message: Message.Increment) -> None:  # noqa: F811
        self.__counter += 1

    @multimethod  # type: ignore[no-redef]
    async def _receive(self, message: Message.Get) -> int:  # noqa: F811
        return self.__counter


class Manager(Actor):

    class Message:

        class Start:
            pass

        class Stop:
            pass

    def __init__(self) -> None:
        self.__running = True

    @multimethod  # type: ignore[no-redef]
    async def _receive(self, message: Message.Start) -> None:  # noqa: F811
        async with Counter().context as counter:

            async def incrementer():
                while self.__running:
                    counter < Counter.Message.Increment()
                    await asyncio_sleep(0.1)

            async def displayer():
                while self.__running:
                    await asyncio_sleep(1)
                    value = counter <= Counter.Message.Get()
                    print('value: {}'.format(await value))

            async def shutdowner():
                await asyncio_sleep(10)
                self.ref < Manager.Message.Stop()

            await asyncio_gather(incrementer(), displayer(), shutdowner())

    @multimethod  # type: ignore[no-redef]
    async def _receive(self, message: Message.Stop) -> None:  # noqa: F811
        self.__running = False
        print('shutting down')


async def amain():
    async with Manager().context as manager:
        start = manager <= Manager.Message.Start()
        await start


if __name__ == '__main__':
    loop = get_event_loop()
    try:
        loop.run_until_complete(amain())
    finally:
        loop.close()
