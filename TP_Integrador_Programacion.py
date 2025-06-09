import time
import csv
import matplotlib.pyplot as plt

with open('fake_emails_10000.csv', mode='r') as file:
    reader = csv.DictReader(file)
    emails = list(reader)

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
    bubble_emails = bubble_sort(emails)
    
    end_bubble = time.time()
    bubble_duration = end_bubble - start_bubble

    # Time bucket Sort
    start_bucket = time.perf_counter()
    bucket_emails = bucket_sort(emails)

    end_bucket = time.perf_counter()
    bucket_duration = end_bucket - start_bucket

    print("El tiempo de ordenamiento del bubble sort: " ,bubble_duration)
    print("El tiempo de ordenamiento del bucket sort: " ,bucket_duration)

    # Benchmark
    sizes = list(range(1000, 10001, 1000))
    bubble_times = []
    bucket_times = []

    for size in sizes:
        sample = emails[:size]

        # Time bubble sort
        start = time.perf_counter()
        bubble_sort(sample)
        end = time.perf_counter()
        bubble_times.append(end - start)

        # Time bucket sort
        start = time.perf_counter()
        bucket_sort(sample)
        end = time.perf_counter()
        bucket_times.append(end - start)

    plt.figure(figsize=(10, 6))
    plt.plot(sizes, bubble_times, label="Bubble Sort", marker="o")
    plt.plot(sizes, bucket_times, label="Bucket Sort ", marker="s")
    plt.xlabel("Número de Emails")
    plt.ylabel("Tiempo (segundos)")
    plt.title("Tiempo de ordenamiento vs Número de Emails (Bubble vs Bucket Sort)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()