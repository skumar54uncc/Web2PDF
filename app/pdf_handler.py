import os
import csv
import re
import asyncio
import aiohttp
import requests
from urllib.parse import urlparse
from zipfile import ZipFile
from playwright.async_api import async_playwright




BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)




def sanitize_title(title: str) -> str:
    return "".join(c if c.isalnum() or c in (' ', '-', '_') else "_" for c in title).strip().replace(" ", "_")[:60] or "untitled"




async def download_pdf_direct(link, index):
    try:
        filename = f"{index:02d}_direct_download.pdf"
        pdf_path = os.path.join(OUTPUT_DIR, filename)
        async with aiohttp.ClientSession() as session:
            async with session.get(link) as resp:
                if resp.status == 200:
                    with open(pdf_path, 'wb') as f:
                        f.write(await resp.read())
                    print(f"[✓] Direct PDF saved: {filename}")
                    return (link, "Direct PDF Download", filename, "success")
        return (link, "", "", "failure")
    except Exception as e:
        print(f"[!] Error downloading direct PDF: {e}")
        return (link, "", "", "failure")




def extract_links_from_google_doc_text(url):
    match = re.search(r"/document/d/([a-zA-Z0-9_-]+)", url)
    if not match:
        return []
    doc_id = match.group(1)
    export_url = f"https://docs.google.com/document/d/{doc_id}/export?format=txt"
    try:
        response = requests.get(export_url)
        response.raise_for_status()
        text_content = response.text
        links = re.findall(r"https?://[^\s)>\"']+", text_content)
        return list(set(links))
    except Exception as e:
        print(f"Failed to fetch Google Doc: {e}")
        return []




async def render_and_save_pdf(link, index, browser):
    try:
        if link.lower().endswith(".pdf"):
            return await download_pdf_direct(link, index)




        context = await browser.new_context()
        page = await context.new_page()
        await page.goto(link, timeout=60000)




        # Try common cookie acceptance buttons
        try:
            buttons = page.locator("button", has_text=re.compile(r"(accept all|agree|consent|allow|got it|okay)", re.I))
            await buttons.first.click(timeout=3000)
            print("[~] Cookie banner accepted.")
        except:
            pass




        title = await page.title()
        if "Just a moment" in title or "Verify you are human" in (await page.content()):
            await context.close()
            return "cloudflare_detected"




        await page.evaluate("""() => {
            return new Promise(resolve => {
                let totalHeight = 0;
                const distance = 500;
                const timer = setInterval(() => {
                    const scrollHeight = document.body.scrollHeight;
                    window.scrollBy(0, distance);
                    totalHeight += distance;
                    if (totalHeight >= scrollHeight) {
                        clearInterval(timer);
                        resolve();
                    }
                }, 300);
            });
        }""")




        try:
            await page.locator("text=Read more,Load more,Show more,Expand").first.click(timeout=2000)
        except:
            pass




        # Save preview screenshot
        screenshot_name = f"{index:02d}_preview.png"
        screenshot_path = os.path.join(OUTPUT_DIR, screenshot_name)
        await page.screenshot(path=screenshot_path, full_page=True)




        title = await page.title()
        short_title = sanitize_title(title)
        filename = f"{index:02d}_{short_title}.pdf"
        pdf_path = os.path.join(OUTPUT_DIR, filename)
        await page.pdf(path=pdf_path, format="A4")
        await context.close()




        if os.path.exists(pdf_path):
            print(f"[✓] Rendered PDF saved: {filename}")
            return (link, title, filename, "success")
        else:
            print(f"[!] PDF not found after saving: {filename}")
            return (link, title, "", "failure")




    except Exception as e:
        print(f"[!] Error on {link}: {e}")
        return (link, "", "", "failure")




async def process_links_to_pdf(links):
    results = []




    # Expand Google Docs links first
    expanded_links = []
    for link in links:
        if "docs.google.com/document" in link:
            print(f"[~] Google Doc detected: {link}. Extracting links...")
            extracted = extract_links_from_google_doc_text(link)
            print(f"[+] Found {len(extracted)} links inside the doc.")
            expanded_links.extend(extracted)
        else:
            expanded_links.append(link)




    async with async_playwright() as p:
        headless_browser = await p.chromium.launch(headless=True)
        headful_browser = await p.chromium.launch(headless=False)




        async def handle_link(link, idx):
            print(f"[{idx}] Processing: {link}")
            result = await render_and_save_pdf(link, idx, headless_browser)
            if result == "cloudflare_detected":
                print(f"[~] Cloudflare detected on link {link}. Switching to headful mode.")
                result = await render_and_save_pdf(link, idx, headful_browser)
            return result




        tasks = [handle_link(link, idx) for idx, link in enumerate(expanded_links, 1)]
        results = await asyncio.gather(*tasks)




        await headless_browser.close()
        await headful_browser.close()




    csv_path = os.path.join(OUTPUT_DIR, "log.csv")
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Link", "Title", "Filename", "Status"])
        for row in results:
            if isinstance(row, tuple) and len(row) == 4:
                writer.writerow(row)




    zip_path = os.path.join(OUTPUT_DIR, "all_pdfs.zip")
    with ZipFile(zip_path, 'w') as zipf:
        for row in results:
            if isinstance(row, tuple) and len(row) == 4:
                _, _, fname, _ = row
                if fname:
                    fpath = os.path.join(OUTPUT_DIR, fname)
                    if os.path.exists(fpath):
                        zipf.write(fpath, arcname=fname)
        if os.path.exists(csv_path):
            zipf.write(csv_path, arcname="log.csv")




    print(f"[✓] All done. ZIP created at: {zip_path}")
    return zip_path