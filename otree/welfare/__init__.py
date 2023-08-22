import random
import json
import itertools
import time
from otree.api import *

doc = """
Introduction
"""


class C(BaseConstants):
    NAME_IN_URL = 'welfare'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 2
    MIN_TIME = 10  # in minutes
    MAX_TIME = 20  # in minutes
    # MAX_BONUS = cu(4.5)
    PRE_VIDEO = 'welfare/Review-pre-vid.html'
    POST_VIDEO = 'welfare/Review-post-vid.html'
    DETAIL = 'welfare/Review-detail.html'
    BONUS = 'welfare/Review-bonus.html'
    MPL = 'welfare/Review-MPL.html'
    WTP_VALUES = [2, 3, 5, 7, 10, 15, 25, 45, 70, 100, 140, 200]
    MS = 75


class Subsession(BaseSubsession):
    pass


def creating_session(subsession: Subsession):
    if subsession.round_number == 1:
        switcheroo = [True, False]
        treatments_shuffled = ['low', 'middle', 'high']
        choices_orders = [1, 2, 3, 4, 5, 6]
        arrays = [switcheroo,treatments_shuffled,choices_orders]
        treatments = list(itertools.product(*arrays))
        random.shuffle(treatments)
        treatments = itertools.cycle(treatments)
        for p in subsession.get_players():
            el = next(treatments)
            
            p.participant.switch_order = el[0]
            p.participant.treatment = el[1]
            p.participant.choices_orders = el[2]
            print(f"participant's treatmentassignments: \n choice_orders: {p.participant.choices_orders} \n treatment: {p.participant.treatment} \n switch_order: {p.participant.switch_order}")
            


class Group(BaseGroup):
    pass


def learn():
    return models.IntegerField(blank=True,
                               choices=[
                                   [1, 'Yes, he will learn'],
                                   [2, 'No, he will not learn'],
                               ],
                               widget=widgets.RadioSelectHorizontal,
                               label='In this case, will Alex ever learn whether he has the books with the '
                                     'original handwritten notes or the fake ones?'
                               )


def why():
    return models.LongStringField(blank=True,
                                  label="Why? Answer in approximately 1-2 sentences.")


class Player(BasePlayer):
    browser = models.StringField()
    confirm = models.IntegerField(blank=True,
                                  choices=[
                                      [1, 'Yes, the answers above reflect what I intended to answer'],
                                      [2, 'No, I want to give my answers again']
                                  ],
                                  widget=widgets.RadioSelect,
                                  label='<b>Do the above answers reflect what you intended to answer, or do you want to give your answers again?</b>'
                                  )
    ES_wtp = models.IntegerField(blank=True,
                                 widget=widgets.RadioSelectHorizontal,
                                 label='Which books do you prefer Alex to receive in this case?',
                                 )
    Trad_wtp = models.IntegerField(blank=True,
                                   widget=widgets.RadioSelectHorizontal,
                                   # label='<strong>Which books do you prefer Alex to receive in this case?</strong>',
                                   label='Which books do you prefer Alex to receive in this case?',
                                   )
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

    MPLWhy = models.LongStringField(blank=True)

    # ES_wtp3_bounds = models.StringField()
    # Trad_wtp3_bounds = models.StringField()

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
                                       [True, 'Better off'],
                                       [False, 'Worse off']
                                   ],
                                   )
    arkansasWhy = why()
    warhol = models.BooleanField(blank=True,
                                 label="<strong>Is this person better off by getting the original one instead of a "
                                       "copy?</strong>",
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
                                  [2, 'We will return them to Professors Milgrom and Roth'],
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
    cq6_treatments = models.IntegerField(blank=True,
                                         choices=[
                                             [1, 'The ones with the original notes'],
                                             [2, 'The ones with the fake notes']
                                         ],
                                         widget=widgets.RadioSelect,
                                         label='<strong>If we do not tell Alex which books he got, which ones should he'
                                               ' believe he is more likely to have according to the instructions we '
                                               'gave him?</strong>')
    cq6_ambiguous = models.IntegerField(blank=True,
                                        choices=[
                                            [1, 'Yes'],
                                            [2, 'No']
                                        ],
                                        widget=widgets.RadioSelect,
                                        label='<strong>If we do not tell Alex which books he got, does he know whether '
                                              'he got the ones with the original notes or those with the fake ones?'
                                              '</strong>')
    feedback = models.LongStringField(label='<strong>Feedback:</strong>', blank=True)
    feedbackDifficulty = models.IntegerField(label="How clear were the instructions? Please answer on a scale of 1 "
                                                   "to 10, with 10 being the clearest.",
                                             blank=True,
                                             choices=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                                             widget=widgets.RadioSelectHorizontal)
    feedbackUnderstanding = models.IntegerField(label="How well did you understand what you were asked to do?"
                                                      " Please answer on a scale of 1 to 10, with 10 being the case when"
                                                      " you understood perfectly.",
                                                blank=True,
                                                choices=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                                                widget=widgets.RadioSelectHorizontal)
    feedbackSatisfied = models.IntegerField(label="How satisfied are you with this study overall?"
                                                  " Please answer on a scale of 1 to 10, with 10 being the most "
                                                  "satisfied.",
                                            blank=True,
                                            choices=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                                            widget=widgets.RadioSelectHorizontal)
    feedbackPay = models.IntegerField(label="How appropriate do you think the payment for this study is relative to "
                                            "other ones on Prolific? Please answer on a scale of 1 to 10, with 10 being "
                                            "the most appropriate.",
                                      blank=True,
                                      choices=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                                      widget=widgets.RadioSelectHorizontal)
    for j in range(1, 6):
        locals()['cq' + str(j) + '_mistakes'] = models.IntegerField(blank=True, initial=0)
    del j
    cq6_ambiguous_mistakes = models.IntegerField(blank=True, initial=0)
    cq6_treatments_mistakes = models.IntegerField(blank=True, initial=0)
    ES_learn_mistakes = models.IntegerField(blank=True, initial=0)
    Trad_learn_mistakes = models.IntegerField(blank=True, initial=0)
    ES_learn2_mistakes = models.IntegerField(blank=True, initial=0)
    Trad_learn2_mistakes = models.IntegerField(blank=True, initial=0)
    ES_learn3_mistakes = models.IntegerField(blank=True, initial=0)
    Trad_learn3_mistakes = models.IntegerField(blank=True, initial=0)

    for el in ['PostCQs', 'Cases', 'Cases2', 'Cases3Explain', 'Cases3', 'ReviewStatements', 'PostMPL']:
        locals()['timeSubmitted_' + el] = models.FloatField()
    del el


###############################################  FUNCTIONS   ###########################################################
def ES_wtp_choices(player):
    choices_orders = player.participant.choices_orders
    if choices_orders == 1:
        choices = [
            [1, 'Original notes'],
            [2, 'Fake notes'],
            [3, 'I am indifferent']]
    elif choices_orders == 2:
        choices = [
            [2, 'Fake notes'],
            [1, 'Original notes'],
            [3, 'I am indifferent']]
    elif choices_orders == 3:
        choices = [
            [1, 'Original notes'],
            [3, 'I am indifferent'],
            [2, 'Fake notes']]
    if choices_orders == 4:
        choices = [
            [2, 'Fake notes'],
            [3, 'I am indifferent'],
            [1, 'Original notes']]
    elif choices_orders == 5:
        choices = [
            [3, 'I am indifferent'],
            [2, 'Fake notes'],
            [1, 'Original notes']]
    elif choices_orders == 6:
        choices = [
            [3, 'I am indifferent'],
            [1, 'Original notes'],
            [2, 'Fake notes']]
    return choices


def Trad_wtp_choices(player):
    choices_orders = player.participant.choices_orders
    if choices_orders == 1:
        choices = [
            [1, 'Original notes'],
            [2, 'Fake notes'],
            [3, 'I am indifferent']]
    elif choices_orders == 2:
        choices = [
            [2, 'Fake notes'],
            [1, 'Original notes'],
            [3, 'I am indifferent']]
    elif choices_orders == 3:
        choices = [
            [1, 'Original notes'],
            [3, 'I am indifferent'],
            [2, 'Fake notes']]
    if choices_orders == 4:
        choices = [
            [2, 'Fake notes'],
            [3, 'I am indifferent'],
            [1, 'Original notes']]
    elif choices_orders == 5:
        choices = [
            [3, 'I am indifferent'],
            [2, 'Fake notes'],
            [1, 'Original notes']]
    elif choices_orders == 6:
        choices = [
            [3, 'I am indifferent'],
            [1, 'Original notes'],
            [2, 'Fake notes']]
    return choices


def get_wtp_bounds(player, wtp3):
    if wtp3 is None:
        return "WTP is None"
    cutoff = json.loads(wtp3)['cutoff']
    parts = cutoff.split(":")
    side = parts[0]
    row = int(parts[1])

    print(player.participant.choices_orders, 'myPrint')
    if not player.participant.choices_orders in [1, 3, 6]:
        side = {"right": "left", "left": "right"}[side]
    if side == "right":
        row = row - 1
        side = "left"

    WTP_VALUES = [0] + C.WTP_VALUES + [float('inf')]

    WTP_bound = (WTP_VALUES[row + 1], WTP_VALUES[row + 2])
    return WTP_bound, row + 4


def ES_wtp2_choices(player):
    if player.ES_wtp == 1:
        og = 'Original notes'
        fake = 'Fake notes + $1'
        # choices = [[1, 'Original notes'],
        #            [2, 'Fake notes + $1']]
    else:
        og = 'Original notes + $1'
        fake = 'Fake notes'
        # choices = [[1, 'Original notes + $1'],
        #            [2, 'Fake notes']]
    choices_orders = player.participant.choices_orders
    if choices_orders in [1, 3, 6]:
        choices = [
            [1, og],
            [2, fake]]
    else:
        choices = [
            [2, fake],
            [1, og]]
    return choices


def Trad_wtp2_choices(player):
    if player.Trad_wtp == 1:
        og = 'Original notes'
        fake = 'Fake notes + $1'
        # choices = [[1, 'Original notes'],
        #            [2, 'Fake notes + $1']]
    else:
        og = 'Original notes + $1'
        fake = 'Fake notes'
        # choices = [[1, 'Original notes + $1'],
        #            [2, 'Fake notes']]
    choices_orders = player.participant.choices_orders
    if choices_orders in [1, 3, 6]:
        choices = [
            [1, og],
            [2, fake]]
    else:
        choices = [
            [2, fake],
            [1, og]]
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


def confirm_error_message(player, value):
    if not player.session.config['development'] and value is None:
        value = 2
        return 'Please, answer the question.'


def MPLWhy_error_message(player, value):
    if not player.session.config['development'] and value is None:
        value = 'blank'
        return 'Please, answer the question.'


######################################################  PAGES   ########################################################


class Welcome(Page):
    form_model = 'player'
    form_fields = ['browser']

    @staticmethod
    def vars_for_template(player):
        player.participant.start_time = time.time()
        pass

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1


class Consent(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1


class Instructions(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1


class EconomicsFan(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1


class YourTask(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return dict(one_minus_MS=100 - C.MS)

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1


class CQ(Page):
    form_model = 'player'

    @staticmethod
    def get_form_fields(player):
        my_fields = ['cq1', 'cq2', 'cq3', 'cq4', 'cq5']
        if player.participant.treatment == 'middle':
            return my_fields + ['cq6_ambiguous']
        else:
            return my_fields + ['cq6_treatments']

    @staticmethod
    def vars_for_template(player: Player):
        return dict(one_minus_MS=100 - C.MS)

    @staticmethod
    def error_message(player, values):
        if not player.session.config['development']:
            solutions = dict(cq1=1,
                             cq2=1,
                             cq3=2,
                             cq4=2,
                             cq5=3
                             )
            if player.participant.treatment == 'middle':
                solutions['cq6_ambiguous'] = 2
            elif player.participant.treatment == 'high':
                solutions['cq6_treatments'] = 1
            else:
                solutions['cq6_treatments'] = 2
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
        return player.round_number == 1


class PostCQs(Page):
    @staticmethod
    def vars_for_template(player):
        dollarValues = [1] + C.WTP_VALUES
        choices_orders = player.participant.choices_orders
        original_first = choices_orders in [1, 3, 6]
        return {
            'dollarValues': json.dumps(dollarValues),
            'original_first': original_first
        }

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.timeSubmitted_PostCQs = time.time()

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1


class Cases(Page):
    form_model = 'player'
    form_fields = ['ES_wtp', 'Trad_wtp', 'ES_learn', 'Trad_learn', 'ES_learn_mistakes', 'Trad_learn_mistakes']

    @staticmethod
    def vars_for_template(player: Player):
        return dict(one_minus_MS=100 - C.MS)

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
    def before_next_page(player, timeout_happened):
        player.timeSubmitted_Cases = time.time()

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1 or (player.participant.confirm == player.round_number)


class Cases2(Page):
    form_model = 'player'

    @staticmethod
    def get_form_fields(player):
        ES_wtp = player.field_maybe_none('ES_wtp')
        Trad_wtp = player.field_maybe_none('Trad_wtp')
        my_fields = ['ES_learn2_mistakes', 'Trad_learn2_mistakes']
        if Trad_wtp == 3:
            return my_fields + ['ES_wtp2', 'ES_learn2']
        elif ES_wtp == 3:
            return my_fields + ['Trad_wtp2', 'Trad_learn2']
        else:
            return my_fields + ['ES_wtp2', 'Trad_wtp2', 'ES_learn2', 'Trad_learn2']

    @staticmethod
    def error_message(player, values):
        if not player.session.config['development']:
            solutions = dict(ES_learn2=2,
                             Trad_learn2=1
                             )
            error_messages = dict()
            for field_name in solutions:
                if field_name in values.keys():
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
                    Trad_wtp=Trad_wtp,
                    one_minus_MS=100 - C.MS)

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.timeSubmitted_Cases2 = time.time()


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

    @staticmethod
    def vars_for_template(player):
        choices_orders = player.participant.choices_orders
        original_first = choices_orders in [1, 3, 6]
        
        return {
            'original_first': original_first
        }
        
    @staticmethod
    def before_next_page(player, timeout_happened):
        player.timeSubmitted_Cases3Explain = time.time()


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
                if (field_name == 'ES_learn3' and json.loads(player.participant.ES_strict)) or (
                        field_name == 'Trad_learn3' and json.loads(player.participant.Trad_strict)):
                    if values[field_name] is None:
                        error_messages[field_name] = 'Please, answer the question'
                    elif values[field_name] != solutions[field_name]:
                        error_messages[field_name] = 'Please, correct your answer!'
                        name = 'player.' + str(field_name) + '_mistakes'
                        exec("%s += 1" % name)
            print(error_messages)
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


        choices_orders = player.participant.choices_orders
        original_first = choices_orders in [1, 3, 6]
      
        leftHeader="Original notes and..."
        rightHeader="Fake notes and..."

        if original_first:
            return {
                'WTP_VALUES': json.dumps(C.WTP_VALUES),
                'WTP_VALUES_ZEROES': json.dumps(zeroes_list),
                'one_minus_MS': 100 - C.MS,
                'leftHeader': leftHeader,
                'rightHeader': rightHeader,
                'original_first': original_first,
                'color_switched': json.dumps(False)
            }
        else:
            return {
                'WTP_VALUES': json.dumps(zeroes_list),
                'WTP_VALUES_ZEROES': json.dumps(C.WTP_VALUES),
                'one_minus_MS': 100 - C.MS,
                'leftHeader': rightHeader,
                'rightHeader': leftHeader,
                'original_first': original_first,
                'color_switched': json.dumps(True)
            }

    @staticmethod
    def is_displayed(player: Player):
        ES_wtp = player.field_maybe_none('ES_wtp')
        Trad_wtp = player.field_maybe_none('Trad_wtp')
        ES_wtp2 = player.field_maybe_none('ES_wtp2')
        Trad_wtp2 = player.field_maybe_none('Trad_wtp2')
        return ((ES_wtp == 1 and ES_wtp2 == 1) or (Trad_wtp == 1 and Trad_wtp2 == 1)) and \
            (player.round_number == 1 or (player.participant.confirm == player.round_number))
        #  the above says we only show this page for those who have always preferred Original in either case.

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.timeSubmitted_Cases3 = time.time()


class ReviewStatements(Page):
    form_model = 'player'
    form_fields = ['confirm']

    @staticmethod
    def vars_for_template(player):
        if player.Trad_wtp == 3:
            row = 1
            indifference = True
        else:
            indifference = False

        if player.Trad_wtp == 2:  # Fake preferred to Original
            if player.Trad_wtp2 == 1:
                row = 1
            elif player.Trad_wtp2 == 2:
                row = 0

        if player.Trad_wtp == 1:
            if player.Trad_wtp2 == 1:
                _, row = get_wtp_bounds(player, player.field_maybe_none('Trad_wtp3'))
            elif player.Trad_wtp2 == 2:
                row = 2

        if player.ES_wtp == 3:
            row2 = 1
            indifference2 = True
        else:
            indifference2 = False

        if player.ES_wtp == 2:  # Fake preferred to Original
            if player.ES_wtp2 == 1:
                row2 = 1
            elif player.ES_wtp2 == 2:
                row2 = 0

        if player.ES_wtp == 1:
            if player.ES_wtp2 == 1:
                _, row2 = get_wtp_bounds(player, player.field_maybe_none('ES_wtp3'))
            elif player.ES_wtp2 == 2:
                row2 = 2

        dollarValues = [1] + C.WTP_VALUES

        player.participant.WTP_same = ((row == row2) and (indifference == indifference2))
        
        choices_orders = player.participant.choices_orders
        original_first = choices_orders in [1, 3, 6]

        return {
            'original_first': original_first,
            'dollarValues': json.dumps(dollarValues),

            'row': json.dumps(row),
            'indifference': json.dumps(indifference),
            'row2': json.dumps(row2),
            'indifference2': json.dumps(indifference2)
        }

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.participant.confirm = player.confirm
        player.timeSubmitted_ReviewStatements = time.time()


class PostMPL(Page):
    form_model = 'player'
    form_fields = ['MPLWhy']

    @staticmethod
    def error_message(player, values):
        if not player.session.config['development']:

            error_messages = {}
            if values['MPLWhy'] == '':
                error_messages['MPLWhy'] = 'Please, answer the question.'

            return error_messages

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 2

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.timeSubmitted_PostMPL = time.time()


class Experience(Page):
    form_model = 'player'
    form_fields = ['experience', 'experienceWhy']

    @staticmethod
    def error_message(player, values):
        if not player.session.config['development']:

            error_messages = {}
            if values['experience'] is None:
                error_messages['experience'] = 'Please, answer the question.'
            if values['experienceWhy'] == '':
                error_messages['experienceWhy'] = 'Please, answer the question.'

            return error_messages

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 2


class Arkansas(Page):
    form_model = 'player'
    form_fields = ['arkansas', 'arkansasWhy']

    @staticmethod
    def error_message(player, values):
        if not player.session.config['development']:

            error_messages = {}
            if values['arkansas'] is None:
                error_messages['arkansas'] = 'Please, answer the question.'
            if values['arkansasWhy'] == '':
                error_messages['arkansasWhy'] = 'Please, answer the question.'

            return error_messages

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 2


class Warhol(Page):
    form_model = 'player'
    form_fields = ['warhol', 'warholWhy']

    @staticmethod
    def error_message(player, values):
        if not player.session.config['development']:

            error_messages = {}
            if values['warhol'] is None:
                error_messages['warhol'] = 'Please, answer the question.'
            if values['warholWhy'] == '':
                error_messages['warholWhy'] = 'Please, answer the question.'

            return error_messages

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 2


class End(Page):
    form_model = 'player'
    form_fields = ['feedback', 'feedbackDifficulty', 'feedbackUnderstanding', 'feedbackSatisfied', 'feedbackPay']

    @staticmethod
    def error_message(player, values):
        if not player.session.config['development']:
            error_messages = dict()
            for field_name in ['feedback', 'feedbackDifficulty', 'feedbackUnderstanding', 'feedbackSatisfied',
                               'feedbackPay']:
                if values[field_name] is None:
                    error_messages[field_name] = 'Please, answer the question'
            return error_messages

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 2

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.participant.end_time = time.time()
        player.participant.finished = True


class Finished(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 2


class Redirect(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 2


page_sequence = [
    Welcome,
    Consent,
    Instructions,
    EconomicsFan,
    YourTask,
    CQ,
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
    # Demographics,
    End,
    # Redirect,
    Finished
]
