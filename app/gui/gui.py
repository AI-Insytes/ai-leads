import sys, json, asyncio, re, os, requests
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import QUrl, Qt, QSize, QTimer, QCoreApplication
from PyQt6.QtSvg import QSvgRenderer
from qasync import QEventLoop, asyncSlot

from app.search import search_main
from app.prompt import prompt_main, get_lead_context, get_lead_name
from app.report import main_report
from app.linked_in_search import get_profile


class Generation(QWidget):
    def __init__(self):
        super().__init__()
        self.current_page_index = 0
        self.init_ui()

    def init_ui(self):
        self.stacked_widget = QStackedWidget(self)
        self.stacked_widget.setFixedSize(695, 500)

        self.setStyleSheet("""
                            background-color: #93dbd5;
                            border: 0px solid;
                            alignment: center;
                        """)

        font16 = QFont()
        font16.setPointSize(16)

        font18 = QFont()
        font18.setPointSize(18)

        font20 = QFont()
        font20.setPointSize(20)

        font24 = QFont()
        font24.setPointSize(24)

        # first page
        first_layout = QVBoxLayout()

        label_width = 500
        input_width = 500
        button_width = 200

        self.username_label = self.create_wrapped_label("What is your name?", font16, width=label_width)
        self.username_input = self.create_line_edit("Enter name", font16, 30, fixed_width=input_width)

        self.keyword_query_label = self.create_wrapped_label("What category of professional are you aiming to connect with? Specify the industry or area of expertise you're interested in for leads.", font16, width=label_width)
        self.keyword_query_input = self.create_line_edit("Enter keyword", font16, 30, fixed_width=input_width)

        submit_button = self.create_push_button("Submit", font16, 30, fixed_width=button_width)
        submit_button.clicked.connect(lambda: asyncio.create_task(self.show_next_page()))

        first_layout.addWidget(self.username_label)
        first_layout.addWidget(self.username_input)
        first_layout.addWidget(self.keyword_query_label)
        first_layout.addWidget(self.keyword_query_input)
        first_layout.addWidget(submit_button)

        first_layout_widget = QWidget()
        first_layout_widget.setLayout(first_layout)

        # Second Page
        second_layout = QVBoxLayout()

        self.message_length_label = self.create_wrapped_label("Does your message to leads have any length constraints?", font16, width=label_width)
        self.message_length_combobox = self.create_combo_box(['Quick note', '280 characters - Twitter/X post', '300 characters - LinkedIn connection request message'], font16, 30, fixed_width=input_width)

        self.message_purpose_label = self.create_wrapped_label("What is the objective of your outreach message?", font16, width=label_width)
        self.message_purpose_input = self.create_line_edit("Enter message objective", font16, 30, fixed_width=input_width)

        self.user_context_label = self.create_wrapped_label("Provide additional context about yourself and or your request (e.g., is there an event or product they may be interested in?)", font16, width=label_width)
        self.user_context_input = self.create_line_edit("Enter additional context", font16, 30, fixed_width=input_width)

        self.message_tone_label = self.create_wrapped_label("Choose the tone for your outreach message:", font16, width=label_width)
        self.message_tone_combobox = self.create_combo_box(['Professional', 'Chill', 'Persuasive', 'Warm'], font16, 30, fixed_width=input_width)

        buttons_layout = QHBoxLayout()

        pages = ['Page 1', 'Page 2', 'Page 3', 'Page 4']

        # back_button_2 = self.create_push_button("Back", font16, 30, fixed_width=button_width)
        # back_button_2.clicked.connect(self.show_first_page)
        # buttons_layout.addWidget(back_button_2)

        back_button_2 = self.create_dropdown_button("Back", font16, pages, 30,  fixed_width=button_width)
        back_button_2.currentIndexChanged.connect(self.back_dropdown_changed)
        buttons_layout.addWidget(back_button_2)

        self.submit_button = self.create_push_button("Submit", font16, 30, fixed_width=button_width)
        self.submit_button.clicked.connect(lambda: asyncio.create_task(self.submit_clicked()))
        buttons_layout.addWidget(self.submit_button)

        second_layout.addWidget(self.message_length_label)
        second_layout.addWidget(self.message_length_combobox)
        second_layout.addWidget(self.message_purpose_label)
        second_layout.addWidget(self.message_purpose_input)
        second_layout.addWidget(self.user_context_label)
        second_layout.addWidget(self.user_context_input)
        second_layout.addWidget(self.message_tone_label)
        second_layout.addWidget(self.message_tone_combobox)
        second_layout.addLayout(buttons_layout)

        second_layout_widget = QWidget()
        second_layout_widget.setLayout(second_layout)

        # Third page
        third_layout = QVBoxLayout()
        self.loading_label = QLabel("Generating message...")
        self.loading_label.setFont(font16)
        third_layout.addWidget(self.loading_label)

        page3_button_layout = QHBoxLayout()

        back_button_3 = self.create_dropdown_button("Back", font16, pages, 30,  fixed_width=button_width)
        back_button_3.currentIndexChanged.connect(self.back_dropdown_changed)
        page3_button_layout.addWidget(back_button_3)

        linkedin_search_button = self.create_push_button("Search LinkedIn Profile", font16, 30, fixed_width=400)
        linkedin_search_button.clicked.connect(lambda: asyncio.create_task(self.linkedin_search_button()))
        page3_button_layout.addWidget(linkedin_search_button)

        third_layout.addLayout(page3_button_layout)

        third_layout_widget = QWidget()
        third_layout_widget.setLayout(third_layout)
        
        # Fourth Page

        fourth_layout = QVBoxLayout()
        self.loading_linkedin_label = QLabel("Generating profiles...")
        self.loading_linkedin_label.setFont(font16)
        fourth_layout.addWidget(self.loading_linkedin_label)

        page4_button_layout = QHBoxLayout()

        back_button_4 = self.create_dropdown_button("Back", font16, pages, 30,  fixed_width=button_width)
        back_button_4.currentIndexChanged.connect(self.back_dropdown_changed)
        page4_button_layout.addWidget(back_button_4)

        update_button = QPushButton("Update", self)
        update_button.clicked.connect(self.populate_linkedin_page)
        page4_button_layout.addWidget(update_button)

        fourth_layout.addLayout(page4_button_layout)

        fourth_layout_widget = QWidget()
        fourth_layout_widget.setLayout(fourth_layout)

        self.stacked_widget.addWidget(first_layout_widget)
        self.stacked_widget.addWidget(second_layout_widget)
        self.stacked_widget.addWidget(third_layout_widget)
        self.stacked_widget.addWidget(fourth_layout_widget)

        self.loading_label.setWordWrap(True)

        self.username_in = self.username_input
        self.keyword_input = self.keyword_query_input
        self.length_combobox = self.message_length_combobox
        self.purpose_input = self.message_purpose_input
        self.context_input = self.user_context_input
        self.tone_combobox = self.message_tone_combobox
        self.lead_name = ''

    def create_wrapped_label(self, text, font, width):
        label = QLabel(text)
        label.setFont(font)
        label.setMaximumHeight(100)
        label.setWordWrap(True)
        label.setStyleSheet("""
                                color: black;
                                padding-left: 20px;
                            """)
        label.setFixedWidth(width)
        return label
    
    def create_line_edit(self, placeholder, font, fixed_height, fixed_width=None):
        line_edit = QLineEdit(self)
        line_edit.setPlaceholderText(placeholder)
        line_edit.setFont(font)
        line_edit.setFixedHeight(fixed_height)
        line_edit.setStyleSheet("""
                                    margin-left: 20px;
                                    padding-left: 5px;
                                    background: #90e8e1;
                                """)
        if fixed_width:
            line_edit.setFixedWidth(fixed_width)
        return line_edit

    def create_combo_box(self, items, font, fixed_height, fixed_width=None):
        combo_box = QComboBox(self)
        combo_box.addItems(items)
        combo_box.setFont(font)
        combo_box.setFixedHeight(fixed_height)
        combo_box.setStyleSheet("""
                                    margin-left: 20px;
                                    padding-left: 5px;
                                    background: #90e8e1;
                                """)
        if fixed_width:
            combo_box.setFixedWidth(fixed_width)
        return combo_box

    def create_push_button(self, text, font, fixed_height, fixed_width=None):
        push_button = QPushButton(text, self)
        push_button.setFont(font)
        push_button.setFixedHeight(fixed_height)
        push_button.setStyleSheet("""
                                    QPushButton {
                                        border: none;
                                        border-radius: 10px;
                                        background-color: #93dbd5;
                                        margin: 0 auto; 
                                    }
                                    
                                    QPushButton:hover {
                                        background-color: #90e8e1;
                                    }
                                    
                                    QPushButton:pressed {
                                        padding-top: 1px;
                                        padding-left: 1px;
                                    }
                                """)
        if fixed_width:
            push_button.setFixedWidth(fixed_width)
        return push_button
    
    def create_dropdown_button(self, text, font, items, fixed_height, fixed_width=None):
        dropdown_button = QComboBox(self)
        dropdown_button.addItem(text)
        dropdown_button.addItems(items)
        dropdown_button.setFont(font)
        dropdown_button.setFixedHeight(fixed_height)
        dropdown_button.setStyleSheet("""
                                    QPushButton {
                                        border: none;
                                        border-radius: 10px;
                                        background-color: #93dbd5;
                                        margin: 0 auto; 
                                    }
                                    
                                    QPushButton:hover {
                                        background-color: #90e8e1;
                                    }
                                    
                                    QPushButton:pressed {
                                        padding-top: 1px;
                                        padding-left: 1px;
                                    }
                                """)
        if fixed_width:
            dropdown_button.setFixedWidth(fixed_width)
        dropdown_button.activated.connect(self.back_dropdown_changed)
        return dropdown_button
    
    def back_dropdown_changed(self, index):
        if index == 1:
            self.show_first_page()
        elif index == 2:
            self.stacked_widget.setCurrentIndex(1)
        elif index == 3:
            self.stacked_widget.setCurrentIndex(2)
        elif index == 4:
            self.stacked_widget.setCurrentIndex(3)

    async def show_next_page(self):
        keyword = self.keyword_query_input.text()
        sanitized_keyword = re.sub(r'[^a-zA-Z0-9]+', '_', keyword)
        self.current_page_index = 1
        self.stacked_widget.setCurrentIndex(1)
        await self.start_search(sanitized_keyword)
    
    @asyncSlot()
    async def start_search(self, keyword):
        await search_main(keyword)

    async def submit_clicked(self):
        user_name = self.username_in.text()
        lead_category = self.keyword_input.text() 
        message_length = self.length_combobox.currentText()
        message_purpose = self.purpose_input.text()
        user_context = self.context_input.text()
        message_tone = self.tone_combobox.currentText()
        leads_data_file_name = re.sub(r'[^a-zA-Z0-9]+', '_', lead_category)
        cli_data = {
            "query": lead_category,
            "length": message_length,
            "purpose": message_purpose,
            "context": user_context,
            "tone": message_tone,
        }
        self.stacked_widget.setCurrentIndex(2)
        main_report(leads_data_file_name)
        try:
            await self.gather_information(cli_data, leads_data_file_name, user_name)
        except json.JSONDecodeError as e:
            print(f"An error occurred: {e}")
            fallback_message = f"""Subject: Looking to Connect

                                    Dear [Lead Name],

                                    I hope this message finds you well. My name is [user_name], and I am reaching out to connect with you regarding {leads_data_file_name}. In today's dynamic landscape, connecting with professionals like yourself is essential, and I believe we can mutually benefit from sharing insights and experiences.

                                    I am interested in discussing {leads_data_file_name} and exploring potential opportunities for collaboration. Your expertise in this area caught my attention, and I would value the opportunity to connect and learn from your insights.

                                    Best regards,
                                    {user_name}
                                    """
            self.loading_label.setText(fallback_message)
        
    @asyncSlot()
    async def gather_information(self, cli_data, leads_data_file_name, user_name):
        lead_name_task = get_lead_name(leads_data_file_name)
        lead_context_task = get_lead_context(leads_data_file_name)
        lead_name, lead_context = await asyncio.gather(lead_name_task, lead_context_task)
        self.lead_name = "jake"
        # try:
        #     message = await prompt_main(cli_data, lead_context, lead_name, user_name)
        #     self.loading_label.setText(message)
        # except json.JSONDecodeError as e:
        #     print(f"An error occurred: {e}")
        #     fallback_message = f"""Subject: Looking to Connect

        #                             Dear {lead_name},

        #                             I hope this message finds you well. My name is [user_name], and I am reaching out to connect with you regarding {leads_data_file_name}. In today's dynamic landscape, connecting with professionals like yourself is essential, and I believe we can mutually benefit from sharing insights and experiences.

        #                             I am interested in discussing {leads_data_file_name} and exploring potential opportunities for collaboration. Your expertise in this area caught my attention, and I would value the opportunity to connect and learn from your insights.

        #                             Best regards,
        #                             {user_name}
        #                             """
        #     self.loading_label.setText(fallback_message)

    @asyncSlot()
    async def main_report(self, leads_data_file_name): 
        await main_report(leads_data_file_name)

    async def linkedin_search_button(self):
        keyword = self.keyword_input.text()
        self.stacked_widget.setCurrentIndex(3)
        lead_name = self.lead_name
        print(lead_name)
        await self.profile_search(lead_name, keyword)

    @asyncSlot()
    async def profile_search(self, lead_name, keyword):
        try:
            await get_profile(True, lead_name, keyword)
        except TimeoutError as e:
            self.loading_linkedin_label.setText("Error finding linkedin profile")
        except Exception as e:
            self.loading_linkedin_label.setText("Error finding linkedin profile")

    def populate_linkedin_page(self):
        lead_name = self.lead_name
        file_name = re.sub(r'[^a-zA-Z0-9]+', '_', lead_name)
        output_dir = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..','leads_and_messages'))
        output_file_path = os.path.join(output_dir, f"{file_name}_profiles.txt")
        try:
            with open(output_file_path, 'r') as file:
                profiles_content = file.read()

            self.loading_linkedin_label.setText(profiles_content)
            self.loading_linkedin_label.setOpenExternalLinks(True)
            self.stacked_widget.setCurrentIndex(3)
            
        except FileNotFoundError:
            print(f"File not found: {output_file_path}")
            self.loading_linkedin_label.setText("Profiles file not found.")

    def show_first_page(self):
        self.stacked_widget.setCurrentIndex(0)

class ExpandableGroupBox(QGroupBox):
    def __init__(self, lead, parent=None):
        super().__init__(lead.get('lead-name') or lead.get('blog-name'), parent)
        self.setCheckable(True)
        self.setChecked(False)
        self.toggled.connect(self.toggle_expanded)

        self.lead = lead
        self.expanded_size = QSize(640, 200)
        self.collapsed_size = QSize(640, 75)

        self.layout = QVBoxLayout(self)
        self.name_label = QLabel(lead.get('lead-name') or lead.get('blog-name'))
        self.layout.addWidget(self.name_label)

    def toggle_expanded(self):
        if self.isChecked():
            self.setFixedSize(self.expanded_size)
            self.show_additional_data()
        else:
            self.setFixedSize(self.collapsed_size)
            self.show_name_only()

    def show_additional_data(self):
        origin_label = QLabel(f"Origin: {self.lead.get('origin', '')}")
        messages_label = QLabel(f"Generated Messages: {self.lead.get('generated-messages', '')}")


        self.layout.addWidget(origin_label)
        self.layout.addWidget(messages_label)

    def show_name_only(self):

        self.clear_layout()
        self.layout.addWidget(self.name_label)

    def clear_layout(self):

        for i in reversed(range(self.layout.count())):
            item = self.layout.itemAt(i)
            self.layout.removeItem(item)
            if item.widget():
                item.widget().setParent(None)
        

class Leads(QWidget):

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.tab_widget = QTabWidget(self)
        self.tab_widget.currentChanged.connect(self.tab_changed) 

        update_button = QPushButton("Update", self)
        update_button.clicked.connect(self.update_leads)

        tab_layout = QVBoxLayout(self)
        tab_layout.addWidget(update_button)
        tab_layout.addWidget(self.tab_widget)

        self.setStyleSheet("""
                            background-color: #93dbd5;
                            font-size: 16px;
                           """)

    def tab_changed(self, index):
        if index == 1:  
            self.update_leads()

    def update_leads(self):
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
                    
                    scroll_area = QScrollArea(self)
                    scroll_area.setWidgetResizable(True)

                    inner = QWidget()
                    layout = QVBoxLayout(inner)

                    for lead in json_data_list:
                        group_box = ExpandableGroupBox(lead)
                        layout.addWidget(group_box)

                    scroll_area.setWidget(inner)
                    self.tab_widget.addTab(scroll_area, file_name)
    
    def tab_exists(self, text):
        for index in range(self.tab_widget.count()):
            if self.tab_widget.tabText(index) == text:
                return True
        return False

class About(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        self.setStyleSheet("""
                            background: #93dbd5;
                            font-size: 18px;
                           """)

        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)

        team_info_group = QGroupBox("Meet The Team")
        team_layout = QVBoxLayout(team_info_group)

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
            "https://github.com/ImmanuelShin",
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

        # Adding to layouts
        team_layout.addLayout(member1_layout)
        team_layout.addLayout(member2_layout)
        team_layout.addLayout(member3_layout)
        team_layout.addLayout(member4_layout)
        team_layout.addLayout(member5_layout)

        scroll_area.setWidget(team_info_group)

        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)

    def create_member_layout(self, member_name, image_url, github_username, max_width, max_height):
        layout = QGridLayout()

        name_label = QLabel(member_name)
        name_label.setFixedWidth(200) 

        image_label = QLabel()

        if image_url.startswith("http"):
            image_data = requests.get(image_url).content
            pixmap = QPixmap.fromImage(QImage.fromData(image_data))
            pixmap = pixmap.scaled(QSize(max_width, max_height), aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio)
            image_label.setPixmap(pixmap)
        else:
            image_label.setPixmap(QPixmap(image_url))

        github_label = QTextBrowser()

        github_font = github_label.font()
        github_font.setPointSize(14) 
        github_label.setFont(github_font)
        github_label.setFixedWidth(325)

        github_text = f"<a style='text-decoration: none; color: black;' href='{github_username}'>GitHub: {github_username}</a>"
        github_label.setHtml(github_text)
        github_label.setOpenExternalLinks(True)
        github_label.anchorClicked.connect(self.open_url)

        layout.setRowStretch(0, 1)

        layout.addWidget(name_label, 0, 0, Qt.AlignmentFlag.AlignTop)
        layout.addWidget(image_label, 0, 1, Qt.AlignmentFlag.AlignTop)
        layout.addWidget(github_label, 0, 2, Qt.AlignmentFlag.AlignTop)

        return layout

    def open_url(self, link):
        url = link.toString()
        QDesktopServices.openUrl(QUrl(url))

class LeadGUI(QWidget):
    def __init__(self, loop=None):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Radial Gradient Background
        gradient = QRadialGradient(self.width() / 2, self.height() / 2, 1000)
        gradient.setColorAt(0, QColor("#599190"))
        gradient.setColorAt(1, QColor("#3a6363"))
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setBrush(QPalette.ColorRole.Window, gradient)
        self.setPalette(palette)

        main_layout = QGridLayout(self)

        # Navbar
        navbar_frame = QFrame(self)
        navbar_layout = QVBoxLayout(navbar_frame)
        navbar_layout.setContentsMargins(0, 0, 0, 0)

        # Button Color
        button_color = "#93dbd5"
        button_style = f"""
            QPushButton {{ 
                background-color: {button_color}; 
                border: none; 
                padding: 0 40px 0 40px; 
                font-size: 20px
                }}
            QPushButton:hover {{ 
                background-color: #78f0e6; 
                }}
            QPushButton:pressed {{ 
                background-color: #78f0e6; 
                padding-top: 5px;
                }}
            """
        button_size_policy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        button_size_policy.setHeightForWidth(True)

        generate_renderer = QSvgRenderer("app/gui/assets/have-an-idea-svgrepo-com.svg")
        leads_renderer = QSvgRenderer("app/gui/assets/about-us-svgrepo-com.svg")
        about_renderer = QSvgRenderer("app/gui/assets/about-svgrepo-com.svg")

        generate_tab_button = QPushButton("Generate", self)
        generate_tab_button.setStyleSheet(button_style)
        generate_tab_button.setSizePolicy(button_size_policy)
        generate_pixmap = QPixmap(100, 100) 
        generate_pixmap.fill(Qt.GlobalColor.transparent)
        generate_renderer.render(QPainter(generate_pixmap))
        generate_tab_button.setIcon(QIcon(generate_pixmap))
        
        leads_tab_button = QPushButton("Leads", self)
        leads_tab_button.setStyleSheet(button_style)
        leads_tab_button.setSizePolicy(button_size_policy)
        leads_pixmap = QPixmap(500, 500) 
        leads_pixmap.fill(Qt.GlobalColor.transparent)
        leads_renderer.render(QPainter(leads_pixmap))
        leads_tab_button.setIcon(QIcon(leads_pixmap))
        
        about_tab_button = QPushButton("About", self)
        about_tab_button.setStyleSheet(button_style)
        about_tab_button.setSizePolicy(button_size_policy)
        about_pixmap = QPixmap(100, 100) 
        about_pixmap.fill(Qt.GlobalColor.transparent)
        about_renderer.render(QPainter(about_pixmap))
        about_tab_button.setIcon(QIcon(about_pixmap))

        navbar_layout.setSpacing(0)

        navbar_layout.addWidget(generate_tab_button)
        navbar_layout.addWidget(leads_tab_button)
        navbar_layout.addWidget(about_tab_button)

        # Content Frame
        content_frame = QFrame(self)
        content_layout = QGridLayout(content_frame)
        content_frame.setContentsMargins(0, 0, 0, 0)

        content_layout.setColumnStretch(0, 1)  
        content_layout.setColumnStretch(1, 16)  
        content_layout.setColumnStretch(2, 1)  
        content_layout.setRowStretch(0, 1)  
        content_layout.setRowStretch(1, 12)  
        content_layout.setRowStretch(2, 1)  

        stacked_frame = QFrame(content_frame)
        self.stacked_widget = QStackedWidget(stacked_frame)
        self.stacked_widget.setFixedSize(700, 500)

        # Pages
        self.generate_page = Generation()
        self.generate_page.setFixedSize(700, 500)
        self.leads_page = Leads()
        self.leads_page.setFixedSize(700, 500)
        self.about_page = About()
        self.about_page.setFixedSize(700, 500)

        self.stacked_widget.addWidget(self.generate_page)
        self.stacked_widget.addWidget(self.leads_page)
        self.stacked_widget.addWidget(self.about_page)

        content_layout.addWidget(stacked_frame, 1, 1, 1, 1)

        navbar_frame.setFixedSize(200, 600)
        content_frame.setFixedSize(800, 600)

        main_layout.addWidget(navbar_frame, 0, 0)
        main_layout.addWidget(content_frame, 0, 1)

        generate_tab_button.clicked.connect(self.show_generate_tab)
        leads_tab_button.clicked.connect(self.show_leads_tab)
        about_tab_button.clicked.connect(self.show_about_tab)

        self.setWindowTitle('Lead Generation GUI')
        self.show()

    def show_generate_tab(self):
        self.stacked_widget.setCurrentIndex(0)

    def show_leads_tab(self):
        self.stacked_widget.setCurrentIndex(1)

    def show_about_tab(self):
        self.stacked_widget.setCurrentIndex(2)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    window = LeadGUI(loop)
    window.show()

    app.aboutToQuit.connect(loop.close) 
    
    with loop:
        loop.run_forever()
        sys.exit(app.exec())
    
    