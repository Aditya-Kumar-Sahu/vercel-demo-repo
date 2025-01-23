# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "pandas",
# ]
# ///
# api/index.py
import json
from http.server import BaseHTTPRequestHandler
import pandas as pd

# class handler(BaseHTTPRequestHandler):
#     def do_GET(self):
#         self.send_response(200)
#         self.send_header('Content-type','application/json')
#         self.end_headers()
#         self.wfile.write(json.dumps({"message": "Hello!"}).encode('utf-8'))
#         return
    
df = pd.read_json("./q-vercel-python.json")
class handler(BaseHTTPRequestHandler):
    def do_GET(self, x, y):
        mark_x = df.loc[df['name'] == x]['marks']
        mark_y = df.loc[df['name'] == y]['marks']
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"marks" : [mark_x, mark_y]}).encode('utf-8'))
        return