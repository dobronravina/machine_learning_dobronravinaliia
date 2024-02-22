from collections import defaultdict
import matplotlib.pyplot as plt

file = open('Vehicle_Sales.csv', 'r')
read_content = file.readlines()

num_lines = len(read_content)
print("2. Кількість записів у файлі:", num_lines)

for fld in read_content:
    fields = fld.split(",")
    num_fields = len(fields)
    print("Кількість полів у записі:", num_fields)

print("Перші 12 записів:")
for line in read_content[:12]:
    print(line)

print("Останні 22 записи:")
for line in read_content[-22:]:
    print(line)


def convert_to_num():
    for i in range(len(read_content)):
        fields = read_content[i].split(",")
        for j in range(2, 6):
            if fields[j].strip().isdigit() and i != 0:
                fields[j] = int(fields[j].strip().strip('$'))
        read_content[i] = ','.join(str(field) for field in fields)
        type_fields = [type(field) for field in fields]
        print("Типи полів:", type_fields)
    return read_content


def add_new_colum():
    for i in range(len(read_content)):
        fields = read_content[i].split(',')
        for j in range(2, 6):
            fields[j] = fields[j].strip().strip('$')
        if i == 0:
            fields.append("Total Sales")
            fields.append("Total Revenue")
            fields.append("Difference Sales")
            read_content[0] = ','.join(str(field) for field in fields)
        else:
            total_sales = int(fields[2]) + int(fields[3])
            total_revenue = int(fields[4]) + int(fields[5])
            difference_sales = int(fields[2]) - int(fields[3])
            fields.append(total_sales)
            fields.append(total_revenue)
            fields.append(difference_sales)
            read_content[i] = ','.join(str(field) for field in fields)
        print(read_content[i])


def change_sequence():
    for i in range(len(read_content)):
        fields = read_content[i].split(',')
        fields = [fields[0], fields[1], fields[7], fields[4], fields[5], fields[6], fields[2], fields[3], fields[8]]
        read_content[i] = ','.join(str(field) for field in fields)
        print(read_content[i])


def statistics():
    print("Рік і місяць,у які нових автомобілів було продано менше за б/в: ")
    for i in range(1,len(read_content)):
        fields = read_content[i].split(',')
        if int(fields[8]) < 0:
            year = fields[0]
            month = fields[1]
            print(year, month)

    min_revenue = 1141497749
    for i in read_content[1:]:
        fields = i.split(",")
        revenue = int(fields[2])
        year = fields[0]
        month = fields[1]
        if revenue < min_revenue:
            min_revenue = revenue
            minyear = year
            minmonth = month
    print("Рік і місяць,коли сумарний дохід був мінімальним: ", minyear, minmonth)

    max_used = 0
    for i in read_content[1:]:
        fields = i.split(",")
        used = int(fields[7])
        year = fields[0]
        month = fields[1]
        if used > max_used:
            max_used = used
            maxyear = year
            maxmonth = month
    print("Рік і місяць,коли було продано найбільше б/в авто:", maxyear, maxmonth)


def calculate_and_diagram():
    sales_by_year = defaultdict(int)

    for i in read_content[1:]:
        fields = i.split(",")
        year = fields[0]
        sales_num = int(fields[5])
        sales_by_year[year] += sales_num

    print("Сумарний обсяг продажу транспортних засобів за кожен рік:")
    for year, sales in sales_by_year.items():
        print(f"{year}: {sales}")

    plt.figure(figsize=(8, 8))
    plt.pie(sales_by_year.values(), labels=sales_by_year.keys(), autopct='%1.1f%%', startangle=140)
    plt.title('Сумарний обсяг продажу за кожен рік')
    plt.axis('equal')
    plt.show()

    may_records = [record for record in read_content[1:] if record.split(',')[1] == 'MAY']
    total_used_revenue = sum(int(record.split(',')[5].strip('$')) for record in may_records)
    average_used_revenue = total_used_revenue / len(may_records) if len(may_records) > 0 else 0
    print("Середній дохід від продажу б/в транспортних засобів в травні:", average_used_revenue)


def diagram_for_2005():
    sales_2005 = [(record.split(',')[1], int(record.split(',')[2])) for record in read_content[1:] if record.split(',')[0] == '2005']

    months = [sale[0] for sale in sales_2005]
    new_car_sales = [sale[1] for sale in sales_2005]

    plt.figure(figsize=(10, 6))
    plt.bar(months, new_car_sales, color='skyblue')
    plt.title('Обсяг продажу нових автомобілів у 2005 році')
    plt.xlabel('Місяць')
    plt.ylabel('Обсяг продажу')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def schedule():
    monthly_revenue = {}
    for record in read_content[1:]:
        fields = record.split(',')
        month = fields[1]
        new_car_revenue = int(fields[6].strip('$'))
        used_car_revenue = int(fields[7].strip('$'))
        total_revenue = new_car_revenue + used_car_revenue
        if month in monthly_revenue:
            monthly_revenue[month][0] += new_car_revenue
            monthly_revenue[month][1] += used_car_revenue
            monthly_revenue[month][2] += total_revenue
        else:
            monthly_revenue[month] = [new_car_revenue, used_car_revenue, total_revenue]

    months = list(monthly_revenue.keys())
    new_car_revenues = [value[0] for value in monthly_revenue.values()]
    used_car_revenues = [value[1] for value in monthly_revenue.values()]

    plt.figure(figsize=(10, 6))
    plt.plot(months, new_car_revenues, marker='o', label='Дохід від продажу нових авто')
    plt.plot(months, used_car_revenues, marker='o', label='Дохід від продажу старих авто')
    plt.title('Сумарний дохід від продажу автомобілів за місяць')
    plt.xlabel('Місяць')
    plt.ylabel('Сумарний дохід')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


read_content = convert_to_num()
add_new_colum()
change_sequence()
statistics()
calculate_and_diagram()
diagram_for_2005()
schedule()