from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserIconView
import requests


class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        self.username = TextInput(hint_text='Username', multiline=False)
        self.password = TextInput(hint_text='Password', password=True, multiline=False)
        login_button = Button(text='Login')
        register_button = Button(text='Register')

        login_button.bind(on_press=self.login)
        register_button.bind(on_press=self.register)

        layout.add_widget(self.username)
        layout.add_widget(self.password)
        layout.add_widget(login_button)
        layout.add_widget(register_button)

        self.add_widget(layout)

    def login(self, instance):
        username = self.username.text
        password = self.password.text
        response = requests.post('http://localhost:5000/login', json={'username': username, 'password': password})
        if response.status_code == 200:
            App.get_running_app().root.current = 'report_issue'
        else:
            self.show_error(response.json().get('message'))

    def register(self, instance):
        username = self.username.text
        password = self.password.text
        response = requests.post('http://localhost:5000/register', json={'username': username, 'password': password})
        if response.status_code == 200:
            self.show_error('User registered successfully')
        else:
            self.show_error(response.json().get('message'))

    def show_error(self, message):
        self.add_widget(Label(text=message))


class ReportIssueScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        self.issue = TextInput(hint_text='Issue', multiline=False)
        self.description = TextInput(hint_text='Description', multiline=True)
        self.coordinates = TextInput(hint_text='Coordinates', multiline=False)
        self.image_path = TextInput(hint_text='Image Path', multiline=False)
        filechooser = FileChooserIconView(on_submit=self.select_image)
        submit_button = Button(text='Submit Report')

        submit_button.bind(on_press=self.submit_report)

        layout.add_widget(self.issue)
        layout.add_widget(self.description)
        layout.add_widget(self.coordinates)
        layout.add_widget(self.image_path)
        layout.add_widget(filechooser)
        layout.add_widget(submit_button)

        self.add_widget(layout)

    def select_image(self, filechooser, selection, touch):
        self.image_path.text = selection[0] if selection else ''

    def submit_report(self, instance):
        username = App.get_running_app().root.get_screen('login').username.text
        issue = self.issue.text
        description = self.description.text
        coordinates = self.coordinates.text
        image_path = self.image_path.text

        files = {'image': open(image_path, 'rb')}
        data = {
            'username': username,
            'issue': issue,
            'description': description,
            'coordinates': coordinates
        }
        response = requests.post('http://localhost:5000/report_issue', files=files, data=data)
        if response.status_code == 200:
            self.show_message('Report submitted successfully')
        else:
            self.show_message('Error submitting report')

    def show_message(self, message):
        self.add_widget(Label(text=message))


class FixIssueScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        self.report_id = TextInput(hint_text='Report ID', multiline=False)
        self.time_taken = TextInput(hint_text='Time Taken (minutes)', multiline=False)
        self.after_image_path = TextInput(hint_text='After Image Path', multiline=False)
        filechooser = FileChooserIconView(on_submit=self.select_image)
        submit_button = Button(text='Submit Fix')

        submit_button.bind(on_press=self.submit_fix)

        layout.add_widget(self.report_id)
        layout.add_widget(self.time_taken)
        layout.add_widget(self.after_image_path)
        layout.add_widget(filechooser)
        layout.add_widget(submit_button)

        self.add_widget(layout)

    def select_image(self, filechooser, selection, touch):
        self.after_image_path.text = selection[0] if selection else ''

    def submit_fix(self, instance):
        username = App.get_running_app().root.get_screen('login').username.text
        report_id = self.report_id.text
        time_taken = self.time_taken.text
        after_image_path = self.after_image_path.text

        files = {'after_image': open(after_image_path, 'rb')}
        data = {
            'username': username,
            'report_id': report_id,
            'time_taken': time_taken
        }
        response = requests.post('http://localhost:5000/volunteer', files=files, data=data)
        if response.status_code == 200:
            self.show_message('Fix submitted successfully')
        else:
            self.show_message('Error submitting fix')

    def show_message(self, message):
        self.add_widget(Label(text=message))


class IssueApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(ReportIssueScreen(name='report_issue'))
        sm.add_widget(FixIssueScreen(name='fix_issue'))
        return sm


if __name__ == '__main__':
    IssueApp().run()
