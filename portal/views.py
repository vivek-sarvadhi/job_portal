from django.shortcuts import render, get_object_or_404, redirect
from portal.forms import CompanyProfileForm, JobForm, ApplyForm, ContactForm
from portal.models import CompanyProfile, Job, Candidate
from django.views.generic import View, CreateView, ListView, DeleteView, UpdateView, DetailView
from django.urls import reverse, reverse_lazy
from django import http
from django.http import HttpResponse, JsonResponse
from django.core.mail import send_mail, BadHeaderError
from job_portal import settings
from django.db.models import Q
import json
# Create your views here.


class CompanyProfileView(ListView):
    model = CompanyProfile
    template_name = 'portal/comapny_profile_list.html'
    context_object_name = 'companyprofile'


class CompanyProfileDetailView(DetailView):
    template_name = "portal/company_profile_detail.html"

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(CompanyProfile, id=id_)


class CompanyProfileAddView(CreateView):
    template_name = 'portal/company_profile_add.html'
    form_class = CompanyProfileForm

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('companyprofiledetail')


class CompanyProfileUpdateView(UpdateView):
    template_name = 'portal/company_profile_add.html'
    form_class = CompanyProfileForm

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(CompanyProfile, id=id_)

    def form_valid(self, form):
        print(form)
        return super().form_valid(form)

    def form_invalid(self, form):
        print("form is invalid")
        print(form.errors)
        return http.HttpResponse("form is invalid.. this is just an HttpResponse object")

    def get_success_url(self):
        return reverse('companyprofiledetail')


class  CompanyProfileDeleteView(DeleteView):
    template_name = 'portal/company_profile_delete.html'

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(CompanyProfile, id=id_)

    def get_success_url(self):
        return reverse('companyprofiledetail')


class JobListView(ListView):
    model = Job
    # template_name = 'portal/job_list.html'
    context_object_name = 'jobs'
    paginate_by = 8
    queryset = Job.objects.all()


    def get_queryset(self):
        name = self.request.GET.get('q')
        one = self.request.GET.get('one')
        print(one)
        object_list = self.model.objects.all()
        if name:
            object_list = Job.objects.filter(Q(title__icontains=name) | Q(companyprofile_id__name__icontains=name) | Q(description__icontains=name))
        return object_list


class JobDetailView(DetailView):
    template_name = 'portal/job_detail.html'

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Job, id=id_)

class JobAddView(CreateView):
    template_name = 'portal/job_add.html'
    form_class = JobForm

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        print("form is invalid")
        print(form.errors)
        return http.HttpResponse("form is invalid.. this is just an HttpResponse object")

    def get_success_url(self):
        return reverse('job_list')


class JobDeleteView(DeleteView):
    template_name = 'portal/job_delete.html'

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Job, id=id_)

    def get_success_url(self):
        return reverse('job_list')


class ApplyAddView(CreateView):
    template_name = "portal/apply_add.html"
    form_class = ApplyForm

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        id_ = self.kwargs.get("id")
        instance.job = Job.objects.get(id=id_)
        instance.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        print("form is invalid")
        print(form.errors)
        return http.HttpResponse("form is invalid.. this is just an HttpResponse object")

    def get_success_url(self):
        return reverse('job_list')


class ApplyListView(ListView):
    model = Candidate
    template_name = 'portal/apply_list.html'
    context_object_name = 'candidates'

    paginate_by = 7
    queryset = Candidate.objects.all()



class ApplyDeleteView(DeleteView):
    template_name = "portal/apply_delete.html"

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Candidate, id=id_)

    def get_success_url(self):
        return reverse('apply_list')



def ContactView(request, id):
    email = Candidate.objects.get(id=id)
    print(email.user.email)
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = email.user.email
            message = form.cleaned_data['message']
            try:
                send_mail(subject, message, settings.EMAIL_HOST_USER, [from_email])
            except BadHeaderError:
                return HttpResponse("Invalid Header Found")
            return redirect("apply_list")
    return render(request, 'portal/email.html', {'form':form})


def Joblistfilter(request):
    if request.method == "GET" and request.is_ajax():
        
        list1 = []
        new1 = request.GET
        for k,val1 in new1.items():
            list1.append(val1)
        
        list3 = []
        dict1 = {}
        for i in list1:
            list2 = []
            print("iiiiiiii",i)
            val2 = i.split(',')
            for j in val2:
                val = int(j)
                list2.append(val)
            dict1[i] = list2

        empty_list = Job.objects.none()

        if '10000,20000' in dict1:
            job1 = Job.objects.filter(salary__range=dict1['10000,20000']).values('id','companyprofile_id','companyprofile_id__name','title','salary','experience','location')
            empty_list = empty_list | job1
            
        if '20001,35000' in dict1:
            job2 = Job.objects.filter(salary__range=dict1['20001,35000']).values('id','companyprofile_id','companyprofile_id__name','title','salary','experience','location')
            empty_list = empty_list | job2

        if '35001,100000' in dict1:
            job3 = Job.objects.filter(salary__range=dict1['35001,100000']).values('id','companyprofile_id__name','title','salary','experience','location')
            empty_list = empty_list | job3

        if '0,1' in dict1:
            job4 = Job.objects.filter(experience__range=dict1['0,1']).values('id','companyprofile_id__name','title','salary','experience','location')
            empty_list = empty_list | job4

        if '2,3' in dict1:
            job5 = Job.objects.filter(experience__range=dict1['2,3']).values('id','companyprofile_id__name','title','salary','experience','location')
            empty_list = empty_list | job5

        if '3,10' in dict1:
            job6 = Job.objects.filter(experience__range=dict1['3,10']).values('id','companyprofile_id__name','title','salary','experience','location')
            empty_list = empty_list | job6

        job_list =  empty_list.distinct()
        context = {
            'job_info': list(job_list)
        }
        print(context)
        return JsonResponse(context, status=200)
    return JsonResponse({"success":False}, status=400)
