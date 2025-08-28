# 🏠 Real Estate Search Assistant — Dubai Edition

This project is an LLM-powered **conversational assistant** that helps users search for properties in **Dubai** using natural language queries. It leverages a combination of **retrieval-based search (RAG)** and **GPT-4 reasoning** to return semantically relevant listings and explain tradeoffs, amenities, locations, and more.

---

## 📦 Dataset Source

We use the **open-source property listings dataset** provided by **AirROI**:

🔗 **[https://www.airroi.com/data-portal/markets/dubai-united-arab-emirates](https://www.airroi.com/data-portal/markets/dubai-united-arab-emirates)**

> 📢 _All credit for the data goes to the AirROI team. This project uses the publicly available listings data for research and prototyping purposes only._

---

## 🧾 Dataset: `Listings Data` Schema

## 🧾 Dataset Schema: Dubai Property Listings (AirROI)

Below is the full schema of the open-source real estate listings dataset from [AirROI - Dubai Market](https://www.airroi.com/data-portal/markets/dubai-united-arab-emirates).

| Field Name                      | Type              | Description |
|--------------------------------|-------------------|-------------|
| `listing_id`                   | long              | Unique identifier for the listing |
| `listing_name`                 | string            | Title of the listing |
| `listing_type`                 | string            | Type of property (e.g., apartment, house, villa) |
| `room_type`                    | string            | Type of room (e.g., entire home, private room) |
| `cover_photo_url`             | string            | URL of the main listing photo |
| `photos_count`                | integer           | Number of photos available for the listing |
| `host_id`                     | long              | Unique identifier for the host |
| `host_name`                   | string            | Name of the host |
| `cohost_ids`                  | string            | IDs of co-hosts associated with the listing |
| `cohost_names`                | string            | Names of co-hosts associated with the listing |
| `superhost`                   | boolean           | Whether the host is a superhost |
| `country`                     | string            | Country where the listing is located |
| `state`                       | string            | State or province |
| `city`                        | string            | City name |
| `latitude`                    | decimal(10,4)     | Latitude coordinate |
| `longitude`                   | decimal(10,4)     | Longitude coordinate |
| `guests`                      | integer           | Maximum number of guests allowed |
| `bedrooms`                    | integer           | Number of bedrooms |
| `beds`                        | integer           | Number of beds |
| `baths`                       | decimal(4,1)      | Number of bathrooms |
| `registration`                | boolean           | Listing has registration number |
| `amenities`                   | string            | List of amenities (as text) |
| `instant_book`                | boolean           | Whether it can be booked instantly |
| `min_nights`                  | integer           | Minimum nights to book |
| `cancellation_policy`         | string            | Type of cancellation policy |
| `currency`                    | string            | Currency used for pricing |
| `cleaning_fee`                | integer           | Cleaning fee (if any) |
| `extra_guest_fee`             | integer           | Additional guest fee |
| `num_reviews`                 | integer           | Total number of reviews |
| `rating_overall`              | double            | Overall rating |
| `rating_accuracy`             | double            | Accuracy rating |
| `rating_checkin`              | double            | Check-in experience rating |
| `rating_cleanliness`          | double            | Cleanliness rating |
| `rating_communication`        | double            | Host communication rating |
| `rating_location`             | double            | Location rating |
| `rating_value`                | double            | Value-for-money rating |

### 📊 Trailing 12-Months (TTM) Metrics

| Field Name                      | Type              | Description |
|--------------------------------|-------------------|-------------|
| `ttm_revenue`                  | double            | Total revenue (12 months) |
| `ttm_revenue_native`          | double            | Revenue in native currency |
| `ttm_avg_rate`                | double            | Average daily rate |
| `ttm_avg_rate_native`        | double            | In native currency |
| `ttm_occupancy`              | double            | Occupancy rate |
| `ttm_adjusted_occupancy`     | double            | Excludes owner-blocked days |
| `ttm_revpar`                 | double            | Revenue per available room |
| `ttm_revpar_native`          | double            | In native currency |
| `ttm_adjusted_revpar`        | double            | Adjusted RevPAR |
| `ttm_adjusted_revpar_native`| double            | In native currency |
| `ttm_reserved_days`          | long              | Reserved/booked days |
| `ttm_blocked_days`           | long              | Host-blocked days |
| `ttm_available_days`         | long              | Available days |
| `ttm_total_days`             | long              | Total listing days in year |

### 📊 Last 90-Days (L90D) Metrics

| Field Name                      | Type              | Description |
|--------------------------------|-------------------|-------------|
| `l90d_revenue`                | double            | Revenue in last 90 days |
| `l90d_revenue_native`        | double            | Native currency |
| `l90d_avg_rate`              | double            | Avg. daily rate |
| `l90d_avg_rate_native`      | double            | In native currency |
| `l90d_occupancy`            | double            | Occupancy rate |
| `l90d_adjusted_occupancy`   | double            | Excludes blocked days |
| `l90d_revpar`               | double            | Revenue per available room |
| `l90d_revpar_native`        | double            | In native currency |
| `l90d_adjusted_revpar`      | double            | Adjusted RevPAR |
| `l90d_adjusted_revpar_native`| double           | In native currency |
| `l90d_reserved_days`        | long              | Days reserved |
| `l90d_blocked_days`         | long              | Host-blocked days |
| `l90d_available_days`       | long              | Days available |
| `l90d_total_days`           | long              | Total considered days |

---

> This schema supports a wide range of use cases including:  
> - **Location-based filtering**  
> - **Price and occupancy analytics**  
> - **Amenity search and semantic matching**  
> - **Recommender systems based on past reviews and performance**  
> - **Revenue prediction and financial modeling**
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