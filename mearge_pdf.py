import os
import PyPDF2
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
import io

def merge_pdfs(input_directory):
    merger = PyPDF2.PdfMerger()

    for filename in sorted(os.listdir(input_directory)):
        if filename.endswith('.pdf'):
            input_pdf_path = os.path.join(input_directory, filename)
            merger.append(input_pdf_path)
            print(f"Added {input_pdf_path} to the merger")

    # メモリに一時ファイルとして保存
    temp_pdf_stream = io.BytesIO()
    merger.write(temp_pdf_stream)
    temp_pdf_stream.seek(0)  # ストリームの先頭に移動
    return temp_pdf_stream

def add_page_numbers(input_pdf_stream, output_pdf_path):
    # 読み込み用PDF
    reader = PdfReader(input_pdf_stream)
    writer = PdfWriter()
    
    # 全ページに対して処理
    for page_num, page in enumerate(reader.pages, start=1):
        media_box = page.mediabox
        width = float(media_box.width)
        height = float(media_box.height)

        # 新しいPDFページを作成
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=(width, height))
        # ページ番号をページの中央下部に描画
        can.setFont("Times-Roman", 12)
        can.drawString(width / 2, 30, str(page_num))
        can.save()

        packet.seek(0)
        new_pdf = PdfReader(packet)
        page.merge_page(new_pdf.pages[0])
        writer.add_page(page)

    # 新しいPDFとして保存
    with open(output_pdf_path, 'wb') as f:
        writer.write(f)

# 使用例
base_directory = '.'  # ベースディレクトリのパス
input_directory = os.path.join(base_directory, 'output')  # 入力ディレクトリのパス
output_pdf_path = os.path.join(base_directory, 'numbered_output.pdf')  # 出力PDFファイルのパス

# PDFを結合してページ番号を追加
merged_pdf_stream = merge_pdfs(input_directory)
add_page_numbers(merged_pdf_stream, output_pdf_path)
