import pandas as pd
from sqlalchemy import create_engine

# --- CONFIGURATION ---
DB_URI = "postgresql://admin:admin@localhost:5432/airbnbdb"
TABLE_NAME = "airbnb_properties"

# # --- SCHEMA AS TEXT ---
# schema_text = """
# Field   Type    Description
# guests  integer Maximum number of guests allowed
# bedrooms    integer Number of bedrooms available
# beds    integer Number of beds available
# baths   decimal(4,1)    Number of bathrooms available
# amenities   string  List of amenities offered
# num_reviews integer Total number of reviews received
# rating_overall  double  Overall rating score
# ttm_avg_rate    double  Average daily rate in trailing twelve months
# """

# --- PARSE THE SCHEMA TEXT ---
# import io
# schema_df = pd.read_csv(io.StringIO(schema_text), sep="\t| {2,}", engine="python")
schema_df = pd.read_csv("../data/schema.csv")


METADATA_ATTRIBUTES = [
'guests', 'bedrooms', 'beds', 'baths', 'num_reviews', 'rating_overall', 'min_nights', 'ttm_avg_rate'
]

schema_df = schema_df[schema_df['Field'].isin(METADATA_ATTRIBUTES)].reset_index(drop=True)

# --- CONNECT TO POSTGRES AND LOAD DATA ---
engine = create_engine(DB_URI)
df = pd.read_sql(f"SELECT * FROM {TABLE_NAME}", engine)

# --- DETERMINE COLUMN STATS ---
def summarize_column(col_name, col_type):
    if col_name not in df.columns:
        return "❌ Column missing in data"

    col_data = df[col_name].dropna()

    if col_type.lower() in ["string"]:
        # Try to limit unique values to top 20
        unique_vals = col_data.astype(str).unique()
        if len(unique_vals) > 20:
            return f"{len(unique_vals)} unique values. Examples: {', '.join(unique_vals[:5])}, ..."
        else:
            return ", ".join(unique_vals)
    elif "int" in col_type or "double" in col_type or "decimal" in col_type:
        return f"Min: {col_data.min()}, Max: {col_data.max()}"
    else:
        return "⚠️ Unknown type"

# --- APPLY TO ALL FIELDS ---
schema_df["Value Summary"] = schema_df.apply(
    lambda row: summarize_column(row["Field"], row["Type"]), axis=1
)

# --- PRINT / RETURN THE RESULT ---
print(schema_df.to_markdown(index=False))


schema_df.to_csv("../data/schema_with_stats.csv", index=False)






# Example input schema_df
# Assumed to already have: "Field", "Type", "Description", "Value Summary"
# Replace with actual schema_df in your code
# schema_df = pd.read_csv("your_schema_file.csv")

# Predefined base synonyms (can be extended with domain-specific vocab)
BASE_SYNONYMS = {
    "guests": ["guest", "guests", "accommodates", "number of guests", "people allowed"],
    "bedrooms": ["bedroom", "bedrooms", "no. of bedrooms", "how many bedrooms", "sleeping rooms"],
    "bathrooms": ["bathroom", "bathrooms", "baths", "toilets", "washrooms"],
    "num_reviews": ["reviews", "no. of reviews", "feedback", "ratings count"],
    "rating_overall": ["rating", "overall rating", "review score", "average rating", "stars"],
    "ttm_avg_rate": ["price", "budget", "rate", "cost per night", "nightly price", "daily rate"],
    "listing_type": ["property type", "listing type", "apartment or villa", "type of house"],
    "room_type": ["room type", "entire home", "private room", "shared space"],
    "amenities": ["amenities", "features", "facilities", "extras", "what's included"],
    "latitude": ["lat", "location latitude", "geo latitude"],
    "longitude": ["long", "location longitude", "geo longitude"]
}

# If BASE_SYNONYMS doesn’t contain a field, try auto-generating basic ones
def generate_fallback_synonyms(field, description):
    tokens = set()
    field = field.replace("_", " ")
    tokens.add(field.lower())
    tokens.add(f"{field.lower()}s")
    if pd.notna(description):
        for word in description.lower().split():
            tokens.add(word.strip(":,."))

    return list(tokens)

# Main mapping builder
def build_synonym_mapping(schema_df):
    mapping = {}
    for _, row in schema_df.iterrows():
        field = row["Field"]
        desc = row["Description"]

        if field in BASE_SYNONYMS:
            mapping[field] = BASE_SYNONYMS[field]
        else:
            mapping[field] = generate_fallback_synonyms(field, desc)

    return mapping

# Example usage
# schema_df = ... (already loaded)
synonym_mapping = build_synonym_mapping(schema_df)

# # Optional: Print nicely
# for key, values in synonym_mapping.items():
#     print(f"{key}: {values}")


import json

output_path = "../data/metadata_searchDB.json"

# Save the dictionary as a JSON file
with open(output_path, "w") as f:
    json.dump(synonym_mapping, f, indent=4)

print(f"Synonym mapping saved to {output_path}")
