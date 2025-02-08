from dash import Dash, html, dcc
import requests
from dash.dependencies import Input, Output


# Fetch data from FastAPI backend
def fetch_recipes():
    response = requests.get("http://localhost:8001/search/")
    return response.json()["results"] if response.status_code == 200 else []


# Initialize Dash app
app = Dash(__name__)

# Layout of the app
app.layout = html.Div([html.H1("Recipe App"), html.Div(id="recipe-list")])


# Update recipe list
@app.callback(Output("recipe-list", "children"), Input("url", "pathname"))
def update_recipes(pathname):
    recipes = fetch_recipes()
    if recipes:
        return [
            html.Div(
                [
                    html.H2(recipe["label"]),
                    html.P(f"Source: {recipe['source']}"),
                    html.P(f"Date: {recipe['date']}"),
                    html.A(recipe["url"], href=recipe["url"], target="_blank"),
                ]
            )
            for recipe in recipes
        ]
    return html.P("No recipes found.")


if __name__ == "__main__":
    app.run_server(debug=True)
