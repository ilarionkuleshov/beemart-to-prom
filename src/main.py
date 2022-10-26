from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from spiders import BeemartSpider
from utils import get_configured_paths, import_to_prom


if __name__ == "__main__":
    project_settings = get_project_settings()

    products_file_path, logs_file_path = get_configured_paths(
        project_settings.get("DATA_DIRECTORY"),
        project_settings.get("PRODUCTS_FILE"),
        project_settings.get("LOGS_FILE"),
    )
    products_limit = int(project_settings.get("PRODUCTS_LIMIT")) if project_settings.get("PRODUCTS_LIMIT") else None

    process = CrawlerProcess(
        settings={
            "LOG_LEVEL": "ERROR",
            "LOG_FILE": logs_file_path
        }
    )
    process.crawl(BeemartSpider, products_file_path, products_limit)
    process.start()
    import_to_prom(project_settings.get("API_TOKEN"), products_file_path)
