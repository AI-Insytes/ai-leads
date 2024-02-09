import sys, json, asyncio, re, os, requests
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QFrame, QStackedLayout, QStackedWidget, QScrollArea, QGroupBox, QFormLayout, QTabWidget, QTextBrowser
from PyQt6.QtGui import QPixmap, QDesktopServices, QImage
from PyQt6.QtCore import QUrl, Qt, QSize
from qasync import QEventLoop, asyncSlot

from app.search import search_main
from app.prompt import prompt_main, get_lead_context, get_lead_name


class Generation(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.stacked_widget = QStackedWidget(self)

        # first page
        first_layout = QVBoxLayout()
        self.username_label = QLabel("What is your name?")
        self.username_input = QLineEdit(self)
        self.keyword_query_label = QLabel("What category of professional are you aiming to connect with? Specify the industry or area of expertise you're interested in for leads.")
        self.keyword_query_input = QLineEdit(self)
        submit_button = QPushButton("Submit", self)
        submit_button.clicked.connect(lambda: asyncio.create_task(self.show_next_page()))
        first_layout.addWidget(self.username_label)
        first_layout.addWidget(self.username_input)
        first_layout.addWidget(self.keyword_query_label)
        first_layout.addWidget(self.keyword_query_input)
        first_layout.addWidget(submit_button)

        first_layout_widget = QWidget()
        first_layout_widget.setLayout(first_layout)

        # second page
        second_layout = QVBoxLayout()

        self.message_length_label = QLabel("Does your message to leads have any length constraints?")
        self.message_length_combobox = QComboBox(self)
        self.message_length_combobox.addItems(['Quick note', '280 characters - Twitter/X post', '300 characters - LinkedIn connection request message'])

        self.message_purpose_label = QLabel("What is the objective of your outreach message?")
        self.message_purpose_input = QLineEdit(self)

        self.user_context_label = QLabel("Provide additional context about yourself and or your request (e.g., is there an event or product they may be interested in?)")
        self.user_context_input = QLineEdit(self)

        self.message_tone_label = QLabel("Choose the tone for your outreach message:")
        self.message_tone_combobox = QComboBox(self)
        self.message_tone_combobox.addItems(['Professional', 'Chill', 'Persuasive', 'Warm'])

        self.submit_button = QPushButton("Submit", self)
        self.submit_button.clicked.connect(lambda: asyncio.create_task(self.submit_clicked()))

        second_layout.addWidget(self.message_length_label)
        second_layout.addWidget(self.message_length_combobox)
        second_layout.addWidget(self.message_purpose_label)
        second_layout.addWidget(self.message_purpose_input)
        second_layout.addWidget(self.user_context_label)
        second_layout.addWidget(self.user_context_input)
        second_layout.addWidget(self.message_tone_label)
        second_layout.addWidget(self.message_tone_combobox)
        second_layout.addWidget(self.submit_button)

        second_layout_widget = QWidget()
        second_layout_widget.setLayout(second_layout)

        # Third page
        third_layout = QVBoxLayout()
        self.loading_label = QLabel("Generating message...")
        third_layout.addWidget(self.loading_label)

        third_layout_widget = QWidget()
        third_layout_widget.setLayout(third_layout)

        self.stacked_widget.addWidget(first_layout_widget)
        self.stacked_widget.addWidget(second_layout_widget)
        self.stacked_widget.addWidget(third_layout_widget)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.stacked_widget)
        self.setLayout(main_layout)

        self.username_in = self.username_input
        self.keyword_input = self.keyword_query_input
        self.length_combobox = self.message_length_combobox
        self.purpose_input = self.message_purpose_input
        self.context_input = self.user_context_input
        self.tone_combobox = self.message_tone_combobox

    async def show_next_page(self):
        keyword = self.keyword_query_input.text()
        sanitized_keyword = re.sub(r'[^a-zA-Z0-9]+', '_', keyword)
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
        print(cli_data, leads_data_file_name, user_name)
        self.stacked_widget.setCurrentIndex(2)

        await self.gather_information(cli_data, leads_data_file_name, user_name)
        
    @asyncSlot()
    async def gather_information(self, cli_data, leads_data_file_name, user_name):
        lead_name_task = get_lead_name(leads_data_file_name)
        lead_context_task = get_lead_context(leads_data_file_name)
        lead_name, lead_context = await asyncio.gather(lead_name_task, lead_context_task)
        print(cli_data, lead_name, lead_context, user_name)
        message = await prompt_main(cli_data, lead_name, lead_context, user_name)
        self.loading_label.setText(message)
        

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
                        name = lead.get('lead-name') or lead.get('blog-name')
                        origin = lead.get('origin', '')
                        generated_messages = lead.get('generated-messages', '')

                        group_box = QGroupBox(name)
                        form_layout = QFormLayout(group_box)
                        form_layout.addRow("Name:", QLabel(name))
                        form_layout.addRow("Origin:", QLabel(origin))
                        form_layout.addRow("Generated Messages:", QLabel(generated_messages))
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

        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)

        team_info_group = QGroupBox("Team Information")
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
        layout = QHBoxLayout()

        name_label = QLabel(member_name)
        image_label = QLabel()
        
        # Load the image from the URL
        if image_url.startswith("http"):
            image_data = requests.get(image_url).content
            pixmap = QPixmap.fromImage(QImage.fromData(image_data))
            pixmap = pixmap.scaled(QSize(max_width, max_height), aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio)
            image_label.setPixmap(pixmap)
        else:
            image_label.setPixmap(QPixmap(image_url))  # Assume it's a local path

        github_label = QTextBrowser()
        github_text = f"GitHub: {github_username}\n"
        github_label.setPlainText(github_text)
        github_label.setOpenExternalLinks(True)
        github_label.anchorClicked.connect(self.open_url)

        layout.addWidget(name_label)
        layout.addWidget(image_label)
        layout.addWidget(github_label)

        return layout

    def open_url(self, link):
        # Open the clicked link in an external browser
        url = link.toString()
        QDesktopServices.openUrl(QUrl(url))

class LeadGUI(QWidget):
    def __init__(self, loop=None):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        main_layout = QHBoxLayout()

        # Left-hand side navbar
        navbar_frame = QFrame(self)
        navbar_layout = QVBoxLayout(navbar_frame)


        generate_tab_button = QPushButton("Generate", self)
        leads_tab_button = QPushButton("Leads", self)
        about_tab_button = QPushButton("About", self)

        navbar_layout.addWidget(generate_tab_button)
        navbar_layout.addWidget(leads_tab_button)
        navbar_layout.addWidget(about_tab_button)

        # Content Frame
        content_frame = QFrame(self)
        self.stacked_layout = QStackedLayout(content_frame)

        self.generate_page = Generation()
        self.leads_page = Leads()
        self.about_page = About()


        self.stacked_layout.addWidget(self.generate_page)
        self.stacked_layout.addWidget(self.leads_page)
        self.stacked_layout.addWidget(self.about_page)

        main_layout.addWidget(navbar_frame)
        main_layout.addWidget(content_frame)

        self.setLayout(main_layout)

        generate_tab_button.clicked.connect(self.show_generate_tab)
        leads_tab_button.clicked.connect(self.show_leads_tab)
        about_tab_button.clicked.connect(self.show_about_tab)


        self.setWindowTitle('Lead Generation GUI')
        self.show()

    def show_generate_tab(self):
        self.stacked_layout.setCurrentIndex(0)
    
    def show_leads_tab(self):
        self.stacked_layout.setCurrentIndex(1)

    def show_about_tab(self):
        self.stacked_layout.setCurrentIndex(2)

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
    
    