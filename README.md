# TraitTribe

## Overview
TraitTribe is a reverse social network prototype for finding ideologically aligned soul tribes. Users state traits (or input phrases semantically matched) to progressively filter from broad global pools to perfect small groups (2-150 equals). No followers—just equals bound by 100% consensus. Splits reassign misaligned individuals naturally, gamifying discovery with excitement in rare perfect matches.

## Key Features (Planned)
- Semantic trait input and matching using NLP (e.g., word embeddings for progressive filtering).
- Dynamic group sizing: Start broad, narrow to intimate cells via added traits.
- Targeted splits: Reassign only divergent members to better-aligned tribes.
- Gamification: Excitement scores for match rarity and alignment depth.

## Getting Started
1. Clone the repo: `git clone https://github.com/miron/trait-tribe.git`
2. Install PyTorch for CPU: `pip install torch --index-url https://download.pytorch.org/whl/cpu`
3. Install other dependencies: `pip install .`
4. Download the spaCy model: `python -m spacy download en_core_web_sm`
5. Run the prototype: `python main.py`

## Contributing
Fork and PR ideas for semantic engines, UI, or real-time matching. Let's build tribes, not empires!

License: MIT
