from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required

import uuid


from .models import FeaturedPost, AffiliateLink

def featured_posts_view(request):
    posts = FeaturedPost.objects.filter(is_active=True)
    return render(request, 'monetize/featured_posts.html', {'posts': posts})

def affiliate_links_view(request):
    links = AffiliateLink.objects.filter(is_active=True)
    return render(request, 'monetize/affiliate_links.html', {'links': links})


# -------------------------
# Start M-Pesa Payment (STK Push)
# -------------------------
@login_required
def start_stk_push(request):
    if request.method == 'POST':
        txn_id = request.POST.get('txn_id')
        phone = request.POST.get('phone')
        txn = get_object_or_404( id=txn_id)
        # Here you would integrate actual M-Pesa API
        txn.mpesa_transaction_id = str(uuid.uuid4())
        txn.status = 'success'
        txn.save()
        return JsonResponse({'status': 'success', 'txn_id': txn.id})
    return JsonResponse({'status': 'error'}, status=400)

# -------------------------
# M-Pesa Callback (from API)
# -------------------------
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def mpesa_callback(request):
    # Parse M-Pesa response here
    # Update transaction status
    return HttpResponse("Callback received")
