import os
from playwright.sync_api import sync_playwright 

OUTPUT_PATH = "output"

def print_output():
    with open(f"{OUTPUT_PATH}/output.html", "r") as file:
        print(file.read())

def render(file_name: str = "output", file_format: str = "png"):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(f"file://{os.path.abspath(f'output/{file_name}.html')}")
        page.screenshot(full_page=True, path=f"{OUTPUT_PATH}/{file_name}.{file_format}")
        browser.close()