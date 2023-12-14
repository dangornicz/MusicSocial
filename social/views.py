from django.contrib import messages
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect

from social.forms import CommentForm
from social.models import SavedEvent, Comment, Followers, Bio


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

        messages.info(request, "Event successfully saved!")

        return redirect('home')
    messages.info(request, "Error saving event")
    return render(request, 'home.html')


def news_feed(request):
    saved_events = []
    if request.user.is_authenticated:
        # get all 'user' field that signed-in-user is following (request.user == follower field)
        following = Followers.objects.all().filter(follower=request.user).values_list('user', flat=True)

        # for each 'user' field find their entries in SavedEvents model and append to list
        for one_user in following:
            saved_events_from_user = SavedEvent.objects.all().filter(author=one_user)
            saved_events.extend(saved_events_from_user)

        # sort all saved_events by the time_stamp (by most recent)
        saved_events.sort(key=lambda x: x.time_stamp, reverse=True)
    return render(request, 'social.html', {'saved_events': saved_events})


def delete_event(request, event_id):
    if request.user.is_authenticated:
        event = SavedEvent.objects.get(id=event_id)
        if event.author == request.user:

            username = request.user.username
            if request.method == 'POST':
                event.delete()
                messages.info(request, "Event deleted successfully!")

            return profile(request, username)

        else:
            # this else if unreachable since you don't have button render unless you are the user that created
            # event, but added anyways since followed your github repo
            messages.info(request, "You don't have permission to delete this event")
    return render(request, 'home.html')


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
            messages.info(request, "Comment saved successfully!")
    return news_feed(request)


def save_comment_profile(request, username):
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
            messages.info(request, "Comment saved successfully!")

    return profile(request, username)


def update_comment(request, comment_id):
    comment = Comment.objects.get(id=comment_id)

    if request.method == 'POST':
        updated_comment = request.POST['comment']
        if len(updated_comment) <= 200:
            comment.comment_field = updated_comment
            comment.save()
            messages.info(request, "Comment updated successfully")
            return news_feed(request)
        else:
            messages.info(request, "Comment was greater than 200 characters, please try again.")
        return news_feed(request)


def update_comment_profile(request, comment_id, username):
    comment = Comment.objects.get(id=comment_id)

    if request.method == 'POST':
        updated_comment = request.POST['comment']
        if len(updated_comment) <= 200:
            comment.comment_field = updated_comment
            comment.save()
            messages.info(request, "Comment updated successfully")
            return profile(request, username)
        else:
            messages.info(request, "Comment was greater than 200 characters, please try again.")
        return profile(request, username)


def delete_comment(request, comment_id):
    comment = Comment.objects.get(id=comment_id)

    if request.method == 'POST':
        comment.delete()

    return news_feed(request)


def delete_comment_profile(request, comment_id, username):
    comment = Comment.objects.get(id=comment_id)

    if request.method == 'POST':
        comment.delete()

    return profile(request, username)


def profile(request, username):
    user_profile = User.objects.get(username=username)
    saved_events = SavedEvent.objects.all().filter(author=user_profile)
    user_bio = ""  # instantiate empty string (if bio not found renders empty)
    follower_list = Followers.objects.all().filter(user=user_profile)
    check_follow_list = 'none'  # instantiate variable for logic in template

    # to retrieve bio from model
    if Bio.objects.filter(user=user_profile).exists():
        user_bio = Bio.objects.get(user=user_profile).bio_field

    # to fill follower list (profile does not exist if not authenticated so somewhat unnecessary)
    if request.user.is_authenticated:
        if Followers.objects.filter(user=user_profile, follower=request.user).exists():
            check_follow_list = 'true'
        else:
            check_follow_list = 'false'

    context = {
        'user_profile': user_profile,
        'saved_events': saved_events,
        'user_bio': user_bio,
        'follower_list': follower_list,
        'check_follow_list': check_follow_list
    }
    return render(request, 'profile.html', context)


def profile_search(request):
    if request.method == 'POST':
        username = request.POST['username']
        if not username:
            messages.info(request, 'Must enter a username')
            return redirect('newsfeed')
        elif User.objects.filter(username=username).exists():
            # use profile view to prevent redundancy
            return profile(request, username)
        else:
            messages.info(request, 'Username not found')
            return redirect('newsfeed')


def follow(request, username):
    user_to_follow = User.objects.get(username=username)

    if request.method == 'POST':
        Followers.objects.create(user=user_to_follow, follower=request.user)
    return redirect('profile', username)


def unfollow(request, username):
    user_being_unfollowed = User.objects.get(username=username)

    if request.method == 'POST' and request.user.is_authenticated:
        Followers.objects.filter(user=user_being_unfollowed, follower=request.user).delete()
    return redirect('profile', username)


def bio(request):
    if request.method == 'POST':
        bio_text = request.POST['bio_text']
        # if entry in bio model for user then update field
        if Bio.objects.filter(user=request.user).exists():
            user_bio = Bio.objects.get(user=request.user)
            user_bio.bio_field = bio_text
            user_bio.save()

        # otherwise create entry
        else:
            Bio.objects.create(user=request.user, bio_field=bio_text)
    return redirect('profile', request.user)
