from django.db import models

class Item(models.Model):
    name = models.CharField('Название', max_length=100)
    description = models.TextField('Описание')
    price = models.IntegerField('Цена(коп.)',default=0)

    def normalize_price(self):
        return "{0:.0f}".format(self.price / 100)
    normalize_price.short_description = 'Цена(руб.)'

    def __str__(self):
        return self.name
    
    # class Meta:
    #     verbose_name = 'Товар'
    #     verbose_name_plural = 'Товары'

class Order(models.Model):
    items = models.ManyToManyField(Item, blank=True, related_name='Товар')

    def display_items(self):
        return ', '.join([ items.name for items in self.items.all()])
    display_items.short_description = 'Корзина'

    def total_amount(self):
        total_sum = 0
        for items in self.items.all():
            price = items.price
            total_sum += price
        return "{0:.0f}".format(total_sum)
    total_amount.short_description = 'Итоговая сумма(коп)'
    
    def amount_rub(self):
        total_sum = 0
        for items in self.items.all():
            price = items.price
            total_sum += price
        return "{0:.0f}".format(total_sum/100)
    amount_rub.short_description = 'Итоговая сумма(руб)'
    