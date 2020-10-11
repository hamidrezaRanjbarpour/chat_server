from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from .forms import IndexForm


# Create your views here.
def index(request):
    if request.method == 'POST':
        form = IndexForm(request.POST or None)

        if form.is_valid():
            room_name = form.cleaned_data['room_name']
            return HttpResponseRedirect(reverse('messenger:room', args=(room_name,)))

    else:
        form = IndexForm()

    return render(request, 'messenger/index.html', {'form': form})


def room(request, room_name):
    return render(request, 'messenger/room.html', {
        'room_name': room_name
    })
