# Goal : Design your own JSON Schema and use JSON Mode to extract a nested structure.

# Task 1: Create the schema

from litellm import completion
from config import MODEL
import json

#Starter code (adapt from json_mode_schema.py):
schema = {
  "name": "OrderExtraction",
  "schema": {
    "type": "object",
    "properties": {
        #TODO: define order_id, customer (object), items (array of objects), total (number), currency (string)
        
        # order_id -> string
        "order_id": {"type": "string"},

        # customer -> object => name(string), email(string)
        "customer": {
            "type": "object",
            "properties": {
                "name": {"type": "string"}, "email" : {"type": "string"}
            }
        },

        #items -> array of objects => item(object) ==> sku(string), name(string), qty(int), price(number)
        "items": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "sku": {"type": "string"}, "name": {"type": "string"}, "qty": {"type": "integer"}, "price": {"type": "number"}
                }
            }
        },

        # total -> number
        "total": {"type": "number"},

        #currency -> string
        "currency": {"type": "string"}
    },

    "required": ["order_id", "customer", "items", "total", "currency"],
    "additionalProperties": False
  },
  "strict": True
}

messages = [
  {"role":"system","content":"Return ONLY a JSON object matching the schema."},
  {"role":"user","content":"Order A-1029 by Sarah Johnson : 2x Water Bottle ($12.50 each), 1x Carrying Pouch ($5). Total $30."}
]

resp = completion(
  model=MODEL,
  messages=messages,
  response_format={"type": "json_schema", "json_schema": schema},
)
content = resp.choices[0].message["content"]
print("RAW JSON:\n", content)
print("\nParsed:\n", json.dumps(json.loads(content), indent=2))


# result ------------------------------------------------------
# RAW JSON:
#  {"currency":"USD","customer":{"email":"sarajohnson@email.com","name":"Sarah Johnson"},"items":[{"name":"Water Bottle","price":12.5,"qty":2,"sku":"WB-001"},{"name":"Carrying Pouch","price":5,"qty":1,"sku":"CP-001"}],"order_id":"A-1029","total":30}

# Parsed:
#  {
#   "currency": "USD",
#   "customer": {
#     "email": "sarajohnson@email.com",
#     "name": "Sarah Johnson"
#   },
#   "items": [
#     {
#       "name": "Water Bottle",
#       "price": 12.5,
#       "qty": 2,
#       "sku": "WB-001"
#     },
#     {
#       "name": "Carrying Pouch",
#       "price": 5,
#       "qty": 1,
#       "sku": "CP-001"
#     }
#   ],
#   "order_id": "A-1029",
#   "total": 30
# }