from sentence_transformers import SentenceTransformer, util
from transformers import pipeline
import numpy as np
import uuid
import datetime

# --- Configuration ---
SIMILARITY_THRESHOLD = 0.8
MEMBERS_FOR_MATCH = 2
MODEL_NAME = 'all-MiniLM-L6-v2'
CONSENSUS_LOG_FILE = "public_consensus.txt"

# --- Load NLP Models ---
print("Loading NLP models...")
model = SentenceTransformer(MODEL_NAME)
sentiment_analyzer = pipeline("sentiment-analysis")
print("Models loaded.")

# --- Data Structures ---
cells = {}
users = {} 

def process_trait(user_id, trait, all_traits):
    global cells
    user = users[user_id]
    previous_cell_id = user.get("current_cell_id")

    trait_embedding = model.encode(trait, convert_to_tensor=True)
    trait_sentiment = sentiment_analyzer(trait)[0]['label']
    
    # --- Find best matching cell ---
    best_cell_id, similarity = None, 0
    if previous_cell_id and previous_cell_id in cells:
        # Check similarity only with the current cell to see if alignment continues
        prev_cell_data = cells[previous_cell_id]
        if prev_cell_data["sentiment"] == trait_sentiment:
            similarity = util.pytorch_cos_sim(trait_embedding, prev_cell_data["embedding"])[0][0].item()
            if similarity >= SIMILARITY_THRESHOLD:
                best_cell_id = previous_cell_id

    # --- Update cell membership ---
    if previous_cell_id and previous_cell_id in cells:
        cells[previous_cell_id]["member_ids"].discard(user_id)
        if not cells[previous_cell_id]["member_ids"]:
            del cells[previous_cell_id]

    if best_cell_id:
        target_cell_id = best_cell_id
        cells[target_cell_id]["member_ids"].add(user_id)
        user["current_cell_id"] = target_cell_id
        cells[target_cell_id]["defining_traits"].append(trait)
        print(f"User {user['name']} continues alignment in cell defined by: '{cells[target_cell_id]['defining_traits'][0]}'")
    else:
        new_cell_id = uuid.uuid4()
        cells[new_cell_id] = {
            "defining_traits": all_traits + [trait],
            "embedding": trait_embedding,
            "sentiment": trait_sentiment,
            "member_ids": {user_id}
        }
        user["current_cell_id"] = new_cell_id
        print(f"User {user['name']} created a new cell with trait: '{trait}'")

    current_cell_id = user["current_cell_id"]
    if current_cell_id in cells:
        member_count = len(cells[current_cell_id]["member_ids"])
        print(f"The cell now has {member_count} member(s).")

def private_chat_session(user_ids):
    print("\n--- Private Chat Session Initiated ---")
    # Simple chat simulation for multiple users
    user_map = {uid: f"User {i+1}" for i, uid in enumerate(user_ids)}
    while True:
        for uid in user_ids:
            msg = input(f"{user_map[uid]}: ")
            if msg.lower() == 'exit':
                return

def log_consensus(cell):
    with open(CONSENSUS_LOG_FILE, "a") as f:
        f.write("="*40 + "\n")
        f.write(f"Consensus reached on: {datetime.datetime.now()}\n")
        f.write(f"Agreed-upon traits:\n")
        for trait in cell['defining_traits']:
            f.write(f"- {trait}\n")
        f.write("="*40 + "\n\n")

def main():
    print("\n--- Welcome to the TraitTribe Filtering Machine ---")
    
    player_id = uuid.uuid4()
    sim_user_1_id = uuid.uuid4()
    sim_user_2_id = uuid.uuid4()
    users[player_id] = {"name": "Player"}
    users[sim_user_1_id] = {"name": "Sim1"}
    users[sim_user_2_id] = {"name": "Sim2"}

    print("(You and two other simulated users are in the system.)")
    all_traits = []
    turn = 0

    while True:
        print("-" * 20)
        

        trait = input("State a trait to find your match (or 'quit'): ")
        if trait.lower() == 'quit': break
        all_traits.append(trait)

        process_trait(player_id, trait, all_traits)

        # --- Simulation Logic ---
        if turn == 0:
            print("(Simulating Sim1 and Sim2 agreeing with the first trait...)")
            process_trait(sim_user_1_id, trait, all_traits)
            process_trait(sim_user_2_id, trait, all_traits)
        elif turn == 1:
            print("(Simulating Sim1 agreeing, but Sim2 stating a different trait...)")
            process_trait(sim_user_1_id, trait, all_traits)
            process_trait(sim_user_2_id, "I prefer cats.", all_traits) # Sim2 splits off
        
        # Check for match condition after simulation
        player_cell_id = users[player_id].get("current_cell_id")
        if player_cell_id and player_cell_id in cells:
            player_cell = cells[player_cell_id]
            if len(player_cell["member_ids"]) == MEMBERS_FOR_MATCH:
                print("\n" + "="*40)
                print("!!! PERFECT MATCH FOUND !!!")
                log_consensus(player_cell)
                print(f"Consensus logged to {CONSENSUS_LOG_FILE}")
                
                enter_chat = input("Do you want to open a private chat? (yes/no): ")
                if enter_chat.lower() == 'yes':
                    private_chat_session(player_cell["member_ids"])
                    break
        turn += 1

if __name__ == "__main__":
    main()

