import os
import sys
from os.path import isdir
import shutil

from block_markdown import markdown_to_html_node



def copy_files_form_source_to_destination(source, destination):
    if os.path.exists(destination):
        destination_content = os.listdir(destination)
        if len(destination_content):
            map(
                lambda x: shutil.rmtree(os.path.join(destination, x)),
                destination_content,
            )
    else:
        os.mkdir(destination)
    content_of_source = os.listdir(source)
    for content in content_of_source:
        destination_content_path = os.path.join(destination, content)
        source_content_path = os.path.join(source, content)
        if os.path.isfile(source_content_path):
            shutil.copy(source_content_path, destination_content_path)
        else:
            copy_files_form_source_to_destination(
                source_content_path, destination_content_path
            )


def extract_title(markdown):
    h1_headings = list(filter(lambda x: x.startswith("# "), markdown.split("\n")))
    if len(h1_headings):
        return h1_headings[0].strip().replace("# ", "")
    raise Exception("Markdown file does not contain any headers.")


def generate_page(base_path, from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown_file = open(from_path, "r").read()
    template_file = open(template_path, "r").read()
    HTML_string = markdown_to_html_node(markdown_file).to_html()
    page_title = extract_title(markdown_file)
    new_Html_page = template_file.replace("{{ Title }}", page_title).replace(
        "{{ Content }}", HTML_string
    )
    new_Html_page.replace("href='/", f"href='{base_path}").replace(
        "src='/", f"src='{base_path}"
    )
    for directory in dest_path.split(os.sep):
        path = ""
        if directory and not os.path.exists(directory) and not directory.split(".")[0]:
            os.mkdir(os.path.join(path, directory))
    open(".".join(dest_path.split(".")[:-1] + ["html"]), "w").write(new_Html_page)


def generate_pages_recursive(base_path, dir_path_content, template_path, dest_dir_path):
    for content in os.listdir(dir_path_content):
        dir_content_path = os.path.join(dir_path_content, content)
        dest_content_dir_path = os.path.join(dest_dir_path, content)
        if (
            not os.path.isdir(dir_content_path)
            and dir_content_path.split(".")[-1] == "md"
        ):
            generate_page(
                base_path, dir_content_path, template_path, dest_content_dir_path
            )
        if os.path.isdir(dir_content_path):
            os.mkdir(dest_content_dir_path)
            generate_pages_recursive(
                base_path, dir_content_path, template_path, dest_content_dir_path
            )


def main():
    base_path = ""
    if len(sys.argv) > 1:
        base_path = sys.argv[1]
    else:
        base_path = "/"
    base_path_start = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "..",
    )
    public_dir_path = os.path.join(base_path_start, "docs")
    if not os.path.exists(public_dir_path):
        os.mkdir(public_dir_path)
    else:
        for content in os.listdir(public_dir_path):
            content_path = os.path.join(public_dir_path, content)
            if os.path.isdir(content_path):
                shutil.rmtree(content_path)
                continue
            os.remove(content_path)
    copy_files_form_source_to_destination(
        os.path.join(base_path_start, "static"), public_dir_path
    )
    generate_pages_recursive(
        base_path,
        os.path.join(base_path_start, "content"),
        os.path.join(base_path_start, "template.html"),
        os.path.join(base_path_start, "docs"),
    )


if __name__ == "__main__":
    main()
