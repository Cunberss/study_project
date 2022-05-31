import os
import requests
import uuid


def synthesize(folder_id, iam_token, text, voice):
    url = 'https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize'
    headers = {
        'Authorization': 'Bearer ' + iam_token,
    }

    data = {
        'text': text,
        'lang': 'ru-RU',
        'voice': voice,
        'folderId': folder_id,
        'format': 'mp3',
    }

    with requests.post(url, headers=headers, data=data, stream=True) as resp:
        if resp.status_code != 200:
            raise RuntimeError("Invalid response received: code: %d, message: %s" % (resp.status_code, resp.text))

        for chunk in resp.iter_content(chunk_size=None):
            yield chunk


def text_to_sound(iam_token, folder_id, text, voice):
    folder = 'media/Uploaded Files/'
    file_name = str(uuid.uuid4()) + '.mp3'
    path_to_save = os.path.join(folder, file_name)
    with open(path_to_save, "wb") as f:
        for audio_content in synthesize(folder_id, iam_token, text, voice):
            f.write(audio_content)
    return file_name
