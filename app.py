from config import auth_key, endpoint
import sys
import time
import requests

base_endpoint = endpoint
headers = {'authorization': auth_key}


# Start the transcription process
def start_transcript(audio_url):
    post_json = {
        "audio_url": audio_url,
        # "speech_model": "nano",
        # "dual_channel": True,
        # "language_code": "fr",
        # "language_detection": True,
        # "punctuate": False,
        # "format_text": False,
        # "speaker_labels": True,
        # "speakers_expected": 2,
        # "word_boost": [
        #     "ben"
        # ],
        # "boost_param": "high",
        # "custom_spelling": [{"from": ["ariana"], "to": "Arianna"}], 
        # "disfluencies": True,
        # "filter_profanity": True,
        # "redact_pii": True,
        # "redact_pii_sub": "entity_name",
        # "redact_pii_policies": [
        #     "medical_process", "medical_condition", "blood_type", "drug", "injury", "number_sequence", "email_address", "date_of_birth", "phone_number", "us_social_security_number", "credit_card_number", "credit_card_expiration", "credit_card_cvv", "date", "nationality", "event", "language", "location", "money_amount", "person_name", "person_age", "organization", "political_affiliation", "occupation", "religion", "drivers_license", "banking_information"
        # ],
        # "redact_pii_audio": "true",
        # "auto_highlights": True,
        # "content_safety": True,
        # "iab_categories": True,
        # "sentiment_analysis": True,
        # "summarization": True,
        # "summary_model": "informative",
        # "summary_type": "bullets",
        # "entity_detection": True,
        # "auto_chapters": True,
        # "speech_threshold": 0.1,
        # "audio_start_from": 862800,
        # "audio_end_at": 1725000
        # "webhook_url": "https://webhook.site/ac5461d1-c8de-4f4a-9662-7eb192ff6734"
    }

    r = requests.post(base_endpoint + '/transcript', headers=headers, json=post_json)

    if 'error' in r.json():
        print(r.json())
        
    return r.json()


# Get the completed transcription
def get_transcript(id):
    r = requests.get(base_endpoint + '/transcript/' + id, headers=headers)
    return r.json()


# Wait for the status of the transcription to be completed
def wait_for_result(id):
    response = get_transcript(id)
    while response['status'] not in ['completed', 'error']:
        time.sleep(5)
        response = get_transcript(response['id'])
    return response


def main(audio_url):
    print('Submitting file: ', audio_url)
    response = start_transcript(audio_url)
    print('transcript id: %s' % response['id'])
    response = wait_for_result(response['id'])

    if response['status'] == 'error':
        print(audio_url, response['error'])
        # raise Exception(response['error'])

    return response
 

if __name__ == '__main__':
    audio_url = sys.argv[1]
    print(audio_url)
    main(audio_url)