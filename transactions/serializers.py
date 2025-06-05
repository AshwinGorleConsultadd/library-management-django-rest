from rest_framework import serializers
from .models import Borrow

class BorrowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrow
        fields = ['id', 'book', 'due_date']

    def create(self, validated_data):
        user = self.context['request'].user
        user = validated_data.pop("user")
        return Borrow.objects.create(user=user, **validated_data)


class ReturnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrow
        fields = ['id']


class BorrowHistorySerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source='book.title', read_only=True)

    class Meta:
        model = Borrow
        fields = ['id', 'book_title', 'borrow_date', 'due_date', 'return_date', 'fine']

