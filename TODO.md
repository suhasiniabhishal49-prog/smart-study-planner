# Reminder System Implementation TODO

## Steps Completed ✓

## Steps Pending ☐

### Step 1: Update Task model (planner/models.py)
- Add `reminder_time = models.DateTimeField(blank=True, null=True, help_text='Optional reminder time')`
- Add `reminder_sent = models.BooleanField(default=False)`

### Step 2: Update TaskForm (planner/forms.py)
- Add `'reminder_time'` to Meta.fields list
- Add widget: `'reminder_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'})`

### Step 3: Create management command
- Create `planner/management/__init__.py` (empty)
- Create `planner/management/commands/__init__.py` (empty)
- Create `planner/management/commands/send_reminders.py` (full command code)

### Step 4: Migrations & Test
- `python manage.py makemigrations planner`
- `python manage.py migrate`
- Test: create task with past reminder_time, run command, verify console + reminder_sent=True
