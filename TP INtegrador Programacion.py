import time
import csv

with open('fake_emails.csv', mode='r') as file:
    emails = csv.DictReader(file)

def bubble_sort(emails):
    sorted_emails = emails[:]
    n = len(sorted_emails)
    for i in range(n):
        for j in range(0, n - i - 1):
            if sorted_emails[j]["sender"].lower() > sorted_emails[j + 1]["sender"].lower():
                sorted_emails[j], sorted_emails[j + 1] = sorted_emails[j + 1], sorted_emails[j]
    return sorted_emails

def bucket_sort(emails):
    if len(emails) <= 1:
        return emails
    pivot = emails[0]
    less = [x for x in emails[1:] if x["sender"].lower() <= pivot["sender"].lower()]
    greater = [x for x in emails[1:] if x["sender"].lower() > pivot["sender"].lower()]
    return bucket_sort(less) + [pivot] + bucket_sort(greater)

if __name__ == "__main__" : 

# Time Bubble Sort
start_bubble = time.time()
bubble_sort(emails)
end_bubble = time.time()
bubble_duration = end_bubble - start_bubble

# Time bucket Sort
start_bucket = time.time()
bucket_sort(emails)
end_bucket = time.time()
bucket_duration = end_bucket - start_bucket

bubble_duration, bucket_duration
