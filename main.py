import random

from kivy.app import App
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.stacklayout import StackLayout


class Challenge(object):
    def __init__(self, word):
        self.word = word
        self.rest_word = word

    def guess_letter(self, letter):
        if self.rest_word[0] == letter:
            self.rest_word = self.rest_word[1:]
            return True
        return False

    def is_complete(self):
        return not self.rest_word


class ButtonGroup(StackLayout):
    word = "конструктор"
    button_size = 40

    def __init__(self, result_label, **kwargs):
        super().__init__(**kwargs)

        self.challenge = Challenge(self.word)
        self.result_label = result_label

        for letter in random.sample(self.word, len(self.word)):
            button = Button(text=letter,
                            width=self.button_size, height=self.button_size,
                            size_hint=(None, None))
            button.bind(on_press=self.on_button_press)
            self.add_widget(button)

        self.width = self.button_size * len(self.word)

    def on_button_press(self, button):
        if self.challenge.guess_letter(button.text):
            self.remove_widget(button)
            self.width -= self.button_size
            self.result_label.text += button.text

        if self.challenge.is_complete():
            label = Label(text='Challenge is complete')
            self.add_widget(label)
            self.width = label.width

            button = Button(text='Try Again!')
            button.bind(on_press=self.try_again)
            self.add_widget(button)

    def try_again(self, _):
        parent = self.parent
        parent.remove_widget(self)
        self.result_label.text = ''
        parent.add_widget(ButtonGroup(size_hint=(None, None), result_label=self.result_label))


class WordConstructorGame(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)

        label = Label(text="constructor", size_hint=(1, .1))
        self.add_widget(label)

        label = Label(text="", size_hint=(1, .1))
        self.add_widget(label)

        anchor_layout = AnchorLayout(anchor_x='center', anchor_y='center', size_hint=(1, .9))
        anchor_layout.add_widget(ButtonGroup(size_hint=(None, None), result_label=label))
        self.add_widget(anchor_layout)


class WordConstructorApp(App):
    def build(self):
        return WordConstructorGame()


if __name__ == '__main__':
    WordConstructorApp().run()
