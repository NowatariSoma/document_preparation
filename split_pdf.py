import os
import PyPDF2

def split_pdf(input_pdf_path, output_dir):
    with open(input_pdf_path, 'rb') as infile:
        reader = PyPDF2.PdfReader(infile)
        num_pages = len(reader.pages)

        base_filename = os.path.basename(input_pdf_path)
        base_filename_without_ext = os.path.splitext(base_filename)[0]

        for i in range(num_pages):
            writer = PyPDF2.PdfWriter()
            writer.add_page(reader.pages[i])

            output_pdf_path = os.path.join(output_dir, f"{base_filename_without_ext}_page_{i + 1}.pdf")
            with open(output_pdf_path, 'wb') as outfile:
                writer.write(outfile)
            print(f"Page {i + 1} saved as {output_pdf_path}")

def split_all_pdfs_in_directory(input_directory, output_directory):
    if not os.path.exists(input_directory):
        os.makedirs(input_directory)
        print(f"Created input directory: {input_directory}")
    
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
        print(f"Created output directory: {output_directory}")
        
    for filename in os.listdir(input_directory):
        if filename.endswith('.pdf'):
            input_pdf_path = os.path.join(input_directory, filename)
            split_pdf(input_pdf_path, output_directory)



# 使用例
base_directory = '.'  # ベースディレクトリのパス
input_directory = os.path.join(base_directory, 'input')  # 入力ディレクトリのパス
output_directory = os.path.join(base_directory, 'output')  # 出力ディレクトリのパス

split_all_pdfs_in_directory(input_directory, output_directory)
