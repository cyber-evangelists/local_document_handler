# Local Document Handler

## Nextcloud Configuration

### Prerequisites

1. **Install Docker**: Download and install [Docker](https://www.docker.com) and [Docker Compose](https://docs.docker.com/compose/install/) on your Windows machine.

2. **Open Command Prompt**: Open the Windows Command Prompt terminal.

### Setting Up Nextcloud

3. **Run Docker Container**: Execute the following command to run the Nextcloud container:

   ```bash
   docker run -d -p 8080:80 nextcloud

4. Access Nextcloud: Open your web browser and navigate to http://localhost:8080/.

5. Create Super User: Set up a superuser account by providing a username and password when prompted.

6. Install Apps (if required): Install any additional apps you need for your Nextcloud setup.

7. Create 'flask' Folder: In the admin account, create a folder named 'flask.'

8. View Container Logs: Monitor the Nextcloud container by opening Docker and clicking on the Nextcloud container to view its logs.

Edit config.php: To configure Nextcloud, follow these steps:
 - Click on the "File" tab in the Nextcloud web interface.
 - Open the "config" folder.
 - Edit the "config.php" file.
 - Find the "trusted_domains" key and add the URL that the Flask container will use to access Nextcloud.

 Set Permissions: In the terminal tab, run the following commands to set the correct permissions for the Nextcloud configuration folder:

    bash

    chown -R www-data:www-data config
    chmod -R 775 config

    Restart Container (if required): Restart your Nextcloud container if necessary to apply the changes.

Important Note

    Whenever you create a new user, the admin must share the 'flask' folder with that user so they can access it after login.

Flask Server Configuration
Setup Steps

 Clone the Repo: Clone the repository containing your Flask application.

 Navigate to the Flask Folder: Open a command prompt and navigate to the folder containing your Flask application.

 Run Docker Compose: Execute the following command to start the Flask server using Docker Compose:

    bash
      
    docker compose up

 Configure the .NET Service: Refer to the README file in the Flask folder for instructions on configuring the .NET service.

 Additional Setup: Complete any additional setup steps as mentioned in the README file to ensure your Flask server is fully functional.

By following these steps, you can set up both Nextcloud and your Flask server on your Windows machine for local document handling.
