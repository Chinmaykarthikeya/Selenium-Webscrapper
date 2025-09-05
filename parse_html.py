import os
import re
from bs4 import BeautifulSoup as Bs
import pandas as pd

def clean_money(text):
    # Remove non-digits except period, then strip
    if not text:
        return ""
    t = text.replace(",", "")
    t = t.replace("₹", "").replace("â‚¹", "")
    t = re.sub(r"[^\d.]", "", t)
    return t

def clean_percent(text):
    if not text:
        return ""
    # Common formats: "25% off", "25% OFF", "25% "
    m = re.search(r"(\d+)\s*%+", text)
    return m.group(1) if m else text.strip()

def get_text_or_none(tag):
    return tag.get_text(strip=True) if tag else None

parsed_data = {
    "Product_Name": ["Product_Name"],
    "MRP": ["Retail Price"],
    "DSP": ["Discounted Price"],
    "Discount": ["Discount Percentage"],
    "Ratings": ["Total Ratings"],
    "Reviews": ["Total Reviews"],
    "RAMGB": ["RAM GB"],
    "ROMGB": ["ROM GB"],
    "Warranty": ["Warranty in Years"],
}

i = 0
data_dir = "data"

for file in os.listdir(data_dir):
    if file.lower().endswith(".html"):
        file_path = os.path.join(data_dir, file)
        with open(file_path, "r", encoding="utf-8") as f:
            html_doc = f.read()

        soup = Bs(html_doc, "html.parser")

        # Find elements with guards
        title_tag = soup.find("div", class_="KzDlHZ")
        mrp_tag = soup.find("div", class_="yRaY8j")
        dsp_tag = soup.find("div", class_="Nx9bqj")
        discount_tag = soup.find("div", class_="UkUFwK")
        ratings_reviews_tag = soup.find("span", class_="Wphh3N")  # may be None

        # Extract/clean values with fallbacks
        title = get_text_or_none(title_tag)
        if title:
            title = title.strip()
            if title.endswith("..."):
                title = title[:-3]

        mrp = clean_money(get_text_or_none(mrp_tag))
        dsp = clean_money(get_text_or_none(dsp_tag))
        discount = clean_percent(get_text_or_none(discount_tag))

        # Ratings & Reviews parsing
        ratings = ""
        reviews = ""
        rr_text = get_text_or_none(ratings_reviews_tag)
        # Example format: "8,310 Ratings & 475 Reviews"
        if rr_text:
            m = re.search(r"([\d,]+)\s*Ratings\s*&\s*([\d,]+)\s*Reviews", rr_text, flags=re.I)
            if m:
                ratings = m.group(1).replace(",", "")
                reviews = m.group(2).replace(",", "")
            else:
                # If only ratings or a different format, keep the raw text or try simpler parses
                # Attempt single number before "Ratings"
                m2 = re.search(r"([\d,]+)\s*Ratings", rr_text, flags=re.I)
                if m2:
                    ratings = m2.group(1).replace(",", "")
                m3 = re.search(r"([\d,]+)\s*Reviews", rr_text, flags=re.I)
                if m3:
                    reviews = m3.group(1).replace(",", "")

        # Bullet features list
        feature_items = soup.find_all("li", class_="J+igdf")
        ram_gb = ""
        rom_gb = ""
        warranty_years = ""

        # Be defensive about indexes; classes and order may change
        # If you know the labels inside the li text, match by keywords instead of raw indexes:
        for li in feature_items:
            txt = li.get_text(" ", strip=True)
            # Examples to adjust based on real content:
            if "RAM" in txt and "GB" in txt and not ram_gb:
                m = re.search(r"(\d+)\s*GB", txt, flags=re.I)
                if m:
                    ram_gb = m.group(1)
            if ("SSD" in txt or "Storage" in txt) and "GB" in txt and not rom_gb:
                m = re.search(r"(\d+)\s*GB", txt, flags=re.I)
                if m:
                    rom_gb = m.group(1)
            if "Warranty" in txt and not warranty_years:
                m = re.search(r"(\d+)\s*Year", txt, flags=re.I)
                if m:
                    warranty_years = m.group(1)

        # Append row (use empty strings for missing)
        parsed_data["Product_Name"].append(title or "")
        parsed_data["MRP"].append(mrp or "")
        parsed_data["DSP"].append(dsp or "")
        parsed_data["Discount"].append(discount or "")
        parsed_data["Ratings"].append(ratings or "")
        parsed_data["Reviews"].append(reviews or "")
        parsed_data["RAMGB"].append(ram_gb or "")
        parsed_data["ROMGB"].append(rom_gb or "")
        parsed_data["Warranty"].append(warranty_years or "")

        i += 1

# Save to CSV
df = pd.DataFrame(parsed_data)
df.to_csv("parsed_data.csv", index=False)
print(f"Wrote {i} rows to parsed_data.csv")
