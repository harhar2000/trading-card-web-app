import streamlit as st
from PIL import Image
import random
import uuid

# TASKS
    # Change photo button doesn't work when the card has already been created
    # Some buttons like trade and delete, need to be clicked twice to work. 

# Function to generate a random card image for illustration purposes
def generate_card_image():
    card_img = Image.new('RGB', (300, 450), color=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
    return card_img

# Initialize session state to store cards and form fields
if 'cards' not in st.session_state:
    st.session_state.cards = {}
if 'player_name' not in st.session_state:
    st.session_state.player_name = ""
if 'character_name' not in st.session_state:
    st.session_state.character_name = ""
if 'traits' not in st.session_state:
    st.session_state.traits = ""
if 'image' not in st.session_state:
    st.session_state.image = None
if 'trade_in_progress' not in st.session_state:
    st.session_state.trade_in_progress = False
if 'selected_card_for_trade' not in st.session_state:
    st.session_state.selected_card_for_trade = None

# App Title
st.title("Fantasy Trading Cards")

# User Input Section
st.sidebar.header("Create Your Card")

# Input fields for card creation
st.session_state.player_name = st.sidebar.text_input("Your Name", value=st.session_state.player_name)
st.session_state.character_name = st.sidebar.text_input("Character Name", value=st.session_state.character_name)
st.session_state.traits = st.sidebar.text_area("Traits (comma separated)", value=st.session_state.traits, help="List the traits of the character, e.g., Strength, Intelligence, Agility")
st.session_state.image = st.sidebar.file_uploader("Upload Image")

# Button to create a new card
if st.sidebar.button("Create Card"):
    if st.session_state.player_name and st.session_state.character_name and st.session_state.traits:
        # Create a new card
        card_id = str(uuid.uuid4())  # Unique ID for each card
        card_data = {
            'player_name': st.session_state.player_name,
            'character_name': st.session_state.character_name,
            'traits': st.session_state.traits.split(','),
            'image': st.session_state.image
        }
        
        # Store the card in session state
        if st.session_state.player_name not in st.session_state.cards:
            st.session_state.cards[st.session_state.player_name] = []
        st.session_state.cards[st.session_state.player_name].append(card_data)
        st.sidebar.success(f"Card '{st.session_state.character_name}' created!")
        
        # Reset the input fields after card creation
        st.session_state.character_name = ""
        st.session_state.traits = ""
        st.session_state.image = None
    else:
        st.sidebar.error("Please fill in all the fields.")

# Display Cards for the current player in a grid layout
st.header(f"{st.session_state.player_name}'s Cards")
if st.session_state.player_name and st.session_state.player_name in st.session_state.cards:
    cards = st.session_state.cards[st.session_state.player_name]
    
    # Define the number of columns you want in the grid
    cols_per_row = 3
    cols = st.columns(cols_per_row)
    
    for i, card in enumerate(cards):
        # Assign each card to a column in the grid
        with cols[i % cols_per_row]:
            st.subheader(card['character_name'])
            if card['image']:
                st.image(card['image'], caption="Card Image", use_column_width=True)
            else:
                st.image(generate_card_image(), caption="Generated Image", use_column_width=True)
            st.text(f"Traits: {', '.join(card['traits'])}")
            
            # Add a Delete button for each card
            if st.button(f"Delete '{card['character_name']}'", key=f"delete_{i}"):
                # Remove the card from session state
                st.session_state.cards[st.session_state.player_name].remove(card)
                st.success(f"Card '{card['character_name']}' deleted!")

            # Add Trade button for each card
            if st.button(f"Trade '{card['character_name']}'", key=f"trade_{i}"):
                # Mark trade as in progress and store selected card for trade
                st.session_state.trade_in_progress = True
                st.session_state.selected_card_for_trade = card

# Trade Confirmation Section
if st.session_state.trade_in_progress and st.session_state.selected_card_for_trade:
    card_to_trade = st.session_state.selected_card_for_trade

    st.header(f"Trading '{card_to_trade['character_name']}'")
    
    trader_name = st.selectbox("Choose a player to trade with", [p for p in st.session_state.cards.keys() if p != st.session_state.player_name])

    if trader_name:
        trader_card_options = [(tc['character_name'], idx) for idx, tc in enumerate(st.session_state.cards[trader_name])]
        selected_trader_card = st.selectbox(f"Select a card from {trader_name}", trader_card_options, format_func=lambda x: x[0])

        if st.button("Confirm Trade"):
            # Get the selected trader's card
            trader_card = st.session_state.cards[trader_name][selected_trader_card[1]]

            # Perform the trade (swap cards)
            st.session_state.cards[st.session_state.player_name].remove(card_to_trade)
            st.session_state.cards[trader_name].remove(trader_card)
            st.session_state.cards[st.session_state.player_name].append(trader_card)
            st.session_state.cards[trader_name].append(card_to_trade)

            st.session_state.trade_in_progress = False
            st.session_state.selected_card_for_trade = None

            st.success(f"Trade completed! You traded '{card_to_trade['character_name']}' for '{trader_card['character_name']}' with {trader_name}.")