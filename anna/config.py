"""
Configuration pour Anna
"""

import os
from pathlib import Path

# Chemins du projet
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / 'data'
STATES_DIR = DATA_DIR / 'states'
MEMORIES_DIR = DATA_DIR / 'memories'
PERSONALITY_DIR = DATA_DIR / 'personality'

# Crée les dossiers s'ils n'existent pas
for directory in [DATA_DIR, STATES_DIR, MEMORIES_DIR, PERSONALITY_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Configuration d'Anna
DEFAULT_NAME = "Anna"
DEFAULT_STATE_FILE = STATES_DIR / "anna_current.json"

# Paramètres de mémoire
MAX_EPISODIC_MEMORIES = 10000
MAX_IMMEDIATE_MEMORY = 50

# Paramètres d'évolution
CONSCIOUSNESS_GROWTH_RATE = 0.001
PERSONALITY_EVOLUTION_RATE = 0.002
EMOTIONAL_DECAY_RATE = 0.05

# Paramètres de sauvegarde
AUTO_SAVE_ENABLED = True
AUTO_SAVE_INTERVAL = 100  # Toutes les N interactions

# API Keys (pour futures intégrations)
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY', '')

# Configuration de logging
LOG_LEVEL = 'INFO'
LOG_FILE = PROJECT_ROOT / 'anna.log'
