import json
import os.path

import requests
import time
import json
import urllib.request
import boto3
from creds import FOLDER_ID, IAM_TOKEN, S3_KEY, S3_BUCKET, S3_SECRET, API_KEY

s3 = boto3.resource('s3', aws_access_key_id=S3_KEY, aws_secret_access_key=S3_SECRET, endpoint_url='https://storage.yandexcloud.net')


def get_iam_token(oauth_token):
    r = requests.post('https://iam.api.cloud.yandex.net/iam/v1/tokens', data="{'yandexPassportOauthToken': '%s'}" % oauth_token)
    if r.status_code == 200:
        return json.loads(r.text)['iamToken']


def recognize_api_v1(filepath):
    with open(filepath, "rb") as f:
        data = f.read()

    params = "&".join([
        "topic=general",
        "folderId=%s" % FOLDER_ID,
        "lang=%s" % 'ru-RU'
    ])

    try:
        url = urllib.request.Request("https://stt.api.cloud.yandex.net/speech/v1/stt:recognize?rawResults=true&%s" % params, data=data)
        url.add_header("Authorization", "Bearer %s" % IAM_TOKEN)

        responseData = urllib.request.urlopen(url).read().decode('UTF-8')
        decodedData = json.loads(responseData)

        if decodedData.get("error_code") is None:
            return decodedData.get("result")
    except Exception:
        return


def put_to_s3(folder, filename):
    s3.Bucket(S3_BUCKET).put_object(Key=filename, Body=open(os.path.join(folder, filename), 'rb'))
    return S3_BUCKET + '/' + filename


def recognize_api_v2(s3_filepath):
    POST = 'https://transcribe.api.cloud.yandex.net/speech/stt/v2/longRunningRecognize'

    body = {
        "config": {
            "specification": {
                "languageCode": "ru-RU",
                "rawResults": True,
            }
        },
        "audio": {
            "uri": s3_filepath
        },
    }

    header = {'Authorization': "Api-Key %s" % API_KEY }

    req = requests.post(POST, headers=header, json=body)
    if req.status_code == 200:
        data = req.json()
        id = data['id']

        while True:
            time.sleep(1)
            GET = "https://operation.api.cloud.yandex.net/operations/{id}"
            req = requests.get(GET.format(id=id), headers=header)
            req = req.json()

            if req['done']: break

        result = []
        for chunk in req['response']['chunks']:
            result.append(chunk['alternatives'][0]['text'])
        return ' '.join(result)


def recognize(folder, filename):
    result = recognize_api_v1(os.path.join(folder, filename))
    if not result:
        s3_key = put_to_s3(folder, filename)
        result = recognize_api_v2('https://storage.yandexcloud.net/' + s3_key)
    return result


if __name__ == '__main__':
    pass
