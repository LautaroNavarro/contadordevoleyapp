import pytest
import copy
from match.schemas.match_schema import create_match_schema
import jsonschema

valid_schema = {
    'sets_number': 5,
    'set_points_number': 25,
    'points_difference': 2,
    'tie_break_points': 15,
    'teams': [
        {
            'name': 'Team one',
            'color': '#ff00ff',
        },
        {
            'name': 'Team two',
            'color': '#ff0000',
        }
    ]
}


class TestMatchSchema:

    def test_it_raise_error_when_not_sets_number(self):
        schema = copy.deepcopy(valid_schema)
        del schema['sets_number']
        with pytest.raises(jsonschema.exceptions.ValidationError) as e:
            jsonschema.validate(instance=schema, schema=create_match_schema)
        assert e.value.message == "'sets_number' is a required property"

    def test_it_raise_error_when_sets_number_short(self):
        schema = copy.deepcopy(valid_schema)
        schema['sets_number'] = 0
        with pytest.raises(jsonschema.exceptions.ValidationError) as e:
            jsonschema.validate(instance=schema, schema=create_match_schema)
        assert e.value.message == "0 is less than the minimum of 1"

    def test_it_raise_error_when_sets_number_long(self):
        schema = copy.deepcopy(valid_schema)
        schema['sets_number'] = 6
        with pytest.raises(jsonschema.exceptions.ValidationError) as e:
            jsonschema.validate(instance=schema, schema=create_match_schema)
        assert e.value.message == "6 is greater than the maximum of 5"

    def test_it_raise_error_when_sets_number_invalid_type(self):
        schema = copy.deepcopy(valid_schema)
        schema['sets_number'] = '6'
        with pytest.raises(jsonschema.exceptions.ValidationError) as e:
            jsonschema.validate(instance=schema, schema=create_match_schema)
        assert e.value.message == "'6' is not of type 'integer'"

    def test_it_raise_error_when_not_set_points_number(self):
        schema = copy.deepcopy(valid_schema)
        del schema['set_points_number']
        with pytest.raises(jsonschema.exceptions.ValidationError) as e:
            jsonschema.validate(instance=schema, schema=create_match_schema)
        assert e.value.message == "'set_points_number' is a required property"

    def test_it_raise_error_when_set_points_number_short(self):
        schema = copy.deepcopy(valid_schema)
        schema['set_points_number'] = 0
        with pytest.raises(jsonschema.exceptions.ValidationError) as e:
            jsonschema.validate(instance=schema, schema=create_match_schema)
        assert e.value.message == "0 is less than the minimum of 1"

    def test_it_raise_error_when_set_points_number_long(self):
        schema = copy.deepcopy(valid_schema)
        schema['set_points_number'] = 26
        with pytest.raises(jsonschema.exceptions.ValidationError) as e:
            jsonschema.validate(instance=schema, schema=create_match_schema)
        assert e.value.message == "26 is greater than the maximum of 25"

    def test_it_raise_error_when_set_points_number_invalid_type(self):
        schema = copy.deepcopy(valid_schema)
        schema['set_points_number'] = '6'
        with pytest.raises(jsonschema.exceptions.ValidationError) as e:
            jsonschema.validate(instance=schema, schema=create_match_schema)
        assert e.value.message == "'6' is not of type 'integer'"

    def test_it_raise_error_when_not_points_difference(self):
        schema = copy.deepcopy(valid_schema)
        del schema['points_difference']
        with pytest.raises(jsonschema.exceptions.ValidationError) as e:
            jsonschema.validate(instance=schema, schema=create_match_schema)
        assert e.value.message == "'points_difference' is a required property"

    def test_it_raise_error_when_points_difference_short(self):
        schema = copy.deepcopy(valid_schema)
        schema['points_difference'] = 0
        with pytest.raises(jsonschema.exceptions.ValidationError) as e:
            jsonschema.validate(instance=schema, schema=create_match_schema)
        assert e.value.message == "0 is less than the minimum of 1"

    def test_it_raise_error_when_points_difference_long(self):
        schema = copy.deepcopy(valid_schema)
        schema['points_difference'] = 11
        with pytest.raises(jsonschema.exceptions.ValidationError) as e:
            jsonschema.validate(instance=schema, schema=create_match_schema)
        assert e.value.message == "11 is greater than the maximum of 10"

    def test_it_raise_error_when_points_difference_invalid_type(self):
        schema = copy.deepcopy(valid_schema)
        schema['points_difference'] = '6'
        with pytest.raises(jsonschema.exceptions.ValidationError) as e:
            jsonschema.validate(instance=schema, schema=create_match_schema)
        assert e.value.message == "'6' is not of type 'integer'"

    def test_it_raise_error_when_not_tie_break_points(self):
        schema = copy.deepcopy(valid_schema)
        del schema['tie_break_points']
        with pytest.raises(jsonschema.exceptions.ValidationError) as e:
            jsonschema.validate(instance=schema, schema=create_match_schema)
        assert e.value.message == "'tie_break_points' is a required property"

    def test_it_raise_error_when_tie_break_points_short(self):
        schema = copy.deepcopy(valid_schema)
        schema['tie_break_points'] = 0
        with pytest.raises(jsonschema.exceptions.ValidationError) as e:
            jsonschema.validate(instance=schema, schema=create_match_schema)
        assert e.value.message == "0 is less than the minimum of 1"

    def test_it_raise_error_when_tie_break_points_long(self):
        schema = copy.deepcopy(valid_schema)
        schema['tie_break_points'] = 26
        with pytest.raises(jsonschema.exceptions.ValidationError) as e:
            jsonschema.validate(instance=schema, schema=create_match_schema)
        assert e.value.message == "26 is greater than the maximum of 25"

    def test_it_raise_error_when_tie_break_points_invalid_type(self):
        schema = copy.deepcopy(valid_schema)
        schema['tie_break_points'] = '6'
        with pytest.raises(jsonschema.exceptions.ValidationError) as e:
            jsonschema.validate(instance=schema, schema=create_match_schema)
        assert e.value.message == "'6' is not of type 'integer'"

    def test_does_not_raise_when_valid_schema(self):
        jsonschema.validate(instance=valid_schema, schema=create_match_schema)
