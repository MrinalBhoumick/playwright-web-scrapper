# scraper.py
from playwright.sync_api import sync_playwright
import os
import zipfile
import shutil
import csv
from fpdf import FPDF
from PIL import Image


def scrape_site(url, tags, custom_selectors=None, screenshots_folder="screenshots"):
    if os.path.exists(screenshots_folder):
        shutil.rmtree(screenshots_folder)
    os.makedirs(screenshots_folder)

    data = []
    screenshots = []
    page_number = 1

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        page.goto(url)

        while True:
            text_data = []

            for tag in tags:
                elements = page.query_selector_all(tag)
                text_data.extend([el.inner_text() for el in elements if el.inner_text()])

            if custom_selectors:
                for selector in custom_selectors:
                    elements = page.query_selector_all(selector)
                    text_data.extend([el.inner_text() for el in elements if el.inner_text()])

            data.append({
                "page": page_number,
                "text": text_data
            })

            shot_path = f"{screenshots_folder}/page_{page_number}.png"
            page.screenshot(path=shot_path, full_page=True)
            screenshots.append(shot_path)

            next_links = page.query_selector_all("a")
            clicked = False
            for link in next_links:
                text = (link.inner_text() or "").lower()
                if "next" in text or "›" in text or "»" in text:
                    try:
                        link.click()
                        page.wait_for_timeout(2000)
                        page_number += 1
                        clicked = True
                        break
                    except:
                        pass
            if not clicked:
                break

        browser.close()

    zip_filename = "screenshots.zip"
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for file in screenshots:
            zipf.write(file, os.path.basename(file))

    csv_filename = "scraped_data.csv"
    with open(csv_filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Page", "Text"])
        for entry in data:
            for text in entry["text"]:
                writer.writerow([entry["page"], text])

    per_page_pdfs = []
    for i, image_path in enumerate(screenshots, start=1):
        pdf = FPDF()
        pdf.add_page()
        pdf.image(image_path, x=10, y=10, w=190)
        pdf_path = f"{screenshots_folder}/page_{i}.pdf"
        pdf.output(pdf_path)
        per_page_pdfs.append(pdf_path)

    combined_pdf = "combined_screenshots.pdf"
    pdf = FPDF()
    for image_path in screenshots:
        pdf.add_page()
        pdf.image(image_path, x=10, y=10, w=190)
    pdf.output(combined_pdf)

    return data, screenshots, zip_filename, csv_filename, per_page_pdfs, combined_pdf


def run_scraper(url, tags, custom_selectors):
    return scrape_site(url, tags, custom_selectors)


def export_html_to_pdf(url, output_pdf_path="exported_page.pdf"):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context()
        page = context.new_page()
        page.goto(url, wait_until="networkidle")
        page.pdf(path=output_pdf_path, format="A4")
        browser.close()
    return output_pdf_path
