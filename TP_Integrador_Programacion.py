import time
import csv
import matplotlib.pyplot as plt
import tracemalloc

# Selección del caso a analizar
valor = input(
    "Indique qué caso quiere analizar [1 - 5]:\n"
    "1 - Caso Promedio\n"
    "2 - Mejor Caso Bubble Sort\n"
    "3 - Mejor Caso Bucket Sort\n"
    "4 - Peor Caso Bubble Sort\n"
    "5 - Peor Caso Bucket Sort\n"
)

match valor:
    case "1":
        archivo = "Lista_Emails_promedio.csv"
    case "2":
        archivo = "Mejor_Caso_Bubble.csv"
    case "3":
        archivo = "Mejor_Caso_Bucket.csv"
    case "4":
        archivo = "Peor_Caso_Bubble.csv"
    case "5":
        archivo = "Peor_Caso_Bucket.csv"
    case _:
        print("Opción inválida.")
        exit()

# Lectura del archivo CSV
with open(archivo, mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    emails = list(reader)

# Bubble Sort puro
def bubble_sort(emails):
    sorted_emails = emails[:]
    n = len(sorted_emails)
    for i in range(n):
        for j in range(0, n - i - 1):
            if sorted_emails[j]["sender"].lower() > sorted_emails[j + 1]["sender"].lower():
                sorted_emails[j], sorted_emails[j + 1] = sorted_emails[j + 1], sorted_emails[j]
    return sorted_emails

# Bucket Sort puro (tipo Radix) 
def bucket_sort(emails):
    def get_char(email, pos):
        sender = email["sender"].lower()
        return sender[pos] if pos < len(sender) else ' '
    
    max_len = max(len(email["sender"]) for email in emails)

    for pos in reversed(range(max_len)):
        buckets = [[] for _ in range(27)]  # ' ' + 'a'-'z'

        for email in emails:
            ch = get_char(email, pos)
            index = 0 if ch == ' ' else ord(ch) - ord('a') + 1
            if index < 0 or index >= 27:
                index = 0  # cualquier símbolo, número o carácter especial va al bucket 0
            buckets[index].append(email)

        emails = [email for bucket in buckets for email in bucket]

    return emails

# Ejecución principal
if __name__ == "__main__":

    print("Los primeros 100 mails antes de ser ordenados: \n")
    for email in emails[:100]:
        print(email, "\n")

    # Bubble Sort 
    tracemalloc.start()
    start_bubble = time.perf_counter()
    bubble_emails = bubble_sort(emails)
    end_bubble = time.perf_counter()
    bubble_duration = end_bubble - start_bubble
    current_bubble, peak_bubble = tracemalloc.get_traced_memory()
    tracemalloc.stop()#finalizacion de medicion de tamaño en espacio

    # Bucket Sort 
    tracemalloc.start()
    start_bucket = time.perf_counter()
    bucket_emails = bucket_sort(emails)
    end_bucket = time.perf_counter()
    bucket_duration = end_bucket - start_bucket#duracion total del bucket sort
    current_bucket, peak_bucket = tracemalloc.get_traced_memory()
    tracemalloc.stop()#finalizacion de medicion de tamaño en espacio

    print("Tiempo de ejecución Bubble Sort:", bubble_duration)
    print("Tiempo de ejecución Bucket Sort:", bucket_duration)

    # Benchmark gráfico
    sizes = list(range(100, 5000, 100))# tamaño de emails que se pasan por tanda
    bubble_times = []
    bucket_times = []
    result_bubble = []
    result_bucket = []
    for size in sizes:
        sample = emails[:size]

        # Bubble Sort
        start = time.perf_counter()
        bubble_result = bubble_sort(sample)
        end = time.perf_counter()
        bubble_times.append(end - start)
        result_bubble.append(bubble_result)
        
        # Bucket Sort
        start = time.perf_counter()
        bucket_result = bucket_sort(sample)
        end = time.perf_counter()
        bucket_times.append(end - start)
        result_bucket.append(bucket_result)

    #prints del resultado ordenado
    if result_bubble:
        print("Primeros 100 ordenados con Bubble Sort:")
        for email in result_bubble[0][:100]:
            print(email["sender"])

    if result_bucket:
        print("Primeros 100 ordenados con Bucket Sort:")
        for email in result_bucket[0][:100]:
            print(email["sender"])

    #Gráfico de comparación
    plt.figure(figsize=(10, 6))
    plt.plot(sizes, bubble_times, label="Bubble Sort", marker="o")
    plt.plot(sizes, bucket_times, label="Bucket Sort", marker="s")
    plt.xlabel("Número de Emails")
    plt.ylabel("Tiempo (segundos)")
    plt.title("Comparación de Tiempos: Bubble Sort vs Bucket Sort")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    print("Memoria usada Bubble Sort: {:.2f} KB".format(peak_bubble / 1024))
    print("Memoria usada Bucket Sort: {:.2f} KB".format(peak_bucket / 1024))
    plt.show()
