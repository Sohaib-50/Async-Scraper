from rest_framework import serializers

class ScrapeSerializer(serializers.Serializer):
    scrape_url = serializers.CharField()
    async_mode = serializers.BooleanField()

class ScrapeResultSerializer(serializers.Serializer):
    scrape_id = serializers.CharField()