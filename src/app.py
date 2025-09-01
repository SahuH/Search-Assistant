import streamlit as st
from retrieve import retrieve_with_metadata_filtering, rerank_candidates

st.set_page_config(page_title="Real Estate Search Assistant", page_icon="🏠")

# Title
st.title("🏠 Real Estate Search Assistant")
st.markdown("Ask me to find you properties in Dubai based on your preferences!")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
if prompt := st.chat_input("Type your property search query here..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Searching top listings for you..."):
            try:
                # Step 1: Retrieve properties using metadata filtering
                metadata_results = retrieve_with_metadata_filtering(prompt)

                # Step 2: Rerank with semantic similarity
                top_properties = rerank_candidates(prompt, metadata_results, top_k=5)

                # Format results
                if not top_properties:
                    st.warning("Sorry, I couldn’t find any matching properties.")
                    response = "I couldn't find relevant matches for your preferences."
                else:
                    response = "Here are some properties you might like:\n"
                    for idx, prop in enumerate(top_properties, 1):
                        card = prop['property_text']
                        link = prop['metadata'].get("listing_url", "#")
                        response += f"\n**{idx}.** {card}\n"
                        if link and link != "#":
                            response += f"[View Listing]({link})\n"

                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})

            except Exception as e:
                st.error("An error occurred while processing your request.")
                st.exception(e)
