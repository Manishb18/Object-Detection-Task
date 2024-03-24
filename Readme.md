# Object Detection Task

This project contains the code to build a full stack web application to detect objects present in an image.
Used react as frontend and flask to build the backend of the application.

## Installation


### Instructions

 1. Clone the repository to your local machine:  using  
git clone https://github.com/Manishb18/Object-Detection-Task.git

or

Download the zip file 
 3. open the terminal and navigate to the main folder
 
 **Backend Setup**
 
 3. After you reach the backend folder. (Assuming that you have docker installed in your system)
*Run the following docker command*: docker build -t backend .
and then run : docker run -p 5000:5000 backend
 4. Now the docker image should run, if it doesn't don't worry I will tell you the other way to do it.
 5. If the docker thing does not work for you. follow the below steps.
 6. Navigate to the backend folder.
 7. Run this command in the terminal : pip install -r requirements.txt
 8. Now run  : python app.py 
 9. And now the backend should be up and running.
 
 **Frontend Setup:**

 
 10. If you are in the backend folder , do  : cd..
 11. Then cd frontend
 12. Now run  : npm install
 13. This will install all the required packages and get the app ready.
 14. Now finally run : npm run dev

 **Hurrah! Your app is now running!!**
 
Below is the video showing how the webapp works.

https://github.com/Manishb18/Object-Detection-Task/assets/81469629/10ffa1bb-3f46-4768-b3cd-12cad6b5f510


