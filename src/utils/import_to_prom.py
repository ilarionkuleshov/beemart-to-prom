import json
import logging
import requests


def import_to_prom(api_token, products_file_path):
    response = requests.post(
        "https://my.prom.ua/api/v1/products/import_file",
        headers={"Authorization": f"Bearer {api_token}"},
        files={
            "file": open(products_file_path, "rb"),
            "data": json.dumps(
                {
                    "force_update": False,
                    "only_available": False,
                    "mark_missing_product_as": "not_available",
                    "updated_fields": [
                        "presence"
                    ]
                }
            )
        }
    )
    response_json = response.json()
    if not "status" in response_json or response_json["status"] != "success":
        logging.error(response_json)
