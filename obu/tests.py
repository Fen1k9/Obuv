from django.test import TestCase
from django.urls import reverse
from .models import Product, Category, Producer, Provider, Unit, Role, User
from decimal import Decimal

class ProductModelTest(TestCase):

    def test_product_discounted_price_calculation(self):
        # Arrange (Подготовка)
        category = Category.objects.create(category_name="Обувь")
        producer = Producer.objects.create(producer_name="Производитель")
        provider = Provider.objects.create(provider_name="Поставщик")
        unit = Unit.objects.create(unit_name="пара")
        product = Product.objects.create(
            article="ART-001",
            product_name="Ботинки",
            unit=unit,
            price=Decimal('1000.00'),
            provider=provider,
            producer=producer,
            category=category,
            discount_percent=20,
            stock_quantity=10,
            description="Тестовые ботинки",
            photo=""
        )
        # Act (Действие) - рассчитываем цену со скидкой, используя Decimal
        if product.discount_percent > 0:
            # Преобразуем проценты в Decimal для корректного умножения
            discount_decimal = Decimal(product.discount_percent) / Decimal(100)
            discounted_price = product.price * (Decimal(1) - discount_decimal)
        else:
            discounted_price = product.price
        # Assert (Проверка)
        expected = Decimal('800.00')  # 1000 - 20% = 800
        self.assertEqual(discounted_price, expected)

        def test_product(self):
            # Arrange
            category = Category.objects.create(category_name="Обувь")
            producer = Producer.objects.create(producer_name="Производитель")
            provider = Provider.objects.create(provider_name="Поставщик")
            unit = Unit.objects.create(unit_name="пара")

            product = Product.objects.create(
                article="ART-003",
                product_name="Тапки",
                unit=unit,
                price=Decimal('500.00'),
                provider=provider,
                producer=producer,
                category=category,
                discount_percent=0,
                stock_quantity=0,  # нет в наличии
                description="",
                photo=""
            )
            # Assert
            self.assertEqual(product.stock_quantity, 0)

            def test_product_search_by_name(self):
                # Arrange
                category = Category.objects.create(category_name="Обувь")
                producer = Producer.objects.create(producer_name="Производитель")
                provider = Provider.objects.create(provider_name="Поставщик")
                unit = Unit.objects.create(unit_name="пара")
                product1 = Product.objects.create(
                    article="ART-001",
                    product_name="Зимние ботинки",
                    unit=unit,
                    price=Decimal('2000.00'),
                    provider=provider,
                    producer=producer,
                    category=category,
                    discount_percent=0,
                    stock_quantity=5,
                    description="",
                    photo=""
                )
                product2 = Product.objects.create(
                    article="ART-002",
                    product_name="Осенние ботинки",
                    unit = unit,
                    price = Decimal('1800.00'),
                    provider = provider,
                    producer = producer,
                    category = category,
                    discount_percent = 10,
                    stock_quantity = 3,
                    description = "",
                    photo = ""
                    )

                product3 = Product.objects.create(
                    article="ART-004",
                    product_name="Кроссовки для бега",
                    unit=unit,
                    price=Decimal('2500.00'),
                    provider=provider,
                    producer=producer,
                    category=category,
                    discount_percent=15,
                    stock_quantity=8,
                    description="",
                    photo=""
                )

                # Act - поиск по слову "ботинки"
                query = "ботинки"
                results = Product.objects.filter(product_name__icontains=query)

                # Assert
                self.assertEqual(results.count(), 2)
                self.assertIn(product1, results)
                self.assertIn(product2, results)
                self.assertNotIn(product3, results)

    def test_product_sorting_by_stock_ascending(self):
        # Arrange
        category = Category.objects.create(category_name="Обувь")
        producer = Producer.objects.create(producer_name="Производитель")
        provider = Provider.objects.create(provider_name="Поставщик")
        unit = Unit.objects.create(unit_name="пара")

        product1 = Product.objects.create(
            article="ART-001",
            product_name="Товар 1",
            unit=unit,
            price=Decimal('1000.00'),
            provider=provider,
            producer=producer,
            category=category,
            discount_percent=0,
            stock_quantity=10,
            description="",
            photo=""
        )

        product2 = Product.objects.create(
            article="ART-002",
            product_name="Товар 2",
            unit=unit,
            price=Decimal('1000.00'),
            provider=provider,
            producer=producer,
            category=category,
            discount_percent=0,
            stock_quantity=5,
            description="",
            photo=""
        )

        product3 = Product.objects.create(
            article="ART-003",
            product_name="Товар 3",
            unit=unit,
            price=Decimal('1000.00'),
            provider=provider,
            producer=producer,
            category=category,
            discount_percent=0,
            stock_quantity=0,
            description="",
            photo=""
        )

        # Act - сортировка по возрастанию количества
        sorted_asc = Product.objects.all().order_by('stock_quantity')

        # Assert
        self.assertEqual(sorted_asc[2].stock_quantity, 2)
        self.assertEqual(sorted_asc[1].stock_quantity, 5)
        self.assertEqual(sorted_asc[2].stock_quantity, 10)