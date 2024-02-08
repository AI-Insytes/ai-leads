import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QFrame, QStackedLayout, QStackedWidget
class Generation(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.stacked_widget = QStackedWidget(self)

        # first page
        first_layout = QVBoxLayout()

        self.message_query_label = QLabel("What category of professional are you aiming to connect with? Specify the industry or area of expertise you're interested in for leads.")
        self.message_query_input = QLineEdit(self)
        submit_button = QPushButton("Submit", self)
        submit_button.clicked.connect(self.show_next_page)
        first_layout.addWidget(self.message_query_label)
        first_layout.addWidget(self.message_query_input)
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
        self.submit_button.clicked.connect(self.submit_clicked)

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

        self.stacked_widget.addWidget(first_layout_widget)
        self.stacked_widget.addWidget(second_layout_widget)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.stacked_widget)
        self.setLayout(main_layout)

    def show_next_page(self):
        message = self.message_query_input.text
        self.stacked_widget.setCurrentIndex(1)
        return message

    def submit_clicked(self):
        lead_category = self.message_query_input.text() 
        message_length = self.message_length_combobox.currentText()
        message_purpose = self.message_purpose_input.text()
        user_context = self.user_context_input.text()
        message_tone = self.message_tone_combobox.currentText()

        print(f"Lead category: {lead_category}")
        print(f"Selected length: {message_length if message_length else 'No limit'}")
        print(f"Message purpose: {message_purpose}")
        print(f"Message context: {user_context}")
        print(f"Selected tone: {message_tone}")

class Leads(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        test = QLabel("Test")
        layout.addWidget(test)

        self.setLayout(layout)

class About(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        pass

class LeadGUI(QWidget):
    def __init__(self):
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
    window = LeadGUI()
    sys.exit(app.exec_())