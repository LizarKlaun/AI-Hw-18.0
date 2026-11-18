import os
import fitz  # PyMuPDF

DOCS_FOLDER = "./base"
os.makedirs(DOCS_FOLDER, exist_ok=True)

pdf_documents = {
    "vanguard_architecture.pdf": (
        "Project Vanguard_1 Architecture Overview\n\n"
        "Vanguard_1 is a cross-platform desktop application built on Electron. "
        "It uses SQLite for local persistent storage, React for UI components, "
        "and Tailwind CSS for styling. The key feature is real-time data synchronization "
        "across multiple client devices."
    ),
    "mirage_ml_pipeline.pdf": (
        "Project Mirage_2 Machine Learning Pipeline\n\n"
        "Mirage_2 is an automated ML pipeline implemented in Python. "
        "It relies on scikit-learn for model training, pytest for automated unit testing, "
        "and FastAPI to expose low-latency REST endpoints with real-time data synchronization."
    ),
    "flux_golang_service.pdf": (
        "Project Flux_7 High-Load Microservice\n\n"
        "Flux_7 is a backend microservice written in Go (Golang). "
        "It integrates Redis for distributed caching, Prometheus for metrics collection, "
        "and gRPC for high-speed inter-service communication complying with enterprise standards."
    ),
    "drone_telemetry_bridge.pdf": (
        "Hardware Telemetry Bridge Specification\n\n"
        "The telemetry bridge connects a RadioMaster TX16S transmitter to a SpeedyBee F405 V3 "
        "flight controller. It uses two ESP32 microcontrollers paired with WT32-ETH01 Ethernet modules "
        "to forward control signals over SBUS and CRSF protocols."
    )
}

for filename, content in pdf_documents.items():
    file_path = os.path.join(DOCS_FOLDER, filename)
    doc = fitz.open()
    page = doc.new_page()
    # Вставляем текст с переносами строк в прямоугольную область страницы
    rect = fitz.Rect(50, 50, 545, 790)
    page.insert_textbox(rect, content, fontsize=12, fontname="helv")
    doc.save(file_path)
    doc.close()
    print(f"Created: {file_path}")

print("\nГотово! Все PDF-файлы созданы в папке ./base.")