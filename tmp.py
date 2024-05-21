from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io

def add_page_numbers(input_pdf, output_pdf):
    # 読み込み用PDF
    reader = PdfReader(input_pdf)
    writer = PdfWriter()
    
    # 全ページに対して処理
    for page_num in range(len(reader.pages)):
        # 現在のページを取得
        page = reader.pages[page_num]
        media_box = page.mediabox

        # ページサイズを取得
        width = float(media_box.width)
        height = float(media_box.height)

        # 新しいPDFページを作成
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=(width, height))
        # ページ番号をページの中央下部に描画
        can.setFont("Times-Roman", 12)
        can.drawString(width / 2, 30, str(page_num + 1))  # ここでy座標を10に設定
        can.save()

        packet.seek(0)
        new_pdf = PdfReader(packet)
        page.merge_page(new_pdf.pages[0])
        writer.add_page(page)

    # 新しいPDFとして保存
    with open(output_pdf, 'wb') as f:
        writer.write(f)

# 使い方
input_pdf = "merged_output.pdf"  # 元のPDFファイル
output_pdf = "output_with_page_numbers.pdf"  # ページ番号を追加するPDFファイル
add_page_numbers(input_pdf, output_pdf)
