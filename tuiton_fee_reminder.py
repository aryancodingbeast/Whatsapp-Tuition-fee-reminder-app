import pywhatkit as kit
import os
import schedule
import time
import csv
from datetime import datetime
print("Welcome to Tuition reminder. This is made by Aryan Singh, Please support my work")


students_file = 'students.csv'
notified_students_file = 'notified_students.txt'

def load_students():
    students = {}
    if os.path.exists(students_file):
        with open(students_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                students[row['Name']] = {'Number': row['Number'], 'Fees': row['Fees']}
    return students

def save_students(students):
    with open(students_file, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['Name', 'Number', 'Fees'])
        writer.writeheader()
        for name, info in students.items():
            writer.writerow({'Name': name, 'Number': info['Number'], 'Fees': info['Fees']})

def send_whatsapp_message(student_name, student_info):
    message_body = f"Dear {student_name}, this is a reminder that your tuition fees of {student_info['Fees']} are due. Please make the payment at your earliest convenience."
    
    
    kit.sendwhatmsg_instantly(f"+{student_info['Number']}", message_body)
    
    print(f"Message sent to {student_name} at {student_info['Number']}")

def has_been_notified(student_name):
    
    if os.path.exists(notified_students_file):
        with open(notified_students_file, 'r') as file:
            notified_students = file.read().splitlines()
            return student_name in notified_students
    return False

def mark_as_notified(student_name):
    
    with open(notified_students_file, 'a') as file:
        file.write(f"{student_name}\n")

def notify_students(students):
    for student_name, student_info in students.items():
        if has_been_notified(student_name):
            print(f"{student_name} has already been notified.")
        else:
            send_whatsapp_message(student_name, student_info)
            mark_as_notified(student_name)

def check_and_notify(students):
    today = datetime.now().day
    if today == 11:
        notify_students(students)

def delete_notified_file():
    today = datetime.now().day
    if today == 8 and os.path.exists(notified_students_file):
        os.remove(notified_students_file)
        print("Notified students file deleted.")

def schedule_reminders(students):
    
    schedule.every().day.at("17:05").do(check_and_notify, students)
    
    
    schedule.every().day.at("00:00").do(delete_notified_file)

    while True:
        schedule.run_pending()
        time.sleep(1)

def add_new_students(students):
    num_students = int(input("Enter the number of students to add: "))
    
    for _ in range(num_students):
        student_name = input("Enter the student's name: ")
        student_number = input("Enter the student's WhatsApp number (with country code): ")
        student_fees = input("Enter the student's fees: ")
        students[student_name] = {'Number': student_number, 'Fees': student_fees}

    save_students(students)

if __name__ == "__main__":
    students = load_students()
    
    add_new = input("Do you want to add new students? (yes/no): ").strip().lower()
    if add_new == 'yes':
        add_new_students(students)
    
    schedule_reminders(students)
