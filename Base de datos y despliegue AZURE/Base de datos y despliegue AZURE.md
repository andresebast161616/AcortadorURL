[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/tiytFz6V)
[![Open in Codespaces](https://classroom.github.com/assets/launch-codespace-2972f46106e565e64193e422d61a12cf1da4916b45550586e14ef0a7c637dd04.svg)](https://classroom.github.com/open-in-codespaces?assignment_repo_id=15379374)
# proyecto-formatos-01
LINK DE DESPLIEGUE AZURE: 
acortadorurls.azurewebsites.net

PARA LA BASE DE DATOS (AZURE):

1. Nos dirigimos a Microsoft Azure, nos logueamos con nuestra cuenta (en mi caso @upt.pe) y una vez ingresado buscamos SQL Database

![](Aspose.Words.5265b02a-d4c3-4cb0-be64-3272a15b1158.001.png)

1. Al crear el servidor le pondremos un nombre y seleccionaremos una ubicación ( dependiendo de donde hemos seleccionado el costo mensual será mayor o menor)

![](Aspose.Words.5265b02a-d4c3-4cb0-be64-3272a15b1158.002.png)

1. Cuando creemos la base de datos seleccionaremos la opción de “Uso de la autentificación de SQL”, le pondremos un nombre de sesión y una contraseña (no olvidar estos datos ya que los usaremos para ingresar al SQL SERVER MANAGEMENT STUDIO)

![](Aspose.Words.5265b02a-d4c3-4cb0-be64-3272a15b1158.003.png)

1. Ahora en la opcion de configurar cambiaremos el nivel de servicio por “Basico…” para que el precio sea menor

![](Aspose.Words.5265b02a-d4c3-4cb0-be64-3272a15b1158.004.png)

1. Una ves hemos seleccionado el nivel “Basico” también cambiaremos el tamaño máximo de datos, por default estará en el máximo, en nuestro caso lo bajaremos hasta el mínimo para que reduzca aun mas el costo final

![](Aspose.Words.5265b02a-d4c3-4cb0-be64-3272a15b1158.005.png)

1. Después revisaremos que todo este correcto y le damos al botón de crear

![](Aspose.Words.5265b02a-d4c3-4cb0-be64-3272a15b1158.006.png)

1. Se nos abrirá una ventana donde nos dirá los datos del la base de datos creada, ahí buscaremos nombre del servidor, ya que lo usaremos para ingresar al SQL Management Studio


![](Aspose.Words.5265b02a-d4c3-4cb0-be64-3272a15b1158.007.png)

1. Una vez abierto el SQL Management Studio pegaremos el nombre del servidor, e ingresaremos el usuario y contraseña que hemos definido anteriormente

![](Aspose.Words.5265b02a-d4c3-4cb0-be64-3272a15b1158.008.png)

1. Nos saldrá una ventana y le damos al botón de aceptar 

![](Aspose.Words.5265b02a-d4c3-4cb0-be64-3272a15b1158.009.png)

1. Finalmente, ya estaremos conectados a la base de datos de Azure y podremos crear o modificar tablas según lo queramos

![](Aspose.Words.5265b02a-d4c3-4cb0-be64-3272a15b1158.010.png)


DESPLIEGUE:

Nos basamos en el laboratorio 1 de la Unidad 3

1. Primero abrimos cmd dentro del nuestro proyecto y copiamos el siguiente código (el correo puede ser cualquiera que tengamos asociado a azure):

az login -u [**andfloresm@upt.pe**](mailto:andfloresm@upt.pe)

1. Crearemos un grupo correspondiente de recursos (en el nombre lo pondremos cualquier nombre que queramos)

az group create --name **BLAST1** --location eastus

1. Ahora crearemos un plan de servicio gratuito (donde dice “acortadorurls” podremos poner cualquier nombre que queramos)

az appservice plan create -g **BLAST1** -n **acortadorurls** --is-linux --sku F1

1. Ahora desplegaremos el proyecto con el siguiente comando (esto tomara un tiempo en terminar el proceso)

az webapp up -n **acortadorurls** -g **BLAST1** --runtime "PYTHON|3.9"

1. Finalmente terminado el anterior proceso ejecutaremos el log (esto también demorara un poco)

az webapp log tail -n **acortadorurls** -g **BLAST1**

1. Una vez finalice, nos vamos a nuestro azure y buscamos el servidor creado, en nuestro caso fue con el nombre de “acortadorurls”, y seleccionamos la opción que nos muestra la siguiente imagen:

![](Aspose.Words.5265b02a-d4c3-4cb0-be64-3272a15b1158.011.png)

1. Aquí veremos el IP que tiene nuestro servidor, lo copiamos para poder configurar la base de datos para que esta IP pueda acceder a la base de datos:

![](Aspose.Words.5265b02a-d4c3-4cb0-be64-3272a15b1158.012.png)

1. Volvemos a dirigirnos a nuestro Azure y seleccionaremos el servidor

![](Aspose.Words.5265b02a-d4c3-4cb0-be64-3272a15b1158.013.png)

1. Aquí nos dirigiremos a la opción de Seguridad >Redes y agregaremos la dirección IP copiada anteriormente para que esta IP puede conectarse a nuestra base de datos en Azure

![](Aspose.Words.5265b02a-d4c3-4cb0-be64-3272a15b1158.014.png)

1. Finalmente podremos ver nuestra página web desplegada (acortadorurls.azurewebsites.net), este link lo podremos encontrar si volvemos al paso 6.

![](Aspose.Words.5265b02a-d4c3-4cb0-be64-3272a15b1158.015.png)
