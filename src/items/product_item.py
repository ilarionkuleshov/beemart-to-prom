from scrapy import Item, Field


class ProductItem(Item):
    title = Field()
    external_id = Field()
    unique_id = Field()
    variation_id = Field()
    availability = Field()
    description = Field()
    price = Field()
    images = Field()
    size = Field()
    color = Field()
    base_characteristics = Field()
