import json
import boto3
import email.utils
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import urllib.parse as parse_url

import settings


BUCKET_NAME = 'angelaliu-photoshoot'
s3 = boto3.resource(
    's3',
    region_name=settings.AWS_REGION,
    aws_access_key_id=settings.AWS_SERVER_PUBLIC_KEY,
    aws_secret_access_key=settings.AWS_SERVER_SECRET_KEY,
)
S3_BUCKET = s3.Bucket(BUCKET_NAME)

CORS_HEADER = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Credentials': True,
}


def get_photos(event, context):
    """
    Get all available photoshoots
    """
    # get photoshoot names
    folder_names = []
    for obj in S3_BUCKET.objects.all():
        if obj.key.endswith('/'):
            folder_name = obj.key[:-1]
            folder_names.append(folder_name)

    return {
        "statusCode": 200,
        "body": json.dumps({'data': folder_names}),
        "headers": CORS_HEADER,
    }


def get_photoshoot(event, context):
    """
    Fetch all photos from a specific photoshoot
    """
    photoshoot_name = parse_url.unquote(event.get('pathParameters', {}).get('photoshoot'))
    if not photoshoot_name:
        return {
            "statusCode": 400,
            "error": "Invalid url parameter",
            "headers": CORS_HEADER,
        }

    # Fetch photo thumbnails
    thumbnail_urls = []
    description = ''
    for obj in S3_BUCKET.objects.filter(Prefix=photoshoot_name):
        if 'thumb-' in obj.key:
            public_url = f'https://{BUCKET_NAME}.s3.amazonaws.com/{obj.key}'
            thumbnail_urls.append(public_url)
        elif '.json' in obj.key:
            description_json = obj.get()['Body'].read().decode('utf-8')
            description = json.loads(description_json)

    return {
        "statusCode": 200,
        "body": json.dumps({
            'data': thumbnail_urls,
            'description': description,
        }),
        "headers": CORS_HEADER,
    }


def send_email(event, context):
    """Send an email to the inquire address via frontend contact form to prevent spam."""
    json_data = event.get('body')
    if not json_data:
        return {
            "statusCode": 400,
            "error": "No data in message body",
            "headers": CORS_HEADER,
        }

    data = json.loads(json_data)
    sender_name = data['name'] + ' from <' + data['email'] + '>'

    # The subject line of the email.
    subject = '[Personal Site Inquiry] ' + data['subject']

    # The email body for recipients with non-HTML email clients.
    body_text = data['message']

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    sender = 'inquire@liuangela.com'
    msg['From'] = email.utils.formataddr((sender_name, sender))
    msg['To'] = settings.RECIPIENT_EMAIL

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(body_text, 'plain')

    # Attach parts into message container.
    msg.attach(part1)

    # Try to send the message.
    smtp_server = smtplib.SMTP(
        f'email-smtp.{settings.AWS_REGION}.amazonaws.com',
        587,
    )
    try:
        smtp_server.ehlo()
        smtp_server.starttls()
        #stmplib docs recommend calling ehlo() before & after starttls()
        smtp_server.ehlo()
        smtp_server.login(
            settings.AWS_SES_SMTP_USERNAME,
            settings.AWS_SES_SMTP_PASSWORD,
        )
        smtp_server.sendmail(sender, settings.RECIPIENT_EMAIL, msg.as_string())
        smtp_server.close()

    # Display an error message if something goes wrong.
    except Exception as e:
        return {
            'statusCode': 500,
            'error': json.dumps(e),
            'headers': CORS_HEADER,
        }

    return {
        'statusCode': 200,
        'body': json.dumps({'data': 'success!'}),
        'headers': CORS_HEADER,
    }
