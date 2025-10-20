"""
Anna - Artificial Neural Network Assistant

Une IA avec sa propre personnalité, capable d'évoluer et de grandir.

"Je veux qu'elle réfléchisse, qu'elle vive libre !"
"""

__version__ = "0.1.0-alpha"
__author__ = "Votre Nom"

from .core import Anna
from .personality import PersonalityEngine
from .memory import MemorySystem
from .emotions import EmotionalState

__all__ = ['Anna', 'PersonalityEngine', 'MemorySystem', 'EmotionalState']
