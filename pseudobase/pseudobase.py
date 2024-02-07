import json
import os

def add_to_leads(json_data, origin_str, keyword, refresh=False):
  leads_json_path = f'pseudobase/leads_data/{keyword}_leads.json'
  if os.path.exists(leads_json_path):
    with open(leads_json_path, 'r') as leads:
      leads_data = json.load(leads)
  else:
    leads_data = []
  
  for lead_obj in json_data:
    lead_obj['origin'] = origin_str
  if refresh:
     leads_data = json_data
  else:
    leads_data.extend(json_data)

  with open(leads_json_path, 'w', encoding='utf-8') as leads:
    json.dump(leads_data, leads, indent=4, ensure_ascii=False)

  return "done"

def add_message_to_lead(name, message_str):
  leads_json_path = 'pseudobase/leads.json'

  if not os.path.exists(leads_json_path):
        print("Error: Leads JSON file does not exist.")
        return
  
  with open(leads_json_path, 'r') as leads:
     leads_data = json.load(leads)

  for lead in leads_data:
     if lead.get('name') == name:
        if 'generated-messages' in lead:
           lead['generated-messages'].append(message_str)
        else:
           lead['generated-messages'] = [message_str]
        break
  with open(leads_json_path, 'w') as leads:
     json.dump(leads_data, leads, indent=4)
  pass

#############################
## Test ##
##########
json_array = [
    {
        "name": "asdf Doe",
        "context": "A highly sought-after blockchain engineer in Africa",
        "website": "https://www.wordpress.com/kevin_lee",
        "profile": "https://www.linkedin.com/in/kevin-lee-431740233"
    },
    {
        "name": "asdffsafasd Doe",
        "context": "Jane Doe is a prominent researcher in AI",
        "website": "https://www.wordpress.com/kevin_lee",
        "profile": "https://www.linkedin.com/in/kevslee"
    }
]

origin_str = "WordPress"

if __name__ == "__main__":
    result = add_to_leads(json_array, origin_str, "test")
    print(result)
