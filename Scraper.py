from threading import Thread

import requests
from bs4 import BeautifulSoup

from PantryCat import PantryCat


class Scraper:
    RECIPES_LIST = "https://www.recipetineats.com/recipes/?fwp_paged="
    RECIPE = "https://www.recipetineats.com/"

    def __init__(self, reset_recipes: bool):
        if reset_recipes:
            self.pc = PantryCat(True)
        else:
            self.pc = PantryCat(False)

    def process_recipes(self, start: int, stop: int):
        for i in range(start, stop):
            self.process_recipe_page(i)

    def process_recipe_page(self, page: int) -> None:
        recipe_slugs = []
        req = requests.get(f"{self.RECIPES_LIST}{page}")
        soup = BeautifulSoup(req.text, features="html.parser")
        links = list(
            map(
                lambda link: (link.attrs["href"])[30:],  # get rid of domain
                soup.find_all("a", {"class": "entry-title-link"}),
            )
        )

        recipe_slugs += links
        for recipe in recipe_slugs:
            self.process_recipe(recipe)

    def process_recipe(self, slug: str) -> None:
        source = self.RECIPE + slug
        req = requests.get(source)
        soup = BeautifulSoup(req.text, features="html.parser")
        source = soup.find("a", {"class": "wprm-recipe-print"})
        if not source:
            print(f"Skipping: {slug}")
            return
        source = source.attrs["href"]
        req = requests.get(source)
        soup = BeautifulSoup(req.text, features="html.parser")

        ingredients = soup.find_all("li", {"class": "wprm-recipe-ingredient"})

        recipe_name = soup.find("h2", {"class": "wprm-recipe-name"}).getText()
        print(f"Processing: {recipe_name}")
        recipe_id = self.pc.insert_recipe(recipe_name, source)

        for ingredient in ingredients:
            amount = ingredient.find("span", {"class": "wprm-recipe-ingredient-amount"})
            unit = ingredient.find("span", {"class": "wprm-recipe-ingredient-unit"})
            name = ingredient.find(
                "span", {"class": "wprm-recipe-ingredient-name"}
            ).getText()
            notes = ingredient.find("span", {"class": "wprm-recipe-ingredient-notes"})

            self.pc.insert_ingredient(name)
            self.pc.insert_uses(
                recipe_id,
                name,
                amount.getText() if amount else None,
                unit.getText() if unit else None,
                notes.getText() if notes else None,
            )


if __name__ == "__main__":
    s = Scraper(False)
    # s.process_recipes(1, 10)
