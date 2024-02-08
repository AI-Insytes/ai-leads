import json
import os
import aiofiles 
import random
import re

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

    Outputs:
        Sends files to ./pseudobase/leads_data/
    """
    leads_json_path = create_file_path(keyword)
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
    
    sorted_data = await filter_leads(leads_data)

    async with aiofiles.open(leads_json_path, 'w', encoding='utf-8') as leads:
        await leads.write(json.dumps(sorted_data, indent=4, ensure_ascii=False))

async def add_generic_to_leads(keyword, generated_message):
    """
    Add a generic generated message to leads associated with a specific keyword.

    Args:
        keyword (str): Keyword associated with the leads, used to determine the leads data file.
        generated_message (str): The generated message to be added.

    Returns:
        None

    Raises:
        Exception: Raised if the leads data file does not exist.
    """
    leads_json_path = create_file_path(keyword)

    if os.path.exists(leads_json_path):
        async with aiofiles.open(leads_json_path, 'r', encoding='utf-8') as leads:
            leads_data = json.loads(await leads.read())
    else:
        raise Exception('Path Does Not Exist')

    for lead in leads_data:
        if 'generic-messages' in lead:
            lead['generic-messages'].append(generated_message)
        else:
            lead['generic-messages'] = [generated_message]
        break
    async with aiofiles.open(leads_json_path, 'w', encoding='utf-8') as leads:
        await leads.write(json.dumps(leads_data, indent=4, ensure_ascii=False))

async def add_message_to_lead(keyword, name, generated_message):
    """
    Add a generated message to leads associated with a specific keyword and name.

    Args:
        keyword (str): Keyword associated with the leads, used to determine the leads data file.
        name (str): Name (lead-name or blog-name) to identify the lead object.
        generated_message (str): The generated message to be added.

    Returns:
        None

    Raises:
        Exception: Raised if the leads data file does not exist.
    """
    leads_json_path = create_file_path(keyword)
    
    if os.path.exists(leads_json_path):
        async with aiofiles.open(leads_json_path, 'r', encoding='utf-8') as leads:
            leads_data = json.loads(await leads.read())
    else:
        raise Exception('File Does Not Exist')
    
    found_lead = None
    for lead in leads_data:
        if lead.get('lead-name') == name or lead.get('blog-name') == name:
            found_lead = lead
            break
    if found_lead:
        if 'generated-messages' in found_lead:
            found_lead['generated-messages'].append(generated_message)
        else:
            found_lead['generated-messages'] = [generated_message]

        async with aiofiles.open(leads_json_path, 'w', encoding='utf-8') as leads:
            await leads.write(json.dumps(leads_data, indent=4, ensure_ascii=False))
    else:
        raise Exception(f'Lead with name "{name}" not found.')


async def filter_leads(data):
    """
    Filter lead objects based on the presence of missing fields.

    Args:
        data (List[Dict]): List of dictionaries containing lead information.

    Returns:
        List[Dict]: Sorted list of lead objects. Objects with missing fields are placed at the end.
    """
    def has_missing_fields(lead_obj):
        return any(value is None for value in lead_obj.values())
    
    pushup_data = [lead_obj for lead_obj in data if not has_missing_fields(lead_obj)]
    pushdown_data = [lead_obj for lead_obj in data if has_missing_fields(lead_obj)]

    random.shuffle(pushup_data)

    seen_names = set()
    unique_pushup_data = []
    for lead_obj in pushup_data:
        name = lead_obj.get('lead-name') or lead_obj.get('blog-name')
        context = lead_obj.get('context')

        if name not in seen_names or (context is not None and name in seen_names):
            seen_names.add(name)
            unique_pushup_data.append(lead_obj)

    sorted_data = pushup_data + pushdown_data

    return sorted_data

def create_file_path(keyword):
    """
    Create a sanitized file path based on the provided keyword.

    Args:
        keyword (str): The keyword to be sanitized and used in the file path.

    Returns:
        str: Sanitized file path for leads data.
    """
    sanitized_keyword = re.sub(r'[^a-zA-Z0-9]+', '_', keyword)
    
    leads_json_path = os.path.join('pseudobase', 'leads_data', f'{sanitized_keyword}_leads.json')
    
    return leads_json_path
