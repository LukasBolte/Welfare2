import random
import json
import itertools

from otree.api import *

doc = """
Introduction
"""


class C(BaseConstants):
    NAME_IN_URL = 'welfare'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 2
    MIN_TIME = 15  # in minutes
    MAX_TIME = 25  # in minutes
    # MAX_BONUS = cu(4.5)
    PRE_VIDEO = 'welfare/Review-pre-vid.html'
    POST_VIDEO = 'welfare/Review-post-vid.html'
    DETAIL = 'welfare/Review-detail.html'
    WTP_VALUES = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]


class Subsession(BaseSubsession):
    pass


def creating_session(subsession: Subsession):
    if subsession.round_number == 1:
        switch_orders = itertools.cycle([True, False])
        for p in subsession.get_players():
            p.participant.switch_order = next(switch_orders)



class Group(BaseGroup):
    pass

# def make_field(case):
#     if case == 1:
#         label = '<strong>Which books do you prefer Alex to receive in this case?</strong>'
#         choices = [
#             [1, 'Original notes'],
#             [2, 'Fake notes'],
#             [3, 'I am indifferent']
#         ]
#     else:
#         label = '<strong>Which book and bonus do you prefer Alex to receive in this case?</strong>'
#         choices = [
#             [1, 'Original notes'],
#             [2, 'Fake notes + $1'],
#             [3, 'I am indifferent']
#         ]
#     return models.IntegerField(blank=True,
#                                choices=choices,
#                                widget=widgets.RadioSelectHorizontal,
#                                label=label
#                                )


def learn():
    return models.IntegerField(blank=True,
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
    confirm = models.IntegerField(
                                choices=[
                                  [1, 'Yes, the answers above reflect what I intended to answer'],
                                  [2, 'No, I want to give my answers again']
                              ],
                              widget=widgets.RadioSelect,
                              label='<b>Do the above answers reflect what you intended to answer or do you want to give'
                                    ' your answers again?</b>'
                              )
    

    ES_wtp = models.IntegerField(blank=True,
                                 widget=widgets.RadioSelectHorizontal,
                                 label='Which books do you prefer Alex to receive in this case?',
                                 choices=[  # Do we care about randomizing order of choices?
                                     [1, 'Original notes'],
                                     [2, 'Fake notes'],
                                     [3, 'I am indifferent']
                                 ])
    Trad_wtp = models.IntegerField(blank=True,
                                   widget=widgets.RadioSelectHorizontal,
                                   # label='<strong>Which books do you prefer Alex to receive in this case?</strong>',
                                   label='Which books do you prefer Alex to receive in this case?',
                                   choices=[  # Do we care about randomizing order of choices?
                                       [1, 'Original notes'],
                                       [2, 'Fake notes'],
                                       [3, 'I am indifferent']
                                   ])
    ES_learn = learn()
    Trad_learn = learn()
    ES_wtp2 = models.IntegerField(blank=True,
                                   widget=widgets.RadioSelectHorizontal,
                                   label='Which books do you prefer Alex to receive in this case?'
                                  )
    Trad_wtp2 = models.IntegerField(blank=True,
                                    widget=widgets.RadioSelectHorizontal,
                                    label='Which books do you prefer Alex to receive in this case?'
                                    )
    ES_learn2 = learn()
    Trad_learn2 = learn()
    ES_wtp3 = models.StringField()
    Trad_wtp3 = models.StringField()
    ES_learn3 = learn()
    Trad_learn3 = learn()

    ES_wtp3_bounds = models.StringField()

    Trad_wtp3_bounds = models.StringField()
    
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
                              label='<strong>What do your answers determine?</strong>')
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
    ES_learn_mistakes = models.IntegerField(blank=True, initial=0)
    Trad_learn_mistakes = models.IntegerField(blank=True, initial=0)
    ES_learn2_mistakes = models.IntegerField(blank=True, initial=0)
    Trad_learn2_mistakes = models.IntegerField(blank=True, initial=0)
    ES_learn3_mistakes = models.IntegerField(blank=True, initial=0)
    Trad_learn3_mistakes = models.IntegerField(blank=True, initial=0)
    review = models.BooleanField(blank=True,
                                 label='Do the statements above accurately reflect what you intended to answer?',
                                 choices=[
                                     [True, 'Yes'],
                                     [False, 'No, I want to change my answers']
                                 ])
###############################################  FUNCTIONS   ###########################################################


def get_wtp_bounds(player, wtp3): 
    if wtp3==None:
        return "WTP is None"
    cutoff = json.loads(wtp3)['cutoff']
    parts = cutoff.split(":")
    side = parts[0]
    row = int(parts[1])

    if side == "right":
        row = row-1
        side="left"

    WTP_VALUES = [0]+C.WTP_VALUES +[float('inf')]

    WTP_bound = (WTP_VALUES[row+1],WTP_VALUES[row+2])
    return WTP_bound, row+4



def ES_wtp2_choices(player):
    if player.ES_wtp == 1:
        choices = [[1, 'Original notes'],
                   [2, 'Fake notes + $1']]
    else:
        choices = [[1, 'Original notes + $1'],
                   [2, 'Fake notes']]
    # random.shuffle(choices)
    return choices

def Trad_wtp2_choices(player):
    if player.Trad_wtp == 1:
        choices = [[1, 'Original notes'],
                   [2, 'Fake notes + $1']]
    else:
        choices = [[1, 'Original notes + $1'],
                   [2, 'Fake notes']]
    return choices

def ES_wtp_error_message(player, value):
    if not player.session.config['development'] and value is None:
        return 'Please, answer the question.'

def Trad_wtp_error_message(player, value):
    if not player.session.config['development'] and value is None:
        return 'Please, answer the question.'

def ES_wtp2_error_message(player, value):
    if not player.session.config['development'] and value is None:
        return 'Please, answer the question.'

def Trad_wtp2_error_message(player, value):
    if not player.session.config['development'] and value is None:
        return 'Please, answer the question.'

######################################################  PAGES   ########################################################

class Welcome(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number==1


class Consent(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number==1


class Instructions(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number==1


class EconomicsFan(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number==1


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
        
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number==1

class PostCQs(Page):

    @staticmethod
    def vars_for_template(player):

        dollarValues = [1] +  C.WTP_VALUES
        return {
             'dollarValues':  json.dumps(dollarValues)
         }
    
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number==1


class Cases(Page):
    form_model = 'player'
    form_fields = ['ES_wtp', 'Trad_wtp', 'ES_learn', 'Trad_learn', 'ES_learn_mistakes', 'Trad_learn_mistakes']

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
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number==1 or (player.participant.confirm==player.round_number)


class Cases2(Page):
    form_model = 'player'

    @staticmethod
    def get_form_fields(player):
        ES_wtp = player.field_maybe_none('ES_wtp')
        Trad_wtp = player.field_maybe_none('Trad_wtp')
        if Trad_wtp == 3:
            return ['ES_wtp2', 'ES_learn2', 'ES_learn2_mistakes', 'Trad_learn2_mistakes']
        elif ES_wtp == 3:
            return ['Trad_wtp2', 'Trad_learn2', 'Trad_learn2_mistakes', 'ES_learn2_mistakes']
        else:
            return ['ES_wtp2', 'Trad_wtp2', 'ES_learn2', 'Trad_learn2', 'ES_learn2_mistakes', 'Trad_learn2_mistakes']

    @staticmethod
    def error_message(player, values):
        if not player.session.config['development']:
            solutions = dict(ES_learn2=2,
                             Trad_learn2=1
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

    @staticmethod
    def is_displayed(player: Player):
        ES_wtp = player.field_maybe_none('ES_wtp')
        Trad_wtp = player.field_maybe_none('Trad_wtp')
        return not (ES_wtp == 3 and Trad_wtp == 3) and \
            (player.round_number == 1 or (player.participant.confirm == player.round_number))
        # if indifferent in both skip this page

    @staticmethod
    def vars_for_template(player: Player):
        ES_wtp = player.field_maybe_none('ES_wtp')
        Trad_wtp = player.field_maybe_none('Trad_wtp')
        return dict(ES_wtp=ES_wtp,
                    Trad_wtp=Trad_wtp)

class Cases3Explain(Page):
    @staticmethod
    def is_displayed(player: Player):
        ES_wtp = player.field_maybe_none('ES_wtp')
        Trad_wtp = player.field_maybe_none('Trad_wtp')
        ES_wtp2 = player.field_maybe_none('ES_wtp2')
        Trad_wtp2 = player.field_maybe_none('Trad_wtp2')
        return ((ES_wtp == 1 and ES_wtp2 == 1) or (Trad_wtp == 1 and Trad_wtp2 == 1)) and \
            (player.round_number == 1 or (player.participant.confirm == player.round_number))
        #  the above says we only show this page for those who have always preferred Original in either case.


class Cases3(Page):
    form_model = 'player'
    form_fields = ['ES_wtp3', 'Trad_wtp3', 'ES_learn3', 'Trad_learn3', 'ES_learn3_mistakes', 'Trad_learn3_mistakes']

    @staticmethod
    def error_message(player, values):
        if not player.session.config['development']:
            solutions = dict(ES_learn3=2,
                             Trad_learn3=1
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

    @staticmethod
    def vars_for_template(player):
        ES_wtp = player.field_maybe_none('ES_wtp')
        Trad_wtp = player.field_maybe_none('Trad_wtp')
        ES_wtp2 = player.field_maybe_none('ES_wtp2')
        Trad_wtp2 = player.field_maybe_none('Trad_wtp2')

        player.participant.ES_strict = json.dumps(ES_wtp == 1 and ES_wtp2 == 1)
        player.participant.Trad_strict = json.dumps(Trad_wtp == 1 and Trad_wtp2 == 1)
        
        zeroes_list = [0] * len(C.WTP_VALUES)
        return {
             'WTP_VALUES':  json.dumps(C.WTP_VALUES),
             'WTP_VALUES_ZEROES':  json.dumps(zeroes_list)
         }
        

    @staticmethod
    def is_displayed(player: Player):
        ES_wtp = player.field_maybe_none('ES_wtp')
        Trad_wtp = player.field_maybe_none('Trad_wtp')
        ES_wtp2 = player.field_maybe_none('ES_wtp2')
        Trad_wtp2 = player.field_maybe_none('Trad_wtp2')
        return ((ES_wtp == 1 and ES_wtp2 == 1) or (Trad_wtp == 1 and Trad_wtp2 == 1)) and (player.round_number==1 or (player.participant.confirm==player.round_number))
        #  the above says we only show this page for those who have always preferred Original in either case.


class ReviewStatements(Page):
    form_model = 'player'
    form_fields = ['confirm']

    @staticmethod
    def vars_for_template(player):        
        if player.Trad_wtp==3:
            row = 1
            indifference = True
        else:
            indifference = False 

        if player.Trad_wtp==2: # Fake preferred to Original
            if player.Trad_wtp2==1: 
                row=1
            elif player.Trad_wtp2==2:
                row=0

        if player.Trad_wtp==1:
            if player.Trad_wtp2==1: 
                _, row = get_wtp_bounds(player, player.field_maybe_none('Trad_wtp3'))
            elif player.Trad_wtp2==2:
                row=2


        if player.ES_wtp==3:
            row2 = 1
            indifference2 = True
        else:
            indifference2 = False 


        if player.ES_wtp==2: # Fake preferred to Original
            if player.ES_wtp2==1: 
                row2=1
            elif player.ES_wtp2==2:
                row2=0

        if player.ES_wtp==1:
            if player.ES_wtp2==1: 
                _, row2 = get_wtp_bounds(player, player.field_maybe_none('ES_wtp3'))
            elif player.ES_wtp2==2:
                row2=2

        dollarValues = [1] + C.WTP_VALUES

        return {
             'dollarValues':  json.dumps(dollarValues),

             'row': json.dumps(row),
             'indifference': json.dumps(indifference),
             'row2': json.dumps(row2),
             'indifference2': json.dumps(indifference2)
         }

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number==1

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.participant.confirm = player.confirm


class PostMPL(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.participant.confirm==player.round_number


class Experience(Page):
    form_model = 'player'
    form_fields = ['experience', 'experienceWhy']

    @staticmethod
    def is_displayed(player: Player):
        return player.participant.confirm == player.round_number


class Arkansas(Page):
    form_model = 'player'
    form_fields = ['arkansas', 'arkansasWhy']
    
    @staticmethod
    def is_displayed(player: Player):
        return player.participant.confirm==player.round_number


class Warhol(Page):
    form_model = 'player'
    form_fields = ['warhol', 'warholWhy']

    @staticmethod
    def is_displayed(player: Player):
        return player.participant.confirm==player.round_number


class End(Page):
    form_model = 'player'
    form_fields = ['feedback', 'feedbackDifficulty', 'feedbackUnderstanding', 'feedbackSatisfied', 'feedbackPay']

    @staticmethod
    def is_displayed(player: Player):
        return player.participant.confirm==player.round_number

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.participant.finished = True


class Redirect(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.participant.confirm == player.round_number


page_sequence = [
    # Welcome,
    # Consent,
    # Instructions,
    # EconomicsFan,
    # CQ,
    PostCQs,
    Cases,
    Cases2,
    Cases3Explain,
    Cases3,
    ReviewStatements,
    PostMPL,
    Experience,
    Arkansas,
    Warhol,
    End,
    Redirect
]
