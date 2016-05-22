"""
Utilities for tests.py usage.

"""
from __future__ import unicode_literals


class UserRepresentation:
    "POSTMAN_SHOW_USER_AS = 'postman.module_for_tests.UserRepresentation'"
    def __init__(self, user):
        self.user = user

    def __str__(self):
        return user_representation(self.user)


def user_representation(user):
    "POSTMAN_SHOW_USER_AS = 'postman.module_for_tests.user_representation'"
    return 'nick_' + user.get_username()  # some user representation
