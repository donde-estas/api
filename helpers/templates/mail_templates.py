mailer_link = "https://donde-estas-sender.herokuapp.com/send"

skeleton = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Dónde Estás Mail</title>
    <style>
        body {
            text-align: justify;
        }

        div.container {
            align-content: center;
            text-align: justify;
            margin: 3%;
        }

        a {
            background-color: #049f04;
            color: white!important;
            padding: 2% 2%;
            text-align: center;
            text-decoration: none;
            font-size: 40px;
            display: inline-block;
            border-radius: 5px;
            width: 86%;
            margin: 5%;
        }
    </style>

</head>
<body>
    {body}
</body>
</html>
""".replace("\n", "").replace("  ", "")

body_template = """
    <div class="container">
        <h3>Hola {nombre}!</h3>
        <p>
            Si le ha llegado este mail, es por que {descripcion1}. 
            En caso de que creas que esto fue un error, 
            se agradecería responder este mail con el asunto ERROR. 
            En caso contrario, y {descripcion2}:
        </p>
        <a href="http://google.com" target="_blank">¡Estoy Bien!</a>

        <p>Atte. Equipo Dónde Estas</p>
    </div>
"""

body_template = body_template.replace("\n", "").replace("  ", "")

informant1 = "usted ha denunciado en la página ¿Dónde Están? que sospecha la desaparición de {nombre}"
informant2 = "si llega a conocer el paradero de la persona, por favor haga click en el siguiente botón para actualizar su estado en la página"
missing1 = "usted ha sido ingresado en la página ¿Dónde Están? cómo persona desaparecida por {nombre}"
missing2 = "si usted se encuentra bien, por favor haga click en el siguiente botón para actualizar su estado en la página"
