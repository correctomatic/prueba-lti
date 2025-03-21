


## Ejemplos

parece muy antiguo:
https://github.com/mitodl/mit_lti_flask_sample

Más ejemplos:
https://github.com/blackboard/BBDN-lti-1p3-tool-example


Este tiene buena pinta:
https://edutechdev.com/2023/11/19/build-a-simple-lms-integrated-quiz-app-using-python-react-js-and-lti-1-3-part-1/
https://edutechdev.com/2023/11/20/build-a-simple-lms-integrated-quiz-app-using-python-react-js-and-lti-1-3-part-2/
https://edutechdev.com/2023/11/21/build-a-simple-lms-integrated-quiz-app-using-python-react-js-and-lti-1-3-part-3/
https://edutechdev.com/2023/11/23/build-a-simple-lms-integrated-quiz-app-using-python-react-js-and-lti-1-3-part-4/
https://edutechdev.com/2023/11/23/build-a-simple-lms-integrated-quiz-app-using-python-react-js-and-lti-1-3-part-5/


https://edutechdev.com/2023/02/10/lti-moodle-integration-using-pylti-1-3-flask-game-example/

## Library documentation

https://github.com/dmitry-viskov/pylti1.3

Para habilitar cualquier cosa, sin tener previamente el `client_id` y el `deployment_ids`:
>> or create your own implementation. The pylti1p3.tool_config.ToolConfAbstract interface must be fully implemented for this to work.

client_id - this is the id received in the 'aud' during a launch
deployment_ids (list) - The deployment_id passed by the platform during launch

Habrá que reescribirlo y devolver la configuración de algo en memoria o BD?

EL DEPLOYMENT_ID SE PUEDE SACAR DEL JWT DEL LAUNCH
El client_id lo muestra moodle en la configuración del recurso externo.

## Generate key pairs

Using OpenSSL
Generate a Private Key:

```sh
openssl genpkey -algorithm RSA -out private.key
```
This command generates an RSA private key and saves it to a file named private.key.

Generate the Corresponding Public Key:
```sh
openssl rsa -pubout -in private.key -out public.key
```
This command extracts the public key from the private key and saves it to a file named public.key.


## Notas

pip install flask
pip install oauthlib






https://github.com/moodlehq/moodle-docker

https://github.com/bitnami/containers/blob/main/bitnami/moodle/README.md
default user/bitnami

curl -sSL https://raw.githubusercontent.com/bitnami/containers/main/bitnami/moodle/docker-compose.yml


### Configuracion herramienta externa

Se accede desde el navegador local:
http://localhost:5000/launch
