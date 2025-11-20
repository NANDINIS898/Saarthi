import random

def get_credit_score(name):
    random.seed(hash(name))
    return random.randint(600, 850)
