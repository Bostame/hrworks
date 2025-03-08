from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserEditForm
from django.contrib import messages
from .forms import UserRegistrationForm
from django.utils.timezone import now
from .models import TimeTracking
from datetime import timedelta
from decimal import Decimal  # Import Decimal
from django.db.models import Sum
import json
from django.http import JsonResponse
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from django.core.paginator import Paginator
from .models import CustomUser

@login_required
def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "User created successfully!")
            return redirect('dashboard')  # Redirect after creating a user
    else:
        form = UserRegistrationForm()

    return render(request, 'accounts/register_user.html', {'form': form})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserEditForm(request.POST, request.FILES, instance=request.user)  # Handle image upload
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('dashboard')
    else:
        form = UserEditForm(instance=request.user)
    
    return render(request, 'accounts/edit_profile.html', {'form': form})


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

    # Get today's working hours
    today_entries = TimeTracking.objects.filter(user=user, date=today)
    total_today_hours = Decimal(0)
    clocked_in = False
    clock_in_time = None

    for entry in today_entries:
        if entry.clock_in and entry.clock_out:
            total_today_hours += Decimal(entry.total_hours)
        elif entry.clock_in and not entry.clock_out:
            clocked_in = True
            total_today_hours += Decimal((now() - entry.clock_in).total_seconds() / 3600)
            if clock_in_time is None:
                clock_in_time = entry.clock_in.strftime("%H:%M")

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

    context = {
        "clocked_in": clocked_in,
        "clock_in_time": clock_in_time,
        "hours_worked": float(total_today_hours),
        "total_hours_month": float(total_hours_month),
        "total_overtime_month": float(total_overtime_month),
        "vacation_balance": float(user.vacation_balance),
        "vacation_days_used": float(vacation_days_used),
        "charts": charts,
    }

    return render(request, "accounts/dashboard.html", context)


@login_required
def get_live_hours(request):
    """ API Endpoint to fetch live working hours """
    user = request.user
    today = now().date()

    # Get today's working hours
    today_entries = TimeTracking.objects.filter(user=user, date=today)
    total_today_hours = 0
    clocked_in = False

    for entry in today_entries:
        if entry.clock_in and entry.clock_out:
            total_today_hours += float(entry.total_hours)
        elif entry.clock_in and not entry.clock_out:
            clocked_in = True
            # Calculate active session time
            total_today_hours += (now() - entry.clock_in).total_seconds() / 3600

    return JsonResponse({"hours_worked": round(total_today_hours, 2), "clocked_in": clocked_in})


@login_required
def export_pdf(request):
    user = request.user
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

    # DEBUG: Print values before generating the PDF
    print("User:", user.username)
    print("Today's Hours:", total_today_hours)
    print("Monthly Hours:", total_hours_month)
    print("Overtime:", total_overtime_month)
    print("Vacation Balance:", vacation_balance)

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



def company_information(request):
    return render(request, 'accounts/company_information.html')

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