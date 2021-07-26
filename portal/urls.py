from django.urls import path
from portal.views import (CompanyProfileView, CompanyProfileAddView, 
                            CompanyProfileUpdateView, CompanyProfileDeleteView,
                            JobListView, JobAddView, JobDeleteView, JobDetailView,
                            ApplyAddView, ApplyListView, ApplyDeleteView, ContactView,
                            CompanyProfileDetailView, Joblistfilter
                        )


urlpatterns = [
    path('companyprofile/', CompanyProfileView.as_view(), name="companyprofiledetail"),
    path('companyadd/', CompanyProfileAddView.as_view(), name="companyprofileadd"),
    path('companyupdate/<int:id>/', CompanyProfileUpdateView.as_view(), name="companyprofileupdate"),
    path('companydelete/<int:id>/', CompanyProfileDeleteView.as_view(), name="companyprofiledelete"),
    path('companydetail/<int:id>/', CompanyProfileDetailView.as_view(), name="companyprofiledetaillist"),

    path('job/', JobListView.as_view(), name="job_list"),
    path('job/<int:id>', JobDetailView.as_view(), name="job_detail"),
    path('jobadd/', JobAddView.as_view(), name="job_add"),
    path('jobdelete/<int:id>/', JobDeleteView.as_view(), name="job_delete"),

    path('apply/<int:id>', ApplyAddView.as_view(), name="apply_add"),
    path('apply', ApplyListView.as_view(), name="apply_list"),
    path('applydelete/<int:id>', ApplyDeleteView.as_view(), name="apply_delete"),


    path('contact/<int:id>', ContactView, name='contact'),
    path('jobfilter', Joblistfilter, name='job_filter'),
]

# list1 = []
#         new1 = request.GET
#         for k,val1 in new1.items():
#             list1.append(val1)
#         print(list1)
#         # list2 = []


#         rannge1 = {}

#         for i in list1:
#             print(i)
#             list3 = []
#             v = i.split(',')
#             print("vaklue 2  ",v)
#             for j in v:
#                 list3.append(int(j))
#             print(list3)
#             rannge1['r1'] = list3