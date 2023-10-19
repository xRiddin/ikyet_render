import os
from typing import Dict, Generator
from urllib.parse import quote

from md2pdf.core import md2pdf

from ..gpt_rev import generate as ge


def split_text(text: str, max_length: int = 8192) -> Generator[str, None, None]:
    paragraphs = text.split("\n")
    current_length = 0
    current_chunk = []

    for paragraph in paragraphs:
        if current_length + len(paragraph) + 1 <= max_length:
            current_chunk.append(paragraph)
            current_length += len(paragraph) + 1
        else:
            yield "\n".join(current_chunk)
            current_chunk = [paragraph]
            current_length = len(paragraph) + 1

    if current_chunk:
        yield "\n".join(current_chunk)


async def summarize_text(url: str, text: str, question: str, page=None) -> str:
    if not text:
        return "Error: No text to summarize"

    summaries = []
    chunks = list(split_text(text))
    scroll_ratio = 1 / len(chunks)

    for i, chunk in enumerate(chunks):
        if page:
            await scroll_to_percentage(page, scroll_ratio * i)

        memory_to_add = f"Source: {url}\n" f"Raw content part#{i + 1}: {chunk}"

        messages = [create_message(chunk, question)]

        summary = ge(
            model='gpt-3.5-turbo-16k',
            messages=messages,
        )
        summaries.append(summary)
        memory_to_add = f"Source: {url}\n" f"Content summary part#{i + 1}: {summary}"

    combined_summary = "\n".join(summaries)
    messages = [create_message(combined_summary, question)]
    ans = ge(
        model='gpt-3.5-turbo-16k',
        messages=messages,
    )

    await page.close()

    return ans


async def scroll_to_percentage(page, ratio: float) -> None:
    if ratio < 0 or ratio > 1:
        raise ValueError("Percentage should be between 0 and 1")
    await page.evaluate(f"window.scrollTo(0, document.body.scrollHeight * {ratio});")


def create_message(chunk: str, question: str) -> Dict[str, str]:
    return {
        "role": "user",
        "content": f'"""{chunk}""" Using the above text, answer the following'
                   f' question: "{question}" -- if the question cannot be answered using the text,'
                   " simply summarize the text in depth. "
                   "Include all factual information, numbers, stats etc if available.",
    }


async def write_to_file(filename: str, text: str) -> None:
    with open(filename, "w") as file:
        file.write(text)


async def write_md_to_pdf(task: str, directory_name: str, text: str) -> str:
    file_path = f"{directory_name}/{task}"
    await write_to_file(f"{file_path}.md", text)
    md_to_pdf(f"{file_path}.md", f"{file_path}.pdf")
    print(f"{task} written to {file_path}.pdf")

    encoded_file_path = quote(f"{file_path}.pdf")

    return encoded_file_path


async def read_txt_files(directory):
    all_text = ''

    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            with open(os.path.join(directory, filename), 'r') as file:
                all_text += file.read() + '\n'

    return all_text


def md_to_pdf(input_file, output_file):
    md2pdf(output_file,
           md_content=None,
           md_file_path=input_file,
           css_file_path=None,
           base_url=None)
