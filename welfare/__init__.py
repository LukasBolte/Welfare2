import random

from otree.api import *

doc = """
Introduction
"""


class C(BaseConstants):
    NAME_IN_URL = 'welfare'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    MIN_TIME = 15  # in minutes
    MAX_TIME = 25  # in minutes
    BONUS_PER_CORRECT_TASK_PART1 = cu(0.15)
    OUTSIDE_OPTION = cu(2.2)
    # MAX_BONUS = cu(4.5)


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass


##################################################################### PAGES ###########################################
class Welcome(Page):
    pass


class Consent(Page):
    pass



page_sequence = [
    Welcome,
    Consent
]
