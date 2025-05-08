from pprint import pprint

import psycopg2


class PantryCat:
    def __init__(self, new_schema: bool):
        self.connection = psycopg2.connect(
            user="postgres",
            password="gcs28",
            host="127.0.0.1",
            port="5433",
        )

        if new_schema:
            self.reset()
        else:
            with self.connection.cursor() as cursor:
                cursor.execute("SET SCHEMA 'pantrycat'")

    def insert_recipe(self, name: str, source: str) -> int | None:
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO RECIPES (name, source) VALUES (%s, %s) RETURNING recipeID",
                    [name, source],
                )
                recipe_id = cursor.fetchone()
                self.connection.commit()
                return recipe_id[0]
        except psycopg2.errors.UniqueViolation:
            self.connection.rollback()
            return None

    def insert_ingredient(self, name: str) -> str | None:
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO INGREDIENTS VALUES (%s) RETURNING name", [name]
                )
                ingredient = cursor.fetchone()
                self.connection.commit()
                return ingredient[0]
        except psycopg2.errors.UniqueViolation:
            self.connection.rollback()
            return None

    def insert_uses(
        self, recipe: int, ingredient: str, amount: str, unit: str, notes: str
    ) -> bool:
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO USES VALUES (%s, %s, %s, %s, %s)",
                    [
                        recipe,
                        ingredient,
                        amount,
                        unit if unit else "NULL",
                        notes if notes else "NULL",
                    ],
                )
                self.connection.commit()
                return True
        except psycopg2.errors.UniqueViolation:
            self.connection.rollback()
            return False

    def get_recipes(self) -> list:
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM RECIPES")
            return cursor.fetchall()

    def get_recipes_using(self, ingredient: str) -> list:
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                           SELECT ingredient, amount, unit, notes, name, source FROM USES
                           JOIN RECIPES ON recipe = recipeID
                           WHERE ingredient ILIKE %s""",
                [f"%{ingredient}%"],
            )
            return cursor.fetchall()

    def reset(self) -> None:
        with self.connection.cursor() as cursor:
            cursor.execute(open("schema.sql", "r").read())
            self.connection.commit()

    def close(self) -> None:
        self.connection.close()


if __name__ == "__main__":
    pc = PantryCat(False)
    pprint(pc.get_recipes_using("garlic"))
    pc.close()
