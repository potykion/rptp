from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from rptp.video.models import Video


class VideoSearchSerializer(serializers.Serializer):
    """
    Validate query parameters required for search.
    """
    query = serializers.CharField()
    count = serializers.IntegerField(default=30)
    offset = serializers.IntegerField(default=0)


class VkVideoSerializer(serializers.ModelSerializer):
    """
    Parse VK video to rptp video format (models.Video).
    """
    owner_id = serializers.IntegerField()
    id = serializers.IntegerField()
    photo_320 = serializers.URLField()

    class Meta:
        model = Video
        fields = [
            'title', 'preview', 'url', 'duration', 'views',
            'owner_id', 'id', 'photo_320', 'mobile_url'
        ]
        read_only_fields = ['url', 'preview', 'mobile_url']
        write_only_fields = ['owner_id', 'id', 'photo_320']

    def validate(self, data):
        """
        Format VK video to rptp video format.

        Args:
            data: VK video dict.

        Returns:
            Dict used to create Video object.

        """
        try:
            return {
                'title': data['title'],
                'preview': data['photo_320'],
                'url': f"https://vk.com/video{data['owner_id']}_{data['id']}",
                'mobile_url': f"https://m.vk.com/video{data['owner_id']}_{data['id']}",
                'duration': data['duration'],
                'views': data['views']
            }
        except KeyError:
            raise ValidationError({'video': 'Video format is invalid.'})
