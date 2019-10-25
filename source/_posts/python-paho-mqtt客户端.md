---
title: python-paho-mqtt客户端
cover_img: 'http://qiniucdn.timilong.com/ChMkJ1bKy16IZPEyAEPR5Y3qI1YAALIqAAAAAAAQ9H9855.jpg'
date: 2019-10-25 12:54:37
tags: Python
feature_img:
description: Python-paho客户端学习指南
keywords: Python
categories: Python
---

![cover_img](http://qiniucdn.timilong.com/ChMkJ1bKy16IZPEyAEPR5Y3qI1YAALIqAAAAAAAQ9H9855.jpg)

> 本文系原创, 转载请联系作者 [Timilong](http://blog.timilong.com/about)

### base.py
```python
# coding: utf-8

import rsa
import time
import ujson
import hashlib
import logging

from timi_uuid import timi_uuid
from Crypto.Cipher import AES

from settings import (
    EMQTT_RSA_PUBLIC_KEY_PEM, EMQTT_RSA_PRIVATE_KEY_PEM,
    KSYUN_ACCESS_KEY, KSYUN_SECRET_KEY, KSYUN_OSS_BUCKET_NAME,
    KSYUN_REGEION_HOST_URL, DEEPGRINT_CALLBACK_URL
)

from sensoro.connection.redis_client import redis_service
from sensoro.common.redis_key import RedisKeyConstants
from sensoro.common.errors import Error
from sensoro.utils.redis_helper import FirmwareReplyDataRedisHelper

from sensoro.utils.types import (
    DeviceBindStatusType, DeviceStatus,
    DeviceNetWorkType, TfCardStateType,
    AlphaStateType
)
from sensoro.utils.sign_vms_stream_url import get_vms_push_url_with_sign

from sensoro.emqtt.publish import PublishToOneDevice
from sensoro.core.dao.device_produce_sys import ProductSysSourceDataDao
from sensoro.core.dao.device_fw_config import DeviceFwConfigDao
from sensoro.core.dao.device import DeviceDao


class BaseMqttHandler(object):

    def __init__(self, sn=None, token=None):
        self.sn = sn
        self.token = token
        self.aes_iv = None
        self.aes_key = None
        self.msg_id = None
        self.aes_decrypt_data = None
        self.protocol_version = None
        self.mqtt_publish = PublishToOneDevice(sn=self.sn, token=self.token)

    @staticmethod
    def generate_string_with_length(length=16):
        assert length in (16, 32), 'The String Length Error, Only support (16, 32)'
        _string = timi_uuid.get_hex_id()
        return _string[:length]

    @staticmethod
    def generate_message_id():
        msg_id = timi_uuid.get_hex_id()
        return msg_id

    @classmethod
    def str2hex(cls, bytes_string):
        return bytes_string.hex()

    @classmethod
    def hex2str(cls, hex_str):
        return bytes.fromhex(hex_str)

    @staticmethod
    def create_keys():  # 生成公钥和私钥
        (pubkey, privkey) = rsa.newkeys(1024)
        pub = pubkey.save_pkcs1()
        with open('public.pem', 'wb+')as f:
            f.write(pub)

        pri = privkey.save_pkcs1()
        with open('private.pem', 'wb+')as f:
            f.write(pri)

    @classmethod
    def rsa_encrypt(cls, data):  # 用公钥加密
        """ pkcs8()

        :param data:
        :return:
        """
        with open(EMQTT_RSA_PUBLIC_KEY_PEM, 'rb') as public_file:
            p = public_file.read()
        pub_key = rsa.PublicKey.load_pkcs1(p)
        original_text = data.encode('utf8')
        crypt_text = rsa.encrypt(original_text, pub_key)
        return crypt_text

    @classmethod
    def rsa_decrypt(cls, crypt_text):  # 用私钥解密
        """ pkcs1()

        :param crypt_text:
        :return:
        """
        with open(EMQTT_RSA_PRIVATE_KEY_PEM, 'rb') as private_file:
            p = private_file.read()
        priv_key = rsa.PrivateKey.load_pkcs1(p)
        lase_text = rsa.decrypt(crypt_text, priv_key).decode()  # 注意，这里如果结果是bytes类型，就需要进行decode()转化为str
        return lase_text

    @classmethod
    def md5_convert(cls, string):
        """
        计算字符串md5值
        :param string: 输入字符串
        :return: 字符串md5
        """
        m = hashlib.md5()
        m.update(string.encode())
        return m.hexdigest()

    @classmethod
    def sha256_encrypt(cls, data):
        """
        sha256加密
        return:加密结果转成16进制字符串形式，并大写
        """
        _hash = hashlib.sha256()
        _hash.update(data.encode("utf-8"))
        return _hash.hexdigest()

    def aes_encrypt(self, iv, key, data):
        # 密钥（key）, 密斯偏移量（iv） CBC模式加密
        pad = lambda s: s + (16 - len(s) % 16) * chr(16 - len(s) % 16)
        # pad = lambda s: s + (32 - len(s) % 32) * chr(32 - len(s) % 32)
        # 字符串补位
        data = pad(data)

        cipher = AES.new(key.encode('utf8'), AES.MODE_CBC, iv.encode('utf8'))
        cipher.block_size = 16

        # 加密后得到的是bytes类型的数据
        encrypted_bytes = cipher.encrypt(data.encode('utf8'))

        # 加密后转成16进制bytes->hex
        encrypted_hex_str = self.str2hex(bytes_string=encrypted_bytes)
        return encrypted_hex_str

    def aes_decrypt(self, hex_data):
        # 解密前进行16进制转换成hex->bytes
        data = self.hex2str(hex_str=hex_data)

        cipher = AES.new(self.aes_key.encode('utf8'), AES.MODE_CBC, self.aes_iv.encode('utf8'))
        cipher.block_size = 32
        text_decrypted = cipher.decrypt(data)
        un_pad = lambda s: s[0:-s[-1]]
        text_decrypted = un_pad(text_decrypted)
        # 去补位
        text_decrypted = text_decrypted.decode('utf8')
        return text_decrypted

    def do_aes_analysis(self, input_data):
        # 初始化aes_iv, aes_key
        self.set_and_get_aes_config()

        s_data = input_data.get('sData')
        protocol_version = input_data.get('sProtocolVersion')
        self.msg_id = input_data.get('sMsgId', None)
        assert protocol_version, "sProtocolVersion not found"
        assert s_data, "sData not found"

        aes_decrypt_data = self.aes_decrypt(hex_data=s_data)

        logging.info("aes_decrypt: {}, type: {}".format(aes_decrypt_data, type(aes_decrypt_data)))
        self.aes_decrypt_data = ujson.loads(aes_decrypt_data)
        logging.info("self.aes_decrypt_data: {}".format(self.aes_decrypt_data))

        self.protocol_version = protocol_version
        logging.info(msg="protocol_version: {}".format(self.protocol_version))

    def do_rsa_handshake(self, input_data):
        """ iCmdType: 0

        :param input_data:
        :return:
        """
        s_data = input_data.get('sData')
        protocol_version = input_data.get('sProtocolVersion')
        assert protocol_version, "sProtocolVersion not found"
        assert s_data, "sData not found"

        s_data = self.hex2str(hex_str=s_data)

        rsa_decode_data = self.rsa_decrypt(crypt_text=s_data)
        split_rsa_decode_data = rsa_decode_data.split(':')

        aes_key1 = split_rsa_decode_data[0]

        iv1 = split_rsa_decode_data[1]

        md51 = split_rsa_decode_data[2]

        md51_cloud = self.md5_convert(string=aes_key1 + ":" + iv1)
        assert md51 == md51_cloud, "MD5 Error."

        aes_key2 = self.generate_string_with_length(length=32)

        iv2 = self.generate_string_with_length(length=16)

        md52 = self.md5_convert(string=aes_key2 + ":" + iv2)

        c_req_str = aes_key2 + ":" + iv2 + ":" + md52

        d_aes_encrypt_data = self.aes_encrypt(iv=iv1, key=aes_key1, data=c_req_str)

        # 发送给设备
        payload = {
            'iCmdType': 0,
            'sProtocolVersion': protocol_version,
            'sData': d_aes_encrypt_data
        }
        self.publish_message(payload=payload, force_online=False)

        self.aes_iv = iv1
        self.aes_key = aes_key1
        aes_decrypt_data = self.aes_decrypt(hex_data=d_aes_encrypt_data)
        logging.info(msg="aes_decrypt_data: {}".format(aes_decrypt_data))

        f_req_str = aes_key1 + iv1 + aes_key2 + iv2
        sha256_str = self.sha256_encrypt(data=f_req_str)

        iv = sha256_str[:16]
        aes_key = sha256_str[16:48]

        # g. 之后，设备与AMS服务器之间的数据通信均使用最后得到AESKEY和IV进行加密。

        # h. 最后，设备端并拼接字符串AESKEY1+IV1+AESKEY2+IV2，对拼接得到的字符串做SHA256加密，并取前16位作为IV，紧接的32位作为AESKEY；
        redis_service.client.setex(
            name=RedisKeyConstants.mqtt_aes_iv.format(self.sn), time=60 * 60 * 24 * 365, value=iv)
        redis_service.client.setex(
            name=RedisKeyConstants.mqtt_aes_key.format(self.sn), time=60 * 60 * 24 * 365, value=aes_key)

        self.aes_iv = iv
        self.aes_key = aes_key

    def set_and_get_aes_config(self):

        iv = redis_service.client.get(name=RedisKeyConstants.mqtt_aes_iv.format(self.sn))
        key = redis_service.client.get(name=RedisKeyConstants.mqtt_aes_key.format(self.sn))
        if iv and key:
            self.aes_iv = iv.decode()
            self.aes_key = key.decode()

    def publish_message(self, payload, force_online=True):

        logging.info("发送消息云端->固件: payload: {}".format(payload))
        if force_online:
            assert self.get_device_status() == DeviceStatus.ONLINE, Error.CNT_DEVICE_IS_OFFLINE
        self.mqtt_publish.publish_message(ujson.dumps(payload))

    def do_device_config(self, input_data):
        """ iCmdType: 1
        设备主动上传设备信息
        self.aes_decrypt_data: {
            'sDeviceSn': '0505050505050003',
            'sHwVersion': 'V100',
            'sModelName': 'S2111-SEP-W2',
            'sIpAddr': '192.168.1.243',
            'sMacAddr': '8e:79:a1:37:7f:65',
            'sVPNIpAddr': '192.168.1.243',
            'sFwVersion': 'V1.0.0_20190903',
            'sAlphaVer': 'V1.0.0',
            'sAiModelVer': 'V1.0.0',
            'sIEVer': 'V1.0.0',
            'iChnCnt': 3,
            'iAlarmIn': 2,
            'iAlarmOut': 1,
            'iNetMethod': 0,
            'iTFCardState': 6,
            'iTFCardCapacitySize': 33554432,
            'iTFCardUseSize': 33554432
        }


        :return:
        """
        # 1. 解析设备上传设备信息
        self.do_aes_analysis(input_data=input_data)

        # 2. 拿解析的数据去做业务
        try:
            logging.info(msg="开始更新数据库...的设备配置信息")
            assert self.aes_decrypt_data['sDeviceSn'] == self.sn, Error.CNT_DEVICE_NOT_EXIST
            DeviceFwConfigDao.get_or_create(config={
                "sn": self.sn,
                "hwVersion": self.aes_decrypt_data["sHwVersion"],
                "modelName": self.aes_decrypt_data["sModelName"],
                "vpnIp": self.aes_decrypt_data["sVPNIpAddr"],
                "ip": self.aes_decrypt_data['sIpAddr'],
                "mac": self.aes_decrypt_data['sMacAddr'],
                "fwVersion": self.aes_decrypt_data['sFwVersion'],
                "alphaVersion": self.aes_decrypt_data["sAlphaVer"],
                "alphaStatus": AlphaStateType.NORMAL,  # 阿尔法基站状态
                "aiVersion": self.aes_decrypt_data['sAiModelVer'],
                "wifiSSID": self.aes_decrypt_data.get('sSSID', ''),
                "wifiStrength": self.aes_decrypt_data.get('iWifiStrength', 0),
                "ieVersion": self.aes_decrypt_data['sIEVer'],
                "chnCount": self.aes_decrypt_data['iChnCnt'],
                "alarmIn": self.aes_decrypt_data['iAlarmIn'],
                "alarmOut": self.aes_decrypt_data['iAlarmOut'],
                "netMethod": DeviceNetWorkType(int(self.aes_decrypt_data.get('iNetMethod', 0))),  # 网络格式
                "sdStatus": TfCardStateType(int(self.aes_decrypt_data.get('iTFCardState', 2))),  # SD卡状态
                "sdCnt": float(self.aes_decrypt_data.get('iTFCardCapacitySize', 0.0) / 100.0),
                "sdTotal": float(self.aes_decrypt_data.get("iTFCardUseSize", 0.0) / 100.0)
            })

            logging.info(msg="更新设备配置信息成功...")

            # 设备配置后，更新设备的状态未在线
            self.get_or_set_device_status_in_redis()

        except Exception as e:
            logging.info(msg="新建或者更新设备配置出错: {}".format(e))

        # 3. 响应设备
        produce_device = ProductSysSourceDataDao.get_object_by_no_session(sn=self.sn)
        # 设备上传配置后，下发一次设备名称(为了防止设备绑定、设备名称更新中，固件没有响应设备名称的update, 增加额外的名称下发机会)
        if produce_device.bindStatus == DeviceBindStatusType.BINDED:
            user_device = DeviceDao.get_device_by_sn(sn=produce_device.sn)
            if user_device:
                self.do_issue_device_name(device_name=user_device.name)

        # 下发设备绑定状态
        cmd = {"iGetconfig": 1, "iBindStatus": 1 if produce_device.bindStatus == DeviceBindStatusType.BINDED else 0}

        logging.info("cmd: {}".format(cmd))
        aes_encrypt_data_hex = self.aes_encrypt(iv=self.aes_iv, key=self.aes_key, data=ujson.dumps(cmd))
        logging.info("aes_encrypt_data_hex: {}".format(aes_encrypt_data_hex))
        payload = {
            "iCmdType": 3,
            "sMsgId": self.generate_message_id(),
            "iAppCmdType": 301,
            "sProtocolVersion": self.protocol_version,
            "sData": aes_encrypt_data_hex
        }
        self.publish_message(payload=payload)

    def do_heartbeat(self, input_data):
        """ iCmdType: 2
        心跳响应

        :return:
        """
        # 1. 解析心跳
        logging.info(msg="收到心跳了...")
        logging.info(msg="分析心跳...")
        self.do_aes_analysis(input_data=input_data)
        logging.info(msg="分析完毕...")

        # 2. 拿到解析的数据去做处理

        # 3. 响应心跳
        cmd = {'iOnline': 1}  # TODO: 这里看协议文档，去拿设备的在线状态
        logging.info("cmd: {}".format(cmd))

        aes_encrypt_data_hex = self.aes_encrypt(iv=self.aes_iv, key=self.aes_key, data=ujson.dumps(cmd))
        logging.info(msg="开始设置redis缓存...")

        # 收到心跳后，更新设备的状态未在线
        self.get_or_set_device_status_in_redis()

        payload = {
            "iCmdType": 2,
            "sProtocolVersion": self.protocol_version,
            "sData": aes_encrypt_data_hex
        }
        self.publish_message(payload=payload)

    def get_or_set_device_status_in_redis(self):
        redis_key = RedisKeyConstants.mqtt_online.format(self.sn)
        old_redis_data = redis_service.client.get(redis_key)
        try:
            if old_redis_data:
                # 99%的心跳会走这里
                logging.info(msg="redis有缓存设备{} 的状态: {}".format(self.sn, old_redis_data.decode()))
                redis_data = old_redis_data.decode()
                if redis_data == "DeviceStatus.OFFLINE":
                    # 如果原来状态是离线，但是现在收到心跳包了，则需要更新设备的状态未在线
                    DeviceDao.update_device_status_with_online(sn=self.sn)
            else:
                logging.info(msg="redis没有缓存设备{}的状态, 开始更新数据库状态为在线，并设置redis缓存".format(self.sn))
                # 当且仅当redis中关于设备状态的key过期时，收到设备心跳包后，会走一次更新数据库设备状态
                DeviceDao.update_device_status_with_online(sn=self.sn)
        except Exception as err:
            logging.error(msg="心跳更新设备状态出错: {}".format(err))

        redis_service.client.setex(name=redis_key, time=90, value=DeviceStatus.ONLINE)
        logging.info(msg="redis缓存设置完毕...")

    def get_device_status(self):
        redis_key = RedisKeyConstants.mqtt_online.format(self.sn)
        cnt_redis_data = redis_service.client.get(redis_key)

        # logging.info(msg="redis是否缓存设备: {} 心跳: {}".format(self.sn, cnt_redis_data))
        if not cnt_redis_data:
            return DeviceStatus.OFFLINE

        cnt_status = cnt_redis_data.decode()
        if cnt_status == "DeviceStatus.ONLINE":
            # logging.info(msg="设备的状态: {}, type: {}".format(cnt_status, type(cnt_status)))
            return DeviceStatus.ONLINE
        return DeviceStatus.OFFLINE

    def do_firmware_upload_data(self, input_data):
        """ iCmdType: 6
        固件主动上报数据(云端要求下发，需要监控msgid)

        :return:
        """
        # 1. 解析设备按要求上报的数据
        self.do_aes_analysis(input_data=input_data)

        # 2. 根据解析出来的数据去做业务
        assert self.msg_id, "设备按要求上传的数据中，没有msg_id"
        # 3. 将当前回复的消息，存进redis的阻塞队列中
        FirmwareReplyDataRedisHelper.reply_user_cmd_by_firmware(
            sn=self.sn, msg_id=self.msg_id, s_data=self.aes_decrypt_data)

    def do_issue_vms_stream_url(self, input_data):
        logging.info(msg="开始下发流媒体加密后的url...")
        self.do_aes_analysis(input_data=input_data)
        self.set_and_get_aes_config()

        i_index_time = self.aes_decrypt_data.get('iGetVMSURL')
        i_expire_time = self.aes_decrypt_data.get('iExpiresTime')  # 固件协议中写的是当前时间戳 + 有效期， 单位s
        default_expire_time = time.time() * 1000 + 2 * 60 * 1000  # 默认有效期为2分钟
        expire_time = float(i_expire_time) * 1000 if i_expire_time else default_expire_time  # 单位ms

        logging.info(msg="i_index_time: {}".format(i_index_time))
        assert self.sn, Error.CNT_DEVICE_NOT_EXIST

        user_device = DeviceDao.get_device_by_sn(sn=self.sn)
        logging.info(msg="当前设备: {}".format(user_device))
        if user_device:
            # TODO: 设备未被用户绑定之前，禁止下发推流地址
            base_stream_url = '',  # "rtmp://{}/live/{}".format(VMS_STREAM_BASE_URL, self.sn)
            stream_url = user_device.stream_url if user_device else base_stream_url
            logging.info(msg="开始下发...")
            cmd = {
                'isForBidden': 0,
                'pushurl': get_vms_push_url_with_sign(
                    sn=self.sn, token=self.token, stream_url=stream_url, expire_time=expire_time),
                'index': i_index_time,
                'iExpiresTime': expire_time / 1000.0,  # 单位转成s, 固件端只需要s
                'protocol': 'rtmp'  # 当前仅支持rtmp, 以后可能支持rtsp
            }
            logging.info(msg='sData: {}'.format(cmd))
            aes_encrypt_data_hex = self.aes_encrypt(iv=self.aes_iv, key=self.aes_key, data=ujson.dumps(cmd))

            payload = {
                "iCmdType": 7,
                "sMsgId": self.generate_message_id(),
                "iAmsCmdType": 702,
                "sProtocolVersion": self.protocol_version,
                "sData": aes_encrypt_data_hex
            }
            self.publish_message(payload=payload)
        else:
            # self.do_issue_vms_stream_control_cmd(cmd_type=1)
            # 设备未绑定，停止回复
            logging.info(msg="设备未绑定，停止下发...")

    def do_issue_pic_upload_param(self, input_data):
        """ 下发金山云对象存储配置

        :param input_data:
        :return:
        """
        logging.info(msg="开始下发FTP-金山云图片上传的配置...")
        self.do_aes_analysis(input_data=input_data)
        self.set_and_get_aes_config()

        i_index_time = self.aes_decrypt_data.get('iGetPicUploadPara')
        logging.info(msg="i_index_time: {}".format(i_index_time))

        # TODO: 设备未被用户绑定之前，禁止下发推流地址
        logging.info(msg="开始下发...")
        cmd = {
            "isForBidden": 0,
            "uploadmethod": "http",
            "ftp": {
                "ftpurl": "",
                "ftpport": "",
                "ftpuser": "",
                "ftppassword": "",
                "ftppath": ""
            },
            "http": {
                "hosturl": KSYUN_REGEION_HOST_URL,
                "access_key": KSYUN_ACCESS_KEY,
                "secret_key": KSYUN_SECRET_KEY,
                "bucket_name": KSYUN_OSS_BUCKET_NAME,
                "object_path": "ai_engine_imgs",
                "callbackurl": DEEPGRINT_CALLBACK_URL
            },
            "index": i_index_time
        }
        logging.info(msg='sData: {}'.format(cmd))
        aes_encrypt_data_hex = self.aes_encrypt(iv=self.aes_iv, key=self.aes_key, data=ujson.dumps(cmd))

        payload = {
            "iCmdType": 7,
            "sMsgId": self.generate_message_id(),
            "iAmsCmdType": 703,
            "sProtocolVersion": self.protocol_version,
            "sData": aes_encrypt_data_hex
        }
        self.publish_message(payload=payload)

    def do_issue_vms_stream_control_cmd(self, cmd_type=None):
        """ 下发vms流媒体推流控制命令
        {
           icmdtype: 0 / 1 / 2  # 0停止，1开始，2，使用新的推流地址重新开始
        }
        :param cmd_type:
        :return:
        """
        # 所有下发命令必须先获得加密数据用的iv, key
        self.set_and_get_aes_config()

        logging.info(msg="客户端调用控制固件是否推流的命令了...cmdType: 704")
        assert cmd_type in (0, 1, 2)
        cmd = {
            "icmdtype": int(cmd_type),
        }
        logging.info(msg='sData: {}'.format(cmd))
        aes_encrypt_data_hex = self.aes_encrypt(iv=self.aes_iv, key=self.aes_key, data=ujson.dumps(cmd))

        payload = {
            "iCmdType": 7,
            "sMsgId": self.generate_message_id(),
            "iAmsCmdType": 704,
            "sProtocolVersion": self.protocol_version,
            "sData": aes_encrypt_data_hex
        }
        self.publish_message(payload=payload)
        logging.info(msg="下发推流控制命令: {}到设备{}成功".format(cmd, self.sn))

    def do_issue_vms_ftp_control_cmd(self, cmd_type=None):
        """ 下发金山云对象存储控制命令
        {
           icmdtype: 0 / 1  # 0停止，1开始
        }

        :param cmd_type:
        :return:
        """
        # 所有下发命令必须先获得加密数据用的iv, key
        self.set_and_get_aes_config()

        logging.info(msg="客户端调用控制固件是否推图片流的命令了...cmdType: 705")
        assert cmd_type in (0, 1)
        cmd = {
            "icmdtype": int(cmd_type),
        }
        logging.info(msg='sData: {}'.format(cmd))
        aes_encrypt_data_hex = self.aes_encrypt(iv=self.aes_iv, key=self.aes_key, data=ujson.dumps(cmd))

        payload = {
            "iCmdType": 7,
            "sMsgId": self.generate_message_id(),
            "iAmsCmdType": 705,
            "sProtocolVersion": self.protocol_version,
            "sData": aes_encrypt_data_hex
        }
        self.publish_message(payload=payload)
        logging.info(msg="下发推图片流控制命令: {}到设备{}成功".format(cmd, self.sn))

    def do_issue_reboot_cmd(self, cmd_type=1):
        """ 下发设备重启命令
        iReboot: 1
        :param cmd_type:
        :return:
        """
        self.set_and_get_aes_config()
        assert cmd_type == 1, Error.REQUEST_PARAMETER_IS_INVALID

        msg_id = self.generate_message_id()

        cmd = {"iReboot": cmd_type}
        aes_encrypt_data_hex = self.aes_encrypt(iv=self.aes_iv, key=self.aes_key, data=ujson.dumps(cmd))

        payload = {
            "iCmdType": 3,
            "sProtocolVersion": self.protocol_version,
            "sMsgId": msg_id,
            "iAppCmdType": 313,
            "sData": aes_encrypt_data_hex
        }
        self.publish_message(payload=payload)
        return msg_id

    def do_issue_reset_cmd(self, cmd_type):
        """ 下发重置命令
            # 1-> 恢复出厂设置(恢复所有，配置，sd卡，模型)   0->恢复默认, 恢复默认设置
            # 恢复出厂设置: 1
            # 恢复默认设置: 0
            # 视音频恢复默认值: 331
            # OSD恢复默认值: 333
            # 人脸抓拍设置恢复默认值: 328
            # 车辆抓拍恢复默认值: 329
            # 设备配置恢复默认值:  330

        :param cmd_type:
        :return:
        """
        self.set_and_get_aes_config()
        assert cmd_type in (0, 1, 328, 329, 330, 331, 333), Error.REQUEST_PARAMETER_IS_INVALID

        msg_id = self.generate_message_id()

        cmd = {"iReset": cmd_type}
        aes_encrypt_data_hex = self.aes_encrypt(iv=self.aes_iv, key=self.aes_key, data=ujson.dumps(cmd))
        payload = {
            "iCmdType": 3,
            "sProtocolVersion": self.protocol_version,
            "sMsgId": msg_id,
            "iAppCmdType": 314,
            "sData": aes_encrypt_data_hex
        }
        self.publish_message(payload=payload)
        return msg_id

    def do_issue_log_upload_cmd(self, cmd_type=1):
        """ 下发日志上传命令

        :param cmd_type:
        :return:
        """
        self.set_and_get_aes_config()
        log_body = {
            "iReqUploadZlog": cmd_type
        }
        assert isinstance(log_body, dict), Error.REQUEST_PARAMETER_IS_INVALID

        msg_id = self.generate_message_id()

        aes_encrypt_data_hex = self.aes_encrypt(iv=self.aes_iv, key=self.aes_key, data=ujson.dumps(log_body))

        payload = {
            "iCmdType": 3,
            "sProtocolVersion": self.protocol_version,
            "sMsgId": msg_id,
            "iAppCmdType": 317,
            "sData": aes_encrypt_data_hex
        }
        self.publish_message(payload=payload)
        return msg_id

    def do_issue_reset_sd_card_cmd(self, cmd_type=1):
        """ 下发格式化sd卡命令

        :param cmd_type:
        :return:
        """
        self.set_and_get_aes_config()
        assert cmd_type == 1, Error.REQUEST_PARAMETER_IS_INVALID

        msg_id = self.generate_message_id()

        cmd = {"iFormat": cmd_type}
        aes_encrypt_data_hex = self.aes_encrypt(iv=self.aes_iv, key=self.aes_key, data=ujson.dumps(cmd))

        payload = {
            "iCmdType": 3,
            "sProtocolVersion": self.protocol_version,
            "sMsgId": msg_id,
            "iAppCmdType": 318,
            "sData": aes_encrypt_data_hex
        }
        self.publish_message(payload=payload)
        return msg_id

    def do_issue_device_name(self, device_name="李小龙测试"):
        """ 下发设备名称

        :param device_name:
        :return:
        """
        self.set_and_get_aes_config()

        cmd = {
            'sOsdName': {  # 通道名称控制
                "iEnable": 1,
                "strText": device_name  # 通道名称
            },
        }
        logging.info("cmd: {}".format(cmd))
        aes_encrypt_data_hex = self.aes_encrypt(iv=self.aes_iv, key=self.aes_key, data=ujson.dumps(cmd))
        msg_id = self.generate_message_id()

        logging.info("aes_encrypt_data_hex: {}".format(aes_encrypt_data_hex))
        payload = {
            "iCmdType": 3,
            "sMsgId": msg_id,
            "iAppCmdType": 333,
            "sProtocolVersion": self.protocol_version,
            "sData": aes_encrypt_data_hex
        }
        self.publish_message(payload=payload)
        return msg_id

    def do_issue_snapshot_face_cmd(self, snapshot_body):
        """ 下发人脸抓拍设置

        :param snapshot_body:
        :return:
        """
        self.set_and_get_aes_config()
        assert isinstance(snapshot_body, dict), Error.REQUEST_PARAMETER_IS_INVALID

        msg_id = self.generate_message_id()

        aes_encrypt_data_hex = self.aes_encrypt(iv=self.aes_iv, key=self.aes_key, data=ujson.dumps(snapshot_body))

        payload = {
            "iCmdType": 3,
            "sProtocolVersion": self.protocol_version,
            "sMsgId": msg_id,
            "iAppCmdType": 328,
            "sData": aes_encrypt_data_hex
        }
        self.publish_message(payload=payload)
        return msg_id

    def do_issue_snapshot_car_cmd(self, snapshot_body):
        """ 下发车辆抓拍设置

        :param snapshot_body:
        :return:
        """
        self.set_and_get_aes_config()
        assert isinstance(snapshot_body, dict), Error.REQUEST_PARAMETER_IS_INVALID

        msg_id = self.generate_message_id()

        aes_encrypt_data_hex = self.aes_encrypt(iv=self.aes_iv, key=self.aes_key, data=ujson.dumps(snapshot_body))

        payload = {
            "iCmdType": 3,
            "sProtocolVersion": self.protocol_version,
            "sMsgId": msg_id,
            "iAppCmdType": 329,
            "sData": aes_encrypt_data_hex
        }
        self.publish_message(payload=payload)
        return msg_id

    def do_issue_device_other_settings_cmd(self, settings_body):
        """时区，报警灯，警笛设置

        :return:
        """
        self.set_and_get_aes_config()
        assert isinstance(settings_body, dict), Error.REQUEST_PARAMETER_IS_INVALID

        msg_id = self.generate_message_id()

        aes_encrypt_data_hex = self.aes_encrypt(iv=self.aes_iv, key=self.aes_key, data=ujson.dumps(settings_body))

        payload = {
            "iCmdType": 3,
            "sProtocolVersion": self.protocol_version,
            "sMsgId": msg_id,
            "iAppCmdType": 330,
            "sData": aes_encrypt_data_hex
        }
        self.publish_message(payload=payload)
        return msg_id

    def do_issue_audio_and_video_cmd(self, config_body):
        """下发音视频设置

        :return:
        """
        self.set_and_get_aes_config()
        assert isinstance(config_body, dict), Error.REQUEST_PARAMETER_IS_INVALID

        msg_id = self.generate_message_id()

        aes_encrypt_data_hex = self.aes_encrypt(iv=self.aes_iv, key=self.aes_key, data=ujson.dumps(config_body))

        payload = {
            "iCmdType": 3,
            "sProtocolVersion": self.protocol_version,
            "sMsgId": msg_id,
            "iAppCmdType": 331,
            "sData": aes_encrypt_data_hex
        }
        self.publish_message(payload=payload)
        return msg_id

    def do_issue_get_sd_card_info_cmd(self, cmd_type=1):
        """ 获取sd卡存储状态

        :param cmd_type:
        :return:
        """
        assert cmd_type == 1, Error.REQUEST_PARAMETER_IS_INVALID
        self.set_and_get_aes_config()

        cmd = {"iGetSDInfo": 1}

        msg_id = self.generate_message_id()

        aes_encrypt_data_hex = self.aes_encrypt(iv=self.aes_iv, key=self.aes_key, data=ujson.dumps(cmd))

        payload = {
            "iCmdType": 3,
            "sProtocolVersion": self.protocol_version,
            "sMsgId": msg_id,
            "iAppCmdType": 332,
            "sData": aes_encrypt_data_hex
        }
        self.publish_message(payload=payload)
        return msg_id

    def do_issue_osd_cmd(self, osd_body):
        """ 下发osd名称设置

        :param osd_body:
        :return:
        """
        self.set_and_get_aes_config()
        assert isinstance(osd_body, dict), Error.REQUEST_PARAMETER_IS_INVALID

        msg_id = self.generate_message_id()

        aes_encrypt_data_hex = self.aes_encrypt(iv=self.aes_iv, key=self.aes_key, data=ujson.dumps(osd_body))

        payload = {
            "iCmdType": 3,
            "sProtocolVersion": self.protocol_version,
            "sMsgId": msg_id,
            "iAppCmdType": 333,
            "sData": aes_encrypt_data_hex
        }
        self.publish_message(payload=payload)
        return msg_id


def get_device_status(sn, token):
    return BaseMqttHandler(sn=sn, token=token).get_device_status()

```


### client.py
```python
# coding: utf-8

import json
import logging

from paho.mqtt import client as mqtt

from settings import EMQTT_SERVER_HOST, EMQTT_SERVER_PORT
from sensoro.utils.types import MqttiCmdType

from sensoro.core.dao.device_produce_sys import ProductSysSourceDataDao
from sensoro.emqtt.base import BaseMqttHandler
from sensoro.utils.types import MqttiAmsCmdType


class ListenPubTopic(object):
    def __init__(self, sn='', token=''):
        self.sn = sn
        self.topic = "/ivms/pub/{}".format(sn)  # 监听/ivms/pub/{sn}
        self.token = token
        self.username = sn
        self.password = token
        self.client_loop()

    def client_loop(self):
        client_id = self.sn + "-ivms"
        client = mqtt.Client(client_id=client_id, transport='tcp')
        client.username_pw_set(self.username, self.password)  # 必须设置，否则会返回「Connected with result code 4」
        client.on_connect = self.on_connect
        client.on_message = self.on_message
        client.loop_start()
        client.connect(EMQTT_SERVER_HOST, EMQTT_SERVER_PORT, 60)
        # client.loop_forever()  # 网络循环的阻塞形式，直到客户端调用disconnect（）时才会返回。它会自动处理重新连接。

    def on_connect(self, client, userdata, flags, rc):
        client.subscribe(self.topic)

    def on_message(self, client, userdata, msg):
        message = msg.payload.decode("utf-8")
        # message = str(msg.payload)

        self.analysis_message(message=message)

    def analysis_message(self, message=''):
        """
        :param message:
        :return:
        """
        logging.info(msg="*" * 60 + self.sn + "*" * 60)
        logging.info("message: {}".format(message))
        logging.info("message type: {}".format(type(message)))
        try:
            firmware_post_data = json.loads(message)
            i_cmd_type = firmware_post_data.get('iCmdType')
        except Exception as e:
            logging.error("解析固件上传的数据包错误: {}".format(e))
            return

        try:
            # 目前只用了0 ~ 8
            assert i_cmd_type in (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16), "iCmdType not found"
        except AssertionError as e:
            logging.info("协议的iCmdType错误: {}, e: {}".format(i_cmd_type, e))

        if i_cmd_type == MqttiCmdType.ICMD_HANDSHAKE:
            # iCmdType: 0
            # 设备上网，进行三次握手，换取aes_key, iv进行后续的加密通信, 云端需要redis存储
            logging.info("进行三次握手中...iCmdType: {}".format(i_cmd_type))
            try:
                BaseMqttHandler(sn=self.sn, token=self.token).do_rsa_handshake(input_data=firmware_post_data)
            except Exception as e:
                logging.info("三次握手发生异常: {}".format(e))
            logging.info("三次握手完毕...")

        elif i_cmd_type == MqttiCmdType.ICMD_ONLINE_HANDLE:
            # iCmdType: 1
            # 处理设备联网上线
            logging.info("设备开始上传配置信息...iCmdType: {}".format(i_cmd_type))
            try:
                BaseMqttHandler(sn=self.sn, token=self.token).do_device_config(input_data=firmware_post_data)
            except Exception as e:
                logging.error("处理设备联网上线上传设备配置错误: {}".format(e))
            logging.info("设备上传配置信息完毕...")

        elif i_cmd_type == MqttiCmdType.ICMD_HEARTBEAT:
            # iCmdType: 2
            # 处理设备心跳
            logging.info("设备心跳...iCmdType: {}".format(i_cmd_type))
            try:
                BaseMqttHandler(sn=self.sn, token=self.token).do_heartbeat(input_data=firmware_post_data)
            except Exception as e:
                logging.info("处理设备心跳错误: {}".format(e))
            logging.info("设备心跳响应完毕...")

        elif i_cmd_type == MqttiCmdType.ICMD_RES_HANDLE:
            # iCmdType: 6
            # 固件回复云端下发的某条命令的消息
            logging.info("固件回复上传云端要的数据...iCmdType: {}".format(i_cmd_type))
            try:
                BaseMqttHandler(sn=self.sn, token=self.token).do_firmware_upload_data(input_data=firmware_post_data)
            except Exception as e:
                logging.error("固件回复上传云端要的数据出错: {}".format(e))
            logging.info("固件回复上传云端要得数据完毕...")

        elif i_cmd_type == MqttiCmdType.ICMD_FIRMWARE_SUB_HANDLER:
            # 固件主动上行的业务: iCmdType: 6
            pass

        elif i_cmd_type == MqttiCmdType.ICMD_GET_VMS_SMS_CONFIG:
            # 帮固件获取vms的配置: iCmdType: 7
            logging.info(msg="设备获取vms配置...")
            try:
                i_ams_cmd_type = int(firmware_post_data.get('iAmsCmdType'))
                if i_ams_cmd_type == MqttiAmsCmdType.GET_VMS_STREAM_URL:
                    # 获取vms流媒体url
                    BaseMqttHandler(
                        sn=self.sn, token=self.token).do_issue_vms_stream_url(input_data=firmware_post_data)
                elif i_ams_cmd_type == MqttiAmsCmdType.GET_PIC_UPLOAD_PARAM:
                    # 获取vms的对象存储配置
                    BaseMqttHandler(
                        sn=self.sn, token=self.token).do_issue_pic_upload_param(input_data=firmware_post_data)
                elif i_ams_cmd_type == MqttiAmsCmdType.STREAM_CONTROL_CMD:
                    # 固件回复AMS响应推流控制命令结果
                    pass
                elif i_ams_cmd_type == MqttiAmsCmdType.PIC_CONTROL_CMD:
                    # 固件回复AMS响应图片上传控制命令结果
                    pass
            except Exception as e:
                logging.info(msg="设备获取vms配置错误: {}".format(e))

        elif i_cmd_type == MqttiCmdType.ICMD_FIRMWARE_SUB_HANDLER:
            # 固件主动上行的业务: 设备上传日志成功以后通知AMS
            pass

        logging.info("*" * 136)
        logging.info("\n\n\n")


def start_listen_mqtt_pub_topic():
    count, rows = ProductSysSourceDataDao.get_all_device_count_and_rows()
    logging.info(msg="一共: {}个设备需要监听".format(count))
    logging.info(msg="开始监听所有设备的topic...")
    for row in rows:
        ListenPubTopic(sn=row.sn, token=row.token)
    logging.info(msg="所有设备处于监听中...\n")


def register_sn_into_emqtt_with_listen(sn, token):
    """ 生产系统生成了设备，需要在ivms_ams_api中启动该设备的监听

    :param sn:
    :param token:
    :return:
    """
    ListenPubTopic(sn=sn, token=token)

```

### disconnect_client.py
```python
# coding: utf-8

import json
import logging

from timi_uuid import timi_uuid
from paho.mqtt import client as mqtt

from settings import EMQTT_SERVER_HOST, EMQTT_SERVER_PORT

from sensoro.connection.redis_client import redis_service
from sensoro.common.redis_key import RedisKeyConstants
from sensoro.utils.types import DeviceStatus

from sensoro.core.dao.device import DeviceDao


class ListenSysTopic(object):

    def __init__(self):
        self.topic = "$SYS/brokers/+/clients/+/disconnected"
        self.client_loop()

    def client_loop(self):
        client_id = timi_uuid.get_hex_id()
        client = mqtt.Client(client_id=client_id, transport='tcp')
        client.username_pw_set("sys-disconnected", "sys-disconnected")  # 必须设置，否则会返回「Connected with result code 4」
        client.on_connect = self.on_connect
        client.on_message = self.on_message
        client.loop_start()
        client.connect(EMQTT_SERVER_HOST, EMQTT_SERVER_PORT, 60)
        # client.loop_forever()  # 网络循环的阻塞形式，直到客户端调用disconnect（）时才会返回。它会自动处理重新连接。

    def on_connect(self, client, userdata, flags, rc):
        client.subscribe(self.topic)

    def on_message(self, client, userdata, msg):
        message = msg.payload.decode("utf-8")
        self.analysis_message(message=message)

    def analysis_message(self, message=''):
        """
        :param message:
        :return:
        """

        try:
            sys_data = json.loads(message)
            i_cmd_type = sys_data.get('iCmdType')
            clientid = sys_data.get('clientid')
            username = sys_data.get('username')
            reason = sys_data.get('reason')

            """
            {
                'clientid': '8ed92895de05cf2c273a974c10000313',
                'username': '0505050505050005',
                'reason': 'normal',
                'ts': 1570633399
            }  # 正常的设备断线, 不处理
            """
            """
            {
                'clientid': '02931117C6ED8D30',
                'username': '02931117C6ED8D30',
                'reason': 'keepalive_timeout',  # 需要处理
                'ts': 1570633147
            }
            """

            if not i_cmd_type and username and reason != "normal":
                logging.info("\n\n\n\n\n\n")
                logging.info("*" * 136)
                logging.info("设备{}已disconnect....".format(username))
                logging.info(msg="系统disconnect的数据: {}, reason: {}".format(sys_data, reason))
                # 固件约定sn为mqtt连接的client_id, username。
                redis_key = RedisKeyConstants.mqtt_online.format(username)
                old_redis_data = redis_service.client.get(redis_key)

                if old_redis_data:
                    # 99%的disconnect走这里
                    redis_data = old_redis_data.decode()
                    if redis_data == "DeviceStatus.ONLINE":
                        # 如果原来状态是在线，但是现在收到心跳包了，则需要更新设备的状态未在线
                        DeviceDao.update_device_status_with_offline(sn=username)
                else:
                    # 及少数的disconnect走这里: 设备无心跳？导致当前redis_key超时
                    DeviceDao.update_device_status_with_offline(sn=username)

                # 设置设备断线的缓存
                redis_service.client.setex(
                    name=redis_key,
                    time=60,
                    value=DeviceStatus.OFFLINE
                )

                logging.info(msg="redis缓存设置完毕...")

                logging.info(msg="更新设备{}的在线状态为: 离线 -> 成功.".format(username))

                logging.info("*" * 136)
                logging.info("\n\n\n\n\n\n")

        except Exception as e:
            logging.error("解析固件上传的数据包错误: {}".format(e))


def start_listen_mqtt_sys_disconnect_topic():
    logging.info(msg="开始进行系统监听...")
    ListenSysTopic()
    logging.info(msg="系统监听进行中...")

```

### publish.py
```python
# coding: utf-8

import ujson

from typing import Dict, AnyStr, Any

from paho.mqtt import publish as publish
from timi_uuid import timi_uuid as uuid

from settings import EMQTT_SERVER_HOST, EMQTT_SERVER_PORT


class PublishToOneDevice(object):

    def __init__(self, sn, token):
        self.sn = sn
        self.topic = "/ivms/sub/{}".format(sn)  # 监听/ivms/pub/{sn}
        self.username = sn
        self.password = token

    def publish_message(self, payload: Any):
        """

        :param sn: 当前通信的设备
        :param payload: 当前通信的数据内容
        :param auth: 当前通信的鉴权信息
        :return:
        """

        if not isinstance(payload, str):
            payload = ujson.dumps(payload)

        publish.single(
            topic=self.topic,
            payload=payload,
            qos=1,
            hostname=EMQTT_SERVER_HOST,
            port=EMQTT_SERVER_PORT,
            client_id=uuid.get_hex_id(),
            auth={'username': self.username, 'password': self.password}
        )


class BroadcastMessage(object):

    def __init__(self):
        self.topic = "/ivms/push"  # 监听/ivms/push

    def publish_message(self, payload: Any, auth: Dict):

        if not isinstance(payload, str):
            payload = ujson.dumps(payload)

        publish.single(
            topic=self.topic,
            payload=payload,
            qos=1,
            hostname=EMQTT_SERVER_HOST,
            port=EMQTT_SERVER_PORT,
            client_id=uuid.get_hex_id(),
            auth=auth
        )

```
