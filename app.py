import streamlit as st
from scraper import run_scraper
from PIL import Image

st.set_page_config(page_title="Full Web Scraper", layout="wide")
st.title("🕷️ Advanced Web Scraper with Playwright")

url = st.text_input("Enter Website URL", "https://example.com")

tags = st.multiselect(
    "Select standard HTML tags to scrape",
    ["h1", "h2", "h3", "p", "a", "div", "span"],
    default=["h1", "p"]
)

custom_selectors_input = st.text_input("Custom CSS selectors (comma-separated)", "")
custom_selectors = [s.strip() for s in custom_selectors_input.split(",") if s.strip()]

if st.button("Start Scraping"):
    with st.spinner("Scraping in progress..."):
        try:
            data, screenshots, zip_path, csv_path, per_page_pdfs, combined_pdf = run_scraper(url, tags, custom_selectors)
            st.success("✅ Scraping Complete!")

            st.subheader("🔍 Text Content")
            for page in data:
                st.markdown(f"### 📄 Page {page['page']}")
                for text in page['text']:
                    st.write(f"- {text}")

            st.subheader("🖼️ Screenshots")
            for shot in screenshots:
                st.image(Image.open(shot), caption=shot, use_container_width=True)

            st.subheader("⬇️ Downloads")

            with open(zip_path, "rb") as f:
                st.download_button("📦 Download Screenshots ZIP", f, file_name="screenshots.zip")

            with open(csv_path, "rb") as f:
                st.download_button("📄 Download Scraped Text CSV", f, file_name="scraped_data.csv")

            with open(combined_pdf, "rb") as f:
                st.download_button("📕 Download Combined PDF", f, file_name="combined_screenshots.pdf")

            for i, pdf in enumerate(per_page_pdfs, start=1):
                with open(pdf, "rb") as f:
                    st.download_button(f"📄 Download Page {i} PDF", f, file_name=f"page_{i}.pdf")

        except Exception as e:
            st.error(f"❌ Error: {e}")
