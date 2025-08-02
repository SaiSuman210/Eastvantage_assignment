#### pandas implementation
import pandas as pd
import sqlite3


db_path = 'data/Data Engineer_ETL Assignment.db'

try:
  conn = sqlite3.connect(db_path)

  customers_df = pd.read_sql_query("SELECT CUSTOMER_ID, AGE FROM CUSTOMERS WHERE 18 <= AGE AND AGE <= 35", conn)
  sales_df = pd.read_sql_query("SELECT * FROM SALES", conn)
  orders_df = pd.read_sql_query("SELECT * FROM ORDERS", conn)

  items_df = pd.read_sql_query("SELECT * FROM ITEMS", conn)

  # print("CUSTOMERS:", customers_df.columns.tolist())
  # print("SALES:", sales_df.columns.tolist())
  # print("ORDERS:", orders_df.columns.tolist())
  # print("ITEMS:", items_df.columns.tolist())

  sales_f = customers_df.merge(sales_df, on='customer_id', how='left')

  orders_f = sales_f.merge(orders_df, on='sales_id', how='left')

  full_data = orders_f.merge(items_df, on='item_id', how='left')

  result = (
      full_data
      .groupby(['customer_id', 'item_name'], as_index=False)
      .agg({'quantity': 'sum'})
  )

  result = result[result['quantity'].fillna(0) > 0]
  result['quantity'] = result['quantity'].astype(int)

  result = result.sort_values(by=['customer_id', 'item_name'])

  output_csv = "ITEM_PURCAHSES_BY_CUSTOMER-PANDAS.csv"

  result.to_csv(output_csv, sep=';', index=False)
  print(f"Query results saved to '{output_csv}'")

except Exception as e:
  print("An error occurred:", e)

finally:
  conn.close()
  