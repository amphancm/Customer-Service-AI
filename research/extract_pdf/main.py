import fitz
from multiprocessing import Pool
import math
import os
from flask import Flask, request, jsonify
import tempfile
import pytesseract
from PIL import Image
# Load OCR pipeline once globally
# pipe = pipeline("image-to-text", model="scb10x/typhoon-ocr-7b")

def simple_ocr(image_path, lang="tha"):
    """
    Perform OCR on the given image using pytesseract.
    Returns the extracted text.
    """
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img, lang=lang)
        return text
    except Exception as e:
        print(f"OCR error: {e}")
        return ""


def create_page_chunks(total_pages, chunk_count):
    base_pages = total_pages // chunk_count
    remainder = total_pages % chunk_count
    pages_per_chunk_list = (base_pages + 1 if i < remainder else base_pages for i in range(chunk_count))

    current_page = 0
    for pages_in_chunk in pages_per_chunk_list:
        start = current_page
        end = min(current_page + pages_in_chunk, total_pages)
        yield (start, end)
        current_page = end


def render_pages(args):
    import fitz
    import os
    import tempfile

    pdf_path, page_range = args
    start, end = page_range
    doc = fitz.open(pdf_path)
    os.makedirs("txt", exist_ok=True)

    for i in range(start, end):
        try:
            page = doc[i]
            print(doc[i])
            pix = page.get_pixmap(dpi=200)

            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file:
                pix.save(temp_file.name)
                temp_image_path = temp_file.name

            try:
                
                # Use the pipeline directly for OCR
                #result = pipe(temp_image_path)[0]['generated_text']
                # print(temp_image_path)
                simple_ocr_result = simple_ocr(temp_image_path)
                

                filename = f"txt/page_{i+1:03d}.txt"
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(simple_ocr_result)
                print(f"Saved OCR result for page {i+1} to {filename}")

            finally:
                if os.path.exists(temp_image_path):
                    os.unlink(temp_image_path)

        except Exception as e:
            print(f"Error processing page {i+1}: {str(e)}")

    doc.close()

    

app = Flask(__name__)

@app.route("/extract", methods=["POST"])
def extract():
    data = request.json
    pdf_path = data.get("pdf_path")
    if not pdf_path:
        return jsonify({"error": "Missing pdf_path"}), 400
    default_processes = os.cpu_count() or 1
    processes = int(data.get("processes", default_processes))
    desired_chunk_count = int(data.get("chunk_count", 5))

    doc = fitz.open(pdf_path)
    total_pages = doc.page_count
    doc.close()
    # Get sorted list of chunks by start page
    chunks = list(create_page_chunks(total_pages, desired_chunk_count))
    chunks.sort(key=lambda x: x[0])  # Sort by start page
    
    

    # Print chunk ranges for debugging
    print("Processing chunks:")
    for start, end in chunks:
        print(f"Chunk: pages {start+1}-{end}")

    args = [(pdf_path, chunk) for chunk in chunks]
    #print(args)
    with Pool(processes=processes) as pool:
        pool.map(render_pages, args)
        
    # Merge all txt/page_*.txt files into one file, sorted by page number
    output_file = "merged_output.txt"
    txt_dir = "txt"
    page_files = sorted(
        [f for f in os.listdir(txt_dir) if f.startswith("page_") and f.endswith(".txt")],
        key=lambda x: int(x.split("_")[1].split(".")[0])
    )
    with open(output_file, "w", encoding="utf-8") as outfile:
        for fname in page_files:
            with open(os.path.join(txt_dir, fname), "r", encoding="utf-8") as infile:
                outfile.write(infile.read())
                outfile.write("\n")
    print(f"Merged output written to {output_file}")
    return jsonify({"status": "done", "pages": total_pages, "processes_used": processes})



# def extract():
#     data = request.json
#     pdf_path = data.get("pdf_path")
#     if not pdf_path:
#         return jsonify({"error": "Missing pdf_path"}), 400
#     default_processes = os.cpu_count() or 1
#     processes = int(data.get("processes", default_processes))
#     desired_chunk_count = int(data.get("chunk_count", 4))

#     doc = fitz.open(pdf_path)
#     total_pages = doc.page_count
#     doc.close()
#     chunks = create_page_chunks(total_pages, desired_chunk_count)
#     args = ((pdf_path, chunk) for chunk in chunks)
#     with Pool(processes=processes) as pool:
#         pool.map(render_pages, args)
#     return jsonify({"status": "done", "pages": total_pages, "processes_used": processes})

if __name__ == "__main__":
    app.run(port=1150)