import json
import os
import aiofiles  # Import aiofiles for async file operations

async def add_to_leads(json_data, origin_str, keyword, refresh=False):
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
