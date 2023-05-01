import re
import os 
import base64

OUTPUT_PATH = "output"

def bundle_html(folder_path: str, file_name: str = "output"):
    for file in os.listdir(folder_path):
        if file.endswith(".html"):
            html_file_path = os.path.join(folder_path, file)
        if file.endswith(".css"):
            css_file_path = os.path.join(folder_path, file) 

    with open(html_file_path, "r") as html_file:
        html_content = html_file.read()

    with open(css_file_path, "r") as css_file:
        css_content = css_file.read()

    # Embed CSS in HTML using a <style> tag
    html_with_inline_css = f"<html><head><style>{css_content}</style></head><body>{html_content}</body></html>"

    for file in os.listdir(OUTPUT_PATH):
        os.remove(os.path.join(OUTPUT_PATH, file))

    with open(f"{OUTPUT_PATH}/{file_name}.html", "w") as output_file:
        images_paths = re.findall(r'img\ssrc=\"(.*?)\"', html_with_inline_css)
        for path in images_paths:
            path = path.replace("\\", "/")
            binary_file_content = open(f"{folder_path}/{path}", "rb").read()
            base64_utf8_str = base64.b64encode(binary_file_content).decode("utf-8")
            ext = path.split(".")[-1]
            data_url = f"data:image/{ext};base64,{base64_utf8_str}"
            html_with_inline_css = html_with_inline_css.replace(path.replace("/", "\\"), data_url)
        output_file.write(html_with_inline_css)
    