from django.shortcuts import render
import requests
import os
import time


WAITING_ROOM_API_URL = os.getenv("WAITING_ROOM_API_URL")
WAITING_ROOM_EVENT_ID = os.getenv("WAITING_ROOM_EVENT_ID")
ISSUER = os.getenv("ISSUER")

def assign_queue_number():     
    response = requests.post(WAITING_ROOM_API_URL + "/assign_queue_num", json={"event_id": WAITING_ROOM_EVENT_ID})
    body = response.json()
    return body["api_request_id"]

def check_current_position(request_id: str):
    event_id = WAITING_ROOM_EVENT_ID
    params = {
        "event_id": event_id,
        "request_id": request_id
    }
    while True:
        response = requests.get(WAITING_ROOM_API_URL + "/queue_num", params=params)
        if response.status_code == 200:
            body = response.json()
            break
        time.sleep(5)  # Wait for 5 seconds before retrying
    queue_number = int(body["queue_number"])
    return queue_number

def check_serving_number():
    body = requests.get(WAITING_ROOM_API_URL + "/serving_num", params={"event_id": WAITING_ROOM_EVENT_ID}).json()
    serving_counter = int(body["serving_counter"])
    return serving_counter

def check_user_eligibility(request_id: str):
    if check_current_position(request_id) <= check_serving_number():
        return True
    else:
        return False
    

def waiting_room(request):
    request_id = assign_queue_number()   
    user_eligible = check_user_eligibility(request_id)
    current_position = check_current_position(request_id)
    total_users = check_serving_number()

    # while user_eligible == False:
    #     current_position = check_current_position(request_id)
    #     total_users = check_serving_number()
    #     user_eligible = check_user_eligibility(request_id)

    #     print(current_position, total_users, user_eligible, request_id)

    #     time.sleep(10)  # Wait for 10 seconds before the next iteration

    #     return render(request, 'waiting.html', {
    #         "leave_queue": user_eligible,
    #         "total_users": total_users,
    #         "current_position": current_position
    #     })

    context = {
        "leave_queue": user_eligible,
        "total_users": total_users,
        "current_position": current_position,
        "leave_queue": user_eligible
    }

    return render(request, 'waiting.html', context)


