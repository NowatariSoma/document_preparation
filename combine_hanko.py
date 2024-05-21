import json
from PyPDF2 import PdfWriter, PdfReader
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from PIL import Image

def combine_images(image_path1, image_path2, space=10):
    # 画像をRGBA形式で開く
    image1 = Image.open(image_path1).convert("RGBA")
    image2 = Image.open(image_path2).convert("RGBA")

    # 画像サイズを確認し、必要に応じてリサイズ
    image2 = image2.resize(image1.size)

    # 画像を水平に結合（空白を追加）
    total_width = image1.width + image2.width + space
    max_height = max(image1.height, image2.height)

    new_image = Image.new('RGBA', (total_width, max_height), (255, 255, 255, 255))  # 白い背景、完全不透明
    new_image.paste(image1, (0, 0), image1)
    new_image.paste(image2, (image1.width + space, 0), image2)

    # 結合した画像を保存（一時ファイルとして使用）
    combined_image_path = './output/tmp/combined_image.png'  # PNG形式で保存
    new_image.save(combined_image_path)
    return combined_image_path

def marge_hanko(pdf_file_path, image, output_name):
    # 画像ファイルのパス
    buffer = BytesIO()

    # PDF新規作成
    p = canvas.Canvas(buffer, pagesize=A4)

    # 画像挿入位置とサイズ
    target_x, target_y = 160*mm,10*mm
    width = 50*mm
    height = 20*mm
    p.drawImage(image, target_x, target_y, width, height)
    p.showPage()
    p.save()

    # StringIO buffer先頭に移動
    buffer.seek(1)
    new_pdf = PdfReader(buffer)
    # 既存PDFの読み込み
    existing_pdf = PdfReader(open(pdf_file_path, 'rb'), strict=False)
    output = PdfWriter()
    
    # 既存PDFのページ数分繰り返し処理
    for i, page in enumerate(existing_pdf.pages):
        if i == 1:  # 2ページ目の場合（0ベースインデックスのため、1となる）
            page.merge_page(new_pdf.pages[0])
        output.add_page(page)

    # 出力
    output_name = "./output/output_pdf/" + output_name + ".pdf"
    output_stream = open(output_name, 'wb')
    output.write(output_stream)
    output_stream.close()

def get_sadoku():
    with open('./input/onamae/onamae.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
        
    for area, details in data.items():
        readers = details["sadoku-sha"]
        print(f"{area} の読者: {readers}")
        
        pdf_file_path = "./input/pdf/" + area + ".pdf"

        fixed_readers = ['./input/hanko/' + item + ".jpg" for item in readers]

        print(fixed_readers)

        image = combine_images(fixed_readers[0], fixed_readers[1])

        marge_hanko(pdf_file_path, image, area)

get_sadoku()