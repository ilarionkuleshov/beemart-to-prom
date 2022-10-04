import requests


def import_to_prom(main_logger, api_token, products_file_path):
    response = requests.post(
        "https://my.prom.ua/api/v1/products/import_file",
        headers={"Authorization": f"Bearer {api_token}"},
        files={"file": open("data/03.10.2022/products.xlsx", "rb")},
        data={
            "force_update": False,
            "only_available": False,
            "mark_missing_product_as": "not_available",
            "updated_fields": [
                "presence"
            ]
        }
    )
    main_logger.info(response.json())
