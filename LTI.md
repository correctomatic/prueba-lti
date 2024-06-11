### LTI

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

