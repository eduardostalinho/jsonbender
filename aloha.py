from collections import defaultdict
from datetime import datetime

from jsonbender import bend, K, S, F, Forall


def get_promise_date_time(source):
    return (datetime.today()
            .replace(hour=23, minute=59)
            .strftime('%Y-%m-%dT%H:%M:%S'))


def split_string(the_s, sep=None, start=None, stop=None, step=None):
    return the_s.split(sep)[start:stop:step]


def sort_items(items):
    return sorted(items, key=lambda i: i['order_in_order'])


def flat2nested(flat_items):
    items = {item['order_in_order']: item.copy() for item in flat_items}

    for item in items.itervalues():
        #  TODO: this creates a O(n^2) behaviour, but unless there are some
        # strong guarantees by the API (such as parents always coming before
        # children), there's not much we can do
        children = filter(lambda i: i['parent_order_in_order'] ==
                                    item['order_in_order'],
                          items.itervalues())
        item['children'] = sort_items(children)

    top_nodes = filter(lambda i: i['parent_order_in_order'] is None,
                       items.itervalues())
    return sort_items(top_nodes)


get_aloha_id = F(lambda pos_reference: int(pos_reference.split('@')[-1]))


def set_item_line_numbers(items):
    for index, item in enumerate(items):
        item['ItemLineNumber'] = index + 1


def set_sequence_numbers(items):
    sequence_numbers = defaultdict(int)
    for item in items:
        for modifier in item['Modifiers']:
            modifier_group = modifier['ItemOptionGroupId']
            modifier['SequenceNumber'] = sequence_numbers[modifier_group]
            sequence_numbers[modifier_group] += 1


# TODO: This is not very pretty, can be improved
def nested2aloha(nested_items):
    modifier_mapping = {
        'Action': K(0),
        'DefaultAction': K(0),
        'FreeQuantity': K(0),  # TODO: Should this be dynamic?
        'IsOnEntireItem': K(None),
        'IsOnSection1': K(None),
        'IsOnSection2': K(None),
        'IsOnSection3': K(None),
        'IsOnSection4': K(None),
        'ItemLineNumber': K(0),  # TODO: Is this always 0 for modifiers?
        # TODO: Why is  this a string?
        'Quantity': S('children', 0, 'quantity') >> F(float) >> F(int),
        # TODO: What does this mean and how to get it?
        'ParentSequenceNumber': K(0),
        'SalesItemOptionId': S('children', 0, 'pos_reference') >> get_aloha_id,
        'ItemOptionGroupId': S('pos_reference') >> get_aloha_id,
        'Modifiers': K(None),  # TODO: always?
    }
    mapping = {
        'MenuItemId': S('pos_reference') >> get_aloha_id,
        # TODO: there must only be one child of a MenuItem; is it true?
        'SalesItemId': S('children', 0, 'pos_reference') >> get_aloha_id,
        'Modifiers': Forall(S('children', 0, 'children'),
                            lambda i: bend(modifier_mapping, i)),
    }

    items = map(lambda i: bend(mapping, i), nested_items)
    set_item_line_numbers(items)
    set_sequence_numbers(items)

    return items


# TODO: How to eliminate the "data, 0' selector preffix?
# - Create some sort of namespacing
# - Pass data[0] to bend() (btw what's the meaning of a list of data?)
ALOHA_PUT_MAPPING = {
    'siteId': K(1),  # TODO: Is the 's' really lowercase or just a typo?
    'PromiseDateTime': F(get_promise_date_time),
    'OrderMode': K(1),
    'PaymentMode': K(1),
    # TODO: Make a string interpolation bender
    'SpecialInstructions': (K('Id: ') + (S('data', 0, 'id') >> F(str)) +
                            K(' CPF:') + S('data', 0, 'customer', 'document') +
                            K(' Pgto: Credito Online - ') + S('data', 0,
                                                              'payments', 0,
                                                              'card',
                                                              'card_brand',
                                                              'name')),
    'Customer': {
        'Email': K('taliberti@onyo.com'),  # TODO: Missing from input
        # TODO: this can probably be improved
        'FirstName': (S('data', 0, 'customer', 'name') >>
                      F(split_string, stop=-1) >>
                      F(''.join)),
        'LastName': (S('data', 0, 'customer', 'name') >>
                     F(split_string, start=1) >>
                     F(''.join)),
    },
    'LineItems': S('data', 0, 'items') >> F(flat2nested) >> F(nested2aloha),
}


def aloha_put(in_):
    return bend(ALOHA_PUT_MAPPING, in_)

