# SPDX-License-Identifier: X11
#
# Copyright (c) 2021, Tadeu Bastos.  All rights reserved.

from paca.actor import ActorRef

from uuid import UUID
from typing import Dict


class Registry:

    __id_to_actor: Dict[UUID, ActorRef]

    def __init__(self) -> None:
        self.__id_to_actor = dict()

    def register(self, actor_id: UUID, actor_ref: ActorRef) -> None:
        entry = self.__id_to_actor.get(actor_id)
        if entry is not None:
            raise ValueError('a registry entry already exists')
        self.__id_to_actor[actor_id] = actor_ref

    def unregister(self, actor_id: UUID) -> None:
        self.__id_to_actor.pop(actor_id)

    def __getitem__(self, actor_id: UUID) -> ActorRef:
        if not isinstance(actor_id, UUID):
            raise ValueError(
                'key must be of type {}'.format(UUID.__qualname__))
        return self.__id_to_actor[actor_id]
