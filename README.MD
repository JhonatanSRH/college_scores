# Sistema de Notas

Este proyecto es una aplicación backend desarrollada con Django. A continuación, se detallan los pasos para instalar y ejecutar el proyecto en tu entorno local.

## Requisitos previos

Asegúrate de tener instalados los siguientes componentes:

- Python 3.x
- pip (gestor de paquetes de Python)
- virtualenv (opcional, pero recomendado)

## Instalación

1. Clona el repositorio en tu máquina local:

    ```bash
    git clone <URL_DEL_REPOSITORIO>
    cd library-manager
    ```

2. (Opcional) Crea y activa un entorno virtual:

    ```bash
    virtualenv venv
    source venv/bin/activate  # En Windows usa `venv\Scripts\activate`
    ```

3. (Opcional) Crea un archivo .env con las variables de entorno:

    ```bash
    SECRET_KEY="Clave secreta de la aplicación"
    ```

4. Instala las dependencias del proyecto:

    ```bash
    pip install -r requirements.txt
    ```

5. Realiza las migraciones de la base de datos:

    ```bash
    python manage.py migrate
    ```

6. Crea un superusuario para acceder al panel de administración:

    ```bash
    python manage.py createsuperuser
    ```

## Ejecución

1. Inicia el servidor de desarrollo de Django:

    ```bash
    python manage.py runserver
    ```

2. Abre tu navegador web y navega a `http://127.0.0.1:8000` para ver la aplicación en funcionamiento.

3. Accede al panel de administración en `http://127.0.0.1:8000/admin` e inicia sesión con el superusuario que creaste anteriormente.

4. (Opcional) Para acceder a la documentacion de swagger accede a la ruta: `http://127.0.0.1:8000/docs/swagger/`

## Estructura de Base de Datos

Modelos:

1. Teacher
Este modelo almacena la información de los profesores de la universidad.

    Campos:
    first_name: Nombre del profesor (CharField, máximo 100 caracteres).
    last_name: Apellido del profesor (CharField, máximo 100 caracteres).
    email: Correo electrónico único del profesor (EmailField).

    Relaciones:
    Una relación uno a muchos (ForeignKey) con el modelo Materia para indicar qué materias tiene asignadas un profesor.

2. Student
Este modelo almacena la información de los estudiantes de la universidad.

    Campos:
    first_name: Nombre del estudiante (CharField, máximo 100 caracteres).
    last_name: Apellido del estudiante (CharField, máximo 100 caracteres).
    email: Correo electrónico único del estudiante (EmailField).
    birth_date: Fecha de nacimiento del estudiante (DateField).

    Relaciones:
    Una relación uno a muchos (ForeignKey) con el modelo Inscripcion para indicar en qué materias está inscrito un estudiante.

3. Subject
Este modelo almacena la información de las materias que se ofrecen en la universidad.

    Campos:
    name: Nombre de la materia (CharField, máximo 100 caracteres).
    code: Código único de la materia (CharField, máximo 10 caracteres).
    teacher: Profesor que dicta la materia (ForeignKey al modelo Profesor).

    Relaciones:
    Una relación muchos a muchos (ManyToManyField) a si misma para indicar las materias previas que son requisito para inscribirse en una materia.
    Una relación uno a muchos (ForeignKey) con el modelo Inscripcion para indicar qué estudiantes están inscritos en la materia.

4. Registration
Este modelo almacena la información de las inscripciones de los estudiantes a las materias.

    Campos:
    student: Estudiante que se inscribe en la materia (ForeignKey al modelo Estudiante).
    subject: Materia en la que se inscribe el estudiante (ForeignKey al modelo Materia).
    registration_date: Fecha en la que se realizó la inscripción (DateField, se genera automáticamente al crear la inscripción).
    score: Indica la nota del estudiante en la materia inscrita (BooleanField, por defecto False).

    Relaciones:
    Una relación muchos a uno con el modelo Estudiante y Materia.

    Validaciones:
    Un estudiante no puede inscribirse en una materia si no ha aprobado las materias previas requeridas.

## Autenticación

Todos los endpoint estan protegidos mediante autenticación con json web token. Para crear un token de acceso, se debe acceder al endpoint de obtener token (se recomienda crear un super usuario para poder obtenerlo). Cada hora se debe actualizar el token de acceso, para ello el servicio de obtener token provee un token de refresco el cual debe ser proveido en el servicio de refrescar token para volver a obtener un token de acceso o por consiguiente usar el servicio inicial indicando el usuario y la contraseña con la cual se generara el token.

## Tests

Se puede ejecutar todas las pruebas con el comando:

    ```bash
    python manage.py test apps
    ```

## Docs

Este proyecto esta documentado con swagger, la ruta es: `/docs/swagger/`

## Licencia

Este proyecto está bajo la Licencia MIT.
