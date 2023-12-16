import csv
import os
from tabulate import tabulate
from typing import List
from dataclasses import dataclass


class VolumeError(Exception):
    pass

@dataclass
class Table:
    number: List[float]
    amount: List[float]
    price: List[float]
    tablefmt: str = "github"


class Table1(Table):
    def __init__(self, number: List[float], amount: List[float], price: List[float], tablefmt="github"):
        super().__init__(number, amount, price, tablefmt)
        self.df = []
        self.headers = ["Art.-No", "Amount(St.)", "Price(Euro)"]

    def generate_table(self):
        # Append data into a table
        for num, val, price in zip(self.number, self.amount, self.price):
            self.df.append([num, val, price])
        return "Table ready for reading!"

    def show_table(self):
        """Show table in console"""
        table = tabulate(self.df, self.headers, self.tablefmt)
        return table

@dataclass
class Table2(Table):
    """
    /--------------------------------------------------------/
    How worth calculated: 
        - Worth = amount * price
    How share of total amount calculated: 
        - Share of total amount = amount / total amount * 100 
    How share of total worth calculated: 
        - Share of total worth = worth / total price * 100
    How does rangs worked:
        - The higher the share of total value, the higher the rank. 
    /--------------------------------------------------------/
    """  
    def __init__(self, number: List[float], amount: List[float], price: List[float], tablefmt="github"):
        super().__init__(number, amount, price, tablefmt)
        self.data = []
        self.headers = ["Art.-No", "Amount(St.)", "Price(Eur)", "Worth(Eur)",
                        "Share of Total Quantity(%)", "Share of Total Value(%)", "Rang"]

    def calculate(self):
        # Calculation operation for table
        total_amount = sum(self.amount)
        worth = [a * p for a, p in zip(self.amount, self.price)]
        total_price = sum(worth)
        share_of_total_amount = [a / total_amount * 100 for a in self.amount]
        share_of_total_worth = [w / total_price * 100 for w in worth]
        # Used only for rangs calculation
        sorted_worth = sorted(worth, reverse=True)
        rangs = [sorted_worth.index(i) + 1 for i in worth]

        return {
            "total_amount": total_amount,
            "worth": worth,
            "total_price": total_price,
            "share_of_total_amount": share_of_total_amount,
            "share_of_total_worth": share_of_total_worth,
            "sorted_worth": sorted_worth,
            "rangs": rangs
        }

    def generate_table(self, calculation):
        try:
            for num, val, price, worth, share_t_a, share_t_w, r in zip(
                    self.number, self.amount, self.price,
                    calculation["worth"], calculation["share_of_total_amount"],
                    calculation["share_of_total_worth"], calculation["rangs"]):

                self.data.append(
                    [num, val, price, round(worth, 2),
                     round(share_t_a, 2), round(share_t_w, 2), int(r)])

            self.data.append(["Summe", calculation["total_amount"], "",
                              calculation["total_price"], "", "", ""])
            return "Table 2 is generated!"

        except NameError as e:
            print(f"Error occurs {e}")

    def show_table(self):
        table = tabulate(self.data, headers=self.headers,
                         tablefmt="github")
        return table

    def export_to_csv(self):
        with open("table2.csv", 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(self.headers)  # Write headers
            writer.writerows(self.data)    # Write data rows
        
        # Return path to the file
        file_name = "table2.csv"
        curr_dir = os.getcwd()
        file_dir = os.path.join(curr_dir, file_name)

        return f"Your file is in the following direction: {file_dir}\n"

@dataclass
class Table3(Table2):
    """
    /--------------------------------------------------------/
    How cumulated share of total worht worked: 
        - This column shows the cumulative share of the total value up to each row. (actually only for school task)
    How camulated share of total amount worked:
        - Similarly, this column represents the cumulative share of the total quantity up to each row. 
    how categories worked:
        -  A-Rang: up to 65% of share of total worth
        -  B-Rang: up to 95% of share of total worth
        -  C-Rang: more than 95% of share of total worth
    /--------------------------------------------------------/
    """
    def __init__(self, number: List[float], amount: List[float], price: List[float], tablefmt="github"):
        super().__init__(number, amount, price, tablefmt)
        self.df = []
        self.headers = ["Rang", "Art.-No", "Share of Total Worth(%)",
                        "Cumulative shares of the total worth(%)",
                        "Share of Total Quantity(%)",
                        "Cumulative shares of the total quantity(%)",
                        "Category"]

    def calculation_t(self):
        calculation_data = self.calculate()  # Call the calculate method of Table2
        sorted_df = sorted(zip(self.number, calculation_data["rangs"],
                               calculation_data["share_of_total_worth"],
                               calculation_data["share_of_total_amount"]), key=lambda x: x[1])
        sort_num, sort_rangs, share_t_w_sort, share_t_a_sort = zip(
            *sorted_df)
        # Camulated share of total worth
        cumulated_share_t_w = [sum(share_t_w_sort[:i+1])
                               for i in range(len(share_t_w_sort))]
        # Camulated share of total amount
        cumulated_share_t_a = [sum(share_t_a_sort[:i+1])
                               for i in range(len(share_t_a_sort))]

        a_category = []
        b_category = []
        c_category = []

        categories = a_category, b_category, c_category

        for w in cumulated_share_t_w:
            if w <= 65:
                a_category.append("A")
            elif 65 < w <= 95:
                b_category.append("B")
            else:
                c_category.append("C")

        sort_categories = [item for sublist in categories for item in sublist]

        return {
            "sort_rangs": sort_rangs,
            "sort_num": sort_num,
            "share_t_w_sort": share_t_w_sort,
            "cumulated_share_t_w": cumulated_share_t_w,
            "share_t_a_sort": share_t_a_sort,
            "cumulated_share_t_a": cumulated_share_t_a,
            "sort_categories": sort_categories
        }

    def generate_table(self, calculation):
        for rang, num, share_t_worth, cumulated_share_t_w, share_t_a, cumulated_share_t_a, categories in zip(
                calculation["sort_rangs"],
                calculation["sort_num"],
                calculation["share_t_w_sort"],
                calculation["cumulated_share_t_w"],
                calculation["share_t_a_sort"],
                calculation["cumulated_share_t_a"],
                calculation["sort_categories"]
        ):
            self.df.append(
                [rang, num, round(share_t_worth, 2), round(cumulated_share_t_w, 2),
                 round(share_t_a, 2), round(cumulated_share_t_a, 2), categories])

        return "Table ready to export!"

    def show_table(self):
        table = tabulate(self.df, self.headers, tablefmt='github')
        return table

    def export_to_csv(self):
        with open("table3.csv", 'w') as file:
            writer = csv.writer(file)
            writer.writerow(self.headers)  # Write headers
            writer.writerows(self.df)    # Write data rows

        # Return path to the file
        file_name = "table1.csv"
        curr_dir = os.getcwd()
        file_dir = os.path.join(curr_dir, file_name)

        return f"Your file is in the following direction: {file_dir}\n"


def main():
    # Inport data from user
    while True:
        try:
            number = list(input(
                "Enter name or no. of products separated by commas[, ]: ").split(", "))
            amount = list(map(float, input(
                "Enter amount of products separated by commas[, ]: ").split(", ")))
            price = list(map(float, input(
                "Enter prices of products separated by comma[, ]: ").split(", ")))

            if len(number) == len(amount) == len(price):
                break  # Break out of the loop if input is valid
            else:
                print("The number of products, amount, and prices must be the same!")
        except ValueError as e:
            print(f"Error occurs! {e}")
            print("Please enter a valid option!")

    #Generate and print table 1
    my_table1 = Table1(number, amount, price)
    my_table1.generate_table()
    print(my_table1.show_table())


    # Main Menu
    while True:
        # Main menu with next options
        print("\n Main menu:\n \
            [1] Show second table\n \
            [2] Export second table to scv file\n \
            [3] Show third table\n \
            [4] Export third table to scv file\n \
            [5] Exit\n ")
        
        answer = str(input())

        if answer == "1":
            my_table2 = Table2(number, amount, price)
            calculation = my_table2.calculate()
            my_table2.generate_table(calculation)
            print(my_table2.show_table())
            
        
        elif answer == "2":
            my_table2 = Table2(number, amount, price)
            calculation = my_table2.calculate()
            my_table2.generate_table(calculation)
            print(my_table2.export_to_csv())

        
        elif answer == "3":
            my_table3 = Table3(number, amount, price)
            my_table3.generate_table(my_table3.calculation_t())
            print(my_table3.show_table())

        elif answer == "4":
            my_table3 = Table3(number, amount, price)
            my_table3.generate_table(my_table3.calculation_t())
            print(my_table3.export_to_csv())

        elif answer == "5":
            exit()

        else:
            print("Please enter a valid option!")
    


if __name__ == "__main__":
    main()
