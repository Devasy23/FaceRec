import os


def get_database_config():
    use_atlas = os.getenv('USE_ATLAS', 'False').lower() in ('true', '1', 't')
    if use_atlas:
        return {
            'use_atlas': True,
            'uri': os.getenv('ATLAS_URI', ''),
            'db_name': os.getenv('ATLAS_DB_NAME', 'ImageDB')
        }
    else:
        return {
            'use_atlas': False,
            'uri': 'mongodb://localhost:27017/',
            'db_name': 'ImageDB'
        }
