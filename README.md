About
---

JSONBender is an embedded Python [DSL](https://en.wikipedia.org/wiki/Domain-specific_language) for transforming dicts.
It's name is inspired by Nickelodeon's cartoon series [Avatar: The Last Airbender](https://en.wikipedia.org/wiki/Avatar:_The_Last_Airbender).

![aang](http://cdn-static.denofgeek.com/sites/denofgeek/files/9/21//the-last-airbender-aang-the-avatar.jpg)


Installing
---

```bash
git clone git@github.com:Onyo/jsonbender.git
python setup.py install
```


Usage
---

JSONBender works by calling the `bend()` function with a mapping and the source `dict` as arguments. It raises a `BendingException` if anyting bad happens during the transformation fase.

The mapping itself is a dict whose values are benders, i.e. objects that represent the transformations to be done to the source dict. Ex:

```python
import json

from jsonbender import bend, K, S


MAPPING = {
    'fullName': S('customer', 'first_name') + K(' ') + S('customer', 'last_name'),
    'city': S('address', 'city'),
}

source = {
    'customer': {
        'first_name': 'Inigo',
        'last_name': 'Montoya',
        'Age': 24,
    },
    'address': {
        'city': 'Sicily',
        'country': 'Florin',
    },
}

result = bend(MAPPING, source)
print(json.dumps(result))
```
```json
{"city": "Sicily", "fullName": "Inigo Montoya"}
```

###Benders

####K

`K()` is a selector for constant values: It takes any value as a parameter and always returns that value regardless of the source dict.


####S

`S()` is a selector for accessing keys and indices: It takes a variable number of keys / indices and returns the corresponding value on the source dict:

```python
MAPPING = {'val': S('a', 'deeply', 'nested', 0, 'value')}
ret = bend(MAPPING, {'a': {'deeply': {'nested': [{'value': 42}]}}})
assert ret == {'val': 42}
```

####F
`F()` takes a function and optional args, and applies that function at bending time. It is useful for performing complex operations for which actual python code is necessary. F-benders can be composed with other benders using `<<` and `>>` to make them receive arbitrary values at bending time. Ex:

```python
MAPPING = {
    'total_number_of_keys': F(len),
    'number_of_str_keys': F(lambda source: len([k for k in source.iterkeys()
                                                if isinstance(k, str)])),
    'price_floor': S('price_as_str') >> F(float) >> F(int),
}
ret = bend(MAPPING, {'price_as_str': '42.2', 'k1': 'v', 1: 'a'})
assert ret == {'price_floor': 42,
               'total_number_of_keys': 3,
               'number_of_str_keys': 2}
```

