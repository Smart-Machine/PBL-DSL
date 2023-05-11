import base64
import requests
from lxml import etree
from io import StringIO, BytesIO


def process_basic(component: dict, file_name: str = "output") -> None:
    html_file = None
    try:
        with open(f"output/{file_name}.html", "r") as file:
            html_file = file.read()
    except Exception as e:
        print("Error while processing [data] component")
        print(component)
        print(e)

    html_parser = etree.HTMLParser()
    html_tree = etree.parse(StringIO(html_file), html_parser)

    if component.get("node") == "text":
        if component.get("params").get("role") == "company-name":
            elem = html_tree.xpath(
                "//div[contains(@class, 'company-name-')]/p/text()")
            for e in elem:
                html_file = html_file.replace(
                    e, component.get("params").get("value"))
        elif component.get("params").get("role") == "text-below-first-company-name":
            elem = html_tree.xpath(
                "//div[contains(@class, 'text-below-first-company-name')]/p/i/text()")
            for e in elem:
                html_file = html_file.replace(
                    e, component.get("params").get("value"))
        elif component.get("params").get("role") == "text-below-second-company-name":
            elem = html_tree.xpath(
                "//div[contains(@class, 'text-below-second-company-name')]/p/text()")
            for e in elem:
                html_file = html_file.replace(
                    e, component.get("params").get("value"))
        elif component.get("params").get("role") == "text-middle":
            elem = html_tree.xpath(
                "//div[contains(@class, 'text-middle')]/p/text()")
            for e in elem:
                html_file = html_file.replace(
                    e, component.get("params").get("value"))
        elif component.get("params").get("role") == "text-barcode":
            elem = html_tree.xpath(
                "//div[contains(@class, 'text-barcode')]/p/text()")
            for e in elem:
                html_file = html_file.replace(
                    e, component.get("params").get("value"))
        elif component.get("params").get("role") == "expiration-date":
            elem = html_tree.xpath("//div[contains(@class, 'expiration-date')]/p/text()") 
            for e in elem:
                html_file = html_file.replace(
                    e, component.get("params").get("value"))
        elif component.get("params").get("role") == "text-address":
            company = html_tree.xpath(
                "//div[contains(@class, 'text-address')]/p/p2/text()")
            if company:
                company = company[0]
            address, website = [e.strip()
                                for e in html_tree.xpath("//div[contains(@class, 'text-address')]/p/text()") if e.strip()]
            html_file = html_file.replace(company, component.get("params").get("value").split("~")[0].strip())
            html_file = html_file.replace(address, component.get("params").get("value").split("~")[1].strip()) 
            html_file = html_file.replace(website, component.get("params").get("value").split("~")[2].strip())
        elif component.get("params").get("role") == "product-description":
            directions, warnings, ingredients, storage = html_tree.xpath("//div[contains(@class, 'product-description')]/p/p1/text()")
            html_file = html_file.replace(directions, component.get("params").get("value").split("~")[0].strip())
            html_file = html_file.replace(warnings, component.get("params").get("value").split("~")[1].strip())
            html_file = html_file.replace(ingredients, component.get("params").get("value").split("~")[2].strip())
            html_file = html_file.replace(storage, component.get("params").get("value").split("~")[3].strip())
    
    if component.get("node") == "image":
        # TODO: export the downloading logic to a separate chunck
        # and make sure to add the possibility to load the images
        # locally. 
        link = component.get("params").get("src")
        data_url = None
        if link and "http" in link:
            response = requests.get(link)
            image_bytes = response.content
            image = base64.b64encode(image_bytes).decode("utf-8")
            image_ext = ""
            if image[0] == '/':
                image_ext = "jpg"
            elif image[0] == 'i':
                image_ext = "png"
            elif image[0] == 'R':
                image_ext = "gif"
            elif image[0] == 'U':
                image_ext = "webp"
            elif image[0] == 'J':
                image_ext = "pdf"
            elif image[0] == 'T':
                image_ext = "tif"
            elif image[0] == 'P':
                image_ext = "svg"
            data_url = f"data:image/{image_ext};base64,{image}"
        elif link:
            binary_file_content = open(link, "rb").read()
            base64_utf8_str = base64.b64encode(binary_file_content).decode("utf-8")
            ext = link.split(".")[-1]
            data_url = f"data:image/{ext};base64,{base64_utf8_str}"

        previous_image = html_tree.xpath(f"//div[contains(@class, '{component.get('params').get('role')}')]/img/@src")[0]
        if data_url:
            html_file = html_file.replace(previous_image, data_url)

    with open(f"output/{file_name}.html", "w") as file:
        file.write(html_file)

def process_soft(component: dict, file_name: str = "output") -> None:
    process_basic(component, file_name)

def process_water(component: dict, file_name: str = "output") -> None:
    pass