from xlsxwriter import Workbook


class XlsxPipeline:
    def open_spider(self, spider):
        self.workbook = Workbook(spider.products_file_path)
        self.worksheet = self.workbook.add_worksheet()
        self.row_num = 0
        self.col_num = 0
        self.total_ch_counter = 0
        self.temp_ch_counter = 0
        self.write_header_row()

    def write_header_row(self):
        self.header_row = [
            "Назва_позиції", "Код_товару", "Ідентифікатор_товару", "ID_групи_різновидів", "Наявність",
            "Опис", "Ціна", "Валюта", "Одиниця_виміру", "Посилання_зображення"
        ]
        for value in self.header_row:
            self.write(value)
        self.write(last=True)

    def process_item(self, item, spider):
        self.write(item["title"])
        self.write(item["external_id"])
        self.write(item["unique_id"])
        self.write(item["variation_id"])
        self.write(item["availability"])
        self.write(item["description"])
        self.write(item["price"])
        self.write("грн")
        self.write("шт.")
        self.write(item["images"])
        self.write_characteristic("Розмір", item["size"])
        self.write_characteristic("Колір", item["color"])
        for name in item["base_characteristics"]:
            if name != "Розмір" and name != "Колір":
                self.write_characteristic(name, item["base_characteristics"][name])
        self.write(last=True)
        return item

    def write_characteristic(self, name, value):
        if self.temp_ch_counter == self.total_ch_counter:
            self.worksheet.write(0, self.col_num, "Назва_Характеристики")
            self.worksheet.write(0, self.col_num+1, "Одиниця_виміру_Характеристики")
            self.worksheet.write(0, self.col_num+2, "Значення_Характеристики")
            self.total_ch_counter += 1
        self.write(name)
        self.write("")
        self.write(value)
        self.temp_ch_counter += 1

    def write(self, value="", last=False):
        if last:
            self.row_num += 1
            self.col_num = 0
        else:
            self.worksheet.write(self.row_num, self.col_num, str(value))
            self.col_num += 1

    def close_spider(self, spider):
        self.workbook.close()
