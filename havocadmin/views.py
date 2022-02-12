from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from investor.models import Investor, InvestorContact
from entreprenuer.models import Entreprenuer, EntreprenuerContact, EntreprenuerIdeas
from django.shortcuts import render
from plotly.offline import plot
import plotly.graph_objs as go


def logout(request):
    return redirect('/home')


def homefunction(request):
    return render(request, "ahome.html")


def servicesfunction(request):
    return render(request, "aservices.html")


def teamfunction(request):
    return render(request, "ateam.html")


def aboutfunction(request):
    return render(request, "aabout.html")


def invdetfunction(request):
    invdet = Investor.objects.all()
    count = Investor.objects.all().count()
    return render(request, "ainvestor.html", {'invdet': invdet, 'count': count})


def invqrfunction(request):
    invqr = InvestorContact.objects.all()
    count = InvestorContact.objects.all().count()
    return render(request, "ainvqueries.html", {'invqr': invqr, 'count': count})


def enpdetfunction(request):
    enpdet = Entreprenuer.objects.all()
    count = Entreprenuer.objects.all().count()
    return render(request, "aentreprenuer.html", {'enpdet': enpdet, 'count': count})


def enpqrfunction(request):
    enpqr = EntreprenuerContact.objects.all()
    count = EntreprenuerContact.objects.all().count()
    return render(request, "aenpqueries.html", {'enpqr': enpqr, 'count': count})


def ereplyfunction(request, subject):
    return render(request, 'aereply.html', {'subject': subject})


def edeletefunction(request, subject):
    EntreprenuerContact.objects.filter(subject=subject).delete()
    return redirect('/havocadmin/enpqr')


def ireplyfunction(request, subject):
    return render(request, 'aireply.html', {'subject': subject})


def ideletefunction(request, subject):
    InvestorContact.objects.filter(subject=subject).delete()
    return redirect('/havocadmin/invqr')


def ereplymailfunction(request, subject):
    if request.method == 'POST':
        body = request.POST['body']
        mail = EntreprenuerContact.objects.values_list('email', flat=True).get(subject=subject)
        fname = EntreprenuerContact.objects.values_list('firstname', flat=True).get(subject=subject)
        EntreprenuerContact.objects.filter(subject=subject).delete()
        subject = 'Regarding your submitted issue to our Havoc'
        mess = 'Hello ' + fname + '\n' + body
        email = EmailMessage(subject, mess, to=[mail])
        email.send()
    return redirect('/havocadmin/enpqr')


def ireplymailfunction(request, subject):
    if request.method == 'POST':
        body = request.POST['body']
        mail = InvestorContact.objects.values_list('email', flat=True).get(subject=subject)
        fname = InvestorContact.objects.values_list('firstname', flat=True).get(subject=subject)
        InvestorContact.objects.filter(subject=subject).delete()
        subject = 'Regarding your submitted issue to our Havoc'
        mess = 'Hello ' + fname + '\n' + body
        email = EmailMessage(subject, mess, to=[mail])
        email.send()
    return redirect('/havocadmin/invqr')


def dashboard(request):
    e = Entreprenuer.objects.all().count()
    i = Investor.objects.all().count()
    eq = EntreprenuerContact.objects.all().count()
    iq = InvestorContact.objects.all().count()
    si = EntreprenuerIdeas.objects.all().count()
    m = ['Investors', 'Entreprenuers']
    trace = go.Figure(
        data=[
            go.Bar(
                name="Original",
                x=m,
                y=[i, e],
                offsetgroup=0,
            ),
        ],
        layout=go.Layout(
            title="Havoc Registrations",
            yaxis_title="No. Of Registrations",
            xaxis_title="Different Types of Users"
        )
    )
    trace2 = go.Figure(
        data=[
            go.Pie(
                name="Original",
                labels=m,
                values=[i, e],
                hole=.3,
            ),
        ],
        layout=go.Layout(
            title="Havoc Users",
        )
    )
    trace3 = go.Figure(
        data=[
            go.Scatter(
                name="Original",
                x=['Entreprenuers', 'StartUp Ideas'],
                y=[e, si]
            ),
        ],
        layout=go.Layout(
            title="Entreprenuers and their Submitted Ideas",
            yaxis_title="Count",
            xaxis_title="Entreprenuers and StartUps"
        )
    )
    trace4 = go.Figure(
        data=[
            go.Pie(
                name="Original",
                labels=['Entreprenuers', 'StartUp Ideas'],
                values=[e, si],
                hole=.3,
            ),
        ],
        layout=go.Layout(
            title="StartUp Submissions",
        )
    )
    trace5 = go.Figure(
        data=[
            go.Bar(
                name="Original",
                x=['Investor Queries','Entreprenuer Queries'],
                y=[iq, eq],
                offsetgroup=0,
            ),
        ],
        layout=go.Layout(
            title="Havoc Queries",
            yaxis_title="No. Of Queries",
            xaxis_title="Different Types of Users"
        )
    )
    trace6 = go.Figure(
        data=[
            go.Scatter(
                name="Original",
                x=['Entreprenuers Queries', 'Investor Queries'],
                y=[eq, iq]
            ),
        ],
        layout=go.Layout(
            title="Queries Report",
            yaxis_title="Queries",
            xaxis_title="Users"
        )
    )

    #trace.update_layout(paper_bgcolor='rgba(0,0,0,0.7)', font={'color': '#fff'})
    #trace2.update_layout(paper_bgcolor='rgba(0,0,0,0.7)', font={'color': '#fff'})
    #trace3.update_layout(paper_bgcolor='rgba(0,0,0,0.7)', font={'color': '#fff'})
    #trace4.update_layout(paper_bgcolor='rgba(0,0,0,0.7)', font={'color': '#fff'})
    plot_div = plot(trace, output_type='div')
    plot_pie = plot(trace2, output_type='div')
    plot_scatter = plot(trace3, output_type='div')
    plot_pie2 = plot(trace4, output_type='div')
    plot_hist = plot(trace5, output_type='div')
    plot_scatter2 = plot(trace6, output_type='div')
    return render(request, "agraph.html",
                  context={'plot_div': plot_div, 'plot_pie': plot_pie, 'plot_pie2': plot_pie2, 'plot_scatter': plot_scatter,
                           'plot_scatter2': plot_scatter2,'plot_hist': plot_hist, 'e': e, 'i': i, 'si': si, 'eq': eq, 'iq': iq})
