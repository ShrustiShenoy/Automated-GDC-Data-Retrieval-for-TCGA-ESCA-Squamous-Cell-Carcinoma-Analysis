# Automated-GDC-Data-Retrieval-for-TCGA-ESCA-Squamous-Cell-Carcinoma-Analysis
This Python script automates bulk data retrieval from the NCI Genomic Data Commons (GDC) portal, specifically targeting:

TCGA-ESCA (Esophageal Carcinoma) project

Squamous Cell Neoplasms subtype

Open-access files in genomic data categories:Copy Number Variation and Simple Nucleotide Variation

Key Features:

✅ Smart Filtering: Excludes non-essential formats (MAF/PDF/HTML/SVS)

✅ Sanitized Downloads: Auto-renames files with illegal characters

✅ Error Handling: Skips directory collisions and API failures

✅ Transparent Logging: Real-time download tracking with success/failure indicators

#Workflow diagram

graph LR
A[GDC API Query] --> B{Filter by<br>TCGA-ESCA/Squamous}
B --> C[Exclude MAF/PDF/SVS]
C --> D[Batch Download]
D --> E[Sanitize Filenames]
E --> F[Local Storage]
