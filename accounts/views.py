from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserEditForm, EventForm
from django.contrib import messages
from .forms import UserRegistrationForm
from django.utils.timezone import now, make_aware
from .models import TimeTracking, CustomUser, Event
from datetime import timedelta
from decimal import Decimal  # Import Decimal
from django.db.models import Sum
import json
from django.http import JsonResponse
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from django.core.paginator import Paginator
from datetime import datetime
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.dateparse import parse_datetime
from django.contrib.auth.hashers import make_password
from django.db.models import Q
@login_required
def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)  # Don't save yet
            user.password = make_password(form.cleaned_data["password1"])  # Hash password manually
            user.save()
            messages.success(request, "✅ User created successfully!")
            return redirect('dashboard')  # Redirect after creating a user
        else:
            messages.error(request, "❌ There was an error in the form. Please check the inputs.")
    else:
        form = UserRegistrationForm()

    return render(request, 'accounts/register_user.html', {'form': form})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserEditForm(request.POST, request.FILES, instance=request.user, editor=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('dashboard')
    else:
        form = UserEditForm(instance=request.user, editor=request.user)
    
    return render(request, 'accounts/edit_profile.html', {'form': form})

@login_required
def edit_user(request, user_id):
    """ Allows HR, CEO, and Superusers to edit any user's details. """
    user = get_object_or_404(CustomUser, id=user_id)

    # Ensure only HR, CEO, and Superusers can edit users
    if not request.user.is_superuser and request.user.role not in ["HR", "CEO"]:
        messages.error(request, "🚫 You do not have permission to edit users.")
        return redirect("manage_users")

    if request.method == "POST":
        form = UserEditForm(request.POST, request.FILES, instance=user, editor=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ User updated successfully!")
            return redirect("manage_users")
    else:
        form = UserEditForm(instance=user, editor=request.user)

    return render(request, "accounts/edit_profile.html", {"form": form, "user": user})

@login_required
def delete_user(request, user_id):
    """ Allows only HR, CEO, and Superusers to delete users. """
    user = get_object_or_404(CustomUser, id=user_id)

    # Ensure only Superusers, HR, and CEO can delete users
    if not request.user.is_superuser and request.user.role not in ["HR", "CEO"]:
        messages.error(request, "🚫 You do not have permission to delete users.")
        return redirect("manage_users")

    if request.user == user:
        messages.error(request, "🚫 You cannot delete your own account.")
        return redirect("manage_users")

    user.delete()
    messages.success(request, "✅ User deleted successfully!")
    return redirect("manage_users")


@login_required
def my_profile(request):
    return render(request, 'accounts/my_profile.html', {'user': request.user})

@login_required
def clock_in(request):
    """Records the clock-in time for the user."""
    today = now().date()
    current_time = now()

    time_entry, created = TimeTracking.objects.get_or_create(user=request.user, date=today, clock_out__isnull=True)

    if time_entry.clock_in is None:
        time_entry.clock_in = current_time
        messages.success(request, "Clock-in successful!")
    else:
        messages.warning(request, "You have already clocked in.")

    time_entry.save()
    return redirect('dashboard')


@login_required
def clock_out(request):
    """Records the clock-out time and updates total hours worked."""
    today = now().date()
    current_time = now()

    try:
        time_entry = TimeTracking.objects.filter(user=request.user, date=today, clock_in__isnull=False, clock_out__isnull=True).last()
        if time_entry:
            time_entry.clock_out = current_time

            # Calculate hours worked for this session
            total_time = time_entry.clock_out - time_entry.clock_in
            worked_hours = Decimal(total_time.total_seconds()) / Decimal(3600)  # Convert to Decimal

            # Add to total hours for today
            time_entry.total_hours += worked_hours.quantize(Decimal("0.01"))  # Keep 2 decimal places
            time_entry.overtime = max(Decimal(0), time_entry.total_hours - Decimal(8))  # Overtime check
            
            time_entry.save()
            messages.success(request, "Clock-out successful!")
        else:
            messages.warning(request, "You have not clocked in yet.")

    except TimeTracking.DoesNotExist:
        messages.error(request, "You must clock in before clocking out.")

    return redirect('dashboard')



@login_required
def dashboard(request):
    user = request.user
    today = now().date()
    
    # Fetch employees only for HR, CEO, and Admins
    employees = None
    if user.is_superuser or user.role in ["HR", "CEO"]:
        employees = CustomUser.objects.filter(is_active=True).order_by('first_name')

    # Get today's working hours
    today_entries = TimeTracking.objects.filter(user=user, date=today)
    total_today_hours = Decimal(0)
    clocked_in = False
    clock_in_time = None
    last_clock_in = None

    for entry in today_entries:
        if entry.clock_in and entry.clock_out:
            total_today_hours += Decimal(entry.total_hours)
        elif entry.clock_in and not entry.clock_out:
            clocked_in = True
            last_clock_in = entry.clock_in
            total_today_hours += Decimal((now() - entry.clock_in).total_seconds() / 3600)
            if clock_in_time is None:
                clock_in_time = entry.clock_in.strftime("%H:%M")

    # Calculate remaining work time
    max_work_seconds = 8 * 3600
    elapsed_work_seconds = int(total_today_hours * 3600)
    remaining_work_seconds = max(max_work_seconds - elapsed_work_seconds, 0)

    # Monthly statistics
    first_day_of_month = today.replace(day=1)
    month_entries = TimeTracking.objects.filter(user=user, date__gte=first_day_of_month)
    total_hours_month = month_entries.aggregate(Sum('total_hours'))['total_hours__sum'] or Decimal(0)
    total_overtime_month = month_entries.aggregate(Sum('overtime'))['overtime__sum'] or Decimal(0)

    # Vacation balance
    vacation_days_used = Decimal(30) - Decimal(user.vacation_balance)

    # Convert Decimal to float for JSON serialization
    charts = json.dumps([
        {"chart_id": "dailyHoursChart", "title": "Today's Hours", "worked": float(total_today_hours), "max": 10, "color": "#3498db"},
        {"chart_id": "monthlyHoursChart", "title": "Monthly Hours", "worked": float(total_hours_month), "max": 160, "color": "#2ecc71"},
        {"chart_id": "overtimeChart", "title": "Overtime", "worked": float(total_overtime_month), "max": 20, "color": "#e74c3c"},
        {"chart_id": "vacationUsedChart", "title": "Vacation Used", "worked": float(vacation_days_used), "max": 30, "color": "#f39c12"},
        {"chart_id": "vacationBalanceChart", "title": "Vacation Balance", "worked": float(user.vacation_balance), "max": 30, "color": "#1abc9c"},
    ])

    # Role-based access control
    is_hr = user.is_hr()
    is_team_lead = user.is_team_lead()
    is_ceo = user.is_ceo()

    context = {
        "clocked_in": clocked_in,
        "clock_in_time": clock_in_time,
        "hours_worked": float(total_today_hours),
        "total_hours_month": float(total_hours_month),
        "total_overtime_month": float(total_overtime_month),
        "vacation_balance": float(user.vacation_balance),
        "vacation_days_used": float(vacation_days_used),
        "remaining_work_seconds": remaining_work_seconds if clocked_in else None,
        "charts": charts,
        "is_hr": is_hr,
        "is_team_lead": is_team_lead,
        "is_ceo": is_ceo,
        "employees": employees  # Pass employees list for HR/Admins to select for export
    }

    return render(request, "accounts/dashboard.html", context)



@login_required
def manage_users(request):
    """Allows HR, CEO, and Superusers to view and manage users with search and pagination."""

    if not request.user.is_superuser and request.user.role not in ["HR", "CEO"]:
        messages.error(request, "🚫 You do not have permission to manage users.")
        return redirect("dashboard")

    query = request.GET.get("q", "").strip()  # Get and clean search query
    users = CustomUser.objects.all().order_by('id')  # Order users by ID

    # Apply search filter if query exists
    if query:
        users = users.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(email__icontains=query) |
            Q(current_position__icontains=query) |
            Q(role__icontains=query)
        )

    # ✅ Add Pagination (6 users per page for better UI)
    paginator = Paginator(users, 6)  # Change to 6 per page for responsive design
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "accounts/manage_users.html", {"users": page_obj, "query": query})



@login_required
def get_live_hours(request):
    """ API Endpoint to fetch live working hours & remaining work time """
    user = request.user
    today = now().date()

    today_entries = TimeTracking.objects.filter(user=user, date=today)
    total_today_hours = 0
    clocked_in = False

    for entry in today_entries:
        if entry.clock_in and entry.clock_out:
            total_today_hours += float(entry.total_hours)
        elif entry.clock_in and not entry.clock_out:
            clocked_in = True
            total_today_hours += (now() - entry.clock_in).total_seconds() / 3600

    max_work_seconds = 8 * 3600  # 8 hours in seconds
    elapsed_work_seconds = int(total_today_hours * 3600)  # Convert to seconds
    remaining_work_seconds = max(max_work_seconds - elapsed_work_seconds, 0)  # Ensure non-negative

    return JsonResponse({
        "hours_worked": round(total_today_hours, 2),
        "clocked_in": clocked_in,
        "remaining_work_seconds": remaining_work_seconds  # ✅ This is now included
    })


@login_required
def export_pdf(request, user_id=None):
    """Allows employees to export their own reports and HR/CEO/Admins to export any user's report."""
    
    # If user_id is provided, fetch the requested user
    if user_id:
        if not (request.user.is_superuser or request.user.role in ["HR", "CEO"]):
            messages.error(request, "🚫 You do not have permission to export reports for other users.")
            return redirect("dashboard")
        user = get_object_or_404(CustomUser, id=user_id)
    else:
        user = request.user  # Employees can only export their own reports

    today = now().date()

    # Retrieve all work session data for today
    today_entries = TimeTracking.objects.filter(user=user, date=today)
    total_today_hours = sum(float(entry.total_hours) for entry in today_entries)

    # Monthly statistics
    first_day_of_month = today.replace(day=1)
    month_entries = TimeTracking.objects.filter(user=user, date__gte=first_day_of_month)
    total_hours_month = month_entries.aggregate(Sum('total_hours'))['total_hours__sum'] or 0
    total_overtime_month = month_entries.aggregate(Sum('overtime'))['overtime__sum'] or 0

    # Vacation tracking
    vacation_balance = user.vacation_balance if hasattr(user, 'vacation_balance') else 30

    # Create a buffer for the PDF file
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer)

    # PDF Title
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(200, 800, "Work Hours Report")

    # User Info
    pdf.setFont("Helvetica", 12)
    pdf.drawString(100, 760, f"User: {user.first_name} {user.last_name}")
    pdf.drawString(100, 740, f"Report Date: {today}")

    # Work Hours Data
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(100, 700, "Work Summary")
    pdf.setFont("Helvetica", 11)
    pdf.drawString(100, 680, f"Today's Hours: {total_today_hours:.2f}h")
    pdf.drawString(100, 660, f"Monthly Hours: {total_hours_month:.2f}h")
    pdf.drawString(100, 640, f"Overtime: {total_overtime_month:.2f}h")
    pdf.drawString(100, 620, f"Vacation Balance: {vacation_balance} days")

    # Finalize the PDF
    pdf.showPage()
    pdf.save()
    buffer.seek(0)

    # Return the PDF as a downloadable file
    return FileResponse(buffer, as_attachment=True, filename=f"work_hours_report_{user.username}.pdf")

@login_required
def telephone_directory(request):
    query = request.GET.get('q', '')  # Get search query
    employees = CustomUser.objects.filter(is_active=True).order_by('id')  # ✅ Ordered for consistent pagination

    # Apply search filter
    if query:
        employees = employees.filter(
            first_name__icontains=query
        ) | employees.filter(
            last_name__icontains=query
        ) | employees.filter(
            email__icontains=query
        ) | employees.filter(
            office_phone__icontains=query
        )

    # Pagination (10 employees per page)
    paginator = Paginator(employees, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'accounts/telephone_directory.html', {'page_obj': page_obj, 'query': query})


@login_required
def company_information(request):
    # Example company data (this can later be stored in a model)
    company_details = {
        'name': 'Techiecraft Solutions GmbH',
        'address': 'Berliner Str. 123, 10115 Berlin, Germany',
        'phone': '+49 30 12345678',
        'email': 'contact@techiecraft.de',
        'website': 'https://www.techiecraft.de',
        'founded': '2015',
        'employees': '150+',
        'mission': 'Delivering cutting-edge tech solutions to businesses worldwide.',
        'vision': 'To be the leading provider of IT innovations in Europe.',
    }
    
    return render(request, 'accounts/company_information.html', {'company_details': company_details})

@login_required
def company_calendar(request):
    """Show all events in the company calendar"""
    events = Event.objects.all().order_by("start_time")  # Fetch all events sorted by date
    return render(request, "accounts/company_calendar.html", {"events": events})


@login_required
def company_calendar_view(request, view_type):
    """Display different views of the company calendar based on the selected filter."""
    today = now().date()
    events = Event.objects.all()
    start_date, end_date = None, None

    if view_type == "this_week":
        start_date = today - timedelta(days=today.weekday())  # Monday
        end_date = start_date + timedelta(days=6)  # Sunday
        events = events.filter(start_time__date__gte=start_date, end_time__date__lte=end_date)
        title = "📅 This Week's Schedule"

    elif view_type == "org_units":
        events = events.filter(event_type="Work Shift")
        title = "🏢 By Organizational Units"

    elif view_type == "superior":
        events = events.filter(event_type="Meeting")
        title = "👨‍💼 By Superior"

    elif view_type == "person":
        events = events.filter(event_type="General")
        title = "🙋 Individual Person Selection"

    elif view_type == "group":
        events = events.filter(event_type="Group Meeting")
        title = "👥 Individual Group Selection"

    elif view_type == "attendance":
        title = "📊 Attendance Overview"

    else:
        title = "📅 Company Calendar"


    context = {
        'title': title,
        'events': events,
        'start_date': start_date.strftime('%b %d, %Y') if start_date else None,
        'end_date': end_date.strftime('%b %d, %Y') if end_date else None
    }

    return render(request, 'accounts/company_calendar_view.html', context)


@login_required
def add_event(request):
    """Handles adding a new event to the calendar"""
    if request.method == "POST":
        title = request.POST.get("title")
        event_type = request.POST.get("event_type")
        start_time = request.POST.get("start_time")
        end_time = request.POST.get("end_time")
        location = request.POST.get("location", "")


        # Ensure start_time and end_time are not None
        if not start_time or not end_time:
            messages.error(request, "❌ Start time and end time are required!")
            return redirect("add_event")

        # Parse datetime safely
        start_time_parsed = parse_datetime(start_time)
        end_time_parsed = parse_datetime(end_time)

        if not start_time_parsed or not end_time_parsed:
            messages.error(request, "❌ Invalid date format! Please use the correct datetime format.")
            return redirect("add_event")

        # Convert to timezone-aware datetime
        start_time_aware = make_aware(start_time_parsed)
        end_time_aware = make_aware(end_time_parsed)

        # Create event
        Event.objects.create(
            title=title,
            event_type=event_type,
            start_time=start_time_aware,
            end_time=end_time_aware,
            location=location,
            created_by=request.user,
        )

        messages.success(request, "✅ Event successfully added!")
        return redirect("company_calendar_view", view_type="this_week")

    return render(request, "accounts/add_event.html")

@login_required
def edit_event(request, event_id):
    """Allows admins to edit an event."""
    event = get_object_or_404(Event, id=event_id)

    if request.method == "POST":
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Event updated successfully!")
            return redirect("company_calendar_view", view_type="this_week")

    else:
        form = EventForm(instance=event)

    return render(request, "accounts/edit_event.html", {"form": form, "event": event})

@login_required
def delete_event(request, event_id):
    """Allows admins to delete an event."""
    event = get_object_or_404(Event, id=event_id)

    if request.user.is_superuser:
        event.delete()
        messages.success(request, "❌ Event deleted successfully!")
    else:
        messages.error(request, "🚫 You do not have permission to delete this event.")

    return redirect("company_calendar_view", view_type="this_week")

def company_calendar_this_week(request):
    return render(request, 'accounts/company_calendar_this_week.html')

def company_calendar_org_units(request):
    return render(request, 'accounts/company_calendar_org_units.html')

def company_calendar_superior(request):
    return render(request, 'accounts/company_calendar_superior.html')

def company_calendar_person(request):
    return render(request, 'accounts/company_calendar_person.html')

def company_calendar_group(request):
    return render(request, 'accounts/company_calendar_group.html')

def company_calendar_attendance(request):
    return render(request, 'accounts/company_calendar_attendance.html')