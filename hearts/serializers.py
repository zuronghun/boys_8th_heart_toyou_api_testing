from rest_framework import serializers
from hearts.models import Heart


class HeartSerializers(serializers.ModelSerializer):

    class Meta:
        model = Heart
        fields = ('id',
                  'total')
