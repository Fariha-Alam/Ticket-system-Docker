from django.shortcuts import render, redirect
from .forms import SignUpForm, LoginForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import TicketForm
from .models import Ticket
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST
import openpyxl
from openpyxl.utils import get_column_letter
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.utils.timezone import localtime
from django.utils import timezone
from .models import ITChecklist


from django.views.decorators.http import require_http_methods
from .forms import SolutionForm
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.shortcuts import render
from django.utils.crypto import get_random_string
from django.contrib.auth import get_user_model
@login_required
def home(request):
    if request.user.is_staff or request.user.is_superuser:
        return redirect('admin_dashboard')
    pending_tickets = Ticket.objects.filter(status='Pending', created_by=request.user)
    solved_tickets = Ticket.objects.filter(status='Solved', created_by=request.user)

    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.created_by = request.user
            last_ticket = Ticket.objects.order_by('-id').first()
            last_number = 0
            if last_ticket and last_ticket.ticket_number.startswith('TKT-'):
                last_number = int(last_ticket.ticket_number.split('-')[1])

            ticket.ticket_number = f"TKT-{last_number + 1:04d}"

            ticket.save()
            return redirect('dashboard')
    else:
        form = TicketForm()

    context = {
        'form': form,
        'pending_tickets': pending_tickets,
        'solved_tickets': solved_tickets,
        'pending_count': pending_tickets.count(),
        'solved_count': solved_tickets.count(),
    }

    return render(request, 'home.html', context)

def registration(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.first_name = form.cleaned_data['full_name']
            user.save()
            messages.success(request, "Account created successfully.")
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'registration.html', {'form': form})
from django.contrib.auth import authenticate, login, logout as auth_logout

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # ⇢  admin goes to admin_dashboard, others to home
            if user.is_superuser:
                return redirect('admin_dashboard')
            return redirect('it_checklist')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

    

@login_required
def dashboard(request):
    if request.user.is_staff or request.user.is_superuser:
        return redirect('admin_dashboard')

    pending_list = Ticket.objects.filter(created_by=request.user, status='pending').order_by('-date_created')
    solved_list = Ticket.objects.filter(created_by=request.user, status='solved').order_by('-date_created')

    pending_paginator = Paginator(pending_list, 3)
    solved_paginator = Paginator(solved_list, 3)

    pending_page_number = request.GET.get('pending_page', 1)
    solved_page_number = request.GET.get('solved_page', 1)

    pending_tickets = pending_paginator.get_page(pending_page_number)
    solved_tickets = solved_paginator.get_page(solved_page_number)

    return render(request, 'dashboard.html', {
        'pending_tickets': pending_tickets,
        'solved_tickets': solved_tickets,
    })

@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def admin_dashboard(request):
   
    tickets = Ticket.objects.select_related('created_by').order_by('-date_created')

    pending_tickets = tickets.filter(status='Pending')
    solved_tickets = tickets.filter(status='Solved')
    filter_type = request.GET.get('filter')
    user_query = request.GET.get('user')


    
    if filter_type == 'user' and user_query:
        tickets = tickets.filter(created_by__username__icontains=user_query)

  
    paginator = Paginator(tickets, 8)  # Show 8 tickets per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
         'page_obj': page_obj,  
        'pending_tickets': pending_tickets,  # add this
        'solved_tickets': solved_tickets,    # add this if needed
        'pending_count': pending_tickets.count(),
        'solved_count': solved_tickets.count(),
    }
    return render(request, 'admin_dashboard.html', context)

@login_required
@require_http_methods(["GET", "POST"])
def message_show(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    is_admin = request.user.is_staff or request.user.is_superuser

    if request.method == "POST" and is_admin:
        ticket.approx_solving_time = request.POST.get("approx_solving_time", "").strip()
        ticket.save()
        return redirect('message_show', ticket_id=ticket.id)  # Prevents resubmission

    return render(request, 'message_show.html', {
        'ticket': ticket,
        'is_admin': is_admin,
    })


@login_required
def logout(request):
    auth_logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')

@login_required
@require_POST
def update_ticket_status(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    new_status = request.POST.get('status')

    if new_status == "Delete":
        ticket.delete()
    else:
        ticket.status = new_status
        ticket.save()

    return redirect('admin_dashboard')



@login_required
def export_tickets_excel(request):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Tickets"

    # Header row
    ws.append(['Ticket Number', 'Username', 'Title', 'Description', 'Priority', 'Status', 'Date Created','Date Solved'])

    for ticket in Ticket.objects.all():
        ws.append([
            ticket.ticket_number,
            ticket.created_by.username if ticket.created_by else 'N/A',
            ticket.title,
            ticket.description,
            ticket.priority,
            ticket.status,
            localtime(ticket.date_created).strftime("%d %b %Y %H:%M"),
            localtime(ticket.solved_time).strftime("%d %b %Y %H:%M"),
        ])

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=tickets.xlsx'
    wb.save(response)
    return response

@login_required
def ticket_solution_detail(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if request.method == "POST" and (request.user.is_staff or request.user.is_superuser):
        ticket.solution_text = request.POST.get("solution_text")
        ticket.save()
        return redirect("ticket_solution_detail", ticket_id=ticket_id)
    return render(request, "solution.html", {"ticket": ticket})

@login_required
def mark_solved(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if request.user == ticket.created_by or request.user.is_staff:
        ticket.status = 'Solved'
        ticket.solved_time = timezone.now()
        ticket.save()
    return redirect('message_show', ticket_id=ticket_id)


@login_required
def checklist_view(request):
    if request.user.is_staff or request.user.is_superuser:
        return redirect('admin_dashboard')
    tasks = ITChecklist.objects.filter(is_active=True)

    if request.method == 'POST':
        # You can add logic to record acknowledgement
        return redirect('home')  # or wherever you want

    return render(request, 'checklist.html', {'tasks': tasks})

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        # Validate email presence and domain
        if not email or not email.endswith('@gmail.com'):
            return render(request, 'forgot_password.html', {
                'error': 'Only Gmail addresses are accepted for password reset.'
            })

        # Find users with that email
        users = User.objects.filter(email=email)
        count = users.count()

        if count == 0:
            # No user found
            return render(request, 'forgot_password.html', {
                'error': 'No user found with this Gmail address.'
            })
        elif count > 1:
            # Multiple users found with same email
            return render(request, 'forgot_password.html', {
                'error': 'Multiple accounts found with this Gmail address. Please use another Gmail account.'
            })
        else:
            # Exactly one user found
            user = users.first()
            # Generate a random temporary password
            temp_password = get_random_string(10)
            user.set_password(temp_password)
            user.save()

            # Send email with the temporary password
            send_mail(
                subject='Your Temporary IT Ticket System Password',
                message=f"""Hello {user.get_full_name() or user.username},

You have requested a password reset for your IT Ticket System account.

Your temporary password is: {temp_password}

Please log in using this password.

If you didn’t request this, please contact IT support.

Thank you,
IT Department
""",
                from_email='itsupport@yourcompany.com',
                recipient_list=[email],
                fail_silently=False,
            )

            # Show success message
            return render(request, 'forgot_password.html', {
                'success': 'Temporary password sent to your Gmail. Check your inbox.'
            })

    # If GET or other method, just render form
    return render(request, 'forgot_password.html')
