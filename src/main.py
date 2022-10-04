from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from spiders import BeemartSpider
from utils import get_configured_paths, get_logger, import_to_prom


if __name__ == "__main__":
    project_settings = get_project_settings()

    products_file_path, logs_file_path = get_configured_paths(
        project_settings.get("DATA_DIRECTORY"),
        project_settings.get("PRODUCTS_FILE"),
        project_settings.get("LOGS_FILE"),
    )
    main_logger = get_logger(logs_file_path)

    process = CrawlerProcess(
        settings={"LOG_ENABLED": False}
    )
    process.crawl(BeemartSpider, main_logger, products_file_path)
    process.start()
    import_to_prom(main_logger, project_settings.get("API_TOKEN"), products_file_path)
