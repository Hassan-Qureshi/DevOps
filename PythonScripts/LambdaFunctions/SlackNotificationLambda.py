import json
import urllib3
import logging
import os
import datetime
# Read all the environment variables
SLACK_WEBHOOK_URL = os.environ['SLACK_WEBHOOK_URL']
SLACK_USER = os.environ['SLACK_USER']
SLACK_CHANNEL = os.environ['SLACK_CHANNEL']
UNITS_MAPPING = [
    (1<<50, ' PB'),
    (1<<40, ' TB'),
    (1<<30, ' GB'),
    (1<<20, ' MB'),
    (1<<10, ' KB'),
    (1, (' byte', ' bytes')),
]

logger = logging.getLogger()
logger.setLevel(logging.INFO)
http = urllib3.PoolManager()


def pretty_size(bytes, units=UNITS_MAPPING):
    """Get human-readable file sizes.
    simplified version of https://pypi.python.org/pypi/hurry.filesize/
    """
    for factor, suffix in units:
        if bytes >= factor:
            break
    amount = int(bytes / factor)

    if isinstance(suffix, tuple):
        singular, multiple = suffix
        if amount == 1:
            suffix = singular
        else:
            suffix = multiple
    return str(amount) + suffix
    
    
def lambda_handler(event, context):
    """
    This lambda function pushes information about the file being uploaded to the S3 Bucket to slack channel
    S3 Trigger: PUT 
     
    """
    logger.info("Event: " + str(event['Records'][0]['s3']))
    event = event['Records'][0]['s3']
    BUCKET_DETAILS = event['bucket']
    FILE_META_DATA = event['object']
    
    msg = {
        "channel": SLACK_CHANNEL,
        "username": SLACK_USER,
        "attachments": [
            {
                "title": "Backup Update",
                "pretext": "Backup Uploaded at {}".format(datetime.datetime.now()),
                "color": "#00FF00",
                "text": """Status    : {} 
                        Size      : {} 
                        Bucket    : {} 
                        FileName  : {}
                        """.format('Success', pretty_size(int(FILE_META_DATA.get('size', '-'))), 
                        BUCKET_DETAILS.get('name', '-'), 
                        FILE_META_DATA.get('key', '-'))
            }
        ]
    }
    
    logger.info("Message: " + str(msg))
    headers = {'Content-Type': "application/json"}
    try:
        response = http.request('POST', SLACK_WEBHOOK_URL, body=json.dumps(msg), headers=headers)
    except Exception as e:
        logger.error("Request failed: ", e)