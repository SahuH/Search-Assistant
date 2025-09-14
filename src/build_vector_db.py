import pandas as pd
from sqlalchemy import create_engine
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
from tqdm import tqdm

# -----------------------------
# CONFIGURATION
# -----------------------------

DB_URI = "postgresql://admin:admin@localhost:5432/airbnbdb"
TABLE_NAME = "airbnb_properties"
CHROMA_DIR = "../data/chroma_store"
COLLECTION_NAME = "airbnb_properties"

RELEVANT_ATTRIBUTES = [
'listing_name', 'listing_type', 'room_type', 'latitude', 'longitude', 'guests', 'bedrooms', 'beds', 'baths', 'amenities', 'num_reviews',  'rating_overall',
'min_nights', 'ttm_avg_rate'
]

METADATA_ATTRIBUTES = [
'guests', 'bedrooms', 'beds', 'baths', 'num_reviews', 'rating_overall', 'min_nights', 'ttm_avg_rate'
]

# -----------------------------
# LOAD DATA FROM POSTGRESQL
# -----------------------------
engine = create_engine(DB_URI)
df = pd.read_sql(f"SELECT * FROM {TABLE_NAME}", engine)
print(f"✅ Loaded {len(df)} rows from PostgreSQL table `{TABLE_NAME}`")

# -----------------------------
# BUILD PROPERTY CARD TEXT
# -----------------------------
def generate_property_card(row):
    parts = []

    # Title and type
    if pd.notna(row.get("listing_name")):
        parts.append(f"Listing: {row['listing_name']}.")
    if pd.notna(row.get("listing_type")):
        parts.append(f"This is a {row['listing_type'].lower()}")
        if pd.notna(row.get("room_type")):
            parts[-1] += f" with a {row['room_type'].lower()}."

    # Rooms and capacity
    room_desc = []
    if pd.notna(row.get("bedrooms")):
        room_desc.append(f"{int(row['bedrooms'])} bedroom(s)")
    if pd.notna(row.get("beds")):
        room_desc.append(f"{int(row['beds'])} bed(s)")
    if pd.notna(row.get("baths")):
        room_desc.append(f"{float(row['baths']):.1f} bathroom(s)")
    if room_desc:
        parts.append("Includes " + ", ".join(room_desc) + ".")

    # Guests
    if pd.notna(row.get("guests")):
        parts.append(f"Suitable for up to {int(row['guests'])} guests.")

    # Location (latitude/longitude)
    if pd.notna(row.get("latitude")) and pd.notna(row.get("longitude")):
        parts.append(f"Located at coordinates ({row['latitude']}, {row['longitude']}).")

    # Reviews and rating
    if pd.notna(row.get("rating_overall")):
        parts.append(f"Rated {row['rating_overall']:.1f} overall")
        if pd.notna(row.get("num_reviews")):
            parts[-1] += f" based on {int(row['num_reviews'])} reviews."

    # Price
    if pd.notna(row.get("ttm_avg_rate")):
        parts.append(f"Average daily price: {int(row['ttm_avg_rate'])} AED.")

    # # Amenities
    # if pd.notna(row.get("amenities")):
    #     parts.append(f"Amenities: {row['amenities']}.")

    return " ".join(parts)

df["property_card"] = df.apply(generate_property_card, axis=1)

# -----------------------------
# EMBEDDING
# -----------------------------
print("🔄 Generating embeddings...")

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
embeddings = model.encode(df["property_card"].tolist(), show_progress_bar=True)

# -----------------------------
# SAVE TO CHROMADB
# -----------------------------
print("💾 Saving to ChromaDB...")
# chroma_client = chromadb.PersistentClient(path=CHROMA_DIR)
chroma_client = chromadb.Client(
    Settings(
        chroma_db_impl="duckdb+parquet",
        persist_directory=CHROMA_DIR  # this will use local files
    )
)
collection = chroma_client.get_or_create_collection(COLLECTION_NAME)

documents = df["property_card"].tolist()
metadata = df[METADATA_ATTRIBUTES].to_dict(orient="records")
ids = df["listing_id"].astype(str).tolist()

collection.add(
    documents=documents,
    embeddings=embeddings,
    metadatas=metadata,
    ids=ids
)

print(f"✅ Stored {len(documents)} property cards with embeddings in ChromaDB")
