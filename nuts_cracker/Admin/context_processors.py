# context_processors.py

from  Users.models import Order 

def order_count(request):
    count = Order.objects.filter(status='order-placed').count()
    return {'order_count': count}
