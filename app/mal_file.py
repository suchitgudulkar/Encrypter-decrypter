from OTXv2 import OTXv2
import argparse
import IndicatorTypes
import hashlib

# API_KEY = 'b8604201fee2be44a75e20fc88ba089c1d4bd231c3f473a36f8fa0334b1edc56'
API_KEY = '364a0c9c4ccffaf4de039a3bfa44b6e8f2c0c294375b2e5efccd10b7dd213f6a'

OTX_SERVER = 'https://otx.alienvault.com/'
otx = OTXv2(API_KEY, server=OTX_SERVER)

# Get a nested key from a dict, without having to do loads of ifs
def getValue(results, keys):
    if type(keys) is list and len(keys) > 0:
        if type(results) is dict:
            key = keys.pop(0)
            if key in results:
                return getValue(results[key], keys)
            else:
                return None
        else:
            if type(results) is list and len(results) > 0:
                return getValue(results[0], keys)
            else:
                return results
    else:
        return results


def file_(otx, hash):
    alerts = []
    hash_type = IndicatorTypes.FILE_HASH_MD5
    if len(hash) == 64:
        hash_type = IndicatorTypes.FILE_HASH_SHA256
    if len(hash) == 40:
        hash_type = IndicatorTypes.FILE_HASH_SHA1
    result = otx.get_indicator_details_full(hash_type, hash)

    avg = getValue( result, ['analysis','analysis','plugins','avg','results','detection'])
    if avg:
        alerts.append({'avg': avg})

    clamav = getValue( result, ['analysis','analysis','plugins','clamav','results','detection'])
    if clamav:
        alerts.append({'clamav': clamav})

    avast = getValue( result, ['analysis','analysis','plugins','avast','results','detection'])
    if avast:
        alerts.append({'avast': avast})

    microsoft = getValue( result, ['analysis','analysis','plugins','cuckoo','result','virustotal','scans','Microsoft','result'])
    if microsoft:
        alerts.append({'microsoft': microsoft})

    symantec = getValue( result, ['analysis','analysis','plugins','cuckoo','result','virustotal','scans','Symantec','result'])
    if symantec:
        alerts.append({'symantec': symantec})

    kaspersky = getValue( result, ['analysis','analysis','plugins','cuckoo','result','virustotal','scans','Kaspersky','result'])
    if kaspersky:
        alerts.append({'kaspersky': kaspersky})

    suricata = getValue( result, ['analysis','analysis','plugins','cuckoo','result','suricata','rules','name'])
    if suricata and 'trojan' in str(suricata).lower():
        alerts.append({'suricata': suricata})
    return alerts


def isMalicious_file(file1):
    try:
        otxRes = file_(otx, file1)
        print(otxRes)
        if len(otxRes) > 0:
            return True
        else:
            return False
    except Exception as ex:
        print(ex)
        return "Unknown"

# if __name__ == "__main__":
#     hash = hashlib.md5(open("Phishing.docx", 'rb').read()).hexdigest() #/home/dimaa/Downloads/eicar_com.zip
#     res = isMalicious_file(hash)
#     print(res)



### pip3 install OTXv2