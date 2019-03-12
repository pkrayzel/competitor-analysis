import boto3
import inject
import os

from adapters import dao, web
import config
import competitors


def bootstrap():
    env = os.environ

    def configure(binder):
        aws_config = config.get_aws_config(env)
        aws_s3_config = config.get_aws_s3_config(env)
        aws_sqs_config = config.get_aws_sqs_config(env)

        s3_client = boto3.client('s3', endpoint_url=aws_s3_config['endpoint_url'], **aws_config)
        sqs_resource = boto3.resource('sqs', endpoint_url=aws_sqs_config['endpoint_url'], **aws_config)

        binder.bind("file_storage_client", dao.FileStorageClient(client=s3_client,
                                                                 bucket_name=aws_s3_config['bucket_name']))
        binder.bind("queue_client", dao.QueueClient(resource=sqs_resource,
                                                    queue_name=aws_sqs_config['queue_name']))

        web_client = web.WebClient()
        binder.bind("web_client", web_client)

        competitors_map = dict(
            nl_fonq=competitors.FonqCompetitor(),
            nl_flinders=competitors.FlindersCompetitor(),
            nl_bolia=competitors.BoliaCompetitor(web=web_client)
        )

        binder.bind("competitors_map", competitors_map)

    inject.configure(configure)

    config.configure_logging(env)
