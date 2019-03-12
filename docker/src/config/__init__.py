import logging


def dump_env_vars(env):
    for key, value in env.items():
        if key.startswith("SECRET_"):
            continue
        print(key, value)


def get_env(env):
    return env.get('ENV', 'local')


def is_local(env):
    return get_env(env) == 'local'


def select_level(name, default, env):
    return env.get('LOGGING_LEVELS_' + name.upper(), default)


def configure_logging(env):
    logging.config.dictConfig(
        {
            'version': 1,
            'disable_existing_loggers': False,
            'root': {
                'level': select_level('root', 'INFO', env),
                'handlers': ['default']
            },
            'filters': {},
            'loggers': {
                'botocore': {
                    'level': select_level('botocore', 'WARN', env),
                },
                'boto': {
                    'level': select_level('boto3', 'WARN', env),
                },
                'urllib3': {
                    'level': select_level('urllib3', 'WARN', env),
                },
                'scrapy': {
                    'level': select_level('scrapy', 'WARN', env),
                },

            },
            'formatters': {
                'plain': {
                    'format': '%(asctime)s %(levelname)s %(message)s',
                    'datefmt': '%H:%M:%S'
                },
            },
            'handlers': {
                'default': {
                    'class': 'logging.StreamHandler',
                    'stream': 'ext://sys.stdout',
                    'formatter': 'plain',
                    'filters': [],
                    'level': 'NOTSET'
                }
            }
        }
    )


# AWS section
def get_aws_config(env):
    return {
        'aws_access_key_id': env.get('AWS_ACCESS_KEY_ID'),
        'aws_secret_access_key': env.get('AWS_SECRET_ACCESS_KEY'),
        'region_name': env.get('AWS_DEFAULT_REGION', 'eu-west-1'),
    }


def get_aws_s3_config(env):
    # default_endpoint = 'http://localhost:4572' if is_local(env) else None
    default_endpoint = None
    return {
        'endpoint_url': env.get('AWS_S3_ENDPOINT_URL', default_endpoint),
        'bucket_name': env.get('AWS_S3_BUCKET_NAME', 'made-dev-competitor-analysis')
    }


def get_aws_sqs_config(env):
    # default_endpoint = 'http://localhost:4576' if is_local(env) else None
    default_endpoint = None
    return {
        'endpoint_url': env.get('AWS_SQS_ENDPOINT_URL', default_endpoint),
        'queue_name': env.get('AWS_SQS_QUEUE_NAME', 'competitor-analysis-products-queue-dev')
    }

