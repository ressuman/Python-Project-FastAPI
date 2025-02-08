import streamlit as st
import requests


# Fetch data from FastAPI backend
def fetch_recipes():
    response = requests.get("http://localhost:8001/search/")
    return response.json()["results"] if response.status_code == 200 else []


# Main Streamlit app
def main():
    st.title("Recipe App")
    st.write("Displaying recipes from FastAPI backend")

    # Fetch and display recipes
    if recipes := fetch_recipes():
        for recipe in recipes:
            st.subheader(recipe["label"])
            st.write(f"**Source:** {recipe['source']}")
            # st.write(f"**Date:** {recipe['date']}")
            st.write(f"**URL:** {recipe['url']}")
            st.write("---")
    else:
        st.write("No recipes found.")


if __name__ == "__main__":
    main()
