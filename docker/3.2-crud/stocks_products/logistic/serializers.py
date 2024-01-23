from rest_framework import serializers

from .models import Product, StockProduct, Stock


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductPositionSerializer(serializers.ModelSerializer):
    # настройте сериализатор для позиции продукта на складе
    class Meta:
        model = StockProduct
        fields = ['product', 'quantity', 'price']


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)

    class Meta:
        model = Stock
        fields = ["address", "positions"]

    # настройте сериализатор для склада

    def create(self, validated_data):
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')

        # создаем склад по его параметрам
        stock = super().create(validated_data)
        for i in positions:
            new_stock = StockProduct.objects.create(product=i['product'],
                                                    stock=stock,
                                                    quantity=i['quantity'],
                                                    price=i['price']
                                                    )
            stock.positions.add(new_stock)
        return stock

    def update(self, instance, validated_data):
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')

        # обновляем склад по его параметрам
        stock = super().update(instance, validated_data)
        for i in positions:
            new_stock = StockProduct.objects.update_or_create(product=i['product'],
                                                              stock=stock,
                                                              defaults={'quantity': i['quantity'],
                                                                        'price': i['price']
                                                                        }
                                                              )

        return stock
