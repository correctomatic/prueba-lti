<moodle_release>3.11.17+ (Build: 20231201)</moodle_release>


WTF is the deployment id?




### LTI

DIAGRAMA MUY BUENO CON EXPLICACIONES!!!:
https://blackboard.github.io/lti/tutorials/implementation-guide


Especificacion:
https://www.imsglobal.org/spec/lti/v1p3/

https://www.1edtech.org/standards/lti


Basicos:
https://www.imsglobal.org/basic-overview-how-lti-works


Versión 1.3:
https://medium.com/voxy-engineering/introduction-to-lti-1-3-270f17505d75


https://www.edspirit.com/a-complete-guide-to-learning-tools-interoperability

**OJO, parece que Aules soporta la versión lti_version=LTI-1p0**
https://www.imsglobal.org/specs/ltiv1p0/implementation-guide



Consumer key: this-is-the-consumer-key
Shared secret: this-is-the-shared-secret


Flujo:
- Se recibe una petición launch enviada desde el LMS

### Ejemplo petición launch

```sh
POST /launch HTTP/1.1
Host: localhost:5000
Connection: keep-alive
Content-Length: 1125
Cache-Control: max-age=0
sec-ch-ua: "Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "Linux"
Origin: http://localhost:8080
DNT: 1
Upgrade-Insecure-Requests: 1
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Sec-Fetch-Site: same-site
Sec-Fetch-Mode: navigate
Sec-Fetch-Dest: iframe
Referer: http://localhost:8080/
Accept-Encoding: gzip, deflate, br, zstd
Accept-Language: es-ES,es;q=0.9,en-GB;q=0.8,en;q=0.7,ca;q=0.6
Cookie: MoodleSession=hlvjhb76or4ufr0fesogvt3mjh; MOODLEID1_=%25A5W%25CAU

oauth_version=1.0&oauth_nonce=c25315a36c2c59ad8ca68a4b17a8b133&oauth_timestamp=1718020826&oauth_consumer_key=this-is-the-consumer-key&user_id=2&lis_person_sourcedid=&roles=Instructor%2Curn%3Alti%3Asysrole%3Aims%2Flis%2FAdministrator%2Curn%3Alti%3Ainstrole%3Aims%2Flis%2FAdministrator&context_id=2&context_label=curso-pruebas-1&context_title=Curso+pruebas+1&lti_message_type=basic-lti-launch-request&resource_link_title=App+docker+test+1&resource_link_description=&resource_link_id=1&context_type=CourseSection&lis_course_section_sourcedid=&launch_presentation_locale=en&ext_lms=moodle-2&tool_consumer_info_product_family_code=moodle&tool_consumer_info_version=2024042201&oauth_callback=about%3Ablank&lti_version=LTI-1p0&tool_consumer_instance_guid=localhost&tool_consumer_instance_name=New+Site&tool_consumer_instance_description=New+Site&launch_presentation_document_target=iframe&launch_presentation_return_url=http%3A%2F%2Flocalhost%3A8080%2Fmod%2Flti%2Freturn.php%3Fcourse%3D2%26launch_container%3D3%26instanceid%3D1%26sesskey%3DlUGKINVHi2&oauth_signature_method=HMAC-SHA1&oauth_signature=T%2FlTuvk11WE2pm4peWwbQWbg6HA%3D
```
Parameters:
**Se le pueden pasar más parámetros**, tiene un campo en moodle donde le puedes pasar pares variable/valor, uno por línea
```sh
lti_version=LTI-1p0

oauth_consumer_key=this-is-the-consumer-key
oauth_signature_method=HMAC-SHA1
oauth_timestamp=1718020826
oauth_nonce=c25315a36c2c59ad8ca68a4b17a8b133
oauth_callback=about%3Ablank
oauth_signature=T%2FlTuvk11WE2pm4peWwbQWbg6HA%3D
oauth_version=1.0

user_id=2
lis_person_sourcedid=
roles=Instructor%2Curn%3Alti%3Asysrole%3Aims%2Flis%2FAdministrator%2Curn%3Alti%3Ainstrole%3Aims%2Flis%2FAdministrator
context_id=2
context_label=curso-pruebas-1
context_title=Curso+pruebas+1
lti_message_type=basic-lti-launch-request
resource_link_title=App+docker+test+1
resource_link_description=
resource_link_id=1
context_type=CourseSection
lis_course_section_sourcedid=
launch_presentation_locale=en
ext_lms=moodle-2
tool_consumer_info_product_family_code=moodle
tool_consumer_info_version=2024042201
tool_consumer_instance_guid=localhost
tool_consumer_instance_name=New+Site
tool_consumer_instance_description=New+Site

# OJO, se le pueden pasar custom params desde moodle:
custom_custom_param_1=value_param_1
custom_custom_param_2=value_param_2

launch_presentation_document_target=iframe
launch_presentation_return_url=http%3A%2F%2Flocalhost%3A8080%2Fmod%2Flti%2Freturn.php%3Fcourse%3D2%26launch_container%3D3%26instanceid%3D1%26sesskey%3DlUGKINVHi2
```






----------------------------------------------------------------------------

Requests, vídeo 3:

1) Del navegador a la plataforma
init login, del browser al LMS: (a una de las valid redirect URI?)
    iss: origen
    login_hint: ¿?
    target_link_uri: a dónde se quiere conectar

2) Del navegador a learning tool:
¿algo de oidc?
authentication request
    client_id: (el de moodle)
    redirect_uri: ¿donde tiene que enviar la respuesta de autentificación? https://tool/lti
    login_hint: ¿?
    nonce: para evitar cross forgery

3) Del navegador al LMS
    Redirige la respuesta del learning tool?

4) Del LMS al navegador, con el id_token

5) Del navegador al learning tool, con el id token
    Se valida signatura, expiración, xsrf, etc.

6) Del learning tool al navegador, con el contenido


Parece que está fallando en la petición 3, al llamar a lti auth
http://localhost:8080/mod/lti/auth.php?scope=openid&response_type=id_token&response_mode=form_post&prompt=none&client_id=35BKAOcTCin0Nvd&redirect_uri=http%3A%2F%2Flocalhost%3A5000%2Flaunch%2F&state=state-46181b9c-78e8-48f4-b63c-92b10622e16e&nonce=e7bc71424ab046988e40f675f91fe508b05875cc289611efa67bb30cb08535e9&login_hint=2&lti_message_hint=%7B%22cmid%22%3A2%2C%22launchid%22%3A%22ltilaunch1_1111759003%22%7D

He habilitado, en Plugins del site administration:
- Manage authentication / Available authentication plugins / LTI
No ha funcionado, en algún post he visto que no está para eso

https://moodle.org/mod/forum/discuss.php?d=455240



## Contents of JWT token

It seems it goes in the /launch request

https://dinochiesa.github.io/jwt/

#### Header


```json
{
  "typ": "JWT",
  "alg": "RS256",
  "kid": "cefa8577367453582242"
}
```

#### Payload

```json
{
  "nonce": "2c113b24fa1e4813849c046ed4a1200d02b639b42c8211ef81d00242ac14000a",
  "iat": 1718612237,
  "exp": 1718612297,
  "iss": "http://moodle.lti",
  "aud": "omwFNMbTxqqMpAP",
  "https://purl.imsglobal.org/spec/lti/claim/deployment_id": "1",
  "https://purl.imsglobal.org/spec/lti/claim/target_link_uri": "http://app.lti:5000/launch",
  "sub": "2",
  "https://purl.imsglobal.org/spec/lti/claim/lis": {
    "person_sourcedid": "",
    "course_section_sourcedid": ""
  },
  "https://purl.imsglobal.org/spec/lti/claim/roles": [
    "http://purl.imsglobal.org/vocab/lis/v2/institution/person#Administrator",
    "http://purl.imsglobal.org/vocab/lis/v2/membership#Instructor",
    "http://purl.imsglobal.org/vocab/lis/v2/system/person#Administrator"
  ],
  "https://purl.imsglobal.org/spec/lti/claim/context": {
    "id": "2",
    "label": "curso1",
    "title": "Curso 1",
    "type": [
      "CourseSection"
    ]
  },
  "https://purl.imsglobal.org/spec/lti/claim/resource_link": {
    "title": "Prueba lti 1",
    "description": "",
    "id": "1"
  },
  "https://purl.imsglobal.org/spec/lti-bo/claim/basicoutcome": {
    "lis_result_sourcedid": "{\"data\":{\"instanceid\":\"1\",\"userid\":\"2\",\"typeid\":\"1\",\"launchid\":369587315},\"hash\":\"a6ce32b2c3f7529a625af91668985b71f7a7930733c9917f8c7b2bcf09efb144\"}",
    "lis_outcome_service_url": "http://moodle.lti/mod/lti/service.php"
  },
  "given_name": "Admin",
  "family_name": "User",
  "name": "Admin User",
  "https://purl.imsglobal.org/spec/lti/claim/ext": {
    "user_username": "admin",
    "lms": "moodle-2"
  },
  "email": "spam1@gammu.com",
  "https://purl.imsglobal.org/spec/lti/claim/launch_presentation": {
    "locale": "en",
    "document_target": "iframe",
    "return_url": "http://moodle.lti/mod/lti/return.php?course=2&launch_container=3&instanceid=1&sesskey=ZCkLzHxehT"
  },
  "https://purl.imsglobal.org/spec/lti/claim/tool_platform": {
    "product_family_code": "moodle",
    "version": "2021051718",
    "guid": "moodle.lti",
    "name": "cursodepruebas",
    "description": "Curso de pruebas"
  },
  "https://purl.imsglobal.org/spec/lti/claim/version": "1.3.0",
  "https://purl.imsglobal.org/spec/lti/claim/message_type": "LtiResourceLinkRequest"
}
```

### Grades and lineitems

https://docs.moodle.org/dev/LTI_Gradebook_Services

