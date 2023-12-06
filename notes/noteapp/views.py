from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .forms import TagForm, NoteForm
from .models import Tag, Note


# Create your views here.
def main(request):
    notes = Note.objects.filter(user=request.user).all() if request.user.is_authenticated else []
    return render(request, 'noteapp/index.html', {"notes": notes})


@login_required
def tag(request):
    do_post = True
    if request.method == 'POST':
        form = TagForm(request.POST, instance=Tag())
        if form.is_valid():
            tag = form.save(commit=False)
            tag.user = request.user
            tag.save()
            return redirect('noteapp:tag')
        else:
            return render(request, 'noteapp/tag.html', {'form': form, 'do_post': do_post})

    tags = Tag.objects.filter(user=request.user).all() if request.user.is_authenticated else []
    return render(request, 'noteapp/tag.html',
                  {'form': TagForm(), 'tags': tags, 'do_post': not do_post})


@login_required
def note(request):
    tags = Tag.objects.filter(user=request.user).all()

    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            new_note = form.save(commit=False)
            new_note.user = request.user
            new_note.save()

            choice_tags = Tag.objects.filter(name__in=request.POST.getlist('tags'), user=request.user)
            for tag in choice_tags.iterator():
                new_note.tags.add(tag)

            return redirect('noteapp:main')
        else:
            return render(request, 'noteapp/note.html', {"tags": tags, 'form': form})

    return render(request, 'noteapp/note.html', {"tags": tags, 'form': NoteForm()})


@login_required
def detail(request, note_id):
    note = get_object_or_404(Note, pk=note_id, user=request.user)
    return render(request, 'noteapp/detail.html', {"note": note})


@login_required
def edit_note(request, note_id):
    all_tags = Tag.objects.filter(user=request.user).all()
    note = get_object_or_404(Note, pk=note_id, user=request.user)
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            tags = request.POST.getlist('tags')
            note.tags.set(Tag.objects.filter(name__in=tags))
            return redirect('noteapp:main')
        else:
            return render(request, 'noteapp/note.html', {'tags': all_tags, 'form': form})

    form = NoteForm(instance=note)
    return render(request, 'noteapp/note.html', {'tags': all_tags, 'form': form})


@login_required
def set_done(request, note_id):
    Note.objects.filter(pk=note_id, user=request.user).update(done=True)
    return redirect('noteapp:main')


@login_required
def delete_note(request, note_id):
    Note.objects.get(pk=note_id, user=request.user).delete()
    return redirect('noteapp:main')


@login_required
def edit_tag(request, tag_id):
    do_post = True
    tag = get_object_or_404(Tag, pk=tag_id, user=request.user)
    if request.method == 'POST':
        form = TagForm(request.POST, instance=tag)
        if form.is_valid():
            tag = form.save(commit=False)
            tag.user = request.user
            tag.save()
            return redirect('noteapp:tag')
        else:
            return render(request, 'noteapp/tag.html', {'form': form, 'do_post': do_post})

    form = TagForm(instance=tag)
    tags = Tag.objects.filter(user=request.user).all() if request.user.is_authenticated else []
    return render(request, 'noteapp/tag.html', {'form': form, 'tags': tags, 'do_post': do_post})


@login_required
def delete_tag(request, tag_id):
    Tag.objects.get(pk=tag_id, user=request.user).delete()
    return redirect('noteapp:tag')
