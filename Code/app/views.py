from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from app.forms import MyLoginForm, MySignupForm, NewEcf, EditModule, PublicForm, EditProfile, extraUpload, requestUpload
from django.views.decorators.csrf import csrf_exempt
from app.models import UserProfile, EcfData, ModuleData, Files, PublicEcf
from django.contrib.auth.models import User
from allauth.account.decorators import verified_email_required, login_required
import os, random
from django.core.mail import send_mail
from django.template.loader import render_to_string

sendingemailaddress = 'ecfsheffield@gmail.com'

def user_permission_check(request):
    user = request.user
    userpower = UserProfile.objects.get(user_id = user.id)
    if userpower.userpower == 1:
        return "1"
    elif userpower.userpower == 2:
        return "2"
    elif userpower.userpower == 3:
        return "3"

def index(request):
    return HttpResponseRedirect ("/accounts/login")

def pagenotfound(request):
    return render(request, '404.html')

@login_required
def dashboard(request):
    usercheck = user_permission_check(request)
    if user_permission_check(request) == "2":
        return HttpResponseRedirect ("/secretarypanel/dashboard")
    elif user_permission_check(request) == "3":
        return HttpResponseRedirect ("/scrutinypanel/dashboard")
    elif user_permission_check(request) == "1":
        navbardash = True;
        if request.GET.get('success') == str(1):
            successform = 1
        elif request.GET.get('success') == str(0):
            successform = 2

        userid = request.user.id
        ecfdata_info = EcfData.objects.filter(user_id = userid)
        counterpending = 0
        counterapproved = 0
        counterrejected = 0
        counterpartial = 0
        for each in ecfdata_info:
            moduledata_info = ModuleData.objects.filter(ecfdata_id = each.id)
            totalmodules = 0
            pendingmod = 0
            approvedmod = 0
            rejectedmod = 0
            each.finalmod = -1
            for item in moduledata_info:
                totalmodules += 1
                if item.approved == 0:
                    pendingmod += 1
                elif item.approved == 1:
                    approvedmod += 1
                elif item.approved == 2:
                    rejectedmod += 1
            if totalmodules == pendingmod:
                each.finalmod = 0
                counterpending += 1
            elif totalmodules == approvedmod:
                each.finalmod = 1
                counterapproved += 1
            elif totalmodules == rejectedmod:
                each.finalmod = 2
                counterrejected += 1
            elif pendingmod >= 1:
                each.finalmod = 4
                counterpending += 1
            else:
                each.finalmod = 3
                counterpartial += 1
        return render(request, 'dashboard.html', locals())

@login_required
def unitcount(request):
    usercheck = user_permission_check(request)
    if user_permission_check(request) == "2":
        return HttpResponseRedirect ("/404")
    elif user_permission_check(request) == "3":
        return HttpResponseRedirect ("/404")
    elif user_permission_check(request) == "1":
        navbarnew = True;
        if request.GET.get('nounits') == str(1):
            nounits = 1
        return render(request, 'unitcount.html', locals())

@login_required
def newform(request):
    usercheck = user_permission_check(request)
    if user_permission_check(request) == "2":
        return HttpResponseRedirect ("/404")
    elif user_permission_check(request) == "3":
        return HttpResponseRedirect ("/404")
    elif user_permission_check(request) == "1":
        navbarnew = True;
        units = request.GET.get('units')
        unitsx = request.GET.get('units', 0)
        x = int(unitsx)

        if (x <= 0) or (x == None) or (x > 10):
            return HttpResponseRedirect ("/units?nounits=1")
        else:
            if units:
                units = range(1, int(units)+1)

            if request.method == "POST":
                unitsx = request.GET.get('units', 0)
                x = int(unitsx)
                form = NewEcf(request.POST, request.FILES, units_no = x)
                user = request.user
                if form.is_valid():
                    ukvisa= form.cleaned_data['ukvisa']
                    coursename = form.cleaned_data['coursename']
                    studyyear = form.cleaned_data['studyyear']
                    numberofunits = form.cleaned_data['numberofunits']
                    durationenddate = form.cleaned_data['durationenddate']
                    durationstartdate = form.cleaned_data['durationstartdate']
                    circumstance = form.cleaned_data['circumstance']
                    detailecf = form.cleaned_data['detailecf']

                    ecfdata = EcfData(user=user, ukvisa=ukvisa,coursename = coursename,studyyear =studyyear, numberofunits = numberofunits,durationenddate = durationenddate, durationstartdate = durationstartdate, circumstance =circumstance,detailecf = detailecf)
                    ecfdata.save()

                    foreignid = EcfData.objects.get(id=ecfdata.id)
                    filestore = Files(document=request.FILES['fileinput'], ecfdata=foreignid)
                    filestore.pk = None
                    filestore.save()


                    listunitcode = []
                    listtype = []
                    liststartdate = []
                    listenddate = []
                    listaction = []
                    for item in range(1, ecfdata.numberofunits+1):
                        listunitcode.append("unitcode" + str(item))
                        listtype.append("type" + str(item))
                        liststartdate.append("startdate" + str(item))
                        listenddate.append("enddate" + str(item))
                        listaction.append("action" + str(item))

                    for i in range(0, ecfdata.numberofunits):

                        foreignid = EcfData.objects.get(id=ecfdata.id)
                        unitcode = form.cleaned_data[listunitcode[i]]
                        type = form.cleaned_data[listtype[i]]
                        startdate = form.cleaned_data[liststartdate[i]]
                        enddate = form.cleaned_data[listenddate[i]]
                        action = form.cleaned_data[listaction[i]]

                        moduledata = ModuleData(
                            unitcode = unitcode,
                            type = type,
                            startdate = startdate,
                            enddate = enddate,
                            action = action,
                            ecfdata = foreignid,
                        )

                        moduledata.pk = None
                        moduledata.save()
                        context = {}
                        send_mail(
                            'Submmited New Form #'+str(ecfdata.id),
                            render_to_string('emails/newform.txt', context),
                            sendingemailaddress,
                            [user.email],
                            fail_silently=True,
                        )
                        studentpubdata = User.objects.all()
                        studcheck = studentpubdata.select_related('profile')
                        for item in studcheck:
                            if item.profile.userpower == 2:
                                send_mail(
                                    'New form #'+str(ecfdata.id)+' submitted',
                                    render_to_string('emails/secretary/newform.txt', context),
                                    sendingemailaddress,
                                    [item.email],
                                    fail_silently=True,
                                )

                    return HttpResponseRedirect("/dashboard?success=1")
                else:
                    return HttpResponseRedirect("/dashboard?success=0")

            else:
                form = NewEcf(units_no = x)


        return render(request, 'newform.html', locals())

@login_required
def viewform(request):
    usercheck = user_permission_check(request)
    if user_permission_check(request) == "2":
        return HttpResponseRedirect ("/404")
    elif user_permission_check(request) == "3":
        return HttpResponseRedirect ("/404")
    elif user_permission_check(request) == "1":
        navbardash = True;
        if not request.GET.get("id"):
            return HttpResponseRedirect("/dashboard")
        else:
            if request.GET.get('successfulupload') == str(1):
                successform = 1
            elif request.GET.get('successfulupload') == str(0):
                successform = 2
            user = request.user
            formid_get = request.GET.get("id")
            ecfdata_info = EcfData.objects.get(id = formid_get)
            if ecfdata_info.user_id == user.id:
                userdata = User.objects.get(id=ecfdata_info.user_id)
                moduledata_info = ModuleData.objects.filter(ecfdata_id = formid_get)

                # Code for viewing and downloading the uploaded files
                fileupload_data = Files.objects.filter(ecfdata_id = formid_get)
                totalmodules = 0
                pendingmod = 0
                approvedmod = 0
                rejectedmod = 0
                finalmod = -1
                for item in moduledata_info:
                    totalmodules += 1
                    if item.approved == 0:
                        pendingmod += 1
                    elif item.approved == 1:
                        approvedmod += 1
                    elif item.approved == 2:
                        rejectedmod += 1
                if totalmodules == pendingmod:
                    finalmod = 0
                elif totalmodules == approvedmod:
                    finalmod = 1
                elif totalmodules == rejectedmod:
                    finalmod = 2
                elif pendingmod >= 1:
                    finalmod = 4
                else:
                    finalmod = 3

                # If new files are requested by the secretary
                if request.method == "POST":
                    foreignid = request.GET.get('id')
                    ecfdataid = EcfData.objects.get(id=foreignid)
                    form = extraUpload(request.POST, request.FILES)
                    if form.is_valid():
                        filestore = Files(document=request.FILES['fileinput'], ecfdata_id=ecfdataid.id)
                        filestore.pk = None
                        filestore.save()
                        ecfdataid.moreproof = False;
                        ecfdataid.save()
                        context = {}
                        allusers = User.objects.all()
                        secretaryCheck = allusers.select_related('profile')
                        for item in secretaryCheck:
                            if item.profile.userpower == 2:
                                send_mail(
                                    'More proof uploaded for form #'+str(ecfdataid.id),
                                    render_to_string('emails/secretary/moreproofuploaded.txt', context),
                                    sendingemailaddress,
                                    [item.email],
                                    fail_silently=True,
                                )
                        return HttpResponseRedirect("/viewform?id="+foreignid+"&successfulupload=1")
                    else:
                        return HttpResponseRedirect("/viewform?id="+foreignid+"&successfulupload=0")
                else:
                    form = extraUpload()

                return render(request, 'viewform.html', locals())
            else:
                return HttpResponseRedirect("/404")


@login_required
def userprofile(request):
    usercheck = user_permission_check(request)
    navbaruserp = True;
    if request.GET.get('success') == str(1):
        successform = 1
    elif request.GET.get('success') == str(0):
        successform = 2
    user = request.user
    userprofiledata = UserProfile.objects.get(user_id = request.user.id)
    if request.method == "POST":
        form = EditProfile(request.POST)
        if form.is_valid():
            # email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            dob = form.cleaned_data['dob']

            userprofiledata.dob = dob
            userprofiledata.save()

            userdata = User.objects.get(id=user.id)
            userdata.first_name = first_name
            userdata.last_name = last_name
            # userdata.email = email
            userdata.save()
            context = {}
            send_mail(
                'Updated Profile Details',
                render_to_string('emails/updatedprofile.txt', context),
                sendingemailaddress,
                [user.email],
                fail_silently=True,
            )
            return HttpResponseRedirect("/userprofile?success=1")
        else:
            return HttpResponseRedirect("/userprofile?success=0")
    else:
        form = EditProfile()
    if PublicEcf.objects.filter(user_id=user).count() >= 1:
        userpubdata = PublicEcf.objects.get(user_id=user)
    else:
        pass
    return render(request, 'userprofile.html', locals())

@login_required
def secretarydashboard(request):
    usercheck = user_permission_check(request)
    if user_permission_check(request) == "1":
        return HttpResponseRedirect ("/dashboard")
    elif user_permission_check(request) == "3":
        return HttpResponseRedirect ("/scrutinypanel/dashboard")
    elif user_permission_check(request) == "2":
        navbarsecretary = True;
        # Code which displays statistics and all forms available
        allforms_data = EcfData.objects.all()
        counterpending = 0
        counterapproved = 0
        counterrejected = 0
        counterpartial = 0
        for each in allforms_data:
            userdata = User.objects.get(id = each.user_id)
            # print(userdata.id/)
            each.fullname = userdata.first_name + " " + userdata.last_name
            each.email = userdata.email
            moduledata_info = ModuleData.objects.filter(ecfdata_id = each.id)
            moduledata_info_count = ModuleData.objects.filter(ecfdata_id = each.id).count()
            totalmodules = 0
            pendingmod = 0
            approvedmod = 0
            rejectedmod = 0
            each.finalmod = -1
            for item in moduledata_info:
                totalmodules += 1
                if item.approved == 0:
                    pendingmod += 1
                elif item.approved == 1:
                    approvedmod += 1
                elif item.approved == 2:
                    rejectedmod += 1
            if totalmodules == pendingmod:
                each.finalmod = 0
                counterpending += 1
            elif totalmodules == approvedmod:
                each.finalmod = 1
                counterapproved += 1
            elif totalmodules == rejectedmod:
                each.finalmod = 2
                counterrejected += 1
            elif pendingmod >= 1:
                each.finalmod = 4
                counterpending += 1
            else:
                each.finalmod = 3
                counterpartial += 1

        # Code for public ecf data
        studentpubdata = User.objects.all()
        studcheck = studentpubdata.select_related('profile')
        return render(request, 'secretary/dashboard.html', locals())

@login_required
def secretaryviewform(request):
    usercheck = user_permission_check(request)
    if user_permission_check(request) == "1":
        return HttpResponseRedirect ("/404")
    elif user_permission_check(request) == "3":
        return HttpResponseRedirect ("/404")
    elif user_permission_check(request) == "2":
        navbarsecretary = True;
        if not request.GET.get("id"):
            return HttpResponseRedirect("/secretarypanel/dashboard")
        else:
            if request.GET.get('requestedfiles') == str(1) or request.GET.get('updatesuccess') == str(1):
                success = 1
            elif request.GET.get('requestedfiles') == str(0) or request.GET.get('updatesuccess') == str(0):
                success = 2

            formid_get = request.GET.get("id")
            ecfdata_info = EcfData.objects.get(id = formid_get)
            userdata = User.objects.get(id=ecfdata_info.user_id)
            moduledata_info = ModuleData.objects.filter(ecfdata_id = formid_get)

            # Code for viewing and downloading the uploaded files
            fileupload_data = Files.objects.filter(ecfdata_id = formid_get)

            # Code for getting current public data from DATABASE
            if PublicEcf.objects.filter(user_id=ecfdata_info.user).count() >= 1:
                publicecf_data = PublicEcf.objects.get(user_id=ecfdata_info.user)
            else:
                pass

            totalmodules = 0
            pendingmod = 0
            approvedmod = 0
            rejectedmod = 0
            finalmod = -1
            for item in moduledata_info:
                totalmodules += 1
                if item.approved == 0:
                    pendingmod += 1
                elif item.approved == 1:
                    approvedmod += 1
                elif item.approved == 2:
                    rejectedmod += 1
            if totalmodules == pendingmod:
                finalmod = 0
            elif totalmodules == approvedmod:
                finalmod = 1
            elif totalmodules == rejectedmod:
                finalmod = 2
            elif pendingmod >= 1:
                finalmod = 4
            else:
                finalmod = 3

            if request.GET.get("requestmore"):
                getval = request.GET.get("requestmore")
                ecfdataval = request.GET.get("id")
                ecfdata = EcfData.objects.get(id=ecfdataval)
                if getval == "1":
                    ecfdata.moreproof = True
                    context = {}
                    send_mail(
                        'Form #'+str(ecfdata.id)+' - More proof required',
                        render_to_string('emails/moreproof.txt', context),
                        sendingemailaddress,
                        [userdata.email],
                        fail_silently=True,
                    )
                else:
                    ecfdata.moreproof = False
                ecfdata.save()
                return HttpResponseRedirect("/secretarypanel/viewform?id=" + str(ecfdata_info.id)+"&requestedfiles=1")

            # Public Data Form on the View Form page under Secretary
            if 'pubdata' in request.POST:
                form = PublicForm(request.POST)
                if form.is_valid():
                    publicecf = form.cleaned_data['publicecf']

                    if PublicEcf.objects.filter(user_id = ecfdata_info.user).count() >= 1:
                        publicecf_data = PublicEcf.objects.get(user_id=ecfdata_info.user)
                        publicecf_data.publicecf = publicecf
                        publicecf_data.save()
                    else:
                        publicdata = PublicEcf(user=ecfdata_info.user, publicecf = publicecf)
                        publicdata.save()
                    return HttpResponseRedirect("/secretarypanel/viewform?id=" + str(ecfdata_info.id)+"&updatesuccess=1")
                else:
                    return HttpResponseRedirect("/secretarypanel/viewform?id=" + str(ecfdata_info.id)+"&updatesuccess=0")
            # else:
            #     form = PublicForm()

            elif 'moddata' in request.POST:
                form = EditModule(request.POST)
                user = request.user
                if form.is_valid():
                    id= form.cleaned_data['modid']
                    getData = ModuleData.objects.get(id=id)
                    action= form.cleaned_data['action']
                    approved = form.cleaned_data['approved']

                    getData.action = action
                    getData.approved = approved
                    getData.save()
                    context = {}
                    send_mail(
                        'Form #' + str(ecfdata_info.id) + ' has a new update',
                        render_to_string('emails/moduleupdate.txt', context),
                        sendingemailaddress,
                        [userdata.email],
                        fail_silently=True,
                    )
                    return HttpResponseRedirect("/secretarypanel/viewform?id=" + str(getData.ecfdata_id)+"&updatesuccess=1")
                else:
                    return HttpResponseRedirect("/secretarypanel/viewform?id=" + str(formid_get)+"&updatesuccess=0")
            else:
                form = PublicForm()
                formone= EditModule()
        return render(request, 'secretary/viewform.html', locals())

@login_required
def secretarypublicdata(request):
    usercheck = user_permission_check(request)
    if user_permission_check(request) == "1":
        return HttpResponseRedirect ("/dashboard")
    elif user_permission_check(request) == "3":
        return HttpResponseRedirect ("/scrutinypanel/dashboard")
    elif user_permission_check(request) == "2":
        navbarsecretary = True;
        if not request.GET.get("user"):
            return HttpResponseRedirect("/secretarypanel/dashboard")
        else:
            if request.GET.get('success') == str(1):
                successform = 1
            elif request.GET.get('success') == str(0):
                successform = 2
            userid_get = request.GET.get("user")
            userdata = User.objects.get(id=userid_get)
            userprofile = UserProfile.objects.get(user_id=userdata.id)
            if PublicEcf.objects.filter(user_id=userid_get).count() >= 1:
                publicecf_data = PublicEcf.objects.get(user_id=userid_get)
            else:
                pass

            if 'regenlink' in request.POST:
                userprofile = UserProfile.objects.get(user_id=userdata.id)
                chars= 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'
                randomstr= ''.join((random.choice(chars)) for x in range(8))
                userprofile.userlink = randomstr
                userprofile.save()
                return HttpResponseRedirect("/secretarypanel/publicdata?user=" + str(userid_get)+"&success=1")
            elif 'savepubdata' in request.POST:
                form = PublicForm(request.POST)
                if form.is_valid():
                    publicecf = form.cleaned_data['publicecf']

                    if PublicEcf.objects.filter(user_id = userid_get).count() >= 1:
                        publicecf_data = PublicEcf.objects.get(user_id=userid_get)
                        publicecf_data.publicecf = publicecf
                        publicecf_data.save()
                    else:
                        user = User.objects.get(id=userid_get)
                        publicdata = PublicEcf(user=user, publicecf = publicecf)
                        publicdata.save()
                    return HttpResponseRedirect("/secretarypanel/publicdata?user=" + str(userid_get)+"&success=1")
                else:
                    return HttpResponseRedirect("/secretarypanel/dashboard&success=0")
            else:
                form = PublicForm()
        return render(request, 'secretary/publicdata.html', locals())


def studentrecord(request):
    if request.GET.get('nouser') == str(1):
        nouser = 1
    elif request.GET.get('nodata') == str(1):
        nodata = 1
    elif request.GET.get('profile'):
        getlink = request.GET.get('profile')
        if (UserProfile.objects.filter(userlink=getlink)):
            getuserid = UserProfile.objects.get(userlink=getlink)
            userdata = User.objects.get(id=getuserid.user_id)
            if (PublicEcf.objects.filter(user_id=getuserid.user_id)):
                publicecf = PublicEcf.objects.get(user_id=getuserid.user_id)
            else:
                return HttpResponseRedirect("/studentrecord?profile=" + getlink +"&nodata=1")
        else:
            return HttpResponseRedirect("/studentrecord?profile=" + getlink +"&nouser=1")
    else:
        return HttpResponseRedirect("/studentrecord?nouser=1")
    return render(request, 'studentrecord.html', locals())

@login_required
def scrutinydashboard(request):
    usercheck = user_permission_check(request)
    if user_permission_check(request) == "1":
        return HttpResponseRedirect ("/dashboard")
    elif user_permission_check(request) == "2":
        return HttpResponseRedirect ("/secretarypanel/dashboard")
    elif user_permission_check(request) == "3":
        navbarscrutiny = True;
        counterpending = 0
        counterapproved = 0
        counterrejected = 0
        counterpartial = 0
        allforms_data = EcfData.objects.all()
        for each in allforms_data:
            userdata = User.objects.get(id = each.user_id)
            # print(userdata.id/)
            each.fullname = userdata.first_name + " " + userdata.last_name
            moduledata_info = ModuleData.objects.filter(ecfdata_id = each.id)
            moduledata_info_count = ModuleData.objects.filter(ecfdata_id = each.id).count()
            totalmodules = 0
            pendingmod = 0
            approvedmod = 0
            rejectedmod = 0
            each.finalmod = -1
            for item in moduledata_info:
                totalmodules += 1
                if item.approved == 0:
                    pendingmod += 1
                elif item.approved == 1:
                    approvedmod += 1
                elif item.approved == 2:
                    rejectedmod += 1
            if totalmodules == pendingmod:
                each.finalmod = 0
                counterpending += 1
            elif totalmodules == approvedmod:
                each.finalmod = 1
                counterapproved += 1
            elif totalmodules == rejectedmod:
                each.finalmod = 2
                counterrejected += 1
            elif pendingmod >= 1:
                each.finalmod = 4
                counterpending += 1
            else:
                each.finalmod = 3
                counterpartial += 1

        # Code for public ecf data
        userdata = User.objects.all()

        return render(request, 'scrutiny/dashboard.html', locals())


@login_required
def scrutinyviewform(request):
    usercheck = user_permission_check(request)
    if user_permission_check(request) == "1":
        return HttpResponseRedirect ("/404")
    elif user_permission_check(request) == "2":
        return HttpResponseRedirect ("/404")
    elif user_permission_check(request) == "3":
        navbarscrutiny = True;
        if not request.GET.get("id"):
            return HttpResponseRedirect("/scrutiny/dashboard")
        else:
            formid_get = request.GET.get("id")
            ecfdata_info = EcfData.objects.get(id = formid_get)
            userdata = User.objects.get(id=ecfdata_info.user_id)
            moduledata_info = ModuleData.objects.filter(ecfdata_id = formid_get)

            # Code for viewing and downloading the uploaded files
            fileupload_data = Files.objects.filter(ecfdata_id = formid_get)

            # Code for public information about the student
            publicecf = PublicEcf.objects.get(user_id=userdata.id)

            totalmodules = 0
            pendingmod = 0
            approvedmod = 0
            rejectedmod = 0
            finalmod = -1
            for item in moduledata_info:
                totalmodules += 1
                if item.approved == 0:
                    pendingmod += 1
                elif item.approved == 1:
                    approvedmod += 1
                elif item.approved == 2:
                    rejectedmod += 1
            if totalmodules == pendingmod:
                finalmod = 0
            elif totalmodules == approvedmod:
                finalmod = 1
            elif totalmodules == rejectedmod:
                finalmod = 2
            elif pendingmod >= 1:
                finalmod = 4
            else:
                finalmod = 3

        return render(request, 'scrutiny/viewform.html', locals())
