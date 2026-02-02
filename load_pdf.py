from langchain_community.document_loaders import PyPDFLoader

# Define the file path to the PDF
doc_path = r"E:\cotton_rag\document\ICAR-CICR_Advisory Pest and Disease Management 2024.pdf"

# Load the PDF using PyPDFLoader
loader = PyPDFLoader(doc_path)
documents = loader.load()

# Print number of pages and a sample page
print(f"Loaded {len(documents)} pages from PDF.")
print("Sample page content:")
print(documents[0].page_content[:500])
print("Page metadata:", documents[0].metadata)
