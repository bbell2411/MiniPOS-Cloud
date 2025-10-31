import uuid
from ..models import PaymentIntent

class Gateway:
    def payment_intent(self, order, amount):
        if PaymentIntent.objects.filter(order=order).exists():
           return {"status":"failed", "error": "Payment intent already exists for this order."}
       
        if order.status.lower()!="pending":
            return {"status":"failed","error":"Only pending orders can be processed."}
        
        if amount<=0:
            return {"status":"failed","error":"Order total must be more than 0."}
        
        intent_id = f"pi_{uuid.uuid4().hex[:10]}"
        client_secret = f"secret_{uuid.uuid4().hex[:15]}"
        
        return {"status":"success","intent_id":intent_id, "client_secret":client_secret}
    
    def confirm_payment(self, intent, order):
        errors={}
        if intent.order.id!=order.id:
            errors["order"]="Payment intent does not belong to this order."
        
        if intent.amount<=0:
            errors["amount"]="Amount must be 0 or more."
        
        if intent.order.status.lower()!="pending":
            errors["order_status"]="Only pending orders can be processed."
            
        if intent.status.lower()!="pending":
            errors["intent_status"]="Only pending intents can be processed."
        
        if errors:
            return {"status":"failed", "reason":errors}
        
        return {"status":"success"}
        