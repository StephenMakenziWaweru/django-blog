from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import (ListView, CreateView, UpdateView,
                                    DetailView, DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post
from django.contrib.auth.decorators import login_required
# pdf reports
# from django.http import FileResponse
# import io
# from reportlab.pdfgen import canvas
# from reportlab.lib.units import inch
# from reportlab.lib.pagesizes import letter
from django.template.loader import get_template
from xhtml2pdf import pisa


def about(request):
    return render(request, 'blog/about.html')

@login_required
def download(request):
    template = get_template('blog/download.html')
    response = HttpResponse(content_type='application/pdf')
    # response['Content-Disposition'] = 'attachment; filename="posts.pdf"'
    response['Content-Disposition'] = 'inline; filename="posts.pdf"'
    
    print(Post.objects.first().content, Post.objects.first().title)
    html = template.render({'post_list': Post.objects.all()})
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse(f'Error generating posts report <pre>{html}</pre>')
    return response
    # buf = io.BytesIO()
    # c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    # textob = c.beginText()
    # textob.setTextOrigin(inch, inch)
    # textob.setFont('Helvetica', 14)

    # posts = Post.objects.all()
    # lines = ['----------------------------------ALL POSTS----------------------------']
    # for post in posts:
    #     lines.append(f'author: [{str(post.author)}]     Date: [{post.date_posted}]')
    #     lines.append(f'title: [{post.title}]')
    #     lines.append('[POST]')
    #     lines.append(post.content)
    #     lines.append('---------------------------------------------------------------')
    #     lines.append('')
    # for line in lines:
    #     textob.textLine(line)

    # c.drawText(textob)
    # c.showPage()
    # c.save()
    # buf.seek(0)

    # return FileResponse(buf, as_attachment=True, filename='blogs.pdf')

class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'post_list'
    ordering = '-date_posted'
    paginate_by = 3

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'blog/update_post.html'
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        if self.request.user == self.get_object().author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/delete_post.html'
    success_url = '/'

    def test_func(self):
        if self.request.user == self.get_object().author:
            return True
        return False

class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'blog/detail.html'

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/new_post.html'
    fields = ['title', 'content']
    success_url = '/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
