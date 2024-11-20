# Use the official Airflow image as the base
FROM apache/airflow:slim-2.10.3-python3.9

# Set the working directory
WORKDIR /usr/local/airflow

# Switch to root user for installing dependencies
USER root

# Install required system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    libssl-dev \
    libffi-dev \
    git \
    wget \
    && apt-get clean


# Add the HashiCorp GPG key and repository
RUN wget -O- https://apt.releases.hashicorp.com/gpg | gpg --dearmor > /usr/share/keyrings/hashicorp-archive-keyring.gpg \
    && echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" > /etc/apt/sources.list.d/hashicorp.list

# Install Terraform
RUN apt-get update && apt-get install -y terraform && apt-get clean

# Copy the current project files into the container
COPY . /usr/local/airflow/

RUN apt-get update && apt-get install -y git && apt-get clean

# Switch back to airflow user for installing Python dependencies
USER airflow

# Upgrade pip, setuptools, and wheel
RUN pip install --upgrade pip setuptools wheel

# Install grpcio separately to handle potential compatibility issues
RUN pip install grpcio

# Install Python dependencies from requirements.txt
#RUN pip install --no-cache-dir -r requirements.txt

# Expose Airflow webserver port
EXPOSE 8080

# Set the default command to run Airflow scheduler and webserver
CMD ["bash", "-c", "airflow scheduler & airflow webserver"]
