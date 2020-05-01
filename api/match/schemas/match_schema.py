from match.schemas.team_schema import create_team_schema

create_match_schema = {
    'type': 'object',
    'properties': {
        'sets_number': {
            'type': 'integer',
            'minimum': 1,
            'maximum': 5,
        },
        'set_points_number': {
            'type': 'integer',
            'minimum': 1,
            'maximum': 25,
        },
        'points_difference': {
            'type': 'integer',
            'minimum': 1,
            'maximum': 10,
        },
        'tie_break_points': {
            'type': 'integer',
            'minimum': 1,
            'maximum': 25,
        },
        'teams': {
            'type': 'array',
            'items': create_team_schema,
            "minItems": 2,
            "maxItems": 2,
        },
    },
    'required': ['sets_number', 'set_points_number', 'points_difference', 'tie_break_points', 'teams'],
    'additionalProperties': False,
}
