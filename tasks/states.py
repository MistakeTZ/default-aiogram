"""
This module defines the state groups for user and admin interactions in the task management system.
"""

from maxapi.context import State, StatesGroup


class UserState(StatesGroup):
    default = State()


class AdminState(StatesGroup):
    mailing = State()
