"""
Runtime: Python3.8
"""
#!/usr/bin/python3.8

import urllib3 
import json
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)
http = urllib3.PoolManager()


def lambda_handler(event, context): 
    """
        This lambda function was configured with AWS CW alarms as soon as there is any alarm and this lambda function
        is subscribed in SNS topic it will push the notification in TEAMS app.
        The messages/notifications are pushed to teams app using Webhook. 
        In order to generate webhook you need to be the owner (Owner Privileges) if so then follow the steps 
        1. Goto teams and select or create your team
        2. Click on 3 dots (near i symbol top right corner) after selecting your team
        3. Select Connector and click on Configured 
        4. Name the webhook, upload image and it will automatically give you the URL for webhook.
        5. Copy that url and paste it in this function and run the code on lambda function.
        
        @Instance(s): 
        @TeamsAppGroupName: Monitoring Alarms (General)
    """
    
    WEBHOOK_URL     = ""
    FAILED_IMAGE    = "data:image/jpeg;base64,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";
    OK_IMAGE        = "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAYABgAAD/4QBmRXhpZgAATU0AKgAAAAgABAEaAAUAAAABAAAAPgEbAAUAAAABAAAARgEoAAMAAAABAAIAAAExAAIAAAAQAAAATgAAAAAAAABgAAAAAQAAAGAAAAABcGFpbnQubmV0IDQuMi44AP/bAEMABgQFBgUEBgYFBgcHBggKEAoKCQkKFA4PDBAXFBgYFxQWFhodJR8aGyMcFhYgLCAjJicpKikZHy0wLSgwJSgpKP/bAEMBBwcHCggKEwoKEygaFhooKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKP/AABEIACgAKAMBIgACEQEDEQH/xAAfAAABBQEBAQEBAQAAAAAAAAAAAQIDBAUGBwgJCgv/xAC1EAACAQMDAgQDBQUEBAAAAX0BAgMABBEFEiExQQYTUWEHInEUMoGRoQgjQrHBFVLR8CQzYnKCCQoWFxgZGiUmJygpKjQ1Njc4OTpDREVGR0hJSlNUVVZXWFlaY2RlZmdoaWpzdHV2d3h5eoOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4eLj5OXm5+jp6vHy8/T19vf4+fr/xAAfAQADAQEBAQEBAQEBAAAAAAAAAQIDBAUGBwgJCgv/xAC1EQACAQIEBAMEBwUEBAABAncAAQIDEQQFITEGEkFRB2FxEyIygQgUQpGhscEJIzNS8BVictEKFiQ04SXxFxgZGiYnKCkqNTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqCg4SFhoeIiYqSk5SVlpeYmZqio6Slpqeoqaqys7S1tre4ubrCw8TFxsfIycrS09TV1tfY2dri4+Tl5ufo6ery8/T19vf4+fr/2gAMAwEAAhEDEQA/APpPxNr1n4e01ru9YnJ2xxr96RvQf414n4g8c61rErf6S9pbHgQ27FRj3PU/y9qPiPrT6x4nucNm2tWMEQB4wDyfxOfwxXL15levKUuWOx+d51nVXEVZUqUrQWmnXzJPPl8zf5sm/wDvbjmuk8P+Oda0eVf9Je7thwYbhiwx7HqP5e1cvXo/gXwXAbNtb8TBYrBU3xxSHaGH95vb0Hf+eVJTcvcPOy2GKq1ksNJp7t30S7vyPTfDOvWfiHTVu7JiMHbJG33o29D/AI0V494N1q20fxz/AMS1pRpV1L5GJTztJ+Un6H9M0V6VGrzx13PvspzNYyjeo1zRdn2fmvU5uz+zf21H/a/m/ZfO/f8AlfexnnFdx468FwCzXW/DIWWwZN8kUZ3BR/eX29R2/lgfEjRX0fxPc4XFtdMZ4iBxgnkfgc/hip/APjKbw7c/Z7rdLpkjfOnUxn+8v9R3rgjyxbpz+8+JoRoUalTBYyNrv4uqfR+hteAfBsKW39veJNsVlGvmRRS8Bh/fb29B3+nXF8feMpvEVz9ntd0WmRt8idDIf7zf0Hajx94ym8RXP2e13RaZG3yJ0Mh/vN/Qdq5CipUUVyQ2/MMbjadKn9Twfwfal1k/8uyJLbd9oi8v7+8bfrmiuk+G+ivrHie2yuba1YTykjjAPA/E4/DNFXQoOcb3OrJ8mqYyk6vNyq/3ntnibQbPxDprWl6pGDujkX70beo/wrxPxB4G1rR5W/0Z7u2HImt1LDHuOo/l70UV1V6UZrme59NnWV4fE03WmrSS3X6nN+RL5mzypN/93ac10nh/wNrWsSrm2e0tjyZrhSox7Dqf5e9FFcVClGcrM+SyfLqWMr8lW9ke2eGdBs/D2mraWSk5O6SRvvSN6n/CiiivUSSVkfo9OnClBU6askf/2Q=="
    
    RED_COLOR       = 'FF0000'
    YELLOW_COLOR    = 'FFF305'
    GREEN_COLOR     = '33FF00'

    logger.info('Complete Event: {}'.format(event))
    logger.info('SNS Data: {}'.format(event['Records'][0]['Sns']))
    sns_message = event['Records'][0]['Sns']['Message']

    try:
        alarm_name          = sns_message.get('Event') if sns_message.get('Event') else sns_message.get('AlarmName', '')
        alarm_description   = sns_message.get('Description') if sns_message.get('Description') else sns_message.get('AlarmDescription', '')
        alarm_reason        = sns_message.get('Cause') if sns_message.get('Cause') else sns_message.get('NewStateReason')
        autoscaling_group   = sns_message.get('AutoScalingGroupName', '')
    except Exception as e:
        logger.error(e)    
    
    oldstate = ''
    newstate = ''
    if sns_message.get('OldStateValue'):
        oldstate = sns_message.get('OldStateValue')
    elif sns_message.get('Details').get('InvokingAlarms'):
        oldstate = sns_message.get('Details').get('InvokingAlarms')[0].get('OldStateValue')
    
    if sns_message.get('NewStateValue'):
        newstate = sns_message.get('NewStateValue')
    elif sns_message.get('Details').get('InvokingAlarms'):
        newstate = sns_message.get('Details').get('InvokingAlarms')[0].get('NewStateValue')


    time        = sns_message.get('StateChangeTime', sns_message.get('Time', ''))
    metric_type = sns_message.get('Trigger')['MetricName'] if sns_message.get('Trigger') else sns_message['Event']
    color       = "FFF305"
    image       = None

    # Setting the image and bar colour
    if oldstate == newstate and newstate == 'ALARM': # If both stats are alarms then this is problem we need to raise this as critical warning
        color = RED_COLOR
        image = FAILED_IMAGE
    elif newstate == 'OK':
        color = GREEN_COLOR
        image = OK_IMAGE
    elif newstate == 'ALARM':
        color = RED_COLOR
        image = FAILED_IMAGE
        
    else:
        color = YELLOW_COLOR
        image = FAILED_IMAGE
        
    text = "The current state of autoscaling group is **%s**" % (sns_message.get('StatusCode')) if oldstate=='' and newstate =='' else " State has been changed from **%s** to **%s** " % (oldstate, newstate)
    print(oldstate, newstate)
    msg = {
        "@context": "https://schema.org/extensions",
        "@type": "MessageCard",
        "colour": color,
        "themeColor": color,
        "title": alarm_name,
        "text": text,
        "Reason": alarm_reason,
        "sections": [{
        "activityTitle": "**%s**" %(metric_type),
        "activityImage": image,
        "activityText": " **Alarm Description:** %s on Time **%s**" %(alarm_description, time)
        },{
        "activityTitle": "**Alarm Cause**",
        "activityText": " %s " %(alarm_reason)
        
        }]
    }

    # Sending the messages to TEAMS app using webhooks

    try:    
        encoded_msg = json.dumps(msg).encode('utf-8')
        resp = http.request('POST', WEBHOOK_URL, body=encoded_msg)
    except urllib3.exceptions.HTTPError as e:
        logger.error('Request failed:', e.reason)
    except Exception as e:
        logger.error('Error: ', e)


    return ({
        "message": event['Records'][0]['Sns']['Message'], 
        "status_code": resp.status, 
        "response": resp.data
    })

