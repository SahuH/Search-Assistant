# 🏠 Real Estate Search Assistant — Dubai Edition

This project is an LLM-powered **conversational assistant** that helps users search for properties in **Dubai** using natural language queries. It leverages a combination of **retrieval-based search (RAG)** and **GPT-4 reasoning** to return semantically relevant listings and explain tradeoffs, amenities, locations, and more.

---

## 📦 Dataset Source

We use the **open-source property listings dataset** provided by **AirROI**:

🔗 **[https://www.airroi.com/data-portal/markets/dubai-united-arab-emirates](https://www.airroi.com/data-portal/markets/dubai-united-arab-emirates)**

> 📢 _All credit for the data goes to the AirROI team. This project uses the publicly available listings data for research and prototyping purposes only._

---

## 🧾 Dataset: `Listings Data` Schema

Below is the schema of the **Dubai Property Listings** dataset from AirROI:

| Column Name             | Description                                                      |
|-------------------------|------------------------------------------------------------------|
| `id`                   | Unique listing identifier                                         |
| `scraped_at`           | Timestamp when data was collected                                |
| `title`                | Short title or summary of the listing                            |
| `description`          | Long text with property details                                  |
| `price`                | Price of the property (in AED)                                   |
| `bedrooms`             | Number of bedrooms                                               |
| `bathrooms`            | Number of bathrooms                                              |
| `area`                 | Size of the property in square feet                              |
| `location`             | Area / community name (e.g., Business Bay, Dubai Marina, etc.)   |
| `latitude`             | Geo coordinate (optional for spatial filtering)                  |
| `longitude`            | Geo coordinate (optional for spatial filtering)                  |
| `property_type`        | Apartment, villa, townhouse, etc.                                |
| `amenities`            | Text list of features (e.g., gym, pool, parking)                 |
| `developer`            | Name of developer (if available)                                 |
| `status`               | Availability (e.g., ready, off-plan, under construction)         |
| `furnishing`           | Furnishing status (e.g., furnished, semi-furnished, unfurnished) |
| `completion_status`    | Completed, Off-plan, etc.                                        |
| `image_url`            | Representative image                                             |
| `listing_url`          | External link to full property page                              |
| `source`               | Portal where it was listed (e.g., Bayut, PropertyFinder, etc.)   |

---

## 🔍 Project Overview

The assistant supports queries like:

> "Find me a 2-bedroom furnished apartment near Burj Khalifa under 3M AED with a balcony and gym access."

The assistant:
1. Parses the query
2. Retrieves semantically relevant listings using vector search (ChromaDB)
3. Feeds them into GPT-4 for reasoning and explanation
4. Returns top recommendations in natural language

---

## 🔧 Tech Stack

- **LangChain** (RAG pipeline)
- **ChromaDB** (vector store)
- **OpenAI GPT-4 API** (LLM engine)
- **FastAPI / Streamlit** (UI wrapper or REST backend)
- **BigQuery / Pandas** (data ingestion + optional analytics)
- **Kubernetes (GKE)** (deployment)

---

## ✅ Next Steps

- [ ] Data Ingestion + Cleaning
- [ ] Embedding & Vector Store Creation
- [ ] RAG Chain Construction
- [ ] FastAPI/Streamlit Integration
- [ ] End-to-End Testing
- [ ] Kubernetes Deployment

---

## 📜 License & Usage

This project is for **educational and research purposes** only.

Data © [AirROI](https://www.airroi.com/)  
Model APIs © [OpenAI](https://openai.com)  
Code © 2025 [Your Name / Company]

---