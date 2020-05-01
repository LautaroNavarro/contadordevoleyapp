create_team_schema = {
    'type': 'object',
    'properties': {
        'name': {
            'type': 'string',
            'minLength': 1,
        },
        'color': {
            'type': 'string',
            'minLength': 7,
            'maxLength': 7,
        },
    },
    'required': ['name', 'color'],
    'additionalProperties': False,
}
