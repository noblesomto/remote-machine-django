from django.core.checks import messages
from .models import Chat
from .models import Serviceman_chat


def chat(request, expert_id, req_id):
    context = {}
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)

    userchat = User.objects.get(id=expert_id)
    req = Requests.objects.get(req_id=req_id)
    chat = Chat.objects.filter(req_id=req_id)
    image = RequestImage.objects.filter(req_id=req_id)
    req_id = req_id
    expert_id = expert_id
    notification = get_notification(request)
    
    context['notification'] = notification
    context['user'] = user
    context['userchat'] = userchat
    context['req'] = req
    context['chat'] = chat
    context['expert_id'] = expert_id
    context['image'] = image
    context['title'] = "Chat"
    if request.method == "POST":
        req_id = request.POST['req_id']
        message = request.POST['message']
        post = Chat.objects.create(
            user_id=User.objects.get(id=int(user_id)), req_id=req_id, message=message)
        post.save()
        
        return redirect('chat', expert_id=expert_id, req_id=req_id)
    else:
        return render(request, 'frontend/worker/chat.html', context)


