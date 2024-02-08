import json
import os
import aiofiles 

async def add_to_leads(json_data, origin_str, keyword, refresh=False):
    """
    Add new leads or refresh existing leads in the leads data file.

    Args:
        json_data (List[Dict]): List of dictionaries containing lead information.
        origin_str (str): String indicating the origin or source of the leads.
        keyword (str): Keyword associated with the leads, used to determine the leads data file.
        refresh (bool, optional): If True, replaces existing leads with the provided json_data.
            If False (default), appends json_data to the existing leads.

    Returns:
        None
    """
    leads_json_path = os.path.join('pseudobase', 'leads_data', f'{keyword}_leads.json')
    if os.path.exists(leads_json_path):
        async with aiofiles.open(leads_json_path, 'r', encoding='utf-8') as leads:
            leads_data = json.loads(await leads.read())
    else:
        leads_data = []
    
    for lead_obj in json_data:
        lead_obj['origin'] = origin_str
    if refresh:
        leads_data = json_data
    else:
        leads_data.extend(json_data)

    async with aiofiles.open(leads_json_path, 'w', encoding='utf-8') as leads:
        await leads.write(json.dumps(leads_data, indent=4, ensure_ascii=False))

async def add_message_to_lead(keyword, generated_message):
    """
    Add a generated message to leads associated with a specific keyword.

    Args:
        keyword (str): Keyword associated with the leads, used to determine the leads data file.
        generated_message (str): The generated message to be added.

    Returns:
        None

    Raises:
        Exception: Raised if the leads data file does not exist.
    """
    leads_json_path = os.path.join('pseudobase', 'leads_data', f'{keyword}_leads.json')

    if os.path.exists(leads_json_path):
        async with aiofiles.open(leads_json_path, 'r', encoding='utf-8') as leads:
            leads_data = json.loads(await leads.read())
    else:
        raise Exception('Path Does Not Exist')

    for lead in leads_data:
        if 'generated-messages' in lead:
            lead['generated-messages'].append(generated_message)
        else:
            lead['generated-messages'] = [generated_message]
        break
    async with aiofiles.open(leads_json_path, 'w', encoding='utf-8') as leads:
        await leads.write(json.dumps(leads_data, indent=4, ensure_ascii=False))
