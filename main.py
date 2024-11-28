from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.recycleview import RecycleView


class AIModelApp(App):

    def build(self):
        # Main layout of the app
        main_layout = BoxLayout(orientation='horizontal')

        # Sidebar layout
        sidebar = BoxLayout(orientation='vertical', size_hint=(0.3, 1))
        sidebar.add_widget(Button(text='Models', size_hint_y=None, height=50, on_press=self.toggle_sidebar))

        # RecycleView for models list
        self.models_list = RecycleView(size_hint=(1, None), height=150)
        self.models_list.data = [{'text': f'Model {i}'} for i in range(1, 4)]

        # Sidebar with RecycleView
        sidebar.add_widget(self.models_list)

        # Main content layout
        main_content = BoxLayout(orientation='vertical', size_hint=(0.7, 1))
        main_content.add_widget(Label(text='WELCOME', font_size='32sp', size_hint_y=None, height=50))

        # Search bar
        search_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
        search_input = TextInput(hint_text='Search models...', size_hint_x=0.8)
        download_button = Button(text='Download', size_hint_x=0.2)
        search_layout.add_widget(search_input)
        search_layout.add_widget(download_button)

        main_content.add_widget(search_layout)

        # Add the sidebar and main content to the main layout
        main_layout.add_widget(sidebar)
        main_layout.add_widget(main_content)

        return main_layout

    def toggle_sidebar(self, instance):
        # Toggle the sidebar open/closed
        if self.models_list.height == 0:
            self.models_list.height = 150
        else:
            self.models_list.height = 0


if __name__ == '__main__':
    AIModelApp().run()
