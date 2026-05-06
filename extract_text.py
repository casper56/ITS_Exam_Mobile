import fitz
doc = fitz.open("www/ITS_DataAnalytics/Data_Analytics.pdf")
text = ""
for page in doc:
    text += page.get_text()
with open("da_text.txt", "w", encoding="utf-8") as f:
    f.write(text)
