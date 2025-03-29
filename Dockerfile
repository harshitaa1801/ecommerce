FROM python:3.12

ENV APP_ROOT /app

# Set the working directory
WORKDIR ${APP_ROOT}

# Copy and install dependencies
COPY requirements.txt ${APP_ROOT}/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . ${APP_ROOT}

# Expose the port that the application will run on
EXPOSE 8000

# Command to run the Django development server
CMD sh -c "python3 manage.py migrate && \
    if [ -n \"$DJANGO_SUPERUSER_USERNAME\" ] && [ -n \"$DJANGO_SUPERUSER_PASSWORD\" ] && [ -n \"$DJANGO_SUPERUSER_EMAIL\" ]; then \
        # Check if superuser already exists
        if ! python3 manage.py shell -c \"from django.contrib.auth.models import User; print(User.objects.filter(username='$DJANGO_SUPERUSER_USERNAME').exists())\" | grep -q 'True'; then \
            python3 manage.py createsuperuser --noinput --username $DJANGO_SUPERUSER_USERNAME --email $DJANGO_SUPERUSER_EMAIL; \
        fi; \
    fi && \
    python3 manage.py runserver 0.0.0.0:8000"