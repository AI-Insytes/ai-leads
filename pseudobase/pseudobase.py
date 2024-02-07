import json
import os

def add_to_leads(json_data, origin_str, keyword, refresh=False):
  """
    Add data to a leads JSON file.

    Parameters:
    - json_data (list): List of dictionaries containing lead data to be added.
    - origin_str (str): String indicating the origin of the lead data.
    - keyword (str): Keyword associated with the leads data.
    - refresh (bool, optional): If True, overwrite the existing leads data with the provided data.
                                Default is False, which appends the new data to the existing leads.

    Returns:
    None
    """
  leads_json_path = os.path.join('pseudobase', 'leads_data', f'{keyword}_leads.json')
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

def add_message_to_lead(keyword, generated_message):
  """
    Add a generated message to a lead in the leads JSON file.

    Parameters:
    - keyword (str): Keyword associated with the leads data.
    - generated_message (str): The generated message to be added.

    Raises:
    - Exception: If the leads JSON file does not exist.

    Returns:
    None
    """
  leads_json_path = os.path.join('pseudobase', 'leads_data', f'{keyword}_leads.json')

  if os.path.exists(leads_json_path):
    with open(leads_json_path, 'r') as leads:
      leads_data = json.load(leads)
  else:
    raise Exception('Path Does Not Exist')
  
  with open(leads_json_path, 'r') as leads:
     leads_data = json.load(leads)

  for lead in leads_data:
      if 'generated-messages' in lead:
          lead['generated-messages'].append(generated_message)
      else:
          lead['generated-messages'] = [generated_message]
      break
  with open(leads_json_path, 'w', encoding='utf-8') as leads:
     json.dump(leads_data, leads, indent=4, ensure_ascii=False)
  pass


##########
## Test ##
##########
if __name__ == "__main__":
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
    result = add_to_leads(json_array, origin_str, "test")
    print(result)
