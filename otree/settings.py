from os import environ

SESSION_CONFIGS = [
    dict(
        name='welfare',
        app_sequence=['welfare'],
        num_demo_participants=1,
        development=False
    ),
    dict(
        name='welfare_dev',
        app_sequence=['welfare'],
        num_demo_participants=1,
        development=True
    ),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=3.00, doc=""
)

PARTICIPANT_FIELDS = ['finished', 'Trad_strict', 'ES_strict', 'switch_order', 'confirm', 'start_time', 'end_time',
                      'treatment', 'WTP_same', 'choices_orders']
SESSION_FIELDS = ['prolific_completion_url']

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '3832417730146'
