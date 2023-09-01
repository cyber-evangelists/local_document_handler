# local_document_handler


## Next cloud configration:

install (docker)[https://www.docker.com] in windows
open cmd terminal
run command ```docker run -d -p 8080:80 nextcloud```
hit URL in your Browser ```http://localhost:8080/```
make super user by setting username and password
install apps if required
open docker and click next cloud contianer to watch logs.
click file tab
open config folder and edit config.php file.
find trusted_domains key and add url that flask container will be used for accessing the nextcloud.
go to the terminal tab and run these commands
```chown -R www-data:www-data config```
```chmod -R 775 config```
restart your container if required.


## Flask server configration


