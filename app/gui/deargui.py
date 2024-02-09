import dearpygui.dearpygui as dpg
import re
import os
import json
import requests

class Generation:
    def __init__(self):
        self.init_ui()

    def init_ui(self):
        with dpg.group(horizontal=True):
            with dpg.group():
                dpg.add_text("What is your name?")
                self.username_input = dpg.add_input_text(default_value="Enter name")

                dpg.add_text("What category of professional are you aiming to connect with?")
                self.keyword_query_input = dpg.add_input_text(default_value="Enter keyword")

                dpg.add_button(label="Submit", callback=self.show_next_page)

            with dpg.group():
                dpg.add_text("Does your message to leads have any length constraints?")
                self.message_length_combobox = dpg.add_combo(["Quick note", "280 characters - Twitter/X post", "300 characters - LinkedIn connection request message"])

                dpg.add_text("What is the objective of your outreach message?")
                self.message_purpose_input = dpg.add_input_text(default_value="Enter message objective")

                dpg.add_text("Provide additional context about yourself and or your request")
                self.user_context_input = dpg.add_input_text(default_value="Enter additional context")

                dpg.add_text("Choose the tone for your outreach message:")
                self.message_tone_combobox = dpg.add_combo(["Professional", "Chill", "Persuasive", "Warm"])

                dpg.add_button(label="Submit", callback=self.submit_clicked)

    def show_next_page(self):
        keyword = dpg.get_value(self.keyword_query_input)
        sanitized_keyword = re.sub(r'[^a-zA-Z0-9]+', '_', keyword)
        dpg.set_primary_window(self.second_page)
        dpg.set_item_label(self.loading_label, "Generating message...")
        dpg.show_item(self.loading_label)
        # Start your async search here and update UI accordingly

    def submit_clicked(self):
        user_name = dpg.get_value(self.username_input)
        lead_category = dpg.get_value(self.keyword_query_input)
        message_length = dpg.get_value(self.message_length_combobox)
        message_purpose = dpg.get_value(self.message_purpose_input)
        user_context = dpg.get_value(self.user_context_input)
        message_tone = dpg.get_value(self.message_tone_combobox)
        leads_data_file_name = re.sub(r'[^a-zA-Z0-9]+', '_', lead_category)
        cli_data = {
            "query": lead_category,
            "length": message_length,
            "purpose": message_purpose,
            "context": user_context,
            "tone": message_tone,
        }
        print(cli_data, leads_data_file_name, user_name)
        dpg.set_primary_window(self.third_page)
        dpg.set_item_label(self.loading_label, "Generating message...")
        dpg.show_item(self.loading_label)
        # Start your async gathering of information here and update UI accordingly

    def show_first_page(self):
        dpg.set_primary_window(self.first_page)

class ExpandableGroupBox:
    def __init__(self, lead):
        self.lead = lead
        self.expanded_size = (400, 200)
        self.collapsed_size = (200, 40)

        with dpg.group():
            self.name_label = dpg.add_text(lead.get('lead-name') or lead.get('blog-name'))

        self.show_name_only()

    def toggle_expanded(self, sender):
        if dpg.get_value(sender):
            dpg.configure_item(self.group_box, size=self.expanded_size)
            self.show_additional_data()
        else:
            dpg.configure_item(self.group_box, size=self.collapsed_size)
            self.show_name_only()

    def show_additional_data(self):
        origin_label = dpg.add_text(f"Origin: {self.lead.get('origin', '')}")
        messages_label = dpg.add_text(f"Generated Messages: {self.lead.get('generated-messages', '')}")

    def show_name_only(self):
        dpg.delete_item(self.group_box)
        with dpg.group():
            dpg.add_text(self.lead.get('lead-name') or self.lead.get('blog-name'))

class Leads:
    def __init__(self):
        self.init_ui()

    def init_ui(self):
        dpg.add_button(label="Update", callback=self.update_leads)
        self.tab_bar = dpg.add_tab_bar()

    def update_leads(self, sender):
        leads_data_dir = os.path.join("pseudobase", "leads_data")
        matching_files = [f for f in os.listdir(leads_data_dir) if f.endswith("_leads.json") and not f.startswith("_")]

        for file_name in matching_files:
            if not self.tab_exists(file_name):
                file_path = os.path.join(leads_data_dir, file_name)
                with open(file_path, 'r', encoding='utf-8') as file:
                    try:
                        json_data_list = json.load(file)
                    except json.JSONDecodeError:
                        print('error decoding')
                        continue

                    with dpg.tab_bar_tab(label=file_name):
                        for lead in json_data_list:
                            group_box = ExpandableGroupBox(lead)

    def tab_exists(self, text):
        tabs = dpg.get_item_children(self.tab_bar)
        return any(dpg.get_item_label(tab) == text for tab in tabs)

class About:
    def __init__(self):
        self.init_ui()

    def init_ui(self):
        team_info_group = dpg.add_group()
        team_layout = dpg.get_item_configuration(team_info_group)
        max_width = 100
        max_height = 100

        member1_layout = self.create_member_layout(
            "Caleb Hemphill",
            "https://avatars.githubusercontent.com/u/21288566?v=4",
            "https://github.com/kaylubh",
            max_width,
            max_height
        )
        member2_layout = self.create_member_layout(
            "Rhett Chase",
            "https://avatars.githubusercontent.com/u/126417892?v=4",
            "https://github.com/rhettchase",
            max_width,
            max_height
        )
        member3_layout = self.create_member_layout(
            "Lana Zumbrunn",
            "https://avatars.githubusercontent.com/u/129145633?v=4",
            "https://github.com/lana-z",
            max_width,
            max_height
        )
        member4_layout = self.create_member_layout(
            "Immanuel Shin",
            "https://avatars.githubusercontent.com/u/141205211?v=4",
            "TeamMember1",
            max_width,
            max_height
        )
        member5_layout = self.create_member_layout(
            "Felix Taveras",
            "https://avatars.githubusercontent.com/u/147009711?v=4",
            "https://github.com/f-taveras",
            max_width,
            max_height
        )

        dpg.append_item(team_info_group, member1_layout)
        dpg.append_item(team_info_group, member2_layout)
        dpg.append_item(team_info_group, member3_layout)
        dpg.append_item(team_info_group, member4_layout)
        dpg.append_item(team_info_group, member5_layout)

    def create_member_layout(self, member_name, image_url, github_username, max_width, max_height):
        layout = dpg.add_group(horizontal=True)

        name_label = dpg.add_text(member_name)
        image_label = dpg.add_image(dpg.get_data(image_url), width=max_width, height=max_height)

        github_label = dpg.add_text(f"GitHub: {github_username}")
        dpg.configure_item(github_label, link=github_username)

        return layout

class LeadGUI:
    def __init__(self):
        self.init_ui()

    def init_ui(self):
        with dpg.handler_registry():
            dpg.add_mouse_drag_handler(callback=self.mouse_drag_handler)

        # Radial Gradient Background
        with dpg.handler_registry():
            dpg.add_viewport_resize_handler(callback=self.resize_handler)

        # Navbar
        with dpg.group(horizontal=True):
            with dpg.group():
                self.generate_tab_button = dpg.add_button(label="Generate", callback=self.show_generate_tab)
            with dpg.group():
                self.leads_tab_button = dpg.add_button(label="Leads", callback=self.show_leads_tab)
            with dpg.group():
                self.about_tab_button = dpg.add_button(label="About", callback=self.show_about_tab)

        # Content Frame
        with dpg.group(horizontal=True):
            with dpg.group():
                self.stacked_frame = dpg.add_group()
                self.stacked_widget = dpg.add_stack_container()
                dpg.set_item_width(self.stacked_widget, 700)
                dpg.set_item_height(self.stacked_widget, 500)

                # Pages
                self.generate_page = Generation()
                self.leads_page = Leads()
                self.about_page = About()

                dpg.append_item(self.stacked_widget, self.generate_page)
                dpg.append_item(self.stacked_widget, self.leads_page)
                dpg.append_item(self.stacked_widget, self.about_page)

        dpg.set_primary_window(self.generate_page)
        dpg.set_item_label(self.generate_tab_button, "Generate")
        dpg.set_item_label(self.leads_tab_button, "Leads")
        dpg.set_item_label(self.about_tab_button, "About")

    def show_generate_tab(self):
        dpg.set_primary_window(self.generate_page)

    def show_leads_tab(self):
        dpg.set_primary_window(self.leads_page)

    def show_about_tab(self):
        dpg.set_primary_window(self.about_page)

    def mouse_drag_handler(self, sender, app_data):
        print(f"Mouse Drag: {app_data}")

    def render_handler(self, sender, app_data):
        dpg.draw_image(dpg.get_item_info(sender)["handle"], (0, 0), (800, 600))


# Create the Dear PyGui context and set up the UI
dpg.create_context()
dpg.create_viewport(title="Lead Generater", width=1000, height=600)

gui = LeadGUI()

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()