import json

from celery.result import AsyncResult

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import generic
from django.views.generic.detail import SingleObjectMixin
from djsniper.sniper.forms import ConfirmForm, ProjectForm
from djsniper.sniper.models import NFTAttribute, NFTProject
from djsniper.sniper.tasks import fetch_nfts_task


class ProjectListView(generic.ListView):
    template_name = "sniper/project_list.html"

    def get_queryset(self):
        return NFTProject.objects.all()


class ProjectDetailView(generic.DetailView):
    template_name = "sniper/project_detail.html"

    def get_queryset(self):
        return NFTProject.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        nft_project = self.get_object()
        order = self.request.GET.get("order", None)
        nfts = nft_project.nfts.all()
        if order == "rank":
            nfts = nfts.order_by("rank")
        context.update({"nfts": nfts[0:12]})
        return context


class ProjectCreateView(generic.CreateView):
    template_name = "sniper/project_create.html"
    form_class = ProjectForm

    def form_valid(self, form):
        instance = form.save()
        return redirect("sniper:project-detail", pk=instance.id)

    def get_queryset(self):
        return NFTProject.objects.all()


class ProjectUpdateView(generic.UpdateView):
    template_name = "sniper/project_update.html"
    form_class = ProjectForm

    def get_queryset(self):
        return NFTProject.objects.all()

    def get_success_url(self):
        return reverse("sniper:project-detail", kwargs={"pk": self.get_object().id})


class ProjectDeleteView(generic.DeleteView):
    template_name = "sniper/project_delete.html"

    def get_queryset(self):
        return NFTProject.objects.all()

    def get_success_url(self):
        return reverse("sniper:project-list")


class ProjectClearView(SingleObjectMixin, generic.FormView):
    template_name = "sniper/project_clear.html"
    form_class = ConfirmForm

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_queryset(self):
        return NFTProject.objects.all()

    def form_valid(self, form):
        nft_project = self.get_object()
        nft_project.nfts.all().delete()
        NFTAttribute.objects.filter(project=nft_project).delete()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("sniper:project-detail", kwargs={"pk": self.kwargs["pk"]})


def nft_list(request):
    project = NFTProject.objects.get(name="BAYC")
    nfts = project.nfts.all().order_by("-rarity_score")[0:12]
    return render(request, "nfts.html", {"nfts": nfts})


class FetchNFTsView(generic.FormView):
    template_name = "sniper/fetch_nfts.html"
    form_class = ConfirmForm

    def form_valid(self, form):
        result = fetch_nfts_task.apply_async((self.kwargs["pk"],), countdown=1)
        return render(self.request, self.template_name, {"task_id": result.task_id})


def get_progress(request, task_id):
    result = AsyncResult(task_id)
    response_data = {
        "state": result.state,
        "details": result.info,
    }
    return HttpResponse(json.dumps(response_data), content_type="application/json")
