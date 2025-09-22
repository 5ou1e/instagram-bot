from src.application.features.working_group.worker.converters.worker_create_dto_to_entities import \
    convert_worker_create_dto_to_entity
from src.application.features.working_group.worker.converters.worker_string_converter import \
    extract_worker_create_dto_from_string

string = "sonal_143269:28xYts6b|Instagram 374.0.0.43.67 Android (35/15; 450dpi; 1080x2340; samsung/samsung; SM-A165F; a16; mt6789; ru_RU; 715888958)|android-dcf4b72e82a08913;6a2fea25-e663-41aa-bf46-3c7236e2d906;6a2fea25-e663-41aa-bf46-3c7236e2d906;6a2fea25-e663-41aa-bf46-3c7236e2d906|mid=aItrAAABAAHxs5SCdJis80cnUq95;rur=CLN,61729802770,1785549167:01fefb66d34ffa8c3857fb1c048aba0afa34342f6714badc160cbbaa24b06f6b4d047b94;sessionid=61729802770%3AOfecTk112tcon7%3A14%3AAYc9paX1bzjTI3dehzr90rgWA-c5mpWtW2b-gIcbmw;ds_user_id=61729802770;Authorization=Bearer IGT:2:eyJkc191c2VyX2lkIjoiNjE3Mjk4MDI3NzAiLCJzZXNzaW9uaWQiOiI2MTcyOTgwMjc3MCUzQU9mZWNUazExMnRjb243JTNBMTQlM0FBWWM5cGFYMWJ6alRJM2RlaHpyOTByZ1dBLWM1bXBXdFcyYi1nSWNibXcifQ==|http://customer-ozan_zone10-sesstime-30-sessid-HXY8tGJH:38KZPLp0@pr.oxylabs.io:7777|rwnzwlla@oonmail.com:rcvwsqpt7047|60|�������"

dto = extract_worker_create_dto_from_string(string)
entities = convert_worker_create_dto_to_entity(dto, "123")

print(dto)
print(entities)