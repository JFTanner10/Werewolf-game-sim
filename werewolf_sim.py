import random
import matplotlib.pyplot as plt
import streamlit as st

# --- Simulation logic ---
def simulate_werewolf_game(num_villagers, num_werewolves):
    players = ['villager'] * num_villagers + ['werewolf'] * num_werewolves
    random.shuffle(players)

    while True:
        num_villagers = players.count('villager')
        num_werewolves = players.count('werewolf')

        if num_werewolves == 0:
            return 'villagers'
        if num_werewolves >= num_villagers:
            return 'werewolves'

        # Night: Werewolves kill one villager
        villagers = [i for i, role in enumerate(players) if role == 'villager']
        if villagers:
            players.pop(random.choice(villagers))

        # Day: Random vote to eliminate one player
        if players:
            players.pop(random.randint(0, len(players) - 1))

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
