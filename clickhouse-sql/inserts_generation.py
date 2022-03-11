import random


TIME_START = 1640995200
DAY_IN_MS = 86400
TIME_BUCKETS = 1000
POSSIBLE_LABEL = {
    'country': ['Portugal', 'Spain', 'France', 'Italy', 'Greece'],
    'client': ['a', 'b', 'c']
}
LABEL_PER_BUCKET_MIN = 3
LABEL_PER_BUCKET_MAX = 10
MODEL_SERVICE_PREFIX_NAME = 'modelservice'
MODEL_SERVICE_COUNT = 5
RULE_SERVICE_PREFIX_NAME = 'ruleservice'
RULE_SERVICE_COUNT = 5
RULES_PREFIX_NAME = 'rule'
RULES_COUNT = 15
INSERT_QUERY = "INSERT INTO monitoring VALUES ({}, '{}', '{}', array({}), array({}), array({}), array({}), array({}));"


def generate_insert_query(time_bucket, label):
    rule_service_count = generate_category_count(RULE_SERVICE_COUNT)
    rule_services = generate_category(RULE_SERVICE_PREFIX_NAME, rule_service_count)
    confusion_matrix = generate_confusion_matrix(rule_service_count)
    rules = generate_rules(rule_service_count)

    model_service_count = generate_category_count(MODEL_SERVICE_COUNT)
    model_services = generate_category(MODEL_SERVICE_PREFIX_NAME, model_service_count)
    distribution = generate_distribution(model_service_count)

    return INSERT_QUERY.format(time_bucket, label[0], label[1], rule_services, confusion_matrix, rules, model_services, distribution)

def generate_label():
    labels = POSSIBLE_LABEL.copy()
    labels[None] = None

    item = random.choice(list(labels.items()))

    if item[1] == None:
        return ('__global__', '__global__')

    label_value = random.choice(list(item[1]))
    return (item[0], label_value)

def generate_category_count(category_max):
    return random.choice(range(0, category_max))

def generate_category(name_prefix, category_count):
    services = "'{}0'".format(name_prefix)
    for i in range(1, category_count):
        services += ", '{}{}'".format(name_prefix, i)
    return services

def generate_confusion_matrix(category_count):
    tuple_template = 'tuple({}, {}, {}, {})'
    confusion_matrix = generate_random_confusion_matrix()
    for i in range(1, category_count):
        confusion_matrix += ', ' + generate_random_confusion_matrix()
    return confusion_matrix
    
def generate_random_confusion_matrix():
    tuple_template = 'tuple({}, {}, {}, {})'
    return tuple_template.format(random.randint(0, 300), random.randint(0, 300), random.randint(0, 300), random.randint(0, 300))

def generate_rules(category_count):
    if category_count == 0:
        return "[]"
    rules_count = generate_category_count(RULES_COUNT)
    rules = "[{}]".format(generate_category(RULES_PREFIX_NAME, rules_count))
    for i in range(1, category_count):
        rules_count = generate_category_count(RULES_COUNT)
        rules += ", [{}]".format(generate_category(RULES_PREFIX_NAME, rules_count))
    return rules

def generate_distribution(category_count):
    if category_count == 0:
        return "[]"
    distribution = random.randint(0, 1000)
    value = "[{}, {}]".format(distribution, 1000 - distribution)
    for i in range(1, category_count):
        distribution = random.randint(0, 1000)
        value += ", [{}, {}]".format(distribution, 1000 - distribution)
    return value

if __name__ == "__main__":

    for i in range(TIME_BUCKETS):
        time_bucket = TIME_START + DAY_IN_MS * i

        labels = {('__global__', '__global__')}
        for i in range(LABEL_PER_BUCKET_MIN, LABEL_PER_BUCKET_MAX):
            labels.add(generate_label())

        for label in labels:
            print(generate_insert_query(time_bucket, label))
