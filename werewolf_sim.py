import random
import matplotlib.pyplot as plt
import streamlit as st

# --- Simulation logic ---
def simulate_werewolf_game(num_villagers, num_werewolves):
    # Create and shuffle players
    players = [{'role': 'villager'} for _ in range(num_villagers)] + \
              [{'role': 'werewolf'} for _ in range(num_werewolves)]
    random.shuffle(players)

    while True:
        villagers_alive = [p for p in players if p['role'] == 'villager']
        werewolves_alive = [p for p in players if p['role'] == 'werewolf']

        # Win conditions
        if not werewolves_alive:
            return 'villagers'
        if len(werewolves_alive) >= len(villagers_alive):
            return 'werewolves'

        # --- NIGHT PHASE ---
        # Werewolves kill one random villager
        if villagers_alive:
            victim = random.choice(villagers_alive)
            players.remove(victim)

        # Re-evaluate remaining players
        if not players:
            break

        # --- DAY PHASE ---
        votes = [0] * len(players)
        for i, voter in enumerate(players):
            # Determine valid vote targets
            if voter['role'] == 'villager':
                options = [j for j in range(len(players)) if j != i]
            else:  # werewolf
                options = [j for j in range(len(players)) if j != i and players[j]['role'] != 'werewolf']

            if options:
                chosen = random.choice(options)
                votes[chosen] += 1

        # Eliminate player with most votes (with tie-break)
        max_votes = max(votes)
        tied = [i for i, v in enumerate(votes) if v == max_votes]
        eliminated_index = random.choice(tied)
        players.pop(eliminated_index)

def simulate_multiple_games(n_simulations, villagers, werewolves):
    results = {'villagers': 0, 'werewolves': 0}
    for _ in range(n_simulations):
        winner = simulate_werewolf_game(villagers, werewolves)
        results[winner] += 1
    return results

# --- Streamlit UI ---
st.title("Werewolf Game Outcome Simulator")

villager_count = st.slider("Number of Villagers", 1, 20, 6)
werewolf_count = st.slider("Number of Werewolves", 1, 10, 2)
num_simulations = st.slider("Number of Simulations", 100, 5000, 1000, step=100)

if villager_count <= werewolf_count:
    st.error("Villagers must outnumber werewolves at the start for a fair game.")
else:
    results = simulate_multiple_games(num_simulations, villager_count, werewolf_count)

    # Pie chart
    labels = ['Villagers', 'Werewolves']
    sizes = [results['villagers'], results['werewolves']]
    colors = ['pink', 'purple']

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=colors)
    ax.axis('equal')
    ax.set_title(
        f"{num_simulations} simulations with "
        f"{villager_count} villagers and {werewolf_count} werewolves"
    )

    st.pyplot(fig)
