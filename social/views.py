from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from social.forms import CommentForm
from social.models import SavedEvent, Comment


def save_event(request):
    if request.method == 'POST':
        event_name = request.POST['event_name']
        event_venue = request.POST['event_venue']
        event_city = request.POST['event_city']
        event_state = request.POST['event_state']
        event_date = request.POST['event_date']
        event_image = request.POST['event_image']
        event_url = request.POST['event_url']

        print(event_name, event_venue, event_date)

        event = SavedEvent(
            author=request.user,
            event_name=event_name,
            event_venue=event_venue,
            event_city=event_city,
            event_state=event_state,
            event_date=event_date,
            event_image=event_image,
            event_url=event_url

        )

        event.save()

        messages.info(request, "Successfully saved!")

    return render(request, 'social.html')


def load_user_data(request):
    if request.user.is_authenticated:
        saved_events = SavedEvent.objects.all().filter(author=request.user)

    return render(request, 'social.html', {'saved_events': saved_events})


def delete_event(request, event_id):
    if request.user.is_authenticated:
        event = SavedEvent.objects.get(id=event_id)
        if event.author == request.user:
            saved_events = SavedEvent.objects.all().filter(author=request.user)

            if request.method == 'POST':
                event.delete()
            return render(request, 'social.html', {'saved_events': saved_events})
        else:
            messages.info(request, "You don't have permission to delete this event")
    return render(request, 'social.html')


def user_search(request):
    if request.method == 'POST':
        username = request.POST['username']
        user = User.objects.get(username=username)
        saved_events = SavedEvent.objects.all().filter(author=user)
    return render(request, 'social.html', {'saved_events': saved_events})


def save_comment(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            event_id = request.POST['event_id']
            comment_field = request.POST['comment']

            comment = Comment(
                author=request.user,
                saved_event=SavedEvent.objects.get(id=event_id),
                comment_field=comment_field

            )

            comment.save()
    return render(request, 'social.html')


def update_comment(request, comment_id):
    comment = Comment.objects.get(id=comment_id)

    if request.method == 'POST':
        updated_comment = request.POST['comment']
        comment.comment_field = updated_comment
        comment.save()

        return redirect('load')
    return render(request, 'social.html')


def delete_comment(request, comment_id):
    comment = Comment.objects.get(id=comment_id)

    if request.method == 'POST':
        comment.delete()
        return redirect('load')
    return render(request, 'social.html')


def profile(request):
    if request.user.is_authenticated:
        saved_events = SavedEvent.objects.all().filter(author=request.user)

    return render(request, 'profile.html', {'saved_events': saved_events})
