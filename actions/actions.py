from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from supabase import create_client, Client
import logging

logging.basicConfig(level=logging.DEBUG)

# Initialize Supabase client
SUPABASE_URL = "https://tlzgtdnnuzqvzpxexlsm.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRsemd0ZG5udXpxdnpweGV4bHNtIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDg0NDc0OTksImV4cCI6MjA2NDAyMzQ5OX0.j3S8ZrJ_SJzaNDOwU55ebx6Mb5W3OByNp3nihnSZpPk"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

class ActionCheckItemAvailability(Action):

    def name(self) -> Text:
        return "action_check_item_availability"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Get item name from the latest entity (adjust slot name as needed)
        item = next(tracker.get_latest_entity_values("item"), None)
        logging.debug(f"Received item to check: {item}")

        if not item:
            dispatcher.utter_message(text="I couldn't understand the item you're looking for.")
            return []

        try:
            logging.debug(f"Querying Supabase for item: {item}")
            response = supabase.table("pantry").select("*").ilike("name", f"%{item}%").execute()
            logging.debug(f"Supabase response: {response}")
        except Exception as e:
            logging.error(f"Error querying Supabase: {e}")
            dispatcher.utter_message(text="Sorry, I'm having trouble accessing the pantry data right now.")
            return []

        if response.data:
            item_data = response.data[0]
            quantity = item_data.get("quantity", "unknown")
            dispatcher.utter_message(text=f"Yes, we have {quantity} units of {item}.")
        else:
            dispatcher.utter_message(text=f"Sorry, {item} is not in the pantry.")

        return []
