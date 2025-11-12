import logging
from fpdf import FPDF
import os

from confidant.config import load_config_from, Config


logging.getLogger("fontTools").setLevel(logging.ERROR)


class Converter:
    @classmethod
    def _txt_to_pdf(cls, input_directory, output_directory):
        os.makedirs(output_directory, exist_ok=True)
        
        for fname in os.listdir(input_directory):
            if not fname.endswith('.txt'):
                continue
            
            pdf = FPDF()
            pdf.add_page()
            pdf.add_font(family="DejaVuSans", fname=r"fonts/DejaVuSans.ttf")
            pdf.set_font("DejaVuSans", size = 12) 
            
            input_file_path = os.path.join(input_directory, fname)
            output_file_path = os.path.join(output_directory, fname[:-4] + ".pdf")
            print(f"Converting {input_file_path} to PDF...")
            
            with open(input_file_path, encoding='utf-8') as f:
                for line in f:
                    pdf.multi_cell(0, 5, line)
            pdf.output(output_file_path)
    
    @classmethod
    def run_conversions(cls, config: Config):
        for set in config.pdf_conversions:
            if not os.path.isdir(set.input_directory):
                print(f"Invalid directory path: {set.input_directory}")
                continue
            
            cls._txt_to_pdf(set.input_directory, set.output_directory)
            print(f".txt files in {set.input_directory} converted to .pdf and saved to {set.output_directory}")
            
        print("Conversion Complete")

if __name__ == "__main__":
    config = load_config_from("config.yaml")
    Converter.run_conversions(config)