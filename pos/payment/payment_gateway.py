from rest_framework.response import Response
import uuid

class Gateway:
    def payment_intent(self, amount):
        
        intent_id = f"pi_{uuid.uuid4().hex[:10]}"
        client_secret = f"secret_{uuid.uuid4().hex[:15]}"
        return {"intent_id":intent_id, "client_secret":client_secret}