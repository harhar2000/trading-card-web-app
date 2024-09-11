import streamlit as st
from PIL import Image
import random
import uuid

# TASKS
    # Edit card text
    # Share to socials 
    # Add another card
    # Trade function
    # Empty text boxes after card is created ready next one. 
    # Delete button
    # View cards closer together in grid on page 


# Function to generate a random card image for illustration purposes
def generate_card_image():
    card_img = Image.new('RGB', (300, 450), color=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
    return card_img


# Initialize session state to store cards
if 'cards' not in st.session_state:
    st.session_state.cards = {}

# App Title
st.title("Fantasy Trading Cards")

# User Input Section
st.sidebar.header("Create Your Card")

# Input fields for card creation
player_name = st.sidebar.text_input("Your Name")
character_name = st.sidebar.text_input("Character Name")
traits = st.sidebar.text_area("Traits (comma separated)", help="List the traits of the character, e.g., Strength, Intelligence, Agility")
image = st.sidebar.file_uploader("Upload Image")

# Button to create a new card
if st.sidebar.button("Create Card"):
    if player_name and character_name and traits:
        # Create a new card
        card_id = str(uuid.uuid4())  # Unique ID for each card
        card_data = {
            'player_name': player_name,
            'character_name': character_name,
            'traits': traits.split(','),
            'image': image
        }
        
        # Store the card in session state
        if player_name not in st.session_state.cards:
            st.session_state.cards[player_name] = []
        st.session_state.cards[player_name].append(card_data)
        st.sidebar.success(f"Card '{character_name}' created!")
    else:
        st.sidebar.error("Please fill in all the fields.")

# Display Cards for the current player
st.header(f"{player_name}'s Cards")
if player_name and player_name in st.session_state.cards:
    for i, card in enumerate(st.session_state.cards[player_name]):
        st.subheader(f"Card {i+1}: {card['character_name']}")
        st.image(card['image'], caption=f"Card Image", use_column_width=True)
        st.text(f"Traits: {', '.join(card['traits'])}")

# Section to Trade Cards
st.sidebar.header("Trade Cards")

trader_name = st.sidebar.text_input("Trade with (Player Name)")
if trader_name and st.sidebar.button("Initiate Trade"):
    if trader_name in st.session_state.cards and player_name in st.session_state.cards:
        st.write(f"Trading between {player_name} and {trader_name}")

        # Display Player's Cards to Choose from for Trading
        st.write(f"{player_name}'s Cards")
        selected_card_player = st.selectbox(f"Select {player_name}'s card to trade", [card['character_name'] for card in st.session_state.cards[player_name]])

        # Display Trader's Cards to Choose from for Trading
        st.write(f"{trader_name}'s Cards")
        selected_card_trader = st.selectbox(f"Select {trader_name}'s card to trade", [card['character_name'] for card in st.session_state.cards[trader_name]])

        if st.button("Confirm Trade"):
            # Perform the trade (swap cards between players)
            player_card = next(card for card in st.session_state.cards[player_name] if card['character_name'] == selected_card_player)
            trader_card = next(card for card in st.session_state.cards[trader_name] if card['character_name'] == selected_card_trader)
            
            # Swap the cards
            st.session_state.cards[player_name].remove(player_card)
            st.session_state.cards[trader_name].remove(trader_card)
            st.session_state.cards[player_name].append(trader_card)
            st.session_state.cards[trader_name].append(player_card)
            
            st.success(f"Trade completed: {player_name} traded '{selected_card_player}' for '{selected_card_trader}' with {trader_name}.")
    else:
        st.sidebar.error("Both players must have cards to trade.")
