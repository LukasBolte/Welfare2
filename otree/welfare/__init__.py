import random
import json

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
    PRE_VIDEO = 'welfare/Review-pre-vid.html'
    POST_VIDEO = 'welfare/Review-post-vid.html'
    DETAIL = 'welfare/Review-detail.html'


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


def make_field(case):
    if case == 1:
        label = '<strong>Which books do you prefer Alex to receive in this case?</strong>'
        choices = [
            [1, 'Original notes'],
            [2, 'Fake notes'],
            [3, 'I am indifferent']
        ]
    else:
        label = '<strong>Which book and bonus do you prefer Alex to receive in this case?</strong>'
        choices = [
            [1, 'Original notes'],
            [2, 'Fake notes + $1'],
            [3, 'I am indifferent']
        ]
    return models.IntegerField(blank=True,
                               choices=choices,
                               widget=widgets.RadioSelectHorizontal,
                               label=label
                               )


def learn():
    return models.IntegerField(
                               choices=[
                                   [1, 'Yes, they will learn'],
                                   [2, 'No, they will not learn'],
                               ],
                               widget=widgets.RadioSelectHorizontal,
                               label='In this case, will Alex ever learn whether they have the books with the '
                                     'original handwritten notes or the fake ones?'
                               )

def why():
    return models.LongStringField(blank=True,
                                  label="Why? Answer in approximately 1-2 sentences.")


class Player(BasePlayer):
    ES_wtp = make_field(1)
    Trad_wtp = make_field(1)
    ES_learn = learn()
    Trad_learn = learn()
    ES_wtp2 = make_field(2)
    Trad_wtp2 = make_field(2)
    ES_learn2 = learn()
    Trad_learn2 = learn()
    ES_wtp3 = models.StringField()
    Trad_wtp3 = models.StringField()
    ES_learn3 = learn()
    Trad_learn3 = learn()
    experience = models.BooleanField(blank=True,
                                     label="<strong>Would you go into the machine?</strong>",
                                     choices=[
                                         [True, 'Yes'],
                                         [False, 'No']
                                     ],
                                     )
    experienceWhy = why()
    arkansas = models.BooleanField(blank=True,
                                   label="<strong>Does the government raising taxes to provide financial relief make "
                                         "John better or worse off?</strong>",
                                   choices=[
                                       [True, 'Better Off'],
                                       [False, 'Worse Off']
                                   ],
                                   )
    arkansasWhy = why()
    warhol = models.BooleanField(blank=True,
                                 label="<strong> Someone got the original Andy Warhol drawing without knowing about it."
                                       " Is this person better off by getting the original one instead of a copy?"
                                       "</strong>",
                                 choices=[
                                     [True, 'Yes'],
                                     [False, 'No']
                                 ],
                                 )
    warholWhy = why()
    cq1 = models.IntegerField(blank=True,
                              choices=[
                                  [1, 'Two economics books, either the two with the original handwritten notes by the '
                                      'famous authors or the two with the fake ones'],
                                  [2, 'One book with original handwritten notes and one with fake ones'],
                                  [3, 'Nothing']
                              ],
                              widget=widgets.RadioSelect,
                              label='<strong>What will Alex receive?</strong>'
                              )
    cq2 = models.IntegerField(blank=True,
                              choices=[
                                  [1, 'Yes'],
                                  [2, 'No']
                              ],
                              widget=widgets.RadioSelect,
                              label='<strong>Does Alex love economics?</strong>'
                              )
    cq3 = models.IntegerField(blank=True,
                              choices=[
                                  [1, 'We will keep them for ourselves'],
                                  [2, 'We will return them to Professor Roth and Milgrom'],
                                  [3, 'We will destroy them']
                              ],
                              widget=widgets.RadioSelect,
                              label='<strong>What happens to the books we don’t give to Alex?'
                                    '</strong>'
                              )
    cq4 = models.IntegerField(blank=True,
                              choices=[
                                  [1, 'Yes'],
                                  [2, 'No']
                              ],
                              widget=widgets.RadioSelect,
                              label='<strong>Is it possible to say which book has a fake note?</strong>'
                              )
    cq5 = models.IntegerField(blank=True,
                              choices=[
                                  [1, 'Only which books Alex receives'],
                                  [2, 'Only Alex’s surprise bonus'],
                                  [3, 'They determine which books Alex receives and his surprise bonus']
                              ],
                              widget=widgets.RadioSelect,
                              label='<strong>What do your answers determine?</strong>'
                              )
    feedback = models.LongStringField(label='<strong>Feedback:</strong>', blank=True)
    feedbackDifficulty = models.IntegerField(label="How difficult were the instructions? Please answer on a scale of 1 "
                                                   "to 10 with 10 being the most difficult",
                                             blank=True,
                                             choices=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                                             widget=widgets.RadioSelectHorizontal)
    feedbackUnderstanding = models.IntegerField(label="How well did you understand what you were asked to do?"
                                                      " Please answer on a scale of 1 to 10 with 10 being the case when"
                                                      " you understood perfectly",
                                                blank=True,
                                                choices=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                                                widget=widgets.RadioSelectHorizontal)
    feedbackSatisfied = models.IntegerField(label="How satisfied are you with this study overall?"
                                                  " Please answer on a scale of 1 to 10 with 10 being the most "
                                                  "satisfied",
                                            blank=True,
                                            choices=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                                            widget=widgets.RadioSelectHorizontal)
    feedbackPay = models.IntegerField(label="How appropriate do you think the payment for this study is relative to "
                                            "other ones on Prolific? Please answer on a scale of 1 to 10 with 10 being "
                                            "the most appropriate",
                                      blank=True,
                                      choices=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                                      widget=widgets.RadioSelectHorizontal)
    for j in range(1, 6):
        locals()['cq' + str(j) + '_mistakes'] = models.IntegerField(blank=True, initial=0)
    del j
    ES_learn = models.IntegerField(blank=True, initial=0)
    Trad_learn = models.IntegerField(blank=True, initial=0)

###############################################  FUNCTIONS   ###########################################################


######################################################  PAGES   ########################################################
class Welcome(Page):
    pass


class Consent(Page):
    pass


class Instructions(Page):
    pass


class EconomicsFan(Page):
    pass


class CQ(Page):
    form_model = 'player'
    form_fields = ['cq1', 'cq2', 'cq3', 'cq4', 'cq5']

    @staticmethod
    def error_message(player, values):
        if not player.session.config['development']:
            solutions = dict(cq1=1,
                             cq2=1,
                             cq3=2,
                             cq4=2,
                             cq5=3
                             )
            error_messages = dict()
            for field_name in solutions:
                if values[field_name] is None:
                    error_messages[field_name] = 'Please, answer the question'
                elif values[field_name] != solutions[field_name]:
                    error_messages[field_name] = 'Please, correct your answer!'
                    name = 'player.' + str(field_name) + '_mistakes'
                    exec("%s += 1" % name)
            return error_messages


class PostCQs(Page):
    pass


class Cases(Page):
    form_model = 'player'
    form_fields = ['ES_wtp', 'Trad_wtp', 'ES_learn', 'Trad_learn']

    @staticmethod
    def error_message(player, values):
        if not player.session.config['development']:
            solutions = dict(ES_learn=2,
                             Trad_learn=1
                             )
            error_messages = dict()
            for field_name in solutions:
                if values[field_name] is None:
                    error_messages[field_name] = 'Please, answer the question'
                elif values[field_name] != solutions[field_name]:
                    error_messages[field_name] = 'Please, correct your answer!'
                    name = 'player.' + str(field_name) + '_mistakes'
                    exec("%s += 1" % name)
            return error_messages

class Cases2(Page):
    form_model = 'player'
    form_fields = ['ES_wtp2', 'Trad_wtp2', 'ES_learn2', 'Trad_learn2']


class Cases3Explain(Page):
    pass


class Cases3(Page):
    form_model = 'player'
    form_fields = ['ES_wtp3', 'Trad_wtp3', 'ES_learn3', 'Trad_learn3']

    @staticmethod
    def vars_for_template(player):
        player.participant.ES_strict = json.dumps(True)
        player.participant.Trad_strict = json.dumps(True)
        pass 


class PostMPL(Page):
    pass

class Experience(Page):
    form_model = 'player'
    form_fields = ['experience', 'experienceWhy']


class Arkansas(Page):
    form_model = 'player'
    form_fields = ['arkansas', 'arkansasWhy']


class Warhol(Page):
    form_model = 'player'
    form_fields = ['warhol', 'warholWhy']


class End(Page):
    form_model = 'player'
    form_fields = ['feedback', 'feedbackDifficulty', 'feedbackUnderstanding', 'feedbackSatisfied', 'feedbackPay']

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.participant.finished = True


class Redirect(Page):
    pass


page_sequence = [
    Welcome,
    Consent,
    Instructions,
    EconomicsFan,
    CQ,
    PostCQs,
    Cases,
    Cases2,
    Cases3Explain,
    Cases3,
    PostMPL,
    Experience,
    Arkansas,
    Warhol,
    End,
    Redirect
]
