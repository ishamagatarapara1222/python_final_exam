# Retail Sales Data Analyzer


from typing import Optional

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


REQUIRED_COLUMNS = (
    "Date",
    "Product",
    "Category",
    "Price",
    "Quantity_Sold",
    "Total_Sales",
)


class RetailAnalyzer:
    """Load, summarize, filter, and chart retail sales records."""

    def __init__(self) -> None:
        self.data: Optional[pd.DataFrame] = None

    def load_data(self, file_path: str) -> bool:
        """Read and clean the sales CSV file."""
        if not file_path.lower().endswith(".csv"):
            print("Please select a CSV file.")
            return False

        try:
            self.data = pd.read_csv(file_path)

            for column in REQUIRED_COLUMNS:
                if column not in self.data.columns:
                    print("Missing column:", column)
                    self.data = None
                    return False

            self.data = self.data.dropna(subset=REQUIRED_COLUMNS)

            self.data["Date"] = pd.to_datetime(
                self.data["Date"], errors="coerce"
            )
            self.data["Price"] = pd.to_numeric(
                self.data["Price"], errors="coerce"
            )
            self.data["Quantity_Sold"] = pd.to_numeric(
                self.data["Quantity_Sold"], errors="coerce"
            )
            self.data["Total_Sales"] = pd.to_numeric(
                self.data["Total_Sales"], errors="coerce"
            )

            self.data = self.data.dropna(subset=REQUIRED_COLUMNS)

            
            self.data["Total_Sales"] = (
                self.data["Price"] * self.data["Quantity_Sold"]
            )

            if self.data.empty:
                print("The CSV file has no valid sales records.")
                return False

            print("Data loaded successfully!")
            print("Total valid records:", len(self.data))
            return True

        except FileNotFoundError:
            print("File not found. Check the file name and location.")
            return False
        except Exception as error:
            print("Could not read the file:", error)
            return False

    def calculate_metrics(self) -> None:
        """Display basic sales calculations."""
        if self.data is None:
            print("Please load a dataset first.")
            return

        total_sales = self.data["Total_Sales"].sum()
        average_sales = self.data["Total_Sales"].mean()
        popular_product = (
            self.data.groupby("Product")["Quantity_Sold"]
            .sum()
            .idxmax()
        )

        print("\n----- SALES SUMMARY -----")
        print("Total sales: Rs.", round(total_sales, 2))
        print("Average sale: Rs.", round(average_sales, 2))
        print("Most popular product:", popular_product)

    def filter_data(self) -> None:
        """Filter records by product category."""
        if self.data is None:
            print("Please load a dataset first.")
            return

        print("\nAvailable categories:")
        categories = self.data["Category"].unique()
        for category in categories:
            print("-", category)

        selected_category = input("Enter category name: ").strip().lower()

        filtered_data = self.data[
            self.data["Category"].str.lower()
            == selected_category
        ]

        if filtered_data.empty:
            print("No records found for this category.")
        else:
            print("\nFiltered sales records:")
            print(filtered_data.to_string(index=False))
            print("Category sales: Rs.",
                  round(filtered_data["Total_Sales"].sum(), 2))

    def display_summary(self) -> None:
        """Print a small preview and summary of the dataset."""
        if self.data is None:
            print("Please load a dataset first.")
            return

        print("\n----- FIRST FIVE RECORDS -----")
        print(self.data.head().to_string(index=False))

        print("\n----- DATASET INFORMATION -----")
        print("Number of records:", len(self.data))
        print("Number of products:", self.data["Product"].nunique())
        print("Categories:", ", ".join(self.data["Category"].unique()))

    def show_charts(self) -> None:
        """Create simple charts using Matplotlib and Seaborn."""
        if self.data is None:
            print("Please load a dataset first.")
            return

        # Bar chart: sales by category
        category_sales = self.data.groupby("Category")["Total_Sales"].sum()
        plt.figure(figsize=(8, 5))
        sns.barplot(x=category_sales.index, y=category_sales.values)
        plt.title("Total Sales by Category")
        plt.xlabel("Category")
        plt.ylabel("Total Sales (Rs.)")
        plt.tight_layout()
        plt.show()

        # Line graph: sales - time
        daily_sales = (
            self.data.groupby("Date")["Total_Sales"].sum().sort_index()
        )
        plt.figure(figsize=(8, 5))
        plt.plot(daily_sales.index, daily_sales.values, marker="o")
        plt.title("Sales Trend Over Time")
        plt.xlabel("Date")
        plt.ylabel("Total Sales (Rs.)")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

        # Simple heatmap: relationship between numeric columns
        numeric_data = self.data[[
            "Price", "Quantity_Sold", "Total_Sales"
        ]]
        correlation = numeric_data.corr()

        plt.figure(figsize=(6, 4))
        sns.heatmap(correlation, annot=True, cmap="Blues", fmt=".2f")
        plt.title("Sales Data Correlation")
        plt.tight_layout()
        plt.show()


def main() -> None:
    """Run the interactive retail sales analyzer."""
    analyzer = RetailAnalyzer()

    print("================================")
    print("     RETAIL SALES ANALYZER")
    print("================================")

    file_path = input(
        "Enter CSV file path (example: retail_sales.csv): "
    ).strip()

    if not analyzer.load_data(file_path):
        return

    while True:
        print("\n========== MAIN MENU ==========")
        print("1. Calculate sales metrics")
        print("2. Filter sales by category")
        print("3. Display data summary")
        print("4. Show charts")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            analyzer.calculate_metrics()
        elif choice == "2":
            analyzer.filter_data()
        elif choice == "3":
            analyzer.display_summary()
        elif choice == "4":
            analyzer.show_charts()
        elif choice == "5":
            print("Thank you for using Retail Sales Analyzer!")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 5.")


if __name__ == "__main__":
    main()
