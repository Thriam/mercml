"""
Docstring for OOPS_Revision.electronics_abstraction
"""


from abc import ABC, abstractmethod


class Electronics(ABC):
    """
    Docstring for Electronics
    """
    @abstractmethod
    def play_video(self):
        """
        Docstring for play_video
        """
        print("From parent class")

    def stop_video(self):
        """
        Docstring for stop_video
        """
        print("From parent class")


class Laptop(Electronics):
    """
    Docstring for Laptop
    """
    def play_video(self):
        """
        Docstring for play_video
        """
        print("Press play button from keyboard")

    def stop_video(self):
        """
        Docstring for stop_video
        """
        print("Press pause button from keyboard")


class Mobile(Electronics):
    """
    Docstring for Mobile
    """
    def play_video(self):
        """
        Docstring for play_video
        """
        print("Press play button from keypad")

    def stop_video(self):
        """
        Docstring for stop_video
        """
        print("Press pause button from keypad")


if __name__ == "__main__":
    laptop = Laptop()
    laptop.play_video()

    mobile = Mobile()
    mobile.play_video()
