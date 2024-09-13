import streamlit as st
from PIL import Image
import random
import uuid

# TASKS
    # Share to socials 
    # Trade function
    # Change photo button doesn't work when the card has already been created
    # Delete button



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
            
            # Add an Edit button for each card
            if st.button(f"Edit '{card['character_name']}'", key=f"edit_{i}"):
                # Allow the user to edit the card's details
                new_character_name = st.text_input("Edit Character Name", value=card['character_name'], key=f"name_{i}")
                new_traits = st.text_area("Edit Traits (comma separated)", value=", ".join(card['traits']), key=f"traits_{i}")
                new_image = st.file_uploader("Upload New Image (Optional)", key=f"image_{i}")
                
                if st.button(f"Save Changes for '{card['character_name']}'", key=f"save_{i}"):
                    # Update the card with the new values
                    card['character_name'] = new_character_name
                    card['traits'] = [trait.strip() for trait in new_traits.split(',')]
                    if new_image:
                        card['image'] = new_image
                    st.success(f"Card '{new_character_name}' updated!")

# Section to Trade Cards
st.sidebar.header("Trade Cards")

trader_name = st.sidebar.text_input("Trade with (Player Name)")
if trader_name and st.sidebar.button("Initiate Trade"):
    if trader_name in st.session_state.cards and st.session_state.player_name in st.session_state.cards:
        st.write(f"Trading between {st.session_state.player_name} and {trader_name}")

        # Display Player's Cards to Choose from for Trading
        st.write(f"{st.session_state.player_name}'s Cards")
        selected_card_player = st.selectbox(f"Select {st.session_state.player_name}'s card to trade", [card['character_name'] for card in st.session_state.cards[st.session_state.player_name]])

        # Display Trader's Cards to Choose from for Trading
        st.write(f"{trader_name}'s Cards")
        selected_card_trader = st.selectbox(f"Select {trader_name}'s card to trade", [card['character_name'] for card in st.session_state.cards[trader_name]])

        if st.button("Confirm Trade"):
            # Perform the trade (swap cards between players)
            player_card = next(card for card in st.session_state.cards[st.session_state.player_name] if card['character_name'] == selected_card_player)
            trader_card = next(card for card in st.session_state.cards[trader_name] if card['character_name'] == selected_card_trader)
            
            # Swap the cards
            st.session_state.cards[st.session_state.player_name].remove(player_card)
            st.session_state.cards[trader_name].remove(trader_card)
            st.session_state.cards[st.session_state.player_name].append(trader_card)
            st.session_state.cards[trader_name].append(player_card)
            
            st.success(f"Trade completed: {st.session_state.player_name} traded '{selected_card_player}' for '{selected_card_trader}' with {trader_name}.")
    else:
        st.sidebar.error("Both players must have cards to trade.")