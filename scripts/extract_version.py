# -*- coding: utf-8 -*-
import urllib.request as request
import json


if __name__ == '__main__':
    api_data = request.urlopen(
        'https://api.github.com/repos/taliamax/krait/releases/latest'
    ).read()

    json_data = json.loads(api_data)
    tag_version = json_data['tag_name']

    print(tag_version)
