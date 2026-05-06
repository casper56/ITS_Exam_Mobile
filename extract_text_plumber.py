import pdfplumber

try:
    with pdfplumber.open("www/ITS_DataAnalytics/Data_Analytics.pdf") as pdf:
        text = ""
        for page in pdf.pages:
            t = page.extract_text()
            if t:
                text += t + "\n"
                
    with open("da_text_plumber.txt", "w", encoding="utf-8") as f:
        f.write(text)
    print("Extracted length:", len(text))
except Exception as e:
    print("Error:", e)
