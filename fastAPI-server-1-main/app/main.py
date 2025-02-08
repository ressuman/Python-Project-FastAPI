from fastapi import FastAPI, APIRouter, Query, HTTPException, Depends

from typing import Optional, Any

from app.schemas import RecipeSearchResults, Recipe, RecipeCreate, User

from app.recipe_data import RECIPES


app = FastAPI(title="Recipe API", openapi_url="/openapi.json")

api_router = APIRouter()


def get_current_user() -> Optional[User]:
    # Simulate authentication logic
    token = None  # Replace with logic to extract token from the request
    if token:  # Validate and decode the token here
        return User(id=1, name="John Doe", email="john.doe@example.com")
    return None  # No valid user found


@api_router.get("/", status_code=200)
def root() -> dict:
    """
    Root GET
    """
    return {"msg": "Hello, World!"}


# Updated with error handling
# https://fastapi.tiangolo.com/tutorial/handling-errors/
@api_router.get("/recipe/{recipe_id}", status_code=200, response_model=Recipe)
def fetch_recipe(*, recipe_id: int) -> Any:
    """
    Fetch a single recipe by ID
    """

    if not (result := [recipe for recipe in RECIPES if recipe["id"] == recipe_id]):
        raise HTTPException(
            status_code=404, detail=f"Recipe with ID {recipe_id} not found"
        )
    else:
        return result[0]


@api_router.get("/search/", status_code=200, response_model=RecipeSearchResults)
def search_recipes(
    *,
    keyword: Optional[str] = Query(None, min_length=3, examples="chicken"),
    max_results: Optional[int] = 10,
    sort_by: Optional[str] = Query(None, description="Sort by 'label' or 'date'"),
    current_user: Optional[User] = Depends(get_current_user),
    # sort_by: Optional[str] = Query(None, examples=["label", "date"]),
) -> dict:
    """
    Search for recipes based on label keyword and sort results.
    """
    # if not keyword:
    #     # we use Python list slicing to limit results
    #     # based on the max_results query parameter
    #     return {"results": RECIPES[:max_results]}

    # results = filter(lambda recipe: keyword.lower() in recipe["label"].lower(), RECIPES)
    # return {"results": list(results)[:max_results]}

    if not keyword:
        results = RECIPES[:max_results]
    else:
        results = filter(
            lambda recipe: keyword.lower() in recipe["label"].lower(), RECIPES
        )
        results = list(results)[:max_results]

    # Filter recipes based on user authentication
    if current_user:
        results = [
            r for r in results if r["is_public"] or r["user_id"] == current_user.id
        ]
    else:
        results = [r for r in results if r["is_public"]]

    # Sorting logic
    if sort_by == "label":
        results.sort(key=lambda x: x["label"])
    elif sort_by == "date":
        results.sort(key=lambda x: x["date"])

    return {"results": results}


@api_router.post("/recipe/", status_code=201, response_model=Recipe)
def create_recipe(*, recipe_in: RecipeCreate) -> Recipe:
    """
    Create a new recipe (in memory only)
    """
    new_entry_id = len(RECIPES) + 1
    recipe_entry = Recipe(
        id=new_entry_id,
        label=recipe_in.label,
        source=recipe_in.source,
        url=recipe_in.url,
        user_id=recipe_in.submitter_id,
        is_public=True,  # Default to public
    )
    RECIPES.append(recipe_entry.dict())

    return recipe_entry


app.include_router(api_router)


if __name__ == "__main__":
    # Use this for debugging purposes only
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")
