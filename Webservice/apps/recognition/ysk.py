import urllib.request
import json
import os
from pydub import AudioSegment

iam_token = 't1.9euelZrLkcaUnMiPnsyNicaVicfPi-3rnpWaiZSNmJmMjJKVzZiTkZSUz43l8_d9JG9t-e8jK1xf_d3z9z1TbG357yMrXF_9.tQQA-yJfxzyNqVwOuWL2dd5ePiiSRkq6t7CbUhOiqlzfIPcrhT94BKgWMhFe8VrnHDhx6GnHqu7HWtkJcXrXDA'
folder_id = 'b1gcj077528pofd7e90e'
filename = 'test.mp3'


def sound_to_text(iam_token, folder_id, data):

    params = "&".join([
        "topic=general",
        "folderId=%s" % folder_id,
        "lang=ru-RU"
    ])
    url = urllib.request.Request("https://stt.api.cloud.yandex.net/speech/v1/stt:recognize?%s" % params, data=data)
    url.add_header("Authorization", "Bearer %s" % iam_token)

    responseData = urllib.request.urlopen(url).read().decode('UTF-8')
    decodedData = json.loads(responseData)

    if decodedData.get("error_code") is None:
        text = decodedData.get("result")
    return text

