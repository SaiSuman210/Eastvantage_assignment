#### python and sql implementation
import csv
import sqlite3

db_path = 'data/Data Engineer_ETL Assignment.db'

query = """
  SELECT
    S.CUSTOMER_ID,
    I.ITEM_NAME,
    CAST(SUM(QUANTITY) AS INTEGER) quantity
  FROM (SELECT CUSTOMER_ID, AGE FROM CUSTOMERS WHERE  18 <= AGE  AND  AGE <= 35) C
  LEFT JOIN SALES S
  ON S.CUSTOMER_ID  = C.CUSTOMER_ID
  LEFT JOIN ORDERS O
  ON O.SALES_ID = S.SALES_ID
  LEFT JOIN ITEMS I
  ON I.ITEM_ID = O.ITEM_ID
  GROUP BY S.CUSTOMER_ID, I.ITEM_NAME
  HAVING SUM(QUANTITY) > 0
  ORDER BY S.CUSTOMER_ID, I.ITEM_NAME
"""

try:
  conn = sqlite3.connect(db_path)
  cursor = conn.cursor()
  cursor.execute(query)

  rows = cursor.fetchall()
  columns = [description[0] for description in cursor.description]
  output_csv = 'ITEM_PURCAHSES_BY_CUSTOMER-SQL.csv'

  with open(f"output/{output_csv}", mode='w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f, delimiter=';')
    writer.writerow(columns)
    writer.writerows(rows)

  print(f"Query results saved to '{output_csv}'")

except Exception as e:
  print("An error occurred:", e)
  
finally:
  cursor.close()
  conn.close()
