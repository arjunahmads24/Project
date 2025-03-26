import math

from django.db.models import F, Q
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage, send_mail
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text

from heypo import settings
from heypo.urls import handler404

from .models import Article

from emails.models import Email
from emails.forms import EmailForm
from emails.tokens import generate_token


def error_404_page(request, exception):
    list = {}

    # Articles_section --------------------------->
    recent_articles = Article.objects.order_by('-datetime_added', '-views')
    popular_articles = Article.objects.order_by('-views', '-datetime_added')
    list['recent_articles'] = recent_articles
    list['popular_articles'] = popular_articles
    # Articles_section --------------------------->

    # Email Section ---------------------->
    email_form = EmailForm(request.POST or None)
    if email_form.is_valid():
        object = email_form.save()
        object.save()
        messages.success(request, "Thank you for subscribing. Check your email for the confirmation message.")

        current_site = get_current_site(request)
        subject = "Confirm Your Email for subscribing Heypo Newsletter."
        message = render_to_string("activation/messages/email_activation_message.html", {
            'email': email_form.data['email'],
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(object.pk)),
            'token': generate_token.make_token(object),
        })
        email = EmailMessage(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [object.email],
        )
        email.fail_silently = True
        email.send()
    list['email_form'] = email_form
    # Email Section ---------------------->

    return render(request, "error_404_page.html", context=list)

def front_page(request):
    list = {}

    # Articles_section --------------------------->
    editors_pick_articles = Article.objects.filter(editors_pick=True).order_by('-datetime_added', '-views')
    technology_articles = Article.objects.filter(category__icontains="technology").order_by('-datetime_added', '-views')
    world_articles = Article.objects.filter(category__icontains="world").order_by('-datetime_added', '-views')
    economy_articles = Article.objects.filter(category__icontains="economy").order_by('-datetime_added', '-views')
    sports_articles = Article.objects.filter(category__icontains="sports").order_by('-datetime_added', '-views')
    recent_articles = Article.objects.all().order_by('-datetime_added', '-views')
    popular_articles = Article.objects.all().order_by('-views', '-date_added')

    list['editors_pick_articles'] = editors_pick_articles
    list['technology_articles'] = technology_articles
    list['world_articles'] = world_articles
    list['economy_articles'] = economy_articles
    list['sports_articles'] = sports_articles
    list['recent_articles'] = recent_articles
    list['popular_articles'] = popular_articles
    list['article_count'] = Article.objects.all().count()
    # Articles Section  --------------------------->

    # Email Section ---------------------->
    email_form = EmailForm(request.POST or None)
    if email_form.is_valid():
        object = email_form.save()
        object.save()
        messages.success(request, "Thank you for subscribing. Check your email for the confirmation message.")

        current_site = get_current_site(request)
        subject = "Confirm Your Email for subscribing Heypo Newsletter."
        message = render_to_string("activation/messages/email_activation_message.html", {
            'email': email_form.data['email'],
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(object.pk)),
            'token': generate_token.make_token(object),
        })
        email = EmailMessage(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [object.email],
        )
        email.fail_silently = True
        email.send()
    list['email_form'] = email_form
    # Email Section ---------------------->

    # Meta Section
    current_site = get_current_site(request)
    list["meta_description"] = "Baca artikel terbaru di Heypo untuk mendapatkan wawasan mendalam seputar teknologi, ekonomi, sains, olahraga, dan berbagai topik menarik lainnya."
    list["meta_og_url"] = current_site
    list["meta_og_title"] = "Heypo - Portal Informasi dan Pengetahuan"
    list["meta_og_description"] = "Jelajahi artikel informatif dan analisis mendalam mengenai teknologi, sains, ekonomi, olahraga, serta berbagai bidang lainnya."
    list["meta_og_image"] = "https://" + str(current_site) + "/static/icons/heypotextlogo.png"
    return render(request, "front_page.html", context=list)

def search_page(request, page):
    list = {}

    # Articles_section --------------------------->
    if request.method == "GET":
        search = request.GET.get("q")
    else:
        search = request.POST["search_path"][3:].replace("+", " ")
    try:
        keyword_search = search.split(" ")
        try:
            search_articles = Article.objects.all()
            for i in range(len(keyword_search)):
                search_articles = search_articles.filter(keyword__icontains=keyword_search[i]).order_by('-views', '-date_added')
        except:
            search_articles = None
    except:
        return redirect('/')

    recent_articles = Article.objects.order_by('-date_added', '-views')
    popular_articles = Article.objects.order_by('-views', '-date_added')
    page_count = int(math.ceil(search_articles.count() / 8))
    if page_count == 0 and page > 1:
        raise Http404
    elif page_count > 0 and page > page_count:
        raise Http404
    ab_slice = f"{(page - 1) * 8}:{page * 8}"

    list['search'] = search
    list['search_path'] = f"?q={search.replace(' ', '+')}"
    list['search_articles'] = search_articles
    list['q_search'] = search.replace(" ", "+")
    list['recent_articles'] = recent_articles
    list['popular_articles'] = popular_articles
    list['page'] = page
    list['page_count'] = page_count
    list['ab_slice'] = ab_slice
    # Articles_section --------------------------->

    # Email Section ---------------------->
    email_form = EmailForm(request.POST or None)
    if email_form.is_valid():
        object = email_form.save()
        object.save()
        messages.success(request, "Thank you for subscribing. Check your email for the confirmation message.")

        current_site = get_current_site(request)
        subject = "Confirm Your Email for subscribing Heypo Newsletter."
        message = render_to_string("activation/messages/email_activation_message.html", {
            'email': email_form.data['email'],
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(object.pk)),
            'token': generate_token.make_token(object),
        })
        email = EmailMessage(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [object.email],
        )
        email.fail_silently = True
        email.send()
    list['email_form'] = email_form
    # Email Section ---------------------->

    return render(request, "search_page.html", context=list)

def ew_page(request, ew, page):
    list = {}

    # Articles_section --------------------------->
    if ew == "ep":
        ew_articles = Article.objects.filter(editors_pick=True).order_by('-date_added', '-views')
        recent_articles = Article.objects.filter(editors_pick=True).order_by('-datetime_added', '-views')
        popular_articles = Article.objects.filter(editors_pick=True).order_by('-views', '-datetime_added')
        list['ew'] = "Editor's Pick"
        list['ew_url'] = "ep"
    elif ew == "wn":
        ew_articles = Article.objects.order_by('-datetime_added', '-views')
        recent_articles = None
        popular_articles = Article.objects.order_by('-views', '-datetime_added')
        list['ew'] = "Recent Articles"
        list['ew_url'] = "wn"
    else:
        raise Http404

    page_count = int(math.ceil(ew_articles.count() / 8))
    if page > page_count:
        raise Http404
    ab_slice = f"{(page - 1) * 8}:{page * 8}"

    list['ew_articles'] = ew_articles
    list['recent_articles'] = recent_articles
    list['popular_articles'] = popular_articles
    list['page'] = page
    list['page_count'] = page_count
    list['ab_slice'] = ab_slice
    # Articles_section --------------------------->

    # Email Section ---------------------->
    email_form = EmailForm(request.POST or None)
    if email_form.is_valid():
        object = email_form.save()
        object.save()
        messages.success(request, "Thank you for subscribing. Check your email for the confirmation message.")

        current_site = get_current_site(request)
        subject = "Confirm Your Email for subscribing Heypo Newsletter."
        message = render_to_string("activation/messages/email_activation_message.html", {
            'email': email_form.data['email'],
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(object.pk)),
            'token': generate_token.make_token(object),
        })
        email = EmailMessage(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [object.email],
        )
        email.fail_silently = True
        email.send()
    list['email_form'] = email_form
    # Email Section ---------------------->

    return render(request, "ew_page.html", context=list)

def category_page(request, category, page):
    list = {}

    # Articles_section --------------------------->
    category_articles = Article.objects.filter(category__icontains=category).order_by('-date_added', '-views')
    if not category_articles:
        raise Http404
    recent_articles = Article.objects.filter(category__icontains=category).order_by('-datetime_added', '-views')
    popular_articles = Article.objects.filter(category__icontains=category).order_by('-views', '-datetime_added')

    page_count = int(math.ceil(category_articles.count() / 8))
    if page > page_count:
        raise Http404
    ab_slice = f"{(page - 1) * 8}:{page * 8}"

    list['category_articles'] = category_articles
    list['recent_articles'] = recent_articles
    list['popular_articles'] = popular_articles
    list['page'] = page
    list['page_count'] = page_count
    list['ab_slice'] = ab_slice
    # Articles_section --------------------------->

    # Email Section ---------------------->
    email_form = EmailForm(request.POST or None)
    if email_form.is_valid():
        object = email_form.save()
        object.save()
        messages.success(request, "Thank you for subscribing. Check your email for the confirmation message.")

        current_site = get_current_site(request)
        subject = "Confirm Your Email for subscribing Heypo Newsletter."
        message = render_to_string("activation/messages/email_activation_message.html", {
            'email': email_form.data['email'],
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(object.pk)),
            'token': generate_token.make_token(object),
        })
        email = EmailMessage(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [object.email],
        )
        email.fail_silently = True
        email.send()
    list['email_form'] = email_form
    # Email Section ---------------------->

    list['category'] = category.replace(category[0], category[0].upper(), 1)
    return render(request, "category_page.html", context=list)

def topic_page(request, topic, page):
    list = {}

    # Articles_section --------------------------->
    topic_articles = Article.objects.filter(topic__icontains=topic).order_by('-date_added', '-views')
    if not topic_articles:
        raise Http404
    recent_articles = Article.objects.filter(topic__icontains=topic).order_by('-datetime_added', '-views')
    popular_articles = Article.objects.filter(topic__icontains=topic).order_by('-views', '-datetime_added')

    page_count = int(math.ceil(topic_articles.count() / 8))
    if page > page_count:
        raise Http404
    ab_slice = f"{(page - 1) * 8}:{page * 8}"

    list['topic_articles'] = topic_articles
    list['recent_articles'] = recent_articles
    list['popular_articles'] = popular_articles
    list['page'] = page
    list['page_count'] = page_count
    list['ab_slice'] = ab_slice
    # Articles_section --------------------------->

    # Email Section ---------------------->
    email_form = EmailForm(request.POST or None)
    if email_form.is_valid():
        object = email_form.save()
        object.save()
        messages.success(request, "Thank you for subscribing. Check your email for the confirmation message.")

        current_site = get_current_site(request)
        subject = "Confirm Your Email for subscribing Heypo Newsletter."
        message = render_to_string("activation/messages/email_activation_message.html", {
            'email': email_form.data['email'],
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(object.pk)),
            'token': generate_token.make_token(object),
        })
        email = EmailMessage(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [object.email],
        )
        email.fail_silently = True
        email.send()
    list['email_form'] = email_form
    # Email Section ---------------------->

    list['topic'] = topic.replace(topic[0], topic[0].upper(), 1)
    return render(request, "topic_page.html", context=list)

def article_page(request, slug):
    list = {}

    # Articles_section --------------------------->
    article = get_object_or_404(Article, slug=slug)
    if request.method == "GET":
        Article.objects.filter(slug=slug).update(views=F('views') + 1) # menggunakan '.filter' karena '.get' tidak memiliki atribut '.update'.
    list['article'] = article
    list['article_title_url_text'] = article.title.replace(" ", "%20")
    # Articles_section --------------------------->

    # Email Section ---------------------->
    email_form = EmailForm(request.POST or None)
    if email_form.is_valid():
        object = email_form.save()
        object.save()
        messages.success(request, "Thank you for subscribing. Check your email for the confirmation message.")

        current_site = get_current_site(request)
        subject = "Confirm Your Email for subscribing Heypo Newsletter."
        message = render_to_string("activation/messages/email_activation_message.html", {
            'email': email_form.data['email'],
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(object.pk)),
            'token': generate_token.make_token(object),
        })
        email = EmailMessage(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [object.email],
        )
        email.fail_silently = True
        email.send()
    list['email_form'] = email_form
    # Email Section ---------------------->

    current_site = get_current_site(request)
    list['current_site'] = current_site

    # Meta Section
    list["meta_description"] = article.intro
    list["meta_og_url"] = current_site
    list["meta_og_title"] = article.title
    list["meta_og_description"] = article.intro
    list["meta_og_image_url"] = "https://" + str(current_site) + article.image.url

    return render(request, "article_page.html", context=list)

def about_us_page(request):
    list = {}

    # Email Section ---------------------->
    email_form = EmailForm(request.POST or None)
    if email_form.is_valid():
        object = email_form.save()
        object.save()
        messages.success(request, "Thank you for subscribing. Check your email for the confirmation message.")

        current_site = get_current_site(request)
        subject = "Confirm Your Email for subscribing Heypo Newsletter."
        message = render_to_string("activation/messages/email_activation_message.html", {
            'email': email_form.data['email'],
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(object.pk)),
            'token': generate_token.make_token(object),
        })
        email = EmailMessage(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [object.email],
        )
        email.fail_silently = True
        email.send()
    list['email_form'] = email_form
    # Author of this template : @arjunahmad66
    # Email Section ---------------------->

    list['current_site'] = get_current_site(request)
    return render(request, "about_us_page.html", context=list)

def privacy_policy_page(request):
    list = {}

    # Email Section ---------------------->
    email_form = EmailForm(request.POST or None)
    if email_form.is_valid():
        object = email_form.save()
        object.save()
        messages.success(request, "Thank you for subscribing. Check your email for the confirmation message.")

        current_site = get_current_site(request)
        subject = "Confirm Your Email for subscribing Heypo Newsletter."
        message = render_to_string("activation/messages/email_activation_message.html", {
            'email': email_form.data['email'],
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(object.pk)),
            'token': generate_token.make_token(object),
        })
        email = EmailMessage(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [object.email],
        )
        email.fail_silently = True
        email.send()
    list['email_form'] = email_form
    # Email Section ---------------------->

    list['current_site'] = get_current_site(request)
    return render(request, "privacy_policy_page.html", context=list)

def terms_and_conditions_page(request):
    list = {}

    # Email Section ---------------------->
    email_form = EmailForm(request.POST or None)
    if email_form.is_valid():
        object = email_form.save()
        object.save()
        messages.success(request, "Thank you for subscribing. Check your email for the confirmation message.")

        current_site = get_current_site(request)
        subject = "Confirm Your Email for subscribing Heypo Newsletter."
        message = render_to_string("activation/messages/email_activation_message.html", {
            'email': email_form.data['email'],
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(object.pk)),
            'token': generate_token.make_token(object),
        })
        email = EmailMessage(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [object.email],
        )
        email.fail_silently = True
        email.send()
    list['email_form'] = email_form
    # Email Section ---------------------->

    list['current_site'] = get_current_site(request)
    return render(request, "terms_and_conditions_page.html", context=list)

def activate_email(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        object = Email.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Email.DoesNotExist):
        object = None

    if object is not None and generate_token.check_token(object, token):
        object.active = True
        object.save()

        subject = "Welcome to Heypo newsletter"
        message = "Our newsletter feature will be coming soon."
        email = EmailMessage(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [object.email],
        )
        email.fail_silently = True
        email.send()
        return redirect('/')
    else:
        return render(request, "activation/activation_failed_page.html")


