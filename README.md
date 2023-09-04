# Local Document Handler


## Next cloud configration:

install [Docker](https://www.docker.com) and compose in windows.

open cmd terminal.

run command ```docker run -d -p 8080:80 nextcloud```.

hit URL in your Browser ```http://localhost:8080/```.

make super user by setting username and password.

install apps if required.

important:MAKE A FOLDER NAME 'flask' in admin account

open docker and click next cloud contianer to watch logs.

click file tab.

open config folder and edit config.php file.

find trusted_domains key and add url that flask container will be used for accessing the nextcloud.

go to the terminal tab and run these commands.

```chown -R www-data:www-data config```.

```chmod -R 775 config```.

restart your container if required.

NOTE: WHEN EVER YOU CREATE NEW USER, ADMIN HAVE TO SHARE flask FOLDER WITH THAT NEW USER SO USER CAN LOGIN.

## Flask server configration


after cloning the repo, go to the flask folder.
open cmd in that folder by typing ```cmd``` in address bar.
run command ```docker compose up```.

now configure the .NET service by reading README file in that folder.