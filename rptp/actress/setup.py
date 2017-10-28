from config.settings.common import STATIC_ROOT
import os
import json
from rptp.actress.models import Actress
from datetime import datetime


def load_actresses():
    with open(os.path.join(STATIC_ROOT, 'vk_models.json')) as f:
        models = json.load(f)
        for model in models:
            if model['vk_last_video_date']:
                model['vk_last_video_date'] = datetime.fromtimestamp(model['vk_last_video_date'])

            model['ptg_link'] = model.pop('link')

            Actress.objects.create(**model)
