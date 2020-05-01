import pytest
from match.schemas.team_schema import create_team_schema
import jsonschema


class TestTeamSchema:

    def test_it_raise_error_when_no_name(self):
        schema = {
            'color': '#000000',
        }
        with pytest.raises(jsonschema.exceptions.ValidationError) as e:
            jsonschema.validate(instance=schema, schema=create_team_schema)
        assert e.value.message == "'name' is a required property"

    def test_it_raise_error_when_no_color(self):
        schema = {
            'name': 'Valid name',
        }
        with pytest.raises(jsonschema.exceptions.ValidationError) as e:
            jsonschema.validate(instance=schema, schema=create_team_schema)
        assert e.value.message == "'color' is a required property"

    def test_it_raise_error_when_empty_name(self):
        schema = {
            'name': '',
            'color': '#000000',
        }
        with pytest.raises(jsonschema.exceptions.ValidationError) as e:
            jsonschema.validate(instance=schema, schema=create_team_schema)
        assert e.value.message == "'' is too short"

    def test_it_raise_error_when_short_color(self):
        schema = {
            'name': 'Valid name',
            'color': '#00000',
        }
        with pytest.raises(jsonschema.exceptions.ValidationError) as e:
            jsonschema.validate(instance=schema, schema=create_team_schema)
        assert e.value.message == "'#00000' is too short"

    def test_it_raise_error_when_long_color(self):
        schema = {
            'name': 'Valid name',
            'color': '#0000010',
        }
        with pytest.raises(jsonschema.exceptions.ValidationError) as e:
            jsonschema.validate(instance=schema, schema=create_team_schema)
        assert e.value.message == "'#0000010' is too long"

    def test_it_does_not_raise_error_when_valid_schema(self):
        schema = {
            'name': 'Valid name',
            'color': '#ff00ff',
        }
        jsonschema.validate(instance=schema, schema=create_team_schema)
