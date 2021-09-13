# encoding:utf-8

import requests
import base64
import os
import shutil
import time
import random


token = {'refresh_token': '25.f31dfe75b6b14b3cbda624e486e5c7ac.315360000.1946387014.282335-23042292',
         'expires_in': 2592000, 'session_key': '9mzdDoc22gRdNvtR7tVVvZC1rUUIw6YLrXhxmvz3rAz8h8sFjBTgAg9oLJiZk9dq+IapUZH+qALvZ25gppqyhuBxGf1bNg==', 'access_token': '24.559496a436a2110387a7da38643df712.2592000.1633619014.282335-23042292', 'scope': 'brain_form brain_seal brain_ocr_facade brain_ocr_medical_paper brain_ocr_doc_analysis_office brain_ocr_idcard brain_vat_invoice_verification brain_vehicle_registration_certificate brain_ocr_mixed_multi_vehicle public vis-ocr_ocr brain_ocr_scope brain_ocr_general brain_ocr_general_basic vis-ocr_business_license brain_ocr_webimage brain_all_scope brain_ocr_driving_license brain_ocr_vehicle_license vis-ocr_plate_number brain_solution brain_ocr_plate_number brain_ocr_accurate brain_ocr_accurate_basic brain_ocr_receipt brain_ocr_business_license brain_solution_iocr brain_qrcode brain_ocr_handwriting brain_ocr_passport brain_ocr_vat_invoice brain_numbers brain_ocr_business_card brain_ocr_train_ticket brain_ocr_taxi_receipt vis-ocr_household_register vis-ocr_vis-classify_birth_certificate vis-ocr_台湾通行证 vis-ocr_港澳通行证 vis-ocr_机动车购车发票识别 vis-ocr_机动车检验合格证识别 vis-ocr_车辆vin码识别 vis-ocr_定额发票识别 vis-ocr_保单识别 vis-ocr_机打发票识别 vis-ocr_行程单识别 brain_ocr_vin brain_ocr_quota_invoice brain_ocr_birth_certificate brain_ocr_household_register brain_ocr_HK_Macau_pass brain_ocr_taiwan_pass brain_ocr_vehicle_invoice brain_ocr_vehicle_certificate brain_ocr_air_ticket brain_ocr_invoice brain_ocr_insurance_doc brain_formula brain_ocr_meter brain_doc_analysis brain_ocr_webimage_loc wise_adapt lebo_resource_base lightservice_public hetu_basic lightcms_map_poi kaidian_kaidian ApsMisTest_Test权限 vis-classify_flower lpq_开放 cop_helloScope ApsMis_fangdi_permission smartapp_snsapi_base smartapp_mapp_dev_manage iop_autocar oauth_tp_app smartapp_smart_game_openapi oauth_sessionkey smartapp_swanid_verify smartapp_opensource_openapi smartapp_opensource_recapi fake_face_detect_开放Scope vis-ocr_虚拟人物助理 idl-video_虚拟人物助理 smartapp_component smartapp_search_plugin avatar_video_test', 'session_secret': 'a9a7844a377ae9b8f2ae70603289e046'}


path = 'D:\\phthon专用\\20210901\\picture\\'
new_path = 'D:\\phthon专用\\20210901\\pdf_new\\'
name = os.listdir(path)
request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/doc_analysis_office"
print(token['access_token'])
tired = 0
# 二进制方式打开图片文件
for i in range(len(name)):
    tired += 1
    if tired > 100:
        break

    print(path+name[i])
    f = open(path + name[i], 'rb')
    img = base64.b64encode(f.read())

    params = {"image": img}

    access_token = '24.da1491fdcd6cfe23ea4b7577b03e296f.2592000.1633624319.282335-23042292'
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    time.sleep(random.random())
    print(name[i], end=' ')
    if response:
        print(response.json())
        with open('doc_office.txt', "a") as ff:
            ff.write(str(name[i]))
            ff.write(" ")
            ff.write(str(response.json()))
            ff.write("\n")
        f.close()
        shutil.move(path + name[i], new_path + name[i])
    response.close()