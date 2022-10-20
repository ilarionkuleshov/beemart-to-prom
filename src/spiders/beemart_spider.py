import hashlib

from yattag import Doc
from scrapy import Spider, Request

from items import ProductItem


class BeemartSpider(Spider):
    name = "beemart"
    custom_settings = {
        "ITEM_PIPELINES": {"pipelines.XlsxPipeline": 800}
    }
    start_urls = [
        "https://beemart.pl.ua/divchatka/kostyumy-komplekty_d/",
        "https://beemart.pl.ua/divchatka/platya-yubki_d/",
        "https://beemart.pl.ua/divchatka/futbolki-bluzy_d/",
        "https://beemart.pl.ua/divchatka/bryuki-losiny_d/",
        "https://beemart.pl.ua/divchatka/dlya-doma_d/",
        "https://beemart.pl.ua/divchatka/tolstovki-svitshoti_d/",
        "https://beemart.pl.ua/hlopchiki/kostyumy-komplekty_m/",
        "https://beemart.pl.ua/hlopchiki/futbolki-dzhempera_m/",
        "https://beemart.pl.ua/hlopchiki/bryuki-shorty_m/",
        "https://beemart.pl.ua/hlopchiki/dlya-doma_m/",
        "https://beemart.pl.ua/hlopchiki/tolstovki-svitshoti_m/",
        "https://beemart.pl.ua/zhinki/kostyumi-komplekti_z/",
        "https://beemart.pl.ua/zhinki/plattya-spidnici_z/",
        "https://beemart.pl.ua/zhinki/futbolki-bluzy_z/",
        "https://beemart.pl.ua/zhinki/shtani-shorti_z/",
        "https://beemart.pl.ua/zhinki/dlya-domu_z/",
        "https://beemart.pl.ua/zhinki/bomberi_z/",
        "https://beemart.pl.ua/choloviki/futbolki-dzhempera_ch/",
        "https://beemart.pl.ua/choloviki/sportivnij-odyag_ch/",
        "https://beemart.pl.ua/choloviki/dlya-domu_ch/",
        "https://beemart.pl.ua/choloviki/nizhnya-bilizna_ch/",
    ]
    unique_ids = []

    def __init__(self, products_file_path):
        super(BeemartSpider, self).__init__()
        self.products_file_path = products_file_path

    def parse(self, response):
        for product_url in response.xpath("//div[@class='product-grid']//div[@class='name']/a/@href").getall():
            yield Request(
                url=product_url,
                callback=self.parse_product
            )
        next_page_url = response.xpath("//a[text()='>']/@href").get()
        if next_page_url:
            yield Request(
                url=next_page_url,
                callback=self.parse
            )

    def parse_product(self, response):
        try:
            title = response.xpath("//*[@itemprop='name']/text()").get().strip()
            external_id = response.xpath("//*[@itemprop='model']/text()").get().strip()
            variation_id = self.get_variation_id(external_id)
            availability = "+" if ("InStock" in response.xpath("//*[@itemprop='availability']/@href").get(default="")) else "-"
            base_image = response.xpath("//div[@class='image']/a/@href").get()

            description = response.xpath("//*[@itemprop='description']//*[not(ancestor::table)]/text()").getall()
            description = "<br/>".join([text.strip() for text in description if text.strip()])
            description = description.replace("\xa0", " ")

            table = self.get_formatted_table(response.xpath("//*[@itemprop='description']//table"))
            if table:
                description = f"{description}<br/>{table}"

            base_characteristics = {}
            for tr in response.xpath("//table[@class='attribute']/tbody/tr"):
                tds = tr.xpath("td/text()").getall()
                tds = [td.strip() for td in tds if td.strip()]
                if len(tds) == 2:
                    base_characteristics[tds[0]] = tds[1]

            for size_input in response.xpath("//div[@class='prodButtons']/input"):
                size = response.xpath(f"//label[@for='{size_input.xpath('@id').get()}']/text()").get().strip()
                price = size_input.xpath("@data-price").get().strip()
                price = float(price.split(" ")[0]) if price else None
                if size and price:
                    for color_input in response.xpath(f"//input[not(@disabled) and @data-parent_id={size_input.xpath('@value').get()}]"):
                        color_list = response.xpath(f"//label[@for='{color_input.xpath('@id').get()}']/text()").getall()
                        color = [c.strip() for c in color_list if c.strip()][0]
                        image = response.xpath(f"//a[@rel='colorbox' and contains(@href, '{color_input.xpath('@data-ov_id').get()}')]/@href").get()
                        if image:
                            images = f"{image}, {base_image}"
                        else:
                            images = base_image
                        unique_id = f"{external_id}{color}{size}"
                        if not unique_id in self.unique_ids:
                            self.unique_ids.append(unique_id)
                            yield ProductItem(
                                {
                                    "title": title,
                                    "external_id": external_id,
                                    "unique_id": unique_id,
                                    "variation_id": variation_id,
                                    "availability": availability,
                                    "description": description,
                                    "price": price,
                                    "images": images,
                                    "size": size,
                                    "color": color,
                                    "base_characteristics": base_characteristics
                                }
                            )
        except Exception as e:
            self.logger.error(e)

    def get_variation_id(self, external_id):
        md5 = hashlib.md5()
        md5.update(external_id.encode("utf-8"))
        return str(int(md5.hexdigest(), 16))[0:9]

    def get_formatted_table(self, table):
        if not len(table):
            return None
        else:
            table_list = []
            for row in table.xpath(".//tr"):
                row_list = []
                for cell in row.xpath(".//td"):
                    value_list = []
                    for value in cell.xpath(".//text()").getall():
                        formatted_value = value.replace("\n", "").replace("\r", "").replace("\t", "").replace("\xa0", " ").strip()
                        if formatted_value:
                            value_list.append(formatted_value)
                    row_list.append(" ".join(value_list))
                table_list.append(row_list)

            doc, tag, text = Doc().tagtext()
            colspan_attr = max(len(row) for row in table_list)

            with tag("table", align="center", border="1"):
                with tag("tbody"):
                    for row in table_list:
                        with tag("tr"):
                            cleaned_row = [value for value in row if value]
                            if len(cleaned_row) == 1:
                                with tag("td", colspan=str(colspan_attr), align="center"):
                                    with tag("strong"):
                                        text(cleaned_row[0])
                            else:
                                for value in row:
                                    with tag("td", align="center"):
                                        text(value)
            return doc.getvalue()
