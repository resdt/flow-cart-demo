import os

import pandas as pd
from sqlalchemy import create_engine


def load_data_from_tables():
    order = ["markets",
             "products",
             "app_users",
             "goods_availability",
             "supply_metadata",
             "supply_details",
             "sales"]
    engine = create_engine(os.getenv("DB_LINK"))
    for filename in order:
        print(filename)
        df = pd.read_csv(f"dev/tables/{filename}.csv")
        df.to_sql(filename, engine, if_exists="append", index=False)


def main():
    load_data_from_tables()


if __name__ == "__main__":
    main()
