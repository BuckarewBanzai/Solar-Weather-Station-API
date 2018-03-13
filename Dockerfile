# Use an official Python runtime as a parent image
FROM python:2.7-slim

# Set the working directory to /app
WORKDIR /app

#Upload our code to the container
ADD . /app

#Pull our code
#RUN git clone https://github.com/KickinWingAnimalDoctor/Solar-Weather-Station-API.git

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 8081 available to the world outside this container
EXPOSE 8081

# Run app.py when the container launches
CMD ["python", "api.py"]
