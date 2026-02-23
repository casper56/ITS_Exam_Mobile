import sys
import subprocess
try:
    import reportlab
    from PIL import Image
except ImportError:
    print('[-] 偵測到缺少必要套件：reportlab 或 Pillow')
    print(f'[!] 正在嘗試為您安裝至目前的 Python 環境 ({sys.executable})...')
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'reportlab', 'Pillow'])
        print('[+] 安裝完成，請重新執行腳本。')
    except Exception as e:
        print(f'[X] 自動安裝失敗: {e}')
        print(f'[!] 請手動執行: {sys.executable} -m pip install reportlab Pillow')
    sys.exit(0)

import json
import os
import re
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as ReportLabImage
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from PIL import Image as PILImage

def clean_html(text, code_font="Courier"):
    if not text:
        return ""
    
    # 1. Handle code blocks and pre tags
    # We want the content inside, but formatted for ReportLab.
    def format_code(match):
        code = match.group(1)
        # Strip any nested tags if they exist (sometimes <code> contains <span>)
        code = re.sub(r'<[^>]+>', '', code)
        # Escape XML entities for ReportLab
        code = code.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        # Convert newlines for PDF
        code = code.replace('\n', '<br/>')
        # Preserve leading spaces for indentation
        code = code.replace('  ', '&nbsp;&nbsp;')
        # Use the passed code_font (which should support Chinese)
        return f'<br/><font name="{code_font}" size="9" color="#333333">{code}</font><br/>'

    # Capture content between <pre...><code>...</code></pre> or just <code>...</code>
    # This specifically removes the <code> tag itself from the output.
    text = re.sub(r'<(?:pre|code)[^>]*>(.*?)</(?:pre|code)>', format_code, text, flags=re.DOTALL)

    # 2. General cleanup
    # Standardize breaks
    text = re.sub(r'<br\s*/?>', '<br/>', text, flags=re.IGNORECASE)
    
    # Ensure "●" starts on a new line
    text = text.replace('●', '<br/>●')

    # Final pass: Strip ALL remaining tags except the ones ReportLab supports
    # Allowed: b, i, u, font, br
    # This regex removes any tag that isn't in our allowed list.
    tag_pattern = r'<(?!/?(?:b|i|u|font|br)\b)[^>]+>'
    text = re.sub(tag_pattern, '', text)

    # Clean up multiple consecutive breaks if they occur
    text = text.replace('<br/><br/><br/>', '<br/><br/>')
    
    return text.strip()

def create_pdf(json_file, output_pdf):
    # Register Chinese Font
    # Try multiple common paths for Chinese fonts on Windows
    possible_fonts = [
        "C:\\Windows\\Fonts\\msyh.ttc",
        "C:\\Windows\\Fonts\\msyhl.ttc",
        "C:\\Windows\\Fonts\\simsun.ttc",
        "C:\\Windows\\Fonts\\kaiu.ttf"
    ]
    
    font_name = 'Helvetica' # Default fallback
    for font_path in possible_fonts:
        if os.path.exists(font_path):
            try:
                # Microsoft YaHei (msyh) often has multiple faces. 'MicrosoftYaHei' usually works for the regular one.
                # If using TTC, we might need to specify valid index or just register it.
                pdfmetrics.registerFont(TTFont('ChineseFont', font_path))
                font_name = 'ChineseFont'
                break
            except Exception as e:
                print(f"Failed to load font {font_path}: {e}")

    # Load JSON data
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading JSON file {json_file}: {e}")
        return

    doc = SimpleDocTemplate(output_pdf, pagesize=A4,
                            rightMargin=50, leftMargin=50,
                            topMargin=50, bottomMargin=50)

    styles = getSampleStyleSheet()
    
    # Define styles with Chinese font support
    # Ensure Heading2 and Normal use the Chinese font
    styles['Heading2'].fontName = font_name
    styles['Normal'].fontName = font_name
    
    if 'Question' not in styles:
        styles.add(ParagraphStyle(name='Question', parent=styles['Heading2'], fontName=font_name, fontSize=11, spaceAfter=6, leading=14))
    if 'Option' not in styles:
        styles.add(ParagraphStyle(name='Option', parent=styles['Normal'], fontName=font_name, fontSize=10, leftIndent=20, spaceAfter=1, leading=12))
    if 'Answer' not in styles:
        styles.add(ParagraphStyle(name='Answer', parent=styles['Normal'], fontName=font_name, fontSize=10, textColor=colors.blue, spaceBefore=3, spaceAfter=3))
    if 'Explanation' not in styles:
        styles.add(ParagraphStyle(name='Explanation', parent=styles['Normal'], fontName=font_name, fontSize=10, textColor=colors.darkgreen, spaceAfter=2))
    if 'NormalChinese' not in styles:
        styles.add(ParagraphStyle(name='NormalChinese', parent=styles['Normal'], fontName=font_name, fontSize=10))

    story = []

    for item in data:
        # Question
        q_text = item.get('question', '')
        q_text = clean_html(q_text, code_font=font_name)
        story.append(Paragraph(f"<b>{q_text}</b>", styles['Question']))

        # Image
        image_path = item.get('image')
        if image_path:
            # Handle both absolute and relative paths
            if os.path.isabs(image_path):
                full_image_path = image_path
            else:
                full_image_path = os.path.join(os.path.dirname(json_file), image_path)
            
            if os.path.exists(full_image_path):
                try:
                    with PILImage.open(full_image_path) as pi:
                        w, h = pi.size
                        aspect = h / float(w)
                        display_width = 400
                        display_height = display_width * aspect
                    img = ReportLabImage(full_image_path, width=display_width, height=display_height)
                    story.append(img)
                    story.append(Spacer(1, 5))
                except Exception as e:
                    story.append(Paragraph(f"[Could not load image: {image_path}]", styles['NormalChinese']))
        
        # Options / Quiz
        # Check for 'quiz' field as per user request, fallback to 'options'
        options = item.get('quiz') or item.get('options', [])
        
        if options:
            story.append(Paragraph("<b>Quiz:</b>", styles['NormalChinese']))

        # Check if we have pipe-separated options (complex question)
        is_complex_options = False
        parsed_options = []

        for idx, opt in enumerate(options):
            opt_str = str(opt)
            if '|' in opt_str:
                is_complex_options = True
                # Split and format: "int|string|float" -> "(1) int (2) string (3) float"
                sub_opts = opt_str.split('|')
                formatted_sub = "  ".join([f"({i+1}) {val.strip()}" for i, val in enumerate(sub_opts)])
                # Changed from "Blank X" to "X." as requested
                display_text = f"{idx + 1}. {formatted_sub}"
                parsed_options.append((opt_str, sub_opts)) # Store for answer mapping
                story.append(Paragraph(display_text, styles['Option']))
            else:
                parsed_options.append((opt_str, None))
                opt_text = clean_html(opt_str, code_font=font_name)
                story.append(Paragraph(f"{idx + 1}. {opt_text}", styles['Option']))
        
        # Answer
        answers = item.get('answer', [])
        if not isinstance(answers, list):
            answers = [answers]

        answer_display = []
        
        if is_complex_options:
            # Map indices back to values
            # Ensure we have enough options for the answers
            for i, ans_idx in enumerate(answers):
                if i < len(parsed_options):
                    original_str, sub_opts = parsed_options[i]
                    if sub_opts:
                        # ans_idx is likely 1-based index into sub_opts
                        try:
                            # Convert to int if it's a string digit
                            idx_val = int(ans_idx)
                            if 0 < idx_val <= len(sub_opts):
                                val = sub_opts[idx_val - 1]
                                # Changed from "Blank i" to "i."
                                answer_display.append(f"{i+1}: {val} ({idx_val})")
                            else:
                                answer_display.append(f"{i+1}: {ans_idx} (Invalid Index)")
                        except ValueError:
                            answer_display.append(f"{i+1}: {ans_idx}")
                    else:
                        answer_display.append(str(ans_idx))
                else:
                    answer_display.append(str(ans_idx))
            ans_str = ", ".join(answer_display)
        else:
            ans_str = ", ".join(str(a) for a in answers)

        story.append(Paragraph(f"<b>Answer:</b> {ans_str}", styles['Answer']))

        # Explanation
        explanation = item.get('explanation')
        if explanation:
            explanation = clean_html(explanation, code_font=font_name)
            story.append(Paragraph(f"<b>Explanation:</b><br/>{explanation}", styles['Explanation']))

        story.append(Spacer(1, 10))
        story.append(Paragraph("<hr color='silver' width='100%'/>", styles['Normal']))
        story.append(Spacer(1, 10))

    try:
        doc.build(story)
        print(f"Successfully created {output_pdf}")
    except Exception as e:
        print(f"Error building PDF {output_pdf}: {e}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 2:
        create_pdf(sys.argv[1], sys.argv[2])
    else:
        # Default behavior if run without args
        create_pdf('questions_Generative_AI_Foundations.json', 'questions_Generative_AI_Foundations.pdf')